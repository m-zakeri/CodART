package org.gudy.azureus2.ui.swt.views.table.painted;

import java.util.*;
import java.util.List;

import org.eclipse.swt.SWT;
import org.eclipse.swt.dnd.*;
import org.eclipse.swt.events.*;
import org.eclipse.swt.graphics.*;
import org.eclipse.swt.layout.*;
import org.eclipse.swt.widgets.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.config.ParameterListener;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.internat.MessageText.MessageTextListener;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.plugins.ui.tables.*;
import org.gudy.azureus2.plugins.ui.tables.TableColumn;
import org.gudy.azureus2.ui.swt.MenuBuildUtils;
import org.gudy.azureus2.ui.swt.SimpleTextEntryWindow;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.debug.ObfusticateImage;
import org.gudy.azureus2.ui.swt.debug.UIDebugGenerator;
import org.gudy.azureus2.ui.swt.mainwindow.Colors;
import org.gudy.azureus2.ui.swt.mainwindow.HSLColor;
import org.gudy.azureus2.ui.swt.plugins.UISWTViewEvent;
import org.gudy.azureus2.ui.swt.pluginsimpl.UISWTViewCore;
import org.gudy.azureus2.ui.swt.shells.GCStringPrinter;
import org.gudy.azureus2.ui.swt.views.table.*;
import org.gudy.azureus2.ui.swt.views.table.impl.*;

import com.aelitis.azureus.ui.common.table.*;
import com.aelitis.azureus.ui.common.table.TableViewFilterCheck;
import com.aelitis.azureus.ui.common.table.impl.TableColumnManager;
import com.aelitis.azureus.ui.common.table.impl.TableRowCoreSorter;
import com.aelitis.azureus.ui.common.table.impl.TableViewImpl;
import com.aelitis.azureus.ui.selectedcontent.ISelectedContent;
import com.aelitis.azureus.ui.selectedcontent.SelectedContentListener;
import com.aelitis.azureus.ui.selectedcontent.SelectedContentManager;
import com.aelitis.azureus.ui.swt.imageloader.ImageLoader;
import com.aelitis.azureus.ui.swt.utils.ColorCache;
import com.aelitis.azureus.ui.swt.utils.FontUtils;

/**
 * A TableView implemented by painting on a canvas
 * 
 * TODO: 
 * Keyboard Selection
 * Cursor
 * Column move and resize past bounds
 */
public class TableViewPainted
	extends TableViewImpl<Object>
	implements ParameterListener, TableViewSWT<Object>, ObfusticateImage,
	MessageTextListener
{

	private static final boolean DEBUG_ROWCHANGE = false;

	private static final boolean DEBUG_WITH_SHELL = false;

	private static final int DEFAULT_HEADER_HEIGHT = 27;

	private Composite cTable;

	private int loopFactor;

	/** How often graphic cells get updated
	 */
	protected int graphicsUpdate = configMan.getIntParameter("Graphics Update");

	protected int reOrderDelay = configMan.getIntParameter("ReOrder Delay");
	
	protected boolean extendedErase = configMan.getBooleanParameter("Table.extendedErase");

	private int defaultRowHeight = 17;

	/**
	 * Rows visible to user.  We assume this list is always up to date
	 */
	LinkedHashSet<TableRowPainted> visibleRows = new LinkedHashSet<TableRowPainted>();
	
	Object visibleRows_sync = new Object();

	Object lock = new Object();

	/**
	 * Up to date table client area.  So far, the best places to refresh
	 * this variable are in the PaintItem event and the scrollbar's events.
	 * Typically table.getClientArea() is time consuming 
	 */
	protected Rectangle clientArea;

	private boolean isVisible;

	private Shell shell;

	private Color colorLine;

	private int headerHeight;

	private Canvas cHeaderArea;

	private Image canvasImage;

	private final String sDefaultSortOn;

	private TableViewSWT_Common tvSWTCommon;

	private TableViewSWT_TabsCommon tvTabsCommon;

	private TableViewSWTPanelCreator mainPanelCreator;

	private boolean isMultiSelect;

	private int columnsWidth;

	private Menu menu;

	protected boolean isHeaderDragging;

	private TableRowPainted focusedRow;

	private boolean enableTabViews;

	protected boolean isDragging;

	private Composite mainComposite;

	private Object heightChangeSync = new Object();
	private int totalHeight = 0;

	private boolean redrawTableScheduled;

	private Font fontHeaderSmall;
	private Font fontHeader;

	private ScrollBar hBar;

	private ScrollBar vBar;
	
	private Canvas sCanvasImage;

	class RefreshTableRunnable extends AERunnable {
		private boolean forceSort;
		public void runSupport() {
			__refreshTable(isForceSort());
		}
		public boolean isForceSort() {
			return forceSort;
		}
		public void setForceSort(boolean forceSort) {
			this.forceSort = forceSort;
		}
	}
	
	private RefreshTableRunnable refreshTableRunnable = new RefreshTableRunnable();

	protected boolean isFocused;

	/**
	 * Main Initializer
	 * @param _sTableID Which table to handle (see 
	 *                   {@link org.gudy.azureus2.plugins.ui.tables.TableManager}).
	 *                   Config settings are stored with the prefix of  
	 *                   "Table.<i>TableID</i>"
	 * @param _sPropertiesPrefix Prefix for retrieving text from the properties
	 *                            file (MessageText).  Typically 
	 *                            <i>TableID</i> + "View"
	 * @param _basicItems Column Definitions
	 * @param _sDefaultSortOn Column name to sort on if user hasn't chosen one yet
	 * @param _iTableStyle SWT style constants used when creating the table
	 */
	public TableViewPainted(Class<?> pluginDataSourceType, String _sTableID,
			String _sPropertiesPrefix, TableColumnCore[] _basicItems,
			String _sDefaultSortOn, int _iTableStyle) {
		super(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems);
		setRowsSync(lock);
		//		boolean wantTree = (_iTableStyle & SWT.CASCADE) != 0;
		//		_iTableStyle &= ~SWT.CASCADE;
		//		if (wantTree) {
		//			useTree = COConfigurationManager.getBooleanParameter("Table.useTree")
		//					&& !Utils.isCarbon;
		//		}
		//		basicItems = _basicItems;
		//		sDefaultSortOn = _sDefaultSortOn;
		//		iTableStyle = _iTableStyle | SWT.V_SCROLL | SWT.DOUBLE_BUFFERED;
		this.sDefaultSortOn = _sDefaultSortOn;
		this.isMultiSelect = (_iTableStyle & SWT.MULTI) > 0;
		
		// Deselect rows if user clicks on a blank spot (a spot with no row)
		tvSWTCommon = new TableViewSWT_Common(this) {
			public void widgetSelected(SelectionEvent event) {
				//updateSelectedRows(table.getSelection(), true);
			}

			@Override
			public void mouseUp(TableRowCore clickedRow, TableCellCore cell, int button,
					int stateMask) {
				super.mouseUp(clickedRow, cell, button, stateMask);
				
				if (clickedRow == null) {
					return;
				}
				if (button == 1) {
  				int keyboardModifier = (stateMask & SWT.MODIFIER_MASK);
  				if ((keyboardModifier & SWT.SHIFT) > 0) {
  					// select from focus to row
  					selectRowsTo(clickedRow);
  					return;
  				} else if (keyboardModifier == 0) {
  					setSelectedRows(new TableRowCore[] {
  						clickedRow
  					});
  					return;
  				}
				}
			}

			@Override
			public void mouseDown(TableRowSWT clickedRow, TableCellCore cell, int button,
					int stateMask) {
				if (clickedRow == null) {
					return;
				}
				int keyboardModifier = (stateMask & SWT.MODIFIER_MASK);
				if (button == 1) {
  				if ((keyboardModifier & (SWT.MOD1)) > 0) {
  					// control (win), alt (mac)
  					setRowSelected(clickedRow, !clickedRow.isSelected(), true);
  					return;
  				} 
				} else if (button == 3) {
					if (!isSelected(clickedRow) && keyboardModifier == 0) {
						setSelectedRows(new TableRowCore[] {
							clickedRow
						});
					}
				}
				if (getSelectedRowsSize() == 0) {
					setSelectedRows(new TableRowCore[] {
						clickedRow
					});
				}
			}

			@Override
			public void keyPressed(KeyEvent event) {
				if (getComposite() != event.widget) {
					super.keyPressed(event);	
					return;
				}
				boolean updateTable = false;
				if (event.keyCode == SWT.ARROW_UP) {
					TableRowCore rowToSelect = getPreviousRow(focusedRow);
					if ((event.stateMask & SWT.SHIFT) > 0) {
						if (rowToSelect != null) {
							TableRowCore[] selectedRows = getSelectedRows();
							Arrays.sort(selectedRows, new TableRowCoreSorter());
							boolean select = selectedRows.length == 0
									|| selectedRows[0] == focusedRow;
//							System.out.println("i=" + selectedRows[0].getIndex() + ";"
//									+ select + ";" + focusedRow.getIndex());
							if (select) {
								rowToSelect.setSelected(select);
							} else {
								focusedRow.setSelected(false);
								setFocusedRow(rowToSelect);
							}
							updateTable = true;
						}
					} else if ((event.stateMask & SWT.CONTROL) > 0) {
						// show one more topRow
						TableRowPainted firstRow = visibleRows.iterator().next();
						if (firstRow != null) {
							int hChange = 0;
							if (isRowPartiallyVisible(firstRow)) {
								hChange =  firstRow.getDrawOffset().y  - clientArea.y;
							} else {
  							TableRowCore prevRow = getPreviousRow(firstRow);
  							if (prevRow != firstRow && prevRow != null) {
  								hChange = -prevRow.getHeight();
  							}
							}
							vBar.setSelection(vBar.getSelection() + hChange);
							swt_vBarChanged();
						}
					} else {
						setSelectedRows(new TableRowCore[] {
							rowToSelect
						});
						updateTable = true;
					}
				} else if (event.keyCode == SWT.PAGE_UP) {
					TableRowCore row = focusedRow;
					TableRowPainted lastRow = getLastVisibleRow();
					int y = lastRow == null ? 0 : (clientArea.y + clientArea.height) - lastRow.getDrawOffset().y;
					while (row != null && y < clientArea.height) {
						y += row.getHeight();
						row = getPreviousRow(row);
					}
					if (row == null) {
						row = getRow(0);
					}
					if ((event.stateMask & SWT.SHIFT) > 0) {
						selectRowsTo(row);
					} else if (event.stateMask == 0) {
  					setSelectedRows(new TableRowCore[] {
  						row
  					});
					}
					updateTable = true;
				} else if (event.keyCode == SWT.HOME) {
					if ((event.stateMask & SWT.SHIFT) > 0) {
						selectRowsTo(getRow(0));
					} else if (event.stateMask == 0) {
  					setSelectedRows(new TableRowCore[] {
  						getRow(0)
  					});
					}
					updateTable = true;
				} else if (event.keyCode == SWT.ARROW_DOWN) {
					if ((event.stateMask & SWT.CONTROL) > 0) {
						// show one less topRow 
						TableRowPainted firstRow = visibleRows.iterator().next();
						if (firstRow != null) {
							int hChange = 0;
							if (isRowPartiallyVisible(firstRow)) {
								hChange = firstRow.getHeight() + (firstRow.getDrawOffset().y - clientArea.y);
							} else {
								hChange = firstRow.getHeight();
							}
							vBar.setSelection(vBar.getSelection() + hChange);
							swt_vBarChanged();
						}
					} else {
						TableRowCore rowToSelect = getNextRow(focusedRow);
  					if (rowToSelect != null) {
  						if ((event.stateMask & SWT.SHIFT) > 0) {
  							TableRowCore[] selectedRows = getSelectedRows();
  							Arrays.sort(selectedRows, new TableRowCoreSorter());
  							boolean select = selectedRows.length == 0
  									|| selectedRows[selectedRows.length - 1] == focusedRow;
  							if (select) {
  								rowToSelect.setSelected(select);
  							} else {
  								focusedRow.setSelected(false);
  								setFocusedRow(rowToSelect);
  							}
  						} else {
  							setSelectedRows(new TableRowCore[] {
  								rowToSelect
  							});
  						}
							updateTable = true;
  					}
					}
				} else if (event.keyCode == SWT.PAGE_DOWN) {
					TableRowCore row = focusedRow;
					TableRowPainted firstRow = visibleRows.size() == 0 ? null : visibleRows.iterator().next();

					int y = firstRow == null ? 0 : firstRow.getHeight() - (clientArea.y - firstRow.getDrawOffset().y);
					while (row != null && y < clientArea.height) {
						y += row.getHeight();
						TableRowCore nextRow = getNextRow(row);
						if (nextRow == null) {
							break;
						}
						row = nextRow;
					}
					if ((event.stateMask & SWT.SHIFT) > 0) {
						selectRowsTo(row);
					} else if (event.stateMask == 0) {
  					setSelectedRows(new TableRowCore[] {
  						row
  					});
					}
					updateTable = true;
				} else if (event.keyCode == SWT.END) {
					TableRowCore lastRow = getRow(getRowCount() - 1);
					if ((event.stateMask & SWT.SHIFT) > 0) {
						selectRowsTo(lastRow);
					} else if (event.stateMask == 0) {
  					setSelectedRows(new TableRowCore[] {
  						lastRow
  					});
					}
					updateTable = true;
				} else if (event.keyCode == SWT.ARROW_RIGHT) {
					if (event.stateMask == 0 && focusedRow != null && !focusedRow.isExpanded() && canHaveSubItems()) {
						focusedRow.setExpanded(true);
					} else {
						if (hBar.isEnabled()) {
							hBar.setSelection(hBar.getSelection() + 50);
							cTable.redraw();
							updateTable = true;
						}
					}
				} else if (event.keyCode == SWT.ARROW_LEFT) {
					if (event.stateMask == 0 && focusedRow != null && focusedRow.isExpanded() && canHaveSubItems()) {
						focusedRow.setExpanded(false);
					} else {
						if (hBar.isEnabled()) {
							hBar.setSelection(hBar.getSelection() - 50);
							cTable.redraw();
							updateTable = true;
						}
					}
				}
				
				if (updateTable) {
					cTable.update();
				}
				super.keyPressed(event);
			}

			@Override
			public void keyReleased(KeyEvent e) {
				swt_calculateClientArea();
				visibleRowsChanged();

				super.keyReleased(e);
			}
		};
	}

	protected boolean isRowPartiallyVisible(TableRowPainted row) {
		if (row == null) {
			return false;
		}
		Point drawOffset = row.getDrawOffset();
		int height = row.getHeight();
		return (drawOffset.y < clientArea.y && drawOffset.y + height > clientArea.y)
				|| (drawOffset.y < clientArea.y + clientArea.height && drawOffset.y
						+ height > clientArea.y + clientArea.height);
	}

	protected void selectRowsTo(TableRowCore clickedRow) {
		if (!isMultiSelect) {
			setSelectedRows(new TableRowCore[] {
				clickedRow
			});
			return;
		}
		TableRowCore[] selectedRows = getSelectedRows();
		TableRowCore firstRow = selectedRows.length > 0 ? selectedRows[0]
				: getRow(0);
		TableRowCore parentFirstRow = firstRow;
		while (parentFirstRow.getParentRowCore() != null) {
			parentFirstRow = parentFirstRow.getParentRowCore();
		}
		TableRowCore parentClickedRow = clickedRow;
		while (parentClickedRow.getParentRowCore() != null) {
			parentClickedRow = parentClickedRow.getParentRowCore();
		}
		int startPos;
		int endPos;
		if (parentFirstRow == parentClickedRow) {
			startPos = parentFirstRow == firstRow ? -1 : firstRow.getIndex();
			endPos = parentClickedRow == clickedRow ? -1 : clickedRow.getIndex();
		} else {
			startPos = indexOf(parentFirstRow);
			endPos = indexOf(parentClickedRow);
			if (endPos == -1 || startPos == -1) {
				return;
			}
		}
		ArrayList<TableRowCore> rowsToSelect = new ArrayList<TableRowCore>(Arrays.asList(selectedRows));
		TableRowCore curRow = firstRow;
		do {
			if (!rowsToSelect.contains(curRow)) {
				rowsToSelect.add(curRow);
			}
			TableRowCore newRow = (startPos < endPos) ? getNextRow(curRow) : getPreviousRow(curRow);
			
				// prevent infinite loop if things go wonky (which they have been soon to do!)
			if ( newRow == curRow ){
				break;
			}else{
				curRow = newRow;
			}
			
		} while (curRow != clickedRow && curRow != null);
		if (curRow != null && !rowsToSelect.contains(curRow)) {
			rowsToSelect.add(curRow);
		}
		setSelectedRows(rowsToSelect.toArray(new TableRowCore[0]));
		setFocusedRow(clickedRow);
	}

	protected TableRowCore getPreviousRow(TableRowCore relativeToRow) {
		TableRowCore rowToSelect = null;
		if (relativeToRow != null) {
			TableRowCore parentRow = relativeToRow.getParentRowCore();
			if (parentRow == null) {
				TableRowCore row = getRow(indexOf(relativeToRow) - 1);
				if (row != null && row.isExpanded() && row.getSubItemCount() > 0) {
					rowToSelect = row.getSubRow(row.getSubItemCount() - 1);
				} else {
					rowToSelect = row;
				}
			} else {
				int index = relativeToRow.getIndex();
				if (index > 0) {
					rowToSelect = parentRow.getSubRow(index - 1);
				} else {
					rowToSelect = parentRow;
				}
			}
		}
		if (rowToSelect == null) {
			rowToSelect = getRow(0);
		}
		return rowToSelect;
	}

	protected TableRowCore getNextRow(TableRowCore relativeToRow) {
		TableRowCore rowToSelect = null;
		if (relativeToRow == null) {
			rowToSelect = getRow(0);
		} else {
			if (relativeToRow.isExpanded() && relativeToRow.getSubItemCount() > 0) {
				TableRowCore[] subRowsWithNull = relativeToRow.getSubRowsWithNull();
				for (TableRowCore row : subRowsWithNull) {
					if (row != null) {
						rowToSelect = row;
						break;
					}
				}
				if (rowToSelect == null) {
					rowToSelect = getRow(relativeToRow.getIndex() + 1);
				}
			} else {
				TableRowCore parentRow = relativeToRow.getParentRowCore();
				if (parentRow != null) {
					rowToSelect = parentRow.getSubRow(relativeToRow.getIndex() + 1);

					if (rowToSelect == null) {
						rowToSelect = getRow(parentRow.getIndex() + 1);
					}
				} else {
					rowToSelect = getRow(relativeToRow.getIndex() + 1);
				}
			}
		}
		return rowToSelect;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#clipboardSelected()
	 */
	public void clipboardSelected() {
		String sToClipboard = "";
		TableColumnCore[] visibleColumns = getVisibleColumns();
		for (int j = 0; j < visibleColumns.length; j++) {
			if (j != 0) {
				sToClipboard += "\t";
			}
			String title = MessageText.getString(visibleColumns[j].getTitleLanguageKey());
			sToClipboard += title;
		}

		TableRowCore[] rows = getSelectedRows();
		for (TableRowCore row : rows) {
			sToClipboard += "\n";
			for (int j = 0; j < visibleColumns.length; j++) {
				TableColumnCore column = visibleColumns[j];
				if (j != 0) {
					sToClipboard += "\t";
				}
				TableCellCore cell = row.getTableCellCore(column.getName());
				if (cell != null) {
					sToClipboard += cell.getClipboardText();
				}
			}
		}
		new Clipboard(getComposite().getDisplay()).setContents(new Object[] {
			sToClipboard
		}, new Transfer[] {
			TextTransfer.getInstance()
		});
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#isDisposed()
	 */
	public boolean isDisposed() {
		return cTable == null || cTable.isDisposed();
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#refreshTable(boolean)
	 */
	public void refreshTable(final boolean bForceSort) {
		//__refreshTable(bForceSort);
		refreshTableRunnable.setForceSort(bForceSort);
		Utils.getOffOfSWTThread(refreshTableRunnable);
	}

	public void __refreshTable(boolean bForceSort) {
		long lStart = SystemTime.getCurrentTime();
		super.refreshTable(bForceSort);

		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				// call to trigger invalidation if visibility changes
				isVisible();
			}
		});
		final boolean bDoGraphics = (loopFactor % graphicsUpdate) == 0;
		final boolean bWillSort = bForceSort || (reOrderDelay != 0)
				&& ((loopFactor % reOrderDelay) == 0);
		//System.out.println("Refresh.. WillSort? " + bWillSort);

		if (bWillSort) {
			TableColumnCore sortColumn = getSortColumn();
			if (bForceSort && sortColumn != null) {
				resetLastSortedOn();
				sortColumn.setLastSortValueChange(SystemTime.getCurrentTime());
			}
			_sortColumn(true, false, false);
		}

		runForAllRows(new TableGroupRowVisibilityRunner() {
			public void run(TableRowCore row, boolean bVisible) {
				row.refresh(bDoGraphics, bVisible);
			}
		});
		loopFactor++;

		long diff = SystemTime.getCurrentTime() - lStart;
		if (diff > 0) {
			//debug("refreshTable took " + diff);
		}

		if (tvTabsCommon != null) {
			Utils.execSWTThread(new AERunnable() {
				public void runSupport() {
					if (tvTabsCommon != null) {
						tvTabsCommon.swt_refresh();
					}
				}
			});
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setEnableTabViews(boolean)
	 */
	public void setEnableTabViews(boolean enableTabViews) {
		this.enableTabViews = enableTabViews;
	}

	public boolean isTabViewsEnabled() {
		return enableTabViews;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setFocus()
	 */
	public void setFocus() {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (isDisposed()) {
					return;
				}
				cTable.setFocus();
			}
		});
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setRowDefaultHeight(int)
	 */
	public void setRowDefaultHeight(int iHeight) {
		if (iHeight > defaultRowHeight) {
			defaultRowHeight = iHeight;
			
			Utils.execSWTThread(new AERunnable() {
				public void runSupport() {
					if (vBar != null && !vBar.isDisposed()) {
						vBar.setIncrement(defaultRowHeight);
					}
				}
			});
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getRow(int, int)
	 */
	public TableRowCore getRow(int x, int y) {
		Set<TableRowPainted> visibleRows = this.visibleRows;
		if (visibleRows.size() == 0) {
			return null;
		}
		boolean firstRow = true;
		int curY = 0;
		for (TableRowPainted row : visibleRows) {
			if (firstRow) {
				curY = row.getDrawOffset().y;
			}
			int h = row.getHeight();
			if (y >= curY && y < curY + h) {
				return row;
			}
			curY += h;
		}
		return null;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#isRowVisible(com.aelitis.azureus.ui.common.table.TableRowCore)
	 */
	public boolean isRowVisible(TableRowCore row) {
		if (row == null) {
			return false;
		}
		synchronized (visibleRows_sync) {
			return visibleRows.contains(row);
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getTableCellWithCursor()
	 */
	public TableCellCore getTableCellWithCursor() {
		// TODO: Make work outside SWT?
		Point pt = cTable.getDisplay().getCursorLocation();
		pt = cTable.toControl(pt);
		return getTableCell(pt.x, clientArea.y + pt.y);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getTableRowWithCursor()
	 */
	public TableRowCore getTableRowWithCursor() {
		// TODO: Make work outside SWT?
		Point pt = cTable.getDisplay().getCursorLocation();
		pt = cTable.toControl(pt);
		return getTableRow(pt.x, pt.y, true);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getRowDefaultHeight()
	 */
	public int getRowDefaultHeight() {
		return defaultRowHeight;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setEnabled(boolean)
	 */
	public void setEnabled(final boolean enable) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (!isDisposed()) {
					cTable.setEnabled(enable);
				}
			}
		});
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#canHaveSubItems()
	 */
	public boolean canHaveSubItems() {
		return true;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setHeaderVisible(boolean)
	 */
	public void setHeaderVisible(final boolean visible) {
		super.setHeaderVisible(visible);

		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (cHeaderArea != null && !cHeaderArea.isDisposed()) {
					cHeaderArea.setVisible(visible);
					FormData fd = Utils.getFilledFormData();
					fd.height = visible ? headerHeight : 1;
					fd.bottom = null;
					cHeaderArea.setLayoutData(fd);
					cHeaderArea.getParent().layout(true);
				}
			}
		});
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getMaxItemShown()
	 */
	public int getMaxItemShown() {
		// NOT USED
		return 0;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#setMaxItemShown(int)
	 */
	public void setMaxItemShown(int newIndex) {
		// NOT USED
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.core3.internat.MessageText.MessageTextListener#localeChanged(java.util.Locale, java.util.Locale)
	 */
	public void localeChanged(Locale old_locale, Locale new_locale) {
		Utils.execSWTThreadLater(0, new AERunnable() {
			public void runSupport() {
				if (tvTabsCommon != null) {
					tvTabsCommon.localeChanged();
				}

				tableInvalidate();
				refreshTable(true);
				cHeaderArea.redraw();
			}
		});
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableStructureModificationListener#columnOrderChanged(int[])
	 */
	public void columnOrderChanged(int[] iPositions) {
		//TODO
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableStructureModificationListener#columnSizeChanged(com.aelitis.azureus.ui.common.table.TableColumnCore, int)
	 */
	public void columnSizeChanged(TableColumnCore tableColumn, int diff) {
		columnsWidth += diff;
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (cHeaderArea != null && !cHeaderArea.isDisposed()) {
					cHeaderArea.redraw();
				}
				swt_fixupSize();
				redrawTable();
			}
		});
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#addKeyListener(org.eclipse.swt.events.KeyListener)
	 */
	public void addKeyListener(KeyListener listener) {
		if (tvSWTCommon == null) {
			return;
		}
		tvSWTCommon.addKeyListener(listener);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#removeKeyListener(org.eclipse.swt.events.KeyListener)
	 */
	public void removeKeyListener(KeyListener listener) {
		if (tvSWTCommon == null) {
			return;
		}
		tvSWTCommon.removeKeyListener(listener);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getKeyListeners()
	 */
	public KeyListener[] getKeyListeners() {
		if (tvSWTCommon == null) {
			return new KeyListener[0];
		}
		return tvSWTCommon.getKeyListeners();
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#addMenuFillListener(org.gudy.azureus2.ui.swt.views.table.TableViewSWTMenuFillListener)
	 */
	public void addMenuFillListener(TableViewSWTMenuFillListener l) {
		if (tvSWTCommon == null) {
			return;
		}
		tvSWTCommon.addMenuFillListener(l);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#createDragSource(int)
	 */
	public DragSource createDragSource(int style) {
		final DragSource dragSource = new DragSource(cTable, style);
		dragSource.addDragListener(new DragSourceAdapter() {
			public void dragStart(DragSourceEvent event) {
				cTable.setCursor(null);
				TableRowCore row = getTableRow(event.x, event.y, true);
				if (row != null && !row.isSelected()) {
					setSelectedRows(new TableRowCore[] { row });
				}
				isDragging = true;
			}

			public void dragFinished(DragSourceEvent event) {
				isDragging = false;
			}
		});
		cTable.addDisposeListener(new DisposeListener() {
			// @see org.eclipse.swt.events.DisposeListener#widgetDisposed(org.eclipse.swt.events.DisposeEvent)
			public void widgetDisposed(DisposeEvent e) {
				if (!dragSource.isDisposed()) {
					dragSource.dispose();
				}
			}
		});
		return dragSource;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#createDropTarget(int)
	 */
	public DropTarget createDropTarget(int style) {
		final DropTarget dropTarget = new DropTarget(cTable, style);
		cTable.addDisposeListener(new DisposeListener() {
			// @see org.eclipse.swt.events.DisposeListener#widgetDisposed(org.eclipse.swt.events.DisposeEvent)
			public void widgetDisposed(DisposeEvent e) {
				if (!dropTarget.isDisposed()) {
					dropTarget.dispose();
				}
			}
		});
		return dropTarget;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getComposite()
	 */
	public Composite getComposite() {
		return cTable;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getRow(org.eclipse.swt.dnd.DropTargetEvent)
	 */
	public TableRowCore getRow(DropTargetEvent event) {
		//TODO
		// maybe
		Point pt = cTable.toControl(event.x, event.y);
		return getRow(pt.x, clientArea.y + pt.y);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getRowSWT(java.lang.Object)
	 */
	public TableRowSWT getRowSWT(Object dataSource) {
		return (TableRowSWT) getRow(dataSource);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableComposite()
	 */
	public Composite getTableComposite() {
		return cTable;
	}

	/** Creates a composite within the specified composite and sets its layout
	 * to a default FillLayout().
	 *
	 * @param composite to create your Composite under
	 * @return The newly created composite
	 */
	public Composite createMainPanel(Composite composite) {
		TableViewSWTPanelCreator mainPanelCreator = getMainPanelCreator();
		if (mainPanelCreator != null) {
			return mainPanelCreator.createTableViewPanel(composite);
		}
		Composite panel = new Composite(composite, SWT.NO_FOCUS);
		composite.getLayout();
		GridLayout layout = new GridLayout();
		layout.marginHeight = 0;
		layout.marginWidth = 0;
		panel.setLayout(layout);

		Object parentLayout = composite.getLayout();
		if (parentLayout == null || (parentLayout instanceof GridLayout)) {
			panel.setLayoutData(new GridData(GridData.FILL_BOTH));
		}

		return panel;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#initialize(org.eclipse.swt.widgets.Composite)
	 */
	public void initialize(Composite parent) {
		tvTabsCommon = new TableViewSWT_TabsCommon(this);

		shell = parent.getShell();
		mainComposite = tvTabsCommon.createSashForm(parent);
		mainComposite.setData("Name", tableID);
		mainComposite.setData("ObfusticateImage", this);
		Composite cTableComposite = tvTabsCommon.tableComposite;

		cTableComposite.setLayout(new FormLayout());
		Layout layout = parent.getLayout();
		if (layout instanceof FormLayout) {
			FormData fd = Utils.getFilledFormData();
			cTableComposite.setLayoutData(fd);
		}

		cHeaderArea = new Canvas(cTableComposite, SWT.DOUBLE_BUFFERED);

		fontHeader = FontUtils.getFontWithHeight(cHeaderArea.getFont(), null, 12);
		fontHeaderSmall = FontUtils.getFontPercentOf(fontHeader, 0.8f);
		cHeaderArea.setFont(fontHeader);

		cTable = new Canvas(cTableComposite, SWT.NO_BACKGROUND | SWT.H_SCROLL | SWT.V_SCROLL);
		
		// good test
		//cTable.setFont(FontUtils.getFontPercentOf(cTable.getFont(), 1.50f));
		int minRowHeight = FontUtils.getFontHeightInPX(cTable.getFont());
		minRowHeight += Math.ceil(minRowHeight * 2.0 / 16.0);
		if (defaultRowHeight < minRowHeight) {
			defaultRowHeight = minRowHeight;
		}

		cTable.setBackground(parent.getDisplay().getSystemColor(
				SWT.COLOR_LIST_BACKGROUND));

		headerHeight = configMan.getIntParameter("Table.headerHeight");
		if (headerHeight <= 0) {
			headerHeight = DEFAULT_HEADER_HEIGHT;
		}

		FormData fd = Utils.getFilledFormData();
		fd.height = headerHeight;
		fd.bottom = null;
		cHeaderArea.setLayoutData(fd);
		fd = Utils.getFilledFormData();
		fd.top = new FormAttachment(cHeaderArea);
		cTable.setLayoutData(fd);

		clientArea = cTable.getClientArea();

		TableColumnCore[] tableColumns = getAllColumns();
		TableColumnCore[] tmpColumnsOrdered = new TableColumnCore[tableColumns.length];
		//Create all columns
		int columnOrderPos = 0;
		Arrays.sort(tableColumns,
				TableColumnManager.getTableColumnOrderComparator());
		for (int i = 0; i < tableColumns.length; i++) {
			int position = tableColumns[i].getPosition();
			if (position != -1 && tableColumns[i].isVisible()) {
				//table.createNewColumn(SWT.NULL);
				//System.out.println(i + "] " + tableColumns[i].getName() + ";" + position);
				tmpColumnsOrdered[columnOrderPos++] = tableColumns[i];
			}
		}
		//int numSWTColumns = table.getColumnCount();
		//int iNewLength = numSWTColumns - (bSkipFirstColumn ? 1 : 0);
		TableColumnCore[] columnsOrdered = new TableColumnCore[columnOrderPos];
		System.arraycopy(tmpColumnsOrdered, 0, columnsOrdered, 0, columnOrderPos);
		setColumnsOrdered(columnsOrdered);

		cTable.addPaintListener(new PaintListener() {
			public void paintControl(PaintEvent e) {
				swt_paintComposite(e);
			}
		});

		menu = createMenu();
		cTable.setMenu(menu);
		cHeaderArea.setMenu(menu);

		setupHeaderArea(cHeaderArea);

		cTable.addControlListener(new ControlListener() {

			public void controlResized(ControlEvent e) {
				swt_calculateClientArea();
				swt_fixupSize();
			}
			
			public void controlMoved(ControlEvent e) {
			}
		});
		
		hBar = cTable.getHorizontalBar();
		if (hBar != null) {
			hBar.setValues(0, 0, 0, 10, 10, 100);
			hBar.addSelectionListener(new SelectionListener() {
				
				public void widgetSelected(SelectionEvent e) {
					//swt_calculateClientArea();
					cTable.redraw();
				}
				
				public void widgetDefaultSelected(SelectionEvent e) {
				}
			});
		}
		vBar = cTable.getVerticalBar();
		if (vBar != null) {
			vBar.setValues(0, 0, 0, 50, getRowDefaultHeight(), 50);
			vBar.addSelectionListener(new SelectionListener() {
				public void widgetSelected(SelectionEvent e) {
					swt_vBarChanged();
				}
				
				public void widgetDefaultSelected(SelectionEvent e) {
				}
			});
		}
		
		if (DEBUG_WITH_SHELL) {
  		Shell shell = new Shell();
  		sCanvasImage = new Canvas(shell, SWT.DOUBLE_BUFFERED);
  		shell.setLayout(new FillLayout());
  		sCanvasImage.addPaintListener(new PaintListener() {
  			public void paintControl(PaintEvent e) {
  				if (canvasImage == null) {
  					return;
  				}
  				e.gc.drawImage(canvasImage, 0, 0);
  				//System.out.println(System.currentTimeMillis() + "] Paint " + e.x + "x" + e.y + " " + e.width + "x" + e.height);
  
  			}
  		});
  		shell.addDisposeListener(new DisposeListener() {
  			public void widgetDisposed(DisposeEvent e) {
  				sCanvasImage = null;
  			}
  		});
  		shell.setVisible(true);
		}


		cTable.addMouseListener(tvSWTCommon);
		cTable.addMouseMoveListener(tvSWTCommon);
		cTable.addKeyListener(tvSWTCommon);
		//composite.addSelectionListener(tvSWTCommon);
		
		cTable.addTraverseListener(new TraverseListener() {
			public void keyTraversed(TraverseEvent e) {
				e.doit = true;
			}
		});
		
		
		SelectedContentManager.addCurrentlySelectedContentListener(new SelectedContentListener() {
			public void currentlySelectedContentChanged(
					ISelectedContent[] currentContent, String viewID) {
				redrawTable();
			}
		});
		
		cTable.addFocusListener(new FocusListener() {
			public void focusLost(FocusEvent e) {
				isFocused = false;
				redrawTable();
			}
			
			public void focusGained(FocusEvent e) {
				isFocused = true;
				redrawTable();
			}
		});
		isFocused = cTable.isFocusControl();

		new TableTooltips(this, cTable);

		TableColumnManager tcManager = TableColumnManager.getInstance();

		String sSortColumn = tcManager.getDefaultSortColumnName(tableID);
		if (sSortColumn == null || sSortColumn.length() == 0) {
			sSortColumn = sDefaultSortOn;
		}

		TableColumnCore tc = tcManager.getTableColumnCore(tableID, sSortColumn);
		if (tc == null && tableColumns.length > 0) {
			tc = tableColumns[0];
		}
		setSortColumn(tc, false);

		triggerLifeCycleListener(TableLifeCycleListener.EVENT_INITIALIZED);

		configMan.addParameterListener("Graphics Update", this);
		configMan.addParameterListener("ReOrder Delay", this);
		configMan.addParameterListener("Table.extendedErase", this);
		configMan.addParameterListener("Table.headerHeight", this);
		Colors.getInstance().addColorsChangedListener(this);

		// So all TableView objects of the same TableID have the same columns,
		// and column widths, etc
		TableStructureEventDispatcher.getInstance(tableID).addListener(this);

	}

	protected void swt_vBarChanged() {
		if (DEBUG_SELECTION) {
			debug("vBar changed " + vBar.getSelection() + " via " + Debug.getCompressedStackTrace());
		}
		swt_calculateClientArea();
		cTable.update();
	}

	private void setupHeaderArea(final Canvas cHeaderArea) {

		cHeaderArea.addPaintListener(new PaintListener() {
			public void paintControl(PaintEvent e) {
				paintHeader(e);
			}
		});

		Listener l = new Listener() {
			boolean mouseDown = false;

			TableColumnCore columnSizing;

			int columnSizingStart = 0;

			public void handleEvent(Event e) {
				switch (e.type) {
					case SWT.MouseDown: {
						if (e.button != 1) {
							return;
						}
						mouseDown = true;

						columnSizing = null;
						int x = -clientArea.x;
						TableColumnCore[] visibleColumns = getVisibleColumns();
						for (TableColumnCore column : visibleColumns) {
							int w = column.getWidth();
							x += w;

							if (e.x >= x - 3 && e.x <= x + 3) {
								columnSizing = column;
								columnSizingStart = e.x;
								break;
							}
						}

						break;
					}

					case SWT.MouseUp: {
						if (e.button != 1) {
							return;
						}
						if (mouseDown && columnSizing == null) {
							TableColumnCore column = getTableColumnByOffset(e.x);
							if (column != null) {
								setSortColumn(column, true);
							}
						}
						columnSizing = null;
						mouseDown = false;
						break;
					}

					case SWT.MouseMove: {
						if (columnSizing != null) {
							int diff = (e.x - columnSizingStart);
							columnSizing.setWidth(columnSizing.getWidth() + diff);
							columnSizingStart = e.x;
						} else {
							int cursorID = SWT.CURSOR_HAND;
							int x = -clientArea.x;
							TableColumnCore[] visibleColumns = getVisibleColumns();
							for (TableColumnCore column : visibleColumns) {
								int w = column.getWidth();
								x += w;

								if (e.x >= x - 3 && e.x <= x + 3) {
									cursorID = SWT.CURSOR_SIZEWE;
									break;
								}
							}
							cHeaderArea.setCursor(e.display.getSystemCursor(cursorID));
							TableColumnCore column = getTableColumnByOffset(e.x);

							if (column == null) {
								cHeaderArea.setToolTipText(null);
							} else {
								String info = MessageText.getString(
										column.getTitleLanguageKey() + ".info", (String) null);
								if (column.showOnlyImage()) {
									String tt = MessageText.getString(
											column.getTitleLanguageKey());
									if (info != null) {
										tt += "\n" + info;
									}
									cHeaderArea.setToolTipText(tt);
								} else {
									cHeaderArea.setToolTipText(info);
								}
							}
						}
					}
					
				}
			}
		};

		cHeaderArea.addListener(SWT.MouseDown, l);
		cHeaderArea.addListener(SWT.MouseUp, l);
		cHeaderArea.addListener(SWT.MouseMove, l);

		Transfer[] types = new Transfer[] {
			TextTransfer.getInstance()
		};

		final DragSource ds = new DragSource(cHeaderArea, DND.DROP_MOVE);
		ds.setTransfer(types);
		ds.addDragListener(new DragSourceListener() {
			private String eventData;

			public void dragStart(DragSourceEvent event) {
				Cursor cursor = cHeaderArea.getCursor();
				if (cursor != null
						&& cursor.equals(event.display.getSystemCursor(SWT.CURSOR_SIZEWE))) {
					event.doit = false;
					return;
				}

				cHeaderArea.setCursor(null);
				TableColumnCore tc = getTableColumnByOffset(event.x);
				isHeaderDragging = tc != null;
				if (isHeaderDragging) {
					eventData = tc.getName();
				}
				System.out.println("drag " + eventData);
			}

			public void dragSetData(DragSourceEvent event) {
				event.data = eventData;
			}

			public void dragFinished(DragSourceEvent event) {
				isHeaderDragging = false;
				eventData = null;
			}
		});

		final DropTarget dt = new DropTarget(cHeaderArea, DND.DROP_MOVE);
		dt.setTransfer(types);
		dt.addDropListener(new DropTargetListener() {

			public void dropAccept(DropTargetEvent event) {
			}

			public void drop(final DropTargetEvent event) {
				if (event.data instanceof String) {
					TableColumn tcOrig = getTableColumn((String) event.data);
					Point pt = cTable.toControl(event.x, event.y);
					TableColumn tcDest = getTableColumnByOffset(pt.x);
					if (tcDest == null) {
						TableColumnCore[] visibleColumns = getVisibleColumns();
						if (visibleColumns != null && visibleColumns.length > 0) {
							tcDest = visibleColumns[visibleColumns.length - 1];
						}
					}
					if (tcOrig != null && tcDest != null) {
						int destPos = tcDest.getPosition();
						int origPos = tcOrig.getPosition();
						final boolean moveRight = destPos > origPos;
						TableColumnCore[] visibleColumns = getVisibleColumns();
						((TableColumnCore) tcOrig).setPositionNoShift(destPos);

						//System.out.println("Move " + origPos + " Right? " + moveRight + " of " + destPos);
						Arrays.sort(visibleColumns, new Comparator<TableColumnCore>() {
							public int compare(TableColumnCore o1, TableColumnCore o2) {
								if (o1 == o2) {
									return 0;
								}
								int diff = o1.getPosition() - o2.getPosition();
								if (diff == 0) {
									int i = o1.getName().equals(event.data) ? -1 : 1;
									if (moveRight) {
										i *= -1;
									}
									return i;
								}
								return diff;
							}
						});

						for (int i = 0; i < visibleColumns.length; i++) {
							TableColumnCore tc = visibleColumns[i];
							tc.setPositionNoShift(i);
						}
						setColumnsOrdered(visibleColumns);

						TableStructureEventDispatcher.getInstance(tableID).tableStructureChanged(
								false, getDataSourceType());
					}
				}
			}

			public void dragOver(DropTargetEvent event) {
			}

			public void dragOperationChanged(DropTargetEvent event) {
			}

			public void dragLeave(DropTargetEvent event) {
			}

			public void dragEnter(DropTargetEvent event) {
			}
		});
		cHeaderArea.addDisposeListener(new DisposeListener() {
			public void widgetDisposed(DisposeEvent e) {
				Utils.disposeSWTObjects(new Object[] {
					ds,
					dt,
					fontHeader,
					fontHeaderSmall
				});
			}
		});
	}

	@Override
	public void tableStructureChanged(final boolean columnAddedOrRemoved,
			final Class forPluginDataSourceType) {

		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				TableViewPainted.super.tableStructureChanged(columnAddedOrRemoved, forPluginDataSourceType);
				if (cHeaderArea != null && !cHeaderArea.isDisposed()) {
					cHeaderArea.redraw();
				}

				redrawTable();
			}
		});
	}

	protected void swt_paintComposite(PaintEvent e) {
		swt_calculateClientArea();
		if (canvasImage == null) {
			return;
		}
		
		//System.out.println(e.count + " paint " + e.gc.getClipping() + ";" + e.x + "," + e.y + "," + e.width + "," + e.height + " via " + Debug.getCompressedStackTrace());

		e.gc.drawImage(canvasImage, -clientArea.x, 0);
		
		// test line
		//e.gc.drawLine(0, 0, cTable.getSize().x, canvasImage.getBounds().height);
	}

	protected void swt_paintCanvasImage(GC gc, Rectangle drawBounds) {
		int end = drawBounds.y + drawBounds.height;

		gc.setFont(cTable.getFont());
		gc.setClipping(drawBounds);
		TableRowCore oldRow = null;
		int pos = -1;
		Set<TableRowPainted> visibleRows = this.visibleRows;
		
		for (TableRowPainted row : visibleRows) {
			TableRowPainted paintedRow = row;
			if (pos == -1) {
				pos = row.getIndex();
			} else {
				pos++;
			}
			Point drawOffset = paintedRow.getDrawOffset();
			int rowStartX = 0;
			int rowStartY = drawOffset.y - clientArea.y;
			int rowHeight = paintedRow.getHeight();
			//debug("Paint " + drawBounds.x + "x" + drawBounds.y + " " + drawBounds.width + "x" + drawBounds.height + "; Row=" +row.getIndex() + ";clip=" + gc.getClipping() +";drawOffset=" + drawOffset);
			if (drawBounds.intersects(rowStartX, rowStartY, 9999, rowHeight)) {
				// ensure full row height
				int diffY2 = (rowStartY + rowHeight) - (drawBounds.y + drawBounds.height); 
				if (diffY2 > 0 ) {
					drawBounds.height += diffY2; 
					gc.setClipping(drawBounds);
				}
				paintedRow.swt_paintGC(gc, drawBounds, rowStartX, rowStartY, pos);
			}
			oldRow = row;
		}

		int h;
		int yDirty;
		if (oldRow == null) {
			yDirty = drawBounds.y;
			h = drawBounds.height;
		} else {
			yDirty = ((TableRowPainted) oldRow).getDrawOffset().y
					+ ((TableRowPainted) oldRow).getFullHeight();
			h = (drawBounds.y + drawBounds.height) - yDirty;
		}
		if (h > 0) {
			int rowHeight = getRowDefaultHeight();
			if (extendedErase) {
				while (yDirty < end) {
					pos++;
					Color color = TableRowPainted.alternatingColors[pos % 2];
					if (color != null) {
						gc.setBackground(color);
					}
					if (color == null) {
						gc.setBackground(gc.getDevice().getSystemColor(
								SWT.COLOR_LIST_BACKGROUND));
					}
					gc.fillRectangle(drawBounds.x, yDirty, drawBounds.width, rowHeight);
					yDirty += rowHeight;
				}
			} else {
				gc.setBackground(gc.getDevice().getSystemColor(
						SWT.COLOR_LIST_BACKGROUND));
				gc.fillRectangle(drawBounds.x, yDirty, drawBounds.width, h);
			}
		}

		//gc.setForeground(getColorLine());
		TableColumnCore[] visibleColumns = getVisibleColumns();
		int x = 0;
		gc.setAlpha(20);
		for (TableColumnCore column : visibleColumns) {
			x += column.getWidth();

			// Vertical lines between columns
			gc.drawLine(x - 1, drawBounds.y, x - 1, drawBounds.y + drawBounds.height);
		}
		gc.setAlpha(255);
	}
	
	private Color getColorLine() {
		if (colorLine == null) {
			colorLine = cTable.getDisplay().getSystemColor(SWT.COLOR_LIST_BACKGROUND);
			HSLColor hslColor = new HSLColor();
			hslColor.initHSLbyRGB(colorLine.getRed(), colorLine.getGreen(),
					colorLine.getBlue());

			int lum = hslColor.getLuminence();
			if (lum > 127)
				lum -= 25;
			else
				lum += 40;
			hslColor.setLuminence(lum);

			colorLine = new Color(cTable.getDisplay(), hslColor.getRed(),
					hslColor.getGreen(), hslColor.getBlue());
		}

		return colorLine;
	}

	private void paintHeader(PaintEvent e) {

		Rectangle ca = cHeaderArea.getClientArea();
		Color c1 = e.display.getSystemColor(SWT.COLOR_LIST_BACKGROUND);
		Color c2 = e.display.getSystemColor(SWT.COLOR_WIDGET_BACKGROUND);
		Color line = c2;
		Color fg = e.display.getSystemColor(SWT.COLOR_LIST_FOREGROUND);

		
		Pattern patternUp = new Pattern(e.display, 0, 0, 0, ca.height, c1, c2);
		Pattern patternDown = new Pattern(e.display, 0, -ca.height , 0, 0, c2, c1);
		//e.gc.setBackgroundPattern(patternUp);
		//e.gc.fillRectangle(ca);

		e.gc.setForeground(line);
		//e.gc.drawLine(0, 0, clientArea.width, 0);
		e.gc.drawLine(0, headerHeight - 1, clientArea.width, headerHeight - 1);

		TableColumnCore[] visibleColumns = getVisibleColumns();
		GCStringPrinter sp;
		TableColumnCore sortColumn = getSortColumn();
		int x = -clientArea.x;
		for (TableColumnCore column : visibleColumns) {
			int w = column.getWidth();

			//squeeze last column's text into available visible space
			if (x + w > ca.width) {
				w = ca.width - x;
				if (w <= 16) {
					break;
				}
			}

			
			boolean isSortColumn = column.equals(sortColumn);

			e.gc.setBackgroundPattern(isSortColumn ? patternDown : patternUp);
			e.gc.fillRectangle(x, 1, w, headerHeight - 2);
			e.gc.setForeground(line);
			e.gc.drawLine(x + w - 1, 0, x + w - 1, headerHeight - 1);

			e.gc.setForeground(fg);
			int yOfs = 0;
			int wText = w;
/* Top Center
			if (isSortColumn) {
				int arrowY = 2;
				int arrowHeight = 6;
				yOfs = 8;
				// draw sort indicator
				int middle = w / 2;
				int y1, y2;
				int arrowHalfW = 4;
				if (column.isSortAscending()) {
					y2 = arrowY;
					y1 = y2 + arrowHeight;
				} else {
					y1 = arrowY;
					y2 = y1 + arrowHeight;
				}
				e.gc.setAntialias(SWT.ON);
				e.gc.setBackground(ColorCache.getColor(e.display, 0, 0, 0));
				e.gc.fillPolygon(new int[] {
					x + middle - arrowHalfW,
					y1,
					x + middle + arrowHalfW,
					y1,
					x + middle,
					y2
				});
			}
*/
			if (isSortColumn) {
				// draw sort indicator
				int arrowHeight = 6;
				int arrowY = (headerHeight / 2) - (arrowHeight / 2);
				int arrowHalfW = 4;
				int middle = w - arrowHalfW - 4;
				wText = w - (arrowHalfW * 2) - 5;
				int y1, y2;
				if (column.isSortAscending()) {
					y2 = arrowY;
					y1 = y2 + arrowHeight;
				} else {
					y1 = arrowY;
					y2 = y1 + arrowHeight;
				}
				e.gc.setAntialias(SWT.ON);
				e.gc.setBackground(fg);
				e.gc.fillPolygon(new int[] {
					x + middle - arrowHalfW,
					y1,
					x + middle + arrowHalfW,
					y1,
					x + middle,
					y2
				});
			}

			int xOfs = x + 2;
			
			boolean onlyShowImage = column.showOnlyImage();
			String text = "";
			if (!onlyShowImage) {
				text = MessageText.getString(column.getTitleLanguageKey());
			}

			int style = SWT.WRAP | SWT.CENTER;
			Image image = null;
			String imageID = column.getIconReference();
			if (imageID != null) {
				image = ImageLoader.getInstance().getImage(imageID);
				if (ImageLoader.isRealImage(image)) {
					if (onlyShowImage) {
						text = null;
						Rectangle imageBounds = image.getBounds();
						e.gc.drawImage(image, (int) (x + (w / 2.0) - (imageBounds.width / 2.0) + 0.5),
								(headerHeight / 2) - (imageBounds.height / 2));
					} else {
						text = "%0 " + text;
					}
				} else {
					image = null;
				}
			}

			if (text != null) {
  			sp = new GCStringPrinter(e.gc, text, new Rectangle(xOfs, yOfs - 1,
  					wText - 4, headerHeight - yOfs + 2), true, false,style);
  			if (image != null) {
  				sp.setImages(new Image[] { image } );
  			}
  			sp.calculateMetrics();
  			if (sp.isWordCut() || sp.isCutoff()) {
  				Font font = e.gc.getFont();
  				e.gc.setFont(fontHeaderSmall);
  				sp.printString();
  				e.gc.setFont(font);
  			} else {
  				sp.printString();
  			}
			}
			
			if (imageID != null) {
				ImageLoader.getInstance().releaseImage(imageID);
			}

			x += w;
		}

		e.gc.setBackgroundPattern(patternUp);
		e.gc.fillRectangle(x, 1, clientArea.width - x, headerHeight - 2);

		patternUp.dispose();
		patternDown.dispose();
		e.gc.setBackgroundPattern(null);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#obfusticatedImage(org.eclipse.swt.graphics.Image)
	 */
	public Image obfusticatedImage(Image image) {
		TableColumnCore[] visibleColumns = getVisibleColumns();
		TableRowPainted[] visibleRows = this.visibleRows.toArray(new TableRowPainted[0]);
		
		for (TableRowPainted row : visibleRows) {
			if (row == null || row.isRowDisposed()) {
				continue;
			}

			for (TableColumnCore tc : visibleColumns) {
				if (tc == null || !tc.isObfusticated()) {
					continue;
				}

				TableCellPainted cell = (TableCellPainted) row.getTableCell(tc.getName());
				if (cell == null) {
					continue;
				}

				String text = cell.getObfusticatedText();

				if (text != null) {

					final Rectangle cellBounds = cell.getBoundsOnDisplay();
					Point ptDisplay = cTable.getShell().getLocation();
					cellBounds.x -= ptDisplay.x;
					cellBounds.y -= ptDisplay.y;
					Rectangle boundsRaw = cell.getBoundsRaw();
					if (boundsRaw.y + cellBounds.height > clientArea.y
							+ clientArea.height) {
						cellBounds.height -= (boundsRaw.y + cellBounds.height)
								- (clientArea.y + clientArea.height);
					}
					int tableWidth = cTable.getClientArea().width;
					if (boundsRaw.x + cellBounds.width > clientArea.x
							+ tableWidth) {
						cellBounds.width -= (boundsRaw.x + cellBounds.width)
								- (clientArea.x + tableWidth);
					}

					UIDebugGenerator.obfusticateArea(image, cellBounds, text);
				}

			}
		}

		UISWTViewCore view = tvTabsCommon == null ? null
				: tvTabsCommon.getActiveSubView();
		if (view instanceof ObfusticateImage) {
			try {
				((ObfusticateImage) view).obfusticatedImage(image);
			} catch (Exception e) {
				Debug.out("Obfuscating " + view, e);
			}
		}
		return image;
	}

	protected TableViewSWTPanelCreator getMainPanelCreator() {
		return mainPanelCreator;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#setMainPanelCreator(org.gudy.azureus2.ui.swt.views.table.TableViewSWTPanelCreator)
	 */
	public void setMainPanelCreator(TableViewSWTPanelCreator mainPanelCreator) {
		this.mainPanelCreator = mainPanelCreator;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#setRowDefaultIconSize(org.eclipse.swt.graphics.Point)
	 */
	public void setRowDefaultIconSize(Point size) {
		setRowDefaultHeight(size.y);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableCell(int, int)
	 */
	public TableCellCore getTableCell(int x, int y) {
		TableRowSWT row = getTableRow(x, y, true);
		if (row == null) {
			return null;
		}

		TableColumnCore column = getTableColumnByOffset(x);
		if (column == null) {
			return null;
		}

		return row.getTableCellCore(column.getName());
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableCellMouseOffset(org.gudy.azureus2.ui.swt.views.table.TableCellSWT)
	 */
	public Point getTableCellMouseOffset(TableCellSWT tableCell) {
		if (tableCell == null) {
			return null;
		}
		Point pt = cTable.getDisplay().getCursorLocation();
		pt = cTable.toControl(pt);

		Rectangle bounds = tableCell.getBounds();
		int x = pt.x - bounds.x;
		if (x < 0 || x > bounds.width) {
			return null;
		}
		int y = pt.y - bounds.y;
		if (y < 0 || y > bounds.height) {
			return null;
		}
		return new Point(x, y);
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#enableFilterCheck(org.eclipse.swt.widgets.Text, com.aelitis.azureus.ui.common.table.TableViewFilterCheck)
	public void enableFilterCheck(Text txtFilter,
			TableViewFilterCheck<Object> filterCheck) {
		TableViewSWTFilter<?> filter = getSWTFilter();
		if (filter != null) {
			if (filter.widget != null && !filter.widget.isDisposed()) {
				filter.widget.removeKeyListener(tvSWTCommon);
				filter.widget.removeModifyListener(filter.widgetModifyListener);
			}
		} else {
			this.filter = filter = new TableViewSWTFilter();
		}
		filter.widget = txtFilter;
		if (txtFilter != null) {
			txtFilter.setMessage(MessageText.getString("MyTorrentsView.filter"));
			txtFilter.addKeyListener(tvSWTCommon);

			filter.widgetModifyListener = new ModifyListener() {
				public void modifyText(ModifyEvent e) {
					setFilterText(((Text) e.widget).getText());
				}
			};
			txtFilter.addModifyListener(filter.widgetModifyListener);

			if (txtFilter.getText().length() == 0) {
				txtFilter.setText(filter.text);
			} else {
				filter.text = filter.nextText = txtFilter.getText();
			}
		} else {
			filter.text = filter.nextText = "";
		}

		filter.checker = filterCheck;

		filter.checker.filterSet(filter.text);
		refilter();
	}
	
	public void disableFilterCheck() {
		TableViewSWTFilter<?> filter = getSWTFilter();
		if ( filter == null ){
			return;
		}
		
		if (filter.widget != null && !filter.widget.isDisposed()) {
			filter.widget.removeKeyListener(tvSWTCommon);
			filter.widget.removeModifyListener(filter.widgetModifyListener);
		}
		filter = null;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#setFilterText(java.lang.String)
	 */
	public void setFilterText(String s) {
		if (tvSWTCommon != null) {
			tvSWTCommon.setFilterText(s);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#enableSizeSlider(org.eclipse.swt.widgets.Composite, int, int)
	 */
	public boolean enableSizeSlider(Composite composite, int min, int max) {
		// TODO
		return false;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#disableSizeSlider()
	 */
	public void disableSizeSlider() {
		// TODO
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#addRowPaintListener(org.gudy.azureus2.ui.swt.views.table.TableRowSWTPaintListener)
	 */
	public void addRowPaintListener(TableRowSWTPaintListener listener) {
		if (tvSWTCommon != null) {
			tvSWTCommon.addRowPaintListener(listener);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#removeRowPaintListener(org.gudy.azureus2.ui.swt.views.table.TableRowSWTPaintListener)
	 */
	public void removeRowPaintListener(TableRowSWTPaintListener listener) {
		if (tvSWTCommon != null) {
			tvSWTCommon.removeRowPaintListener(listener);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#invokePaintListeners(org.eclipse.swt.graphics.GC, com.aelitis.azureus.ui.common.table.TableRowCore, com.aelitis.azureus.ui.common.table.TableColumnCore, org.eclipse.swt.graphics.Rectangle)
	 */
	public void invokePaintListeners(GC gc, TableRowCore row,
			TableColumnCore column, Rectangle cellArea) {
		if (tvSWTCommon != null) {
			tvSWTCommon.invokePaintListeners(gc, row, column, cellArea);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#addRowMouseListener(org.gudy.azureus2.plugins.ui.tables.TableRowMouseListener)
	 */
	public void addRowMouseListener(TableRowMouseListener listener) {
		if (tvSWTCommon != null) {
			tvSWTCommon.addRowMouseListener(listener);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#removeRowMouseListener(org.gudy.azureus2.plugins.ui.tables.TableRowMouseListener)
	 */
	public void removeRowMouseListener(TableRowMouseListener listener) {
		if (tvSWTCommon != null) {
			tvSWTCommon.removeRowMouseListener(listener);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#invokeRowMouseListener(org.gudy.azureus2.plugins.ui.tables.TableRowMouseEvent)
	 */
	public void invokeRowMouseListener(TableRowMouseEvent event) {
		if (tvSWTCommon != null) {
			tvSWTCommon.invokeRowMouseListener(event);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableOrTreeSWT()
	 */
	public TableOrTreeSWT getTableOrTreeSWT() {
		return null;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#packColumns()
	 */
	public void packColumns() {
		// TODO
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.core3.config.ParameterListener#parameterChanged(java.lang.String)
	 */
	public void parameterChanged(String parameterName) {
		boolean invalidate = parameterName == null;
		if (parameterName == null || parameterName.equals("Graphics Update")) {
			graphicsUpdate = configMan.getIntParameter("Graphics Update");
		}
		if (parameterName == null || parameterName.equals("ReOrder Delay")) {
			reOrderDelay = configMan.getIntParameter("ReOrder Delay");
		}
		if (parameterName == null || parameterName.equals("Table.extendedErase")) {
			extendedErase = configMan.getBooleanParameter("Table.extendedErase");
			invalidate = true;
		}
		if (parameterName == null || parameterName.equals("Table.headerHeight")) {
			headerHeight = configMan.getIntParameter("Table.headerHeight");
			if (headerHeight == 0) {
				headerHeight = DEFAULT_HEADER_HEIGHT;
			}
			setHeaderVisible(getHeaderVisible());
		}
		
		if (parameterName == null || parameterName.startsWith("Color")) {
			tableInvalidate();
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.impl.TableViewImpl#createNewRow(java.lang.Object)
	 */
	@Override
	public TableRowCore createNewRow(Object object) {
		return new TableRowPainted(null, this, object, true);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.impl.TableViewImpl#visibleRowsChanged()
	 */
	@Override
	public void visibleRowsChanged() {
		swt_visibleRowsChanged();
	}

	private void swt_visibleRowsChanged() {
		final List<TableRowSWT> newlyVisibleRows = new ArrayList<TableRowSWT>();
		final List<TableRowSWT> nowInVisibleRows;
		final ArrayList<TableRowSWT> rowsStayedVisibleButMoved = new ArrayList<TableRowSWT>();
		List<TableRowSWT> newVisibleRows;
		if (isVisible()) {
			// this makes a copy.. slower
			TableRowCore[] rows = getRows();
			newVisibleRows = new ArrayList<TableRowSWT>();
			recalculateVisibleRows(rows, 0, newVisibleRows,
					rowsStayedVisibleButMoved);

		} else {
			newVisibleRows = Collections.emptyList();
		}
		nowInVisibleRows = new ArrayList<TableRowSWT>(0);
		synchronized (visibleRows_sync) {
			if (visibleRows != null) {
				nowInVisibleRows.addAll(visibleRows);
			}
		}

		LinkedHashSet<TableRowPainted> rows = new LinkedHashSet<TableRowPainted>(newVisibleRows.size());
		for (TableRowSWT row : newVisibleRows) {
			rows.add((TableRowPainted) row);
			boolean removed = nowInVisibleRows.remove(row);
			if (!removed) {
				newlyVisibleRows.add(row);
			}
		}

		synchronized (visibleRows_sync) {
			visibleRows = rows;
		}

		if (DEBUG_ROWCHANGE) {
			debug("visRowsChanged; shown=" + visibleRows.size() + "; +"
					+ newlyVisibleRows.size() + "/-" + nowInVisibleRows.size() + "/"
					+ rowsStayedVisibleButMoved.size() + " via "
					+ Debug.getCompressedStackTrace(8));
		}
		Utils.getOffOfSWTThread(new AERunnable() {

			public void runSupport() {
				boolean bTableUpdate = false;

				for (TableRowSWT row : newlyVisibleRows) {
					// no need to refres, the redraw will do it
					//row.refresh(true, true);
					row.setShown(true, false);
					row.invalidate();
					redrawRow((TableRowPainted) row, false);
					rowsStayedVisibleButMoved.remove(row);
					if (Constants.isOSX) {
						bTableUpdate = true;
					}
				}

				for (TableRowSWT row : rowsStayedVisibleButMoved) {
					row.invalidate();
					redrawRow((TableRowPainted) row, false);
				}

				for (TableRowSWT row : nowInVisibleRows) {
					row.setShown(false, false);
				}

				if (bTableUpdate) {
					Utils.execSWTThread(new AERunnable() {
						public void runSupport() {
							if (cTable != null && !cTable.isDisposed()) {
								cTable.update();
							}
						}
					});
				}

			}
		});
	}

	private void recalculateVisibleRows(TableRowCore[] rows, int yStart,
			List<TableRowSWT> newVisibleRows,
			List<TableRowSWT> rowsStayedVisibleButMoved) {
		Rectangle bounds = clientArea;

		int y = yStart;
		String sDebug;
		if (DEBUG_ROWCHANGE) {
			sDebug = "Visible Rows: ";
		}
		for (TableRowCore row : rows) {
			if (row == null) {
				continue;
			}
			TableRowPainted rowSWT = ((TableRowPainted) row);
			int rowHeight = rowSWT.getHeight();
			int rowFullHeight = rowSWT.getFullHeight();

			if ((y < bounds.y + bounds.height) && (y + rowFullHeight > bounds.y)) {
				// this row or subrows are visible

				boolean offsetChanged = rowSWT.setDrawOffset(new Point(bounds.x, y));

				// check if this row
				if (y + rowHeight > bounds.y) {
					if (DEBUG_ROWCHANGE) {
						sDebug += (rowSWT.getParentRowCore() == null ? ""
								: rowSWT.getParentRowCore().getIndex() + ".")
								+ rowSWT.getIndex()
								+ "(ofs=" + (offsetChanged ? "*" : "")
								+ y
								+ ";rh="
								+ rowHeight + "/" + rowFullHeight + ")" + ", ";
					}

					if (offsetChanged) {
						rowsStayedVisibleButMoved.add(rowSWT);
					}
					newVisibleRows.add(rowSWT);
				}

				// check if subrows
				if (row.isExpanded()) {
					TableRowCore[] subRowsWithNull = row.getSubRowsWithNull();
					if (subRowsWithNull.length > 0) {
						recalculateVisibleRows(subRowsWithNull, y + rowHeight,
								newVisibleRows, rowsStayedVisibleButMoved);
					}
				}
			} else if (newVisibleRows.size() > 0) {
				if (DEBUG_ROWCHANGE) {
					sDebug += "break(ofs=" + y + ";bounds=" + bounds + ";rh=" + rowFullHeight + ")";
				}
				break;
			}
			y += rowFullHeight;
		}
		if (DEBUG_ROWCHANGE) {
			if (yStart == 0) {
				debug(sDebug);
			}
		}
	}
	
	@Override
	public int uiGuessMaxVisibleRows() {
		return (clientArea.height / defaultRowHeight) + 1;
	}

	@Override
	public void uiRemoveRows(TableRowCore[] rows, Integer[] rowIndexes) {
		if (focusedRow != null) {
  		for (TableRowCore row : rows) {
  			if (row == focusedRow) {
  				setFocusedRow(null);
  				break;
  			}
  		}
  	}
		int bottomIndex = getRowCount() - 1;
		if (bottomIndex < 0) {
			redrawTable();
		} else {
			TableRowCore rowBottom = getLastVisibleRow();
			if (rowBottom != null) {
				while (rowBottom.getParentRowCore() != null) {
					rowBottom = rowBottom.getParentRowCore();
				}
				
				if (indexOf(rowBottom) < 0) {
					redrawTable();
				}
			}
		}
	}
	
	private TableRowPainted getLastVisibleRow() {
		synchronized (visibleRows_sync) {
			if (visibleRows == null || visibleRows.size() == 0) {
				return null;
			}
			TableRowPainted rowBottom = null;
			for (TableRowPainted row : visibleRows) {
				rowBottom = row;
			}
			return rowBottom;
		}
	}


	@Override
	public void getOffUIThread(AERunnable runnable) {
		Utils.getOffOfSWTThread(runnable);
	}

	protected void swt_calculateClientArea() {
		if (cTable == null || cTable.isDisposed()) {
			return;
		}
		Rectangle oldClientArea = clientArea;
		Rectangle newClientArea = cTable.getClientArea();
		newClientArea.x = hBar.getSelection();
		newClientArea.y = vBar.getSelection();

		int w = 0;
		TableColumnCore[] visibleColumns = getVisibleColumns();
		for (TableColumnCore column : visibleColumns) {
			w += column.getWidth();
		}
		columnsWidth = w;
		w = newClientArea.width = Math.max(newClientArea.width, w);

		boolean refreshTable = false;
		boolean changedX;
		boolean changedY;
		//boolean changedW;
		boolean changedH;
		if (oldClientArea != null) {
			changedX = oldClientArea.x != newClientArea.x;
			changedY = oldClientArea.y != newClientArea.y;
			//changedW = oldClientArea.width != newClientArea.width;
			changedH = oldClientArea.height != newClientArea.height;
		} else {
			changedX = changedY = changedH = true;
			//changedX = changedY = changedW = changedH = true;
		}
		
		clientArea = newClientArea;
		if (tvSWTCommon != null) {
			tvSWTCommon.xAdj = -clientArea.x;
		}
		
		//System.out.println("CA=" + clientArea + " via " + Debug.getCompressedStackTrace());

		boolean needRedraw = false;
		if (changedY || changedH) {
			visibleRowsChanged();
			if (changedY && oldClientArea != null) {
				Set<TableRowPainted> visibleRows = this.visibleRows;
				if (visibleRows.size() > 0) {
					if (canvasImage != null && !canvasImage.isDisposed() && !changedH) {

						int yDiff = oldClientArea.y - newClientArea.y;
						if (Math.abs(yDiff) < clientArea.height) {
							boolean wasIn = in_swt_updateCanvasImage;
							in_swt_updateCanvasImage = true;
  						GC gc = new GC(canvasImage);
  						Rectangle bounds = canvasImage.getBounds();
  						//System.out.println("moving y " + yDiff + ";cah=" + clientArea.height);
  						if (yDiff > 0) {
  							gc.copyArea(0, 0, bounds.width, bounds.height, 0, yDiff, false);
					  		swt_paintCanvasImage(gc, new Rectangle(0, 0, 9999, yDiff));
					  		gc.setClipping((Rectangle) null);
  						} else {
  							gc.copyArea(0, -yDiff, bounds.width, bounds.height , 0, 0, false);
  							int h = -yDiff;
  							TableRowPainted row = getLastVisibleRow();
  							if (row != null) {
  								//row.invalidate();
  								h += row.getHeight();
  							}
					  		swt_paintCanvasImage(gc, new Rectangle(0, bounds.height - h, 9999, h));
					  		gc.setClipping((Rectangle) null);
  						}
  						gc.dispose();
							in_swt_updateCanvasImage = wasIn;
  						
  						needRedraw = true;
						} else {
							refreshTable = true;
						}
					}

				}
			}
		}

		if (changedX) {
			cHeaderArea.redraw();
		}

		Image newImage = canvasImage;

		//List<TableRowSWT> visibleRows = getVisibleRows();
		int h = 0;
		synchronized (visibleRows_sync) {
			TableRowPainted lastRow = getLastVisibleRow();
			if (lastRow != null) {
				h = lastRow.getDrawOffset().y - clientArea.y + lastRow.getHeight();
				if (h < clientArea.height && lastRow.isExpanded()) {
					TableRowCore[] subRows = lastRow.getSubRowsWithNull();
					for (TableRowCore subRow : subRows) {
						if (subRow == null) {
							continue;
						}
						TableRowPainted subRowP = (TableRowPainted) subRow;

						h += subRowP.getFullHeight();
						if (h >= clientArea.height) {
							break;
						}
					}
				}
			}
		}
		if (h < clientArea.height) {
			h = clientArea.height;
		}

		int oldH = canvasImage == null || canvasImage.isDisposed() ? 0
				: canvasImage.getBounds().height;
		int oldW = canvasImage == null || canvasImage.isDisposed() ? 0
				: canvasImage.getBounds().width;

		if (canvasImage == null || oldW != w || h > oldH) {
			//System.out.println("oldW=" + oldW + ";" + w+ ";h=" + h + ";" + oldH);
			if (h <= 0 || clientArea.width <= 0) {
				newImage = null;
			} else {
				newImage = new Image(shell.getDisplay(), w, h);
			}
		}
		boolean canvasChanged = (canvasImage != newImage);
		if (canvasChanged) {
			Image oldImage = canvasImage;
			canvasImage = newImage;
			
			if (oldImage != null && !oldImage.isDisposed()) {
				oldImage.dispose();
			}
		}
		
		

		// paint event will handle any changedX or changedW
		if (changedH || canvasChanged || refreshTable) {
			//System.out.println(changedX + ";" + changedY + ";" + changedH + ";" + canvasChanged);
			//System.out.println("Redraw " + Debug.getCompressedStackTrace());

			// run refreshTable on SWT (this) thread to ensure rows have been
			// refreshed for the updateCanvasImage call immediately after it
			__refreshTable(false);
			swt_updateCanvasImage(false);
		}
		
		//		System.out.println("imgBounds = " + canvasImage.getBounds() + ";ca="
		//				+ clientArea + ";" + composite.getClientArea() + ";h=" + h + ";oh="
		//				+ oldH + " via " + Debug.getCompressedStackTrace(3));

		if (needRedraw) {
			cTable.redraw();
		}
	}

	public void swt_updateCanvasImage(boolean immediateRedraw) {
		if (canvasImage != null && !canvasImage.isDisposed()) {
			swt_updateCanvasImage(canvasImage.getBounds(), immediateRedraw);
		}
	}

	private boolean in_swt_updateCanvasImage = false;
	protected void swt_updateCanvasImage(final Rectangle bounds, final boolean immediateRedraw) {
		// no need to sync around in_swt_updateCanvasImage, we are assumed to always
		// be on SWT thread and in_swt_updateCanvasImage is only used here
		if (in_swt_updateCanvasImage) {
			Utils.execSWTThreadLater(0, new AERunnable() {
				public void runSupport() {
					swt_updateCanvasImage(bounds, immediateRedraw);
				}
			});
			return;
		}
		in_swt_updateCanvasImage = true;
		try {
  		if (canvasImage == null || canvasImage.isDisposed() || bounds == null) {
  			return;
  		}
  		//System.out.println("UpdateCanvasImage " + bounds + "; via " + Debug.getCompressedStackTrace());
  		GC gc = new GC(canvasImage);
  		swt_paintCanvasImage(gc, bounds);
  		gc.dispose();
  		if (cTable != null && !cTable.isDisposed()) {
  			cTable.redraw(bounds.x - clientArea.x, bounds.y, bounds.width, bounds.height, false);
  			if (immediateRedraw) {
  				cTable.update();
  			}
  		}
  		if (sCanvasImage != null) {
  			sCanvasImage.getShell().setSize(canvasImage.getBounds().width, canvasImage.getBounds().height);
  			sCanvasImage.redraw(bounds.x, bounds.y, bounds.width, bounds.height, true);
  			sCanvasImage.update();
  		}
		} finally {
			in_swt_updateCanvasImage = false;
		}
	}

	public Rectangle getClientArea() {
		return clientArea;
	}

	public boolean isVisible() {
		if (!Utils.isThisThreadSWT()) {
			return isVisible;
		}
		boolean wasVisible = isVisible;
		isVisible = cTable != null && !cTable.isDisposed() && cTable.isVisible()
				&& !shell.getMinimized();
		if (isVisible != wasVisible) {
			visibleRowsChanged();
			UISWTViewCore view = tvTabsCommon == null ? null
					: tvTabsCommon.getActiveSubView();
			if (isVisible) {
				loopFactor = 0;

				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_FOCUSGAINED, null);
				}
			} else {
				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_FOCUSLOST, null);
				}
			}
		}
		return isVisible;
	}

	public void removeAllTableRows() {
		if (DEBUG_ROWCHANGE) {
			debug("RemoveAlLRows");
		}
		super.removeAllTableRows();
		synchronized (visibleRows_sync) {
			visibleRows = new LinkedHashSet<TableRowPainted>();
		}
		setFocusedRow(null);
		totalHeight = 0;
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (cTable == null || cTable.isDisposed()) {
					return;
				}
				swt_fixupSize();
				swt_updateCanvasImage(false);
				if (DEBUG_ROWCHANGE) {
					debug("RemoveAllRows done");
				}
			}
		});
	}

	protected void swt_fixupSize() {
		//debug("Set minSize to " + columnsWidth + "x" + totalHeight + ";ca=" + clientArea + ";" + Debug.getCompressedStackTrace());
		if (vBar != null && !vBar.isDisposed()) {
			int tableSize = clientArea.height;
			int max = totalHeight;
			if (max < tableSize) {
				vBar.setSelection(0);
				vBar.setEnabled(false);
				vBar.setVisible(false);
			} else {
				if (!vBar.isVisible()) {
					vBar.setVisible(true);
					vBar.setEnabled(true);
				}
				if (vBar.getMaximum() != max) {
					vBar.setMaximum(max);
					swt_vBarChanged();
				}
				vBar.setThumb(tableSize);
				vBar.setPageIncrement(tableSize);
			}
		}
		if (hBar != null && !hBar.isDisposed()) {
			int tableSize = cTable.getSize().x;
			int max = columnsWidth;
			if (vBar.isVisible()) {
				max += vBar.getSize().x;
			}
			if (max < tableSize) {
				hBar.setSelection(0);
				hBar.setEnabled(false);
				hBar.setVisible(false);
			} else {
				if (!hBar.isVisible()) {
					hBar.setVisible(true);
					hBar.setEnabled(true);
				}
				hBar.setValues(hBar.getSelection(), 0, max, tableSize, 50, tableSize);
			}
			if (vBar != null && !vBar.isDisposed() && hBar.isVisible()) {
				vBar.setThumb(clientArea.height - hBar.getSize().y);
				vBar.setMaximum(totalHeight - hBar.getSize().y);
				vBar.setPageIncrement(vBar.getPageIncrement() - hBar.getSize().y);
			}

		}
	}

	@Override
	protected void uiChangeColumnIndicator() {
		Utils.execSWTThread(new AERunnable() {

			@Override
			public void runSupport() {
				if (cHeaderArea != null && !cHeaderArea.isDisposed()) {
					cHeaderArea.redraw();
				}
			}
		});
	}

	public TableColumnCore getTableColumnByOffset(int mouseX) {
		int x = -clientArea.x;
		TableColumnCore[] visibleColumns = getVisibleColumns();
		for (TableColumnCore column : visibleColumns) {
			int w = column.getWidth();

			if (mouseX >= x && mouseX < x + w) {
				return column;
			}

			x += w;
		}
		return null;
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableRow(int, int, boolean)
	public TableRowSWT getTableRow(int x, int y, boolean anyX) {
		return (TableRowSWT) getRow(anyX ? 2 : x, clientArea.y + y);
	}

	@Override
	public void setSelectedRows(TableRowCore[] newSelectionArray, boolean trigger) {
		super.setSelectedRows(newSelectionArray, trigger);

		boolean focusInSelection = false;
		for (TableRowCore row : newSelectionArray) {
			if (row == null) {
				continue;
			}
			if (row.equals(focusedRow)) {
				focusInSelection = true;
				break;
			}
		}
		if (!focusInSelection) {
			setFocusedRow(newSelectionArray.length == 0 ? null : newSelectionArray[0]);
		}
	}

	public void setRowSelected(final TableRowCore row, boolean selected,
			boolean trigger) {
		if (selected && !isSelected(row)) {
			setFocusedRow(row);
		}
		super.setRowSelected(row, selected, trigger);

		if (row instanceof TableRowSWT) {
			((TableRowSWT) row).setWidgetSelected(selected);
		}
	}

	public void editCell(int column, int row) {
		//TODO
	}

	public int getColumnNo(int mouseX) {
		int x = -clientArea.x;
		TableColumnCore[] visibleColumns = getVisibleColumns();
		for (int i = 0; i < visibleColumns.length; i++) {
			TableColumnCore column = visibleColumns[i];
			int w = column.getWidth();

			if (mouseX >= x && mouseX < x + w) {
				return i;
			}

			x += w;
		}
		return -1;
	}

	public boolean isDragging() {
		return isDragging;
	}

	public TableViewSWTFilter<?> getSWTFilter() {
		return (TableViewSWTFilter<?>) filter;
	}

	public void openFilterDialog() {
		if (filter == null) {
			return;
		}
		SimpleTextEntryWindow entryWindow = new SimpleTextEntryWindow();
		entryWindow.initTexts("MyTorrentsView.dialog.setFilter.title", null,
				"MyTorrentsView.dialog.setFilter.text", new String[] {
					MessageText.getString(getTableID() + "View" + ".header")
				});
		entryWindow.setPreenteredText(filter.text, false);
		entryWindow.prompt();
		if (!entryWindow.hasSubmittedInput()) {
			return;
		}
		String message = entryWindow.getSubmittedInput();

		if (message == null) {
			message = "";
		}

		setFilterText(message);
	}

	public boolean isSingleSelection() {
		return !isMultiSelect;
	}

	public void expandColumns() {
		//TODO
	}

	@Override
	public void triggerTabViewsDataSourceChanged(boolean sendParent) {
		if (tvTabsCommon != null) {
			tvTabsCommon.triggerTabViewsDataSourceChanged(sendParent);
		}
	}
	
	@Override
	public void uiSelectionChanged(final TableRowCore[] newlySelectedRows,
			final TableRowCore[] deselectedRows) {
		//System.out.println("Redraw " + Debug.getCompressedStackTrace());
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				for (TableRowCore row : deselectedRows) {
					row.invalidate();
					redrawRow((TableRowPainted) row, false);
				}
				for (TableRowCore row : newlySelectedRows) {
					row.invalidate();
					redrawRow((TableRowPainted) row, false);
				}
			}
		});
	}

	public void delete() {
		triggerLifeCycleListener(TableLifeCycleListener.EVENT_DESTROYED);

		if (tvTabsCommon != null) {
			tvTabsCommon.delete();
			tvTabsCommon = null;
		}

		TableStructureEventDispatcher.getInstance(tableID).removeListener(this);
		TableColumnManager tcManager = TableColumnManager.getInstance();
		if (tcManager != null) {
			tcManager.saveTableColumns(getDataSourceType(), tableID);
		}

		Utils.disposeSWTObjects(new Object[] {
			cTable
		});
		cTable = null;

		removeAllTableRows();
		configMan.removeParameterListener("ReOrder Delay", this);
		configMan.removeParameterListener("Graphics Update", this);
		configMan.removeParameterListener("Table.extendedErase", this);
		configMan.removeParameterListener("Table.headerHeight", this);
		Colors.getInstance().removeColorsChangedListener(this);

		super.delete();

		MessageText.removeListener(this);
	}

	@Override
	public void generate(IndentWriter writer) {
		super.generate(writer);

		if (tvTabsCommon != null) {
			tvTabsCommon.generate(writer);
		}
	}

	private Menu createMenu() {
		if (!isMenuEnabled()) {
			return null;
		}

		final Menu menu = new Menu(shell, SWT.POP_UP);
		cTable.addListener(SWT.MenuDetect, new Listener() {
			public void handleEvent(Event event) {
				if (event.widget == cHeaderArea) {
					menu.setData("inBlankArea", false);
					menu.setData("isHeader", true);

				} else {
					boolean noRow = getTableRowWithCursor() == null;

					menu.setData("inBlankArea", noRow);
					menu.setData("isHeader", false);
				}
				Point pt = cHeaderArea.toControl(event.x, event.y);
				menu.setData("column", getTableColumnByOffset(pt.x));
			}
		});
		cHeaderArea.addListener(SWT.MenuDetect, new Listener() {
			public void handleEvent(Event event) {
				menu.setData("inBlankArea", false);
				menu.setData("isHeader", true);
				Point pt = cHeaderArea.toControl(event.x, event.y);
				menu.setData("column", getTableColumnByOffset(pt.x));
			}
		});
		MenuBuildUtils.addMaintenanceListenerForMenu(menu,
				new MenuBuildUtils.MenuBuilder() {
					public void buildMenu(Menu menu, MenuEvent menuEvent) {
						Object oIsHeader = menu.getData("isHeader");
						boolean isHeader = (oIsHeader instanceof Boolean)
								? ((Boolean) oIsHeader).booleanValue() : false;

						Object oInBlankArea = menu.getData("inBlankArea");
						boolean inBlankArea = (oInBlankArea instanceof Boolean)
								? ((Boolean) oInBlankArea).booleanValue() : false;

						TableColumnCore column = (TableColumnCore) menu.getData("column");

						if (isHeader) {
							tvSWTCommon.fillColumnMenu(menu, column, false);
						} else if (inBlankArea) {
							tvSWTCommon.fillColumnMenu(menu, column, true);
						} else {
							tvSWTCommon.fillMenu(menu, column);
						}

					}
				});

		return menu;
	}

	public void showColumnEditor() {
		if (tvSWTCommon != null) {
			tvSWTCommon.showColumnEditor();
		}
	}

	@Override
	public TableRowCore getFocusedRow() {
		return focusedRow;
	}

	public void setFocusedRow(TableRowCore row) {
		TableRowPainted oldFocusedRow = focusedRow;
		if (!(row instanceof TableRowPainted)) {
			row = null;
		}
		focusedRow = (TableRowPainted) row;
		if (focusedRow != null) {
			if (focusedRow.isVisible()
					&& focusedRow.getDrawOffset().y + focusedRow.getHeight() <= clientArea.y + clientArea.height
					&& focusedRow.getDrawOffset().y >= clientArea.y) {
				// redraw for BG color change
				redrawRow(focusedRow, false);
			} else {

				showRow(focusedRow);
			}
		}
		if (oldFocusedRow != null) {
			redrawRow(oldFocusedRow, false);
		}
	}

	public void showRow(final TableRowCore rowToShow) {
		// scrollto
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (isDisposed()) {
					return;
				}
				
				if (rowToShow.isVisible()) {
					// draw offset is valid, use that to scroll
					int y = ((TableRowPainted) rowToShow).getDrawOffset().y;
					if (y + rowToShow.getHeight() > clientArea.y + clientArea.height) {
						y -= (clientArea.height - rowToShow.getHeight());
					}
					vBar.setSelection(y);
					swt_vBarChanged();
				} else {
					TableRowCore parentFocusedRow = rowToShow;
					while (parentFocusedRow.getParentRowCore() != null) {
						parentFocusedRow = parentFocusedRow.getParentRowCore();
					}
					TableRowCore[] rows = getRows();
					int y = 0;
					for (TableRowCore row : rows) {
						if (row == parentFocusedRow) {
							if (parentFocusedRow != rowToShow) {
								y += row.getHeight();
								TableRowCore[] subRowsWithNull = parentFocusedRow.getSubRowsWithNull();
								for (TableRowCore subrow : subRowsWithNull) {
									if (subrow == rowToShow) {
										break;
									}
									y += ((TableRowPainted) subrow).getFullHeight();
								}
							}
							break;
						}
						y += ((TableRowPainted) row).getFullHeight();
					}

					if (y + rowToShow.getHeight() > clientArea.y + clientArea.height) {
						y -= (clientArea.height - rowToShow.getHeight());
					}
					// y now at top of focused row
					vBar.setSelection(y);
					swt_vBarChanged();
				}
			}
		});
	}

	boolean qdRowHeightChanged = false;
	public void rowHeightChanged(final TableRowCore row, int oldHeight,
			int newHeight) {

		synchronized (heightChangeSync) {
  		totalHeight += (newHeight - oldHeight);
  		//System.out.println("Height delta: " + (newHeight - oldHeight) + ";ttl=" + totalHeight);
  
  		if (qdRowHeightChanged) {
  			return;
  		}
  		qdRowHeightChanged = true;
		}
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				synchronized (heightChangeSync) {
					qdRowHeightChanged = false;
				}
				// if moving visibleRowsChanged(), make sure subrows being resized on
				// add trigger work properly
				visibleRowsChanged();
				swt_fixupSize();
			}
		});
	}

	public void redrawTable() {
		synchronized (TableViewPainted.this) {
			if (redrawTableScheduled) {
				return;
			}
			redrawTableScheduled = true;
		}

		visibleRowsChanged();
		//System.out.println("Redraw " + Debug.getCompressedStackTrace());
		Utils.execSWTThreadLater(0, new AERunnable() {
			public void runSupport() {
				synchronized (TableViewPainted.this) {
					redrawTableScheduled = false;
				}

				if (canvasImage != null && !canvasImage.isDisposed()) {
					canvasImage.dispose();
					canvasImage = null;
				}
				swt_calculateClientArea();
			}
		});
	}
	
	private String prettyIndex(TableRowCore row) {
		String s = "" + row.getIndex();
		if (row.getParentRowCore() != null) {
			s = row.getParentRowCore().getIndex() + "." + s;
		}
		return s;
	}

	public void redrawRow(final TableRowPainted row, final boolean immediateRedraw) {
		if (row == null) {
			return;
		}
		if (TableRowPainted.DEBUG_ROW_PAINT) {
			System.out.println(SystemTime.getCurrentTime() + "} redraw "
					+ prettyIndex(row) + " scheduled via " + Debug.getCompressedStackTrace());
		}
		Utils.execSWTThread(new AERunnable() {

			public void runSupport() {
				if (!isVisible || !row.isVisible()) {
					return;
				}
				Rectangle bounds = row.getDrawBounds();
				if (TableRowPainted.DEBUG_ROW_PAINT) {
					System.out.println(SystemTime.getCurrentTime() + "] redraw "
							+ prettyIndex(row) + " @ " + bounds);
				}
				if (bounds != null) {
					Composite composite = getComposite();
					if (composite != null && !composite.isDisposed()) {
						int h = isLastRow(row) ? composite.getSize().y - bounds.y
								: bounds.height;
						//row.debug("isLastRow?" + isLastRow(row) + ";" + bounds + ";" + h);
						swt_updateCanvasImage(new Rectangle(bounds.x, bounds.y, bounds.width, h), immediateRedraw);
					}
				}
			}
		});
	}

	public Object getSyncObject() {
		return lock;
	}
	
	@Override
	public boolean isTableSelected() {
		TableView tv = SelectedContentManager.getCurrentlySelectedTableView();
		return tv == this || (tv == null && isFocused);
	}
}
