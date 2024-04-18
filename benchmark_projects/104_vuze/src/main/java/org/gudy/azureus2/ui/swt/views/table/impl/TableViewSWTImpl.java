/*
 *
 * Copyright (C) 2004, 2005, 2006 Aelitis SAS, All rights Reserved
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details ( see the LICENSE file ).
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * AELITIS, SAS au capital de 46,603.30 euros,
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 */
package org.gudy.azureus2.ui.swt.views.table.impl;

import java.lang.reflect.Method;
import java.util.*;
import java.util.List;

import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.*;
import org.eclipse.swt.dnd.*;
import org.eclipse.swt.events.*;
import org.eclipse.swt.graphics.*;
import org.eclipse.swt.layout.*;
import org.eclipse.swt.widgets.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.config.ParameterListener;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.internat.MessageText.MessageTextListener;
import org.gudy.azureus2.core3.logging.LogEvent;
import org.gudy.azureus2.core3.logging.LogIDs;
import org.gudy.azureus2.core3.logging.Logger;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.plugins.ui.tables.TableRowMouseEvent;
import org.gudy.azureus2.plugins.ui.tables.TableRowMouseListener;
import org.gudy.azureus2.ui.swt.*;
import org.gudy.azureus2.ui.swt.debug.ObfusticateImage;
import org.gudy.azureus2.ui.swt.debug.UIDebugGenerator;
import org.gudy.azureus2.ui.swt.mainwindow.Colors;
import org.gudy.azureus2.ui.swt.plugins.UISWTViewEvent;
import org.gudy.azureus2.ui.swt.pluginsimpl.*;
import org.gudy.azureus2.ui.swt.views.table.*;
import org.gudy.azureus2.ui.swt.views.table.utils.TableColumnSWTUtils;

import com.aelitis.azureus.ui.common.table.*;
import com.aelitis.azureus.ui.common.table.TableViewFilterCheck;
import com.aelitis.azureus.ui.common.table.impl.TableColumnManager;
import com.aelitis.azureus.ui.common.table.impl.TableViewImpl;
import com.aelitis.azureus.ui.swt.imageloader.ImageLoader;

/** 
 * An IView with a sortable table.  Handles composite/menu/table creation
 * and management.
 *
 * @deprecated This implementation requires much massaging of the native table/tree widget
 * 
 * @author Olivier (Original PeersView/MyTorrentsView/etc code)
 * @author TuxPaper
 *         2004/Apr/20: Remove need for tableItemToObject
 *         2005/Oct/07: Virtual Table
 *         2005/Nov/16: Moved TableSorter into TableView
 *         
 * @note From TableSorter.java:<br>
 *   <li>2004/Apr/20: Remove need for tableItemToObject (store object in tableItem.setData)
 *   <li>2004/May/11: Use Comparable instead of SortableItem
 *   <li>2004/May/14: moved from org.gudy.azureus2.ui.swt.utils
 *   <li>2005/Oct/10: v2307 : Sort SWT.VIRTUAL Tables, Column Indicator
 *   
 * @future TableView should be split into two.  One for non SWT functions, and
 *          the other extending the first, with extra SWT stuff. 
 *
 * @future dataSourcesToRemove should be removed after a certain amount of time
 *          has passed.  Currently, dataSourcesToRemove is processed every
 *          refresh IF the table is visible, or it is processed when we collect
 *          20 items to remove.
 *          
 * @note 4005: We set a text cell's measured width to the columns prefered width
 *             instead of setting it to the actual space needed for the text.
 *             We should really store the last measured width in TableCell and
 *             use that.
 */
public class TableViewSWTImpl<DATASOURCETYPE>
	extends TableViewImpl<DATASOURCETYPE>
	implements ParameterListener, TableViewSWT<DATASOURCETYPE>,
	ObfusticateImage, MessageTextListener
{
	protected final static boolean DRAW_VERTICAL_LINES = Constants.isWindows;

	protected static final boolean DRAW_FULL_ROW = Constants.isWindows;

	private final static LogIDs LOGID = LogIDs.GUI;

	protected static final boolean DEBUG_CELL_CHANGES = false;

	private static final boolean DEBUG_ROWCHANGE = false;

	private static final boolean OBEY_COLUMN_MINWIDTH = false;

	/** Column name to sort on if user hasn't chosen one yet 
	 */
	protected String sDefaultSortOn;

	/** 1st column gap problem (Eclipse Bug 43910).  Set to true when table is 
	 * using TableItem.setImage 
	 */
	protected boolean bSkipFirstColumn = true;

	private Point ptIconSize = null;

	/** Composite for IView implementation */
	private Composite mainComposite;

	/** Composite that stores the table (sometimes the same as mainComposite) */
	private Composite tableComposite;

	/** Table for SortableTable implementation */
	private TableOrTreeSWT table;

	private ControlEditor editor;

	/** SWT style options for the creation of the Table */
	protected int iTableStyle;

	/** Context Menu */
	private Menu menu;

	/** For updating GUI.  
	 * Some UI objects get updating every X cycles (user configurable) 
	 */
	protected int loopFactor;

	/** How often graphic cells get updated
	 */
	protected int graphicsUpdate = configMan.getIntParameter("Graphics Update");

	protected int reOrderDelay = configMan.getIntParameter("ReOrder Delay");

	/**
	 * Cache of selected table items to bypass insufficient drawing on Mac OS X
	 */
	//private ArrayList oldSelectedItems;

	private ColumnMoveListener columnMoveListener = new ColumnMoveListener();

	/** TabViews */
	public boolean bEnableTabViews = false;

	private TableRowSWT[] visibleRows;

	private boolean[] columnsVisible;

	private TableViewSWTPanelCreator mainPanelCreator;

	private boolean columnPaddingAdjusted = false;

	private boolean columnVisibilitiesChanged = true;

	/**
	 * Up to date table client area.  So far, the best places to refresh
	 * this variable are in the PaintItem event and the scrollbar's events.
	 * Typically table.getClientArea() is time consuming 
	 */
	protected Rectangle clientArea;

	private boolean isVisible;

	// private Rectangle firstClientArea;

	private int lastHorizontalPos;
	

	private boolean useTree;

	protected int headerHeight;

	private Shell shell;

	private TableViewSWT_Common tvSWTCommon;

	private TableViewSWT_TabsCommon tvTabsCommon;


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
	public TableViewSWTImpl(Class<?> pluginDataSourceType, String _sTableID,
			String _sPropertiesPrefix, TableColumnCore[] _basicItems,
			String _sDefaultSortOn, int _iTableStyle) {
		super(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems);
		setProvideIndexesOnRemove(true);
		boolean wantTree = (_iTableStyle & SWT.CASCADE) != 0;
		_iTableStyle &= ~SWT.CASCADE;
		if (wantTree) {
			useTree = COConfigurationManager.getBooleanParameter("Table.useTree")
					&& !Utils.isCarbon;
		}
		sDefaultSortOn = _sDefaultSortOn;
		iTableStyle = _iTableStyle | SWT.V_SCROLL | SWT.DOUBLE_BUFFERED;

		tvSWTCommon = new TableViewSWT_Common(this) {
			@Override
			public void mouseDown(TableRowSWT row, TableCellCore cell, int button,
					int stateMask) {
				if (row != null && !row.isRowDisposed()) {
					tv.setRowSelected(row, true, true);
				}
			}
			
			public void widgetSelected(SelectionEvent event) {
				updateSelectedRows(table.getSelection(), true);
			}
			
			@Override
			public void keyReleased(KeyEvent e) {
				swt_calculateClientArea();
				visibleRowsChanged();

				super.keyReleased(e);
			}
		};
	}

	/**
	 * Main Initializer. Table Style will be SWT.SINGLE | SWT.FULL_SELECTION
	 *
	 * @param _sTableID Which table to handle (see 
	 *                   {@link org.gudy.azureus2.plugins.ui.tables.TableManager}
	 *                   ).  Config settings are stored with the prefix of 
	 *                   "Table.<i>TableID</i>"
	 * @param _sPropertiesPrefix Prefix for retrieving text from the properties
	 *                            file (MessageText).  
	 *                            Typically <i>TableID</i> + "View"
	 * @param _sDefaultSortOn Column name to sort on if user hasn't chosen one
	 *                         yet
	 */
	public TableViewSWTImpl(Class<?> pluginDataSourceType, String _sTableID,
			String _sPropertiesPrefix, String _sDefaultSortOn) {

		this(pluginDataSourceType, _sTableID, _sPropertiesPrefix,
				new TableColumnCore[0], _sDefaultSortOn, SWT.SINGLE
						| SWT.FULL_SELECTION | SWT.VIRTUAL);
	}

	// AbstractIView::initialize
	public void initialize(Composite composite) {
		composite.setRedraw(false);

		tvTabsCommon = new TableViewSWT_TabsCommon(this);

		shell = composite.getShell();
		mainComposite = tvTabsCommon.createSashForm(composite);
		tableComposite = tvTabsCommon.tableComposite;
		table = createTable(tableComposite);
		menu = createMenu(table);
		clientArea = table.getClientArea();
		editor = TableOrTreeUtils.createTableOrTreeEditor(table);
		editor.minimumWidth = 80;
		editor.grabHorizontal = true;
		initializeTable(table);

		triggerLifeCycleListener(TableLifeCycleListener.EVENT_INITIALIZED);

		configMan.addParameterListener("Graphics Update", this);
		configMan.addParameterListener("ReOrder Delay", this);
		Colors.getInstance().addColorsChangedListener(this);

		// So all TableView objects of the same TableID have the same columns,
		// and column widths, etc
		TableStructureEventDispatcher.getInstance(tableID).addListener(this);
		composite.setRedraw(true);
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

	/** Creates the Table.
	 *
	 * @return The created Table.
	 */
	public TableOrTreeSWT createTable(Composite panel) {
		table = TableOrTreeUtils.createGrid(panel, iTableStyle, useTree);
		table.setLayoutData(new GridData(GridData.FILL_BOTH));

		return table;
	}

	/** Sets up the sorter, columns, and context menu.
	 *
	 * @param table Table to be initialized
	 */
	public void initializeTable(final TableOrTreeSWT table) {
		iTableStyle = table.getStyle();
		if ((iTableStyle & SWT.VIRTUAL) == 0) {
			throw new Error("Virtual Table Required");
		}

		table.setLinesVisible(Utils.TABLE_GRIDLINE_IS_ALTERNATING_COLOR);
		table.setMenu(menu);
		table.setData("Name", tableID);
		table.setData("ObfusticateImage", this);
		
		// On Windows, TreeItems POSTPAINT event spendsabout 7% of it's time in getFont()
		// calling the OS API.  If we set the font, it skips the API call.
		// This could be optimized further by setting the font on each table item,
		// however, it's unknown what performace hit we'd get on row creation.
		table.setFont(table.getFont());

		// Setup table
		// -----------

		table.addPaintListener(new PaintListener() {
			public void paintControl(PaintEvent event) {
				swt_changeColumnIndicator();
				// This fixes the scrollbar not being long enough on Win2k
				// There may be other methods to get it to refresh right, but
				// layout(true, true) didn't work.
				table.setRedraw(false);
				table.setRedraw(true);
				table.removePaintListener(this);
			}
		});

		table.addListener(SWT.PaintItem, new TableViewSWT_PaintItem(this, table));

		if (Constants.isWindows) {
			TableViewSWT_EraseItem eraseItemListener = new TableViewSWT_EraseItem(this, table);
			table.addListener(SWT.EraseItem, eraseItemListener);
			table.addListener(SWT.Paint, eraseItemListener);
		}

		ScrollBar horizontalBar = table.getHorizontalBar();
		if (horizontalBar != null) {
			horizontalBar.addSelectionListener(new SelectionListener() {
				public void widgetDefaultSelected(SelectionEvent e) {
					Utils.execSWTThreadLater(0, new AERunnable() {
						public void runSupport() {
							swt_calculateClientArea();
						}
					});
					//updateColumnVisibilities();
				}

				public void widgetSelected(SelectionEvent e) {
					Utils.execSWTThreadLater(0, new AERunnable() {
						public void runSupport() {
							swt_calculateClientArea();
						}
					});
					//updateColumnVisibilities();
				}
			});
		}

		table.addListener(SWT.MeasureItem, new Listener() {
			public void handleEvent(Event event) {
				int iColumnNo = event.index;

				if (bSkipFirstColumn) {
					iColumnNo--;
				}

				TableColumnCore[] columnsOrdered = getVisibleColumns();
				if (iColumnNo >= 0 && iColumnNo < columnsOrdered.length) {
					TableColumnCore tc = columnsOrdered[iColumnNo];
					int preferredWidth = tc.getPreferredWidth();
					event.width = preferredWidth;
				}

				int defaultHeight = getRowDefaultHeight();
				if (event.height < defaultHeight) {
					event.height = defaultHeight;
				}
			}
		});

		// Deselect rows if user clicks on a blank spot (a spot with no row)
		table.addMouseListener(tvSWTCommon);
		table.addMouseMoveListener(tvSWTCommon);
		table.addSelectionListener(tvSWTCommon);
		
		// we are sent a SWT.Settings event when the language changes and
		// when System fonts/colors change.  In both cases, invalidate
		table.addListener(SWT.Settings, new Listener() {
			public void handleEvent(Event e) {
				tableInvalidate();
			}
		});
		
		if (useTree) {
  		Listener listenerExpandCollapse = new Listener() {
  			public void handleEvent(Event event) {
  				TableItemOrTreeItem item = TableOrTreeUtils.getEventItem(event.item);
  				if (item == null) {
  					return;
  				}
  				TableRowCore row = getRow(item);
  				if (row == null || row.isRowDisposed()) {
  					return;
  				}
  				row.setExpanded(event.type == SWT.Expand ? true : false);
  				Utils.execSWTThreadLater(0, new AERunnable() {
						public void runSupport() {
							visibleRowsChanged();
						}
					});
  			}
  		};
  		table.addListener(SWT.Expand, listenerExpandCollapse);
  		table.addListener(SWT.Collapse, listenerExpandCollapse);
		}

		new TableTooltips(this, table.getComposite());

		table.addKeyListener(tvSWTCommon);
		
		table.addDisposeListener(new DisposeListener(){
			public void widgetDisposed(DisposeEvent e) {
				TableViewSWTFilter<?> filter = getSWTFilter();
				if (filter != null && filter.widget != null && !filter.widget.isDisposed()) {
					filter.widget.removeKeyListener(tvSWTCommon);
					filter.widget.removeModifyListener(filter.widgetModifyListener);
				}
				Utils.disposeSWTObjects(new Object[] { sliderArea } );
			}
		});
/*
		if (Utils.isCocoa) {
			table.addListener(SWT.MouseVerticalWheel, new Listener() {
				public void handleEvent(Event event) {
					calculateClientArea();
					visibleRowsChanged();
				}
			});
		}
*/		
		ScrollBar bar = table.getVerticalBar();
		if (bar != null) {
			bar.addSelectionListener(new SelectionAdapter() {
				public void widgetSelected(SelectionEvent e) {
					Utils.execSWTThreadLater(0, new AERunnable() {
						public void runSupport() {
							// need to calc later as getClientArea isn't up to date yet
							// on Win
							swt_calculateClientArea();
							visibleRowsChanged();
						}
					});
					// Bug: Scroll is slow when table is not focus
					if (!table.isFocusControl()) {
						table.setFocus();
					}
				}
			});
		}

		table.setHeaderVisible(getHeaderVisible());
		headerHeight = table.getHeaderHeight();

		clientArea = table.getClientArea();
		//firstClientArea = table.getClientArea();
		table.addListener(SWT.Resize, new Listener() {
			public void handleEvent(Event event) {
				swt_calculateClientArea();
			}
		});

		swt_initializeTableColumns(table);

		MessageText.addListener(this);
	}
	
	public void localeChanged(Locale old_locale, Locale new_locale) {
		Utils.execSWTThreadLater(0, new AERunnable() {
			public void runSupport() {
				if (tvTabsCommon != null) {
					tvTabsCommon.localeChanged();
				}
				tableInvalidate();
				refreshTable(true);

				TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
				for (int i = 0; i < tableColumnsSWT.length; i++) {
					TableColumnCore column = (TableColumnCore) tableColumnsSWT[i].getData("TableColumnCore");
					if (column != null) {
						Messages.setLanguageText(tableColumnsSWT[i].getColumn(),
								column.getTitleLanguageKey());
					}
				}

			}
		});
	}

	
	// @see com.aelitis.azureus.ui.common.table.TableView#setHeaderVisible(boolean)
	public void setHeaderVisible(boolean visible) {
		super.setHeaderVisible(visible);

		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (table != null && !table.isDisposed()) {
					table.setHeaderVisible(getHeaderVisible());
					headerHeight = table.getHeaderHeight();
				}
			}
		});
	}

	protected void swt_calculateClientArea() {
		Rectangle oldClientArea = clientArea;
		clientArea = table.getClientArea();
		ScrollBar horizontalBar = table.getHorizontalBar();
		boolean clientAreaCausedVisibilityChanged = false;
		if (horizontalBar != null) {
			int pos = horizontalBar.getSelection();
			if (pos != lastHorizontalPos) {
				lastHorizontalPos = pos;
				clientAreaCausedVisibilityChanged = true;
			}
		}
		if (oldClientArea != null
				&& (oldClientArea.x != clientArea.x || oldClientArea.width != clientArea.width)) {
			clientAreaCausedVisibilityChanged = true;
		}
		if (oldClientArea != null
				&& (oldClientArea.y != clientArea.y || oldClientArea.height != clientArea.height)) {
			visibleRowsChanged();
		}
		if (oldClientArea != null
				&& (oldClientArea.height < table.getHeaderHeight())) {
			clientAreaCausedVisibilityChanged = true;
		}
		if (clientAreaCausedVisibilityChanged) {
			columnVisibilitiesChanged = true;
			Utils.execSWTThreadLater(50, new AERunnable() {
				public void runSupport() {
					if (columnVisibilitiesChanged) {
						refreshTable(false);
					}
				}
			});
		}
	}

	public void triggerTabViewsDataSourceChanged(boolean sendParent) {
		if (tvTabsCommon != null) {
			tvTabsCommon.triggerTabViewsDataSourceChanged(sendParent);
		}
	}

	private interface SourceReplaceListener
	{
		void sourcesChanged();

		void cleanup(Text toClean);
	}

	private SourceReplaceListener cellEditNotifier;

	private Control sliderArea;

	private boolean isDragging;

	private int maxItemShown = -1;

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#editCell(int, int)
	 */
	public void editCell(final int column, final int row) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				swt_editCell(column, row);
			}
		});
	}

	private void swt_editCell(final int column, final int row) {
		Text oldInput = (Text) editor.getEditor();
		if (column >= table.getColumnCount() || row < 0
				|| row >= table.getItemCount()) {
			cellEditNotifier = null;
			if (oldInput != null && !oldInput.isDisposed()) {
				editor.getEditor().dispose();
			}
			return;
		}

		TableColumnOrTreeColumn tcColumn = table.getColumn(column);
		final TableItemOrTreeItem item = table.getItem(row);

		String cellName = (String) tcColumn.getData("Name");
		final TableRowSWT rowSWT = (TableRowSWT) getRow(row);
		final TableCellSWT cell = rowSWT.getTableCellSWT(cellName);

		// reuse widget if possible, this way we'll keep the focus all the time on jumping through the rows
		final Text newInput = oldInput == null || oldInput.isDisposed() ? new Text(
				table.getComposite(), Constants.isOSX ? SWT.NONE : SWT.BORDER) : oldInput;
		final DATASOURCETYPE datasource = (DATASOURCETYPE) cell.getDataSource();
		if (cellEditNotifier != null) {
			cellEditNotifier.cleanup(newInput);
		}

		table.showItem(item);
		table.showColumn(tcColumn);

		newInput.setText(cell.getText());

		newInput.setSelection(0);
		newInput.selectAll();
		newInput.setFocus();

		class QuickEditListener
			implements ModifyListener, SelectionListener, KeyListener,
			TraverseListener, SourceReplaceListener, ControlListener
		{
			boolean resizing = true;

			public QuickEditListener(Text toAttach) {
				toAttach.addModifyListener(this);
				toAttach.addSelectionListener(this);
				toAttach.addKeyListener(this);
				toAttach.addTraverseListener(this);
				toAttach.addControlListener(this);

				cellEditNotifier = this;
			}

			public void modifyText(ModifyEvent e) {
				if (item.isDisposed()) {
					sourcesChanged();
					return;
				}
				if (((TableColumnCore) cell.getTableColumn()).inplaceValueSet(cell,
						newInput.getText(), false)) {
					newInput.setBackground(null);
				} else {
					newInput.setBackground(Colors.colorErrorBG);
				}
			}

			public void widgetDefaultSelected(SelectionEvent e) {
				if (item.isDisposed()) {
					sourcesChanged();
					newInput.traverse(SWT.TRAVERSE_RETURN);
					return;
				}
				((TableColumnCore) cell.getTableColumn()).inplaceValueSet(cell,
						newInput.getText(), true);
				rowSWT.invalidate();
				editCell(column, row + 1);
			}

			public void widgetSelected(SelectionEvent e) {
			}

			public void keyPressed(KeyEvent e) {
				if (e.keyCode == SWT.ARROW_DOWN || e.keyCode == SWT.ARROW_UP) {
					e.doit = false;
					editCell(column, row + (e.keyCode == SWT.ARROW_DOWN ? 1 : -1));
				}
			}

			public void keyReleased(KeyEvent e) {
			}

			public void keyTraversed(TraverseEvent e) {
				if (e.detail == SWT.TRAVERSE_ESCAPE) {
					e.doit = false;
					editCell(column, -1);
				}
			}

			public void sourcesChanged() {
				if (getRow(datasource) == rowSWT || getRow(datasource) == null
						|| newInput.isDisposed()) {
					return;
				}
				String newVal = newInput.getText();
				Point sel = newInput.getSelection();
				editCell(column, getRow(datasource).getIndex());
				if (newInput.isDisposed()) {
					return;
				}
				newInput.setText(newVal);
				newInput.setSelection(sel);
			}

			public void cleanup(Text oldText) {
				if (!oldText.isDisposed()) {
					oldText.removeModifyListener(this);
					oldText.removeSelectionListener(this);
					oldText.removeKeyListener(this);
					oldText.removeTraverseListener(this);
					oldText.removeControlListener(this);
				}
			}

			public void controlMoved(ControlEvent e) {
				table.showItem(item);
				if (resizing) {
					return;
				}
				resizing = true;

				Point sel = newInput.getSelection();

				TableOrTreeUtils.setEditorItem(editor, newInput, column, item);

				editor.minimumWidth = newInput.computeSize(SWT.DEFAULT, SWT.DEFAULT).x;

				Rectangle leftAlignedBounds = item.getBounds(column);
				leftAlignedBounds.width = editor.minimumWidth = newInput.computeSize(
						SWT.DEFAULT, SWT.DEFAULT).x;
				if (leftAlignedBounds.intersection(clientArea).equals(leftAlignedBounds)) {
					editor.horizontalAlignment = SWT.LEFT;
				} else {
					editor.horizontalAlignment = SWT.RIGHT;
				}

				editor.layout();

				newInput.setSelection(0);
				newInput.setSelection(sel);

				resizing = false;
			}

			public void controlResized(ControlEvent e) {
			}
		}

		QuickEditListener l = new QuickEditListener(newInput);

		l.modifyText(null);

		TableOrTreeUtils.setEditorItem(editor, newInput, column, item);
		table.deselectAll();
		table.select(table.getItem(row));
		setSelectedRows(new TableRowCore[] { getRow(row) }, true);

		l.resizing = false;

		l.controlMoved(null);
	}

	private void swt_updateColumnVisibilities(boolean doInvalidate) {
		TableColumnOrTreeColumn[] columns = table.getColumns();
		if (table.getItemCount() < 1 || columns.length == 0 || !table.isVisible()) {
			return;
		}
		columnVisibilitiesChanged = false;
		TableItemOrTreeItem topRow = table.getTopItem();
		if (topRow == null) {
			return;
		}
		for (int i = 0; i < columns.length; i++) {
			final TableColumnCore tc = (TableColumnCore) columns[i].getData("TableColumnCore");
			if (tc == null) {
				continue;
			}

			int position = tc.getPosition();
			if (position < 0 || position >= columnsVisible.length) {
				continue;
			}

			Rectangle size = topRow.getBounds(i);
			//System.out.println(tableID + ": column " + i + ":" + tc.getName() + ": size="  + size + "; ca=" + clientArea + "; pos=" + position);
			size.intersect(clientArea);
			boolean nowVisible = !size.isEmpty();
			//System.out.println("  visible; was=" + columnsVisible[position] + "; now=" + nowVisible + ";doValidae=" + doInvalidate);
			if (columnsVisible[position] != nowVisible) {
				columnsVisible[position] = nowVisible;
				if (nowVisible && doInvalidate) {
					swt_runForVisibleRows(new TableGroupRowRunner() {
						public void run(TableRowCore row) {
							TableCellCore cell = row.getTableCellCore(tc.getName());
							if (cell != null) {
  							cell.invalidate();
  							cell.redraw();
							}
						}
					});
				}
			}
		}
	}

	public boolean isColumnVisible(
			org.gudy.azureus2.plugins.ui.tables.TableColumn column) {
		int position = column.getPosition();
		if (position < 0 || position >= columnsVisible.length) {
			return false;
		}
		return columnsVisible[position];

	}

	protected void swt_initializeTableColumns(final TableOrTreeSWT table) {
		TableColumnOrTreeColumn[] oldColumns = table.getColumns();

		for (int i = 0; i < oldColumns.length; i++) {
			oldColumns[i].removeListener(SWT.Move, columnMoveListener);
		}

		for (int i = oldColumns.length - 1; i >= 0; i--) {
			oldColumns[i].dispose();
		}

		columnPaddingAdjusted = false;

		// Pre 3.0RC1 SWT on OSX doesn't call this!! :(
		ControlListener resizeListener = new ControlAdapter() {
			// Bug: getClientArea() eventually calls back to controlResized,
			//      creating a loop until a stack overflow
			private boolean bInFunction = false;

			public void controlResized(ControlEvent e) {
				TableColumnOrTreeColumn column = TableOrTreeUtils.getTableColumnEventItem(e.widget);
				if (column == null || column.isDisposed() || bInFunction) {
					return;
				}

				try {
					bInFunction = true;

					TableColumnCore tc = (TableColumnCore) column.getData("TableColumnCore");
					if (tc != null) {
						Long lPadding = (Long) column.getData("widthOffset");
						int padding = (lPadding == null) ? 0 : lPadding.intValue();
						int newWidth = column.getWidth();
						if (OBEY_COLUMN_MINWIDTH) {
  						int minWidth = tc.getMinWidth();
  						if (minWidth > 0 && newWidth - padding < minWidth) {
  							newWidth = minWidth + padding;
  							column.setWidth(minWidth);
  						}
						}
						tc.setWidth(newWidth - padding);
					}

					int columnNumber = table.indexOf(column);
					locationChanged(columnNumber);
				} finally {
					bInFunction = false;
				}
			}
		};

		// Add 1 to position because we make a non resizable 0-sized 1st column
		// to fix the 1st column gap problem (Eclipse Bug 43910)

		// SWT does not set 0 column width as expected in OS X; see bug 43910
		// this will be removed when a SWT-provided solution is available to satisfy all platforms with identation issue
		//bSkipFirstColumn = bSkipFirstColumn && !Constants.isOSX;

		if (bSkipFirstColumn) {
			TableColumnOrTreeColumn tc = table.createNewColumn(SWT.NULL);
			//tc.setWidth(useTree ? 25 : 0);
			tc.setWidth(0);
			tc.setResizable(false);
			tc.setMoveable(false);
		}

		TableColumnCore[] tableColumns = getAllColumns();
		TableColumnCore[] tmpColumnsOrdered = new TableColumnCore[tableColumns.length];
		//Create all columns
		int columnOrderPos = 0;
		Arrays.sort(tableColumns,
				TableColumnManager.getTableColumnOrderComparator());
		for (int i = 0; i < tableColumns.length; i++) {
			int position = tableColumns[i].getPosition();
			if (position != -1 && tableColumns[i].isVisible()) {
				table.createNewColumn(SWT.NULL);
				//System.out.println(i + "] " + tableColumns[i].getName() + ";" + position);
				tmpColumnsOrdered[columnOrderPos++] = tableColumns[i];
			}
		}
		int numSWTColumns = table.getColumnCount();
		int iNewLength = numSWTColumns - (bSkipFirstColumn ? 1 : 0);
		TableColumnCore[] columnsOrdered = new TableColumnCore[iNewLength];
		System.arraycopy(tmpColumnsOrdered, 0, columnsOrdered, 0, iNewLength);
		setColumnsOrdered(columnsOrdered);
		columnsVisible = new boolean[tableColumns.length];

		ColumnSelectionListener columnSelectionListener = new ColumnSelectionListener();

		//Assign length and titles
		//We can only do it after ALL columns are created, as position (order)
		//may not be in the natural order (if the user re-order the columns).
		int swtColumnPos = (bSkipFirstColumn ? 1 : 0);
		for (int i = 0; i < tableColumns.length; i++) {
			TableColumnCore columnCore = tableColumns[i];
			int position = columnCore.getPosition();
			if (position == -1 || !columnCore.isVisible()) {
				continue;
			}

			columnsVisible[i] = false;

			String sName = columnCore.getName();
			// +1 for Eclipse Bug 43910 (see above)
			// user has reported a problem here with index-out-of-bounds - not sure why
			// but putting in a preventative check so that hopefully the view still opens
			// so they can fix it

			if (swtColumnPos >= numSWTColumns) {
				Debug.out("Incorrect table column setup, skipping column '" + sName
						+ "', position=" + swtColumnPos + ";numCols=" + numSWTColumns);
				continue;
			}

			TableColumnOrTreeColumn column = table.getColumn(swtColumnPos);
			try {
				column.setMoveable(true);
			} catch (NoSuchMethodError e) {
				// Ignore < SWT 3.1
			}
			column.setAlignment(TableColumnSWTUtils.convertColumnAlignmentToSWT(columnCore.getAlignment()));
			String iconReference = columnCore.getIconReference();
			if (iconReference != null) {
				Image image = ImageLoader.getInstance().getImage(iconReference);
				column.setImage(image);
			} else {
				Messages.setLanguageText(column.getColumn(), columnCore.getTitleLanguageKey());
			}
			if (!Constants.isUnix && !Utils.isCarbon) {
				column.setWidth(columnCore.getWidth());
			} else {
				column.setData("widthOffset", new Long(1));
				column.setWidth(columnCore.getWidth() + 1);
			}
			if (columnCore.getMinWidth() == columnCore.getMaxWidth()
					&& columnCore.getMinWidth() > 0) {
				column.setResizable(false);
			}
			column.setData("TableColumnCore", columnCore);
			column.setData("configName", "Table." + tableID + "." + sName);
			column.setData("Name", sName);

			column.addControlListener(resizeListener);
			// At the time of writing this SWT (3.0RC1) on OSX doesn't call the 
			// selection listener for tables
			column.addListener(SWT.Selection, columnSelectionListener);
			

			swtColumnPos++;
		}

		// Initialize the sorter after the columns have been added
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
		fixAlignment(tc, true);
		swt_changeColumnIndicator();

		// Add move listener at the very end, so we don't get a bazillion useless 
		// move triggers
		TableColumnOrTreeColumn[] columns = table.getColumns();
		for (int i = 0; i < columns.length; i++) {
			TableColumnOrTreeColumn column = columns[i];
			column.addListener(SWT.Move, columnMoveListener);
		}

		columnVisibilitiesChanged = true;
	}

	public void fixAlignment(TableColumnCore tc, boolean sorted) {
		if (Constants.isOSX) {
			if (table.isDisposed() || tc == null) {
				return;
			}
			int[] columnOrder = table.getColumnOrder();
			int i = tc.getPosition() - (bSkipFirstColumn ? 1 : 0);
			if (i < 0 || i >= columnOrder.length) {
				return;
			}
			TableColumnOrTreeColumn swtColumn = table.getColumn(columnOrder[i]);
			if (swtColumn != null) {
				if (swtColumn.getAlignment() == SWT.RIGHT && sorted) {
					swtColumn.setText("   " + swtColumn.getText() + "   ");
				} else {
					swtColumn.setText(swtColumn.getText().trim());
				}
			}
		}
	}

	/** Creates the Context Menu.
	 * @param table 
	 *
	 * @return a new Menu object
	 */
	private Menu createMenu(final TableOrTreeSWT table) {
		if (!isMenuEnabled()) {
			return null;
		}
		
		final Menu menu = new Menu(shell, SWT.POP_UP);
		table.addListener(SWT.MenuDetect, new Listener() {
			public void handleEvent(Event event) {
				Point pt = event.display.map(null, table.getComposite(), new Point(event.x, event.y));
				boolean noRow = table.getItem(pt) == null;

				Rectangle clientArea = table.getClientArea();
				boolean inHeader = clientArea.y <= pt.y && pt.y < (clientArea.y + headerHeight);
				if (!noRow) {
					noRow = inHeader;
				}
				
				menu.setData("inBlankArea", (!inHeader && noRow));

				menu.setData("isHeader", new Boolean(noRow));

				menu.setData("column",getTableColumnByOffset(event.x)); 
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
							tvSWTCommon.fillColumnMenu(menu, column, inBlankArea);
						} else {
							tvSWTCommon.fillMenu(menu, column);
						}

					}
				});

		return menu;
	}


	/** IView.getComposite()
	 * @return the composite for this TableView
	 */
	public Composite getComposite() {
		return mainComposite;
	}

	public Composite getTableComposite() {
		return tableComposite;
	}
	
	public TableOrTreeSWT getTableOrTreeSWT() {
		return table;
	}

	// see common.TableView
	public void refreshTable(final boolean bForceSort) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				swt_refreshTable(bForceSort);

				if (tvTabsCommon != null) {
					tvTabsCommon.swt_refresh();
				}
			}
		});

		super.refreshTable(bForceSort);
	}

	private void swt_refreshTable(boolean bForceSort) {
		// don't refresh while there's no table
		if (table == null) {
			return;
		}

		// call to trigger invalidation if visibility changes
		isVisible();

		// XXX Try/Finally used to be there for monitor.enter/exit, however
		//     this doesn't stop re-entry from the same thread while already in
		//     process.. need a bAlreadyRefreshing variable instead
		try {
			if (getComposite() == null || getComposite().isDisposed()) {
				return;
			}

			if (columnVisibilitiesChanged == true) {
				swt_updateColumnVisibilities(true);
			}

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

			long lTimeStart = SystemTime.getMonotonousTime();

			Utils.getOffOfSWTThread(new AERunnable() {
				public void runSupport() {
					//Refresh all visible items in table...
					runForAllRows(new TableGroupRowVisibilityRunner() {
						public void run(TableRowCore row, boolean bVisible) {
							row.refresh(bDoGraphics, bVisible);
						}
					});
				}
			});

			if (TableViewImpl.DEBUGADDREMOVE) {
				long lTimeDiff = (SystemTime.getMonotonousTime() - lTimeStart);
				if (lTimeDiff > 500) {
					debug(lTimeDiff + "ms to refresh rows");
				}
			}

			loopFactor++;
		} finally {
		}
	}

	private void swt_refreshVisibleRows() {
		if (getComposite() == null || getComposite().isDisposed()) {
			return;
		}

		swt_runForVisibleRows(new TableGroupRowRunner() {
			public void run(TableRowCore row) {
				row.refresh(false, true);
			}
		});
	}

	private void locationChanged(final int iStartColumn) {
		if (getComposite() == null || getComposite().isDisposed()) {
			return;
		}

		columnVisibilitiesChanged = true;

		runForAllRows(new TableGroupRowRunner() {
			public void run(TableRowCore row) {
				row.locationChanged(iStartColumn);
			}
		});
	}

	/*
	private void doPaint(final GC gc, final Rectangle dirtyArea) {
		if (getComposite() == null || getComposite().isDisposed()) {
			return;
		}

		swt_runForVisibleRows(new TableGroupRowRunner() {
			public void run(TableRowCore row) {
				if (!(row instanceof TableRowSWT)) {
					return;
				}
				TableRowSWT rowSWT = (TableRowSWT) row;
				Rectangle bounds = rowSWT.getBounds();
				if (bounds.intersects(dirtyArea)) {

					if (Constants.isWindowsVistaOrHigher) {
						Image imgBG = new Image(gc.getDevice(), bounds.width, bounds.height);
						gc.copyArea(imgBG, bounds.x, bounds.y);
						rowSWT.setBackgroundImage(imgBG);
					}

					//System.out.println("paint " + row);
					Color oldBG = (Color) row.getData("bgColor");
					Color newBG = rowSWT.getBackground();
					if (oldBG == null || !oldBG.equals(newBG)) {
						//System.out.println("redraw " + row + "; " + oldBG + ";" + newBG);
						row.invalidate();
						row.redraw();
						row.setData("bgColor", newBG);
					} else {
						rowSWT.doPaint(gc, true);
					}
				}
			}
		});
	}
	*/

	/** IView.delete: This method is called when the view is destroyed.
	 * Each color instanciated, images and such things should be disposed.
	 * The caller is the GUI thread.
	 */
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

		if (table != null && !table.isDisposed()) {
			table.dispose();
		}
		removeAllTableRows();
		configMan.removeParameterListener("ReOrder Delay", this);
		configMan.removeParameterListener("Graphics Update", this);
		Colors.getInstance().removeColorsChangedListener(this);

		super.delete();

		//oldSelectedItems =  null;
		Composite comp = getComposite();
		if (comp != null && !comp.isDisposed()) {
			comp.dispose();
		}
		
		MessageText.removeListener(this);
	}

	// see common.TableView


	private void addDataSourcesToSWT(final Object dataSources[], boolean async) {
		try {
			if (isDisposed()) {
				return;
			}
			if (DEBUGADDREMOVE) {
				debug("--" + " Add " + dataSources.length + " rows to SWT "
						+ (async ? " async " : " NOW"));
			}

			
			if (async) {
				Utils.execSWTThreadLater(0, new AERunnable() {
					public void runSupport() {
						_addDataSourcesToSWT(dataSources);
					}
				});
			} else {
				Utils.execSWTThread(new AERunnable() {
					public void runSupport() {
						_addDataSourcesToSWT(dataSources);
					}
				}, false);
			}

			for (int i = 0; i < dataSources.length; i++) {
				Object dataSource = dataSources[i];
				if (dataSource == null) {
					continue;
				}
				TableRowCore row = getRow((DATASOURCETYPE) dataSource);
				TableColumnCore sortColumn = getSortColumn();
  			if (row != null && sortColumn != null) {
  				TableCellCore cell = row.getSortColumnCell(sortColumn.getName());
  				if (cell != null) {
  					try {
  						cell.invalidate();
  						cell.refresh(true);
  					} catch (Exception e) {
  						Logger.log(new LogEvent(LOGID,
  								"Minor error adding a row to table " + tableID, e));
  					}
  				}
  			}
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void _addDataSourcesToSWT(final Object dataSources[]) {
		if (table == null || table.isDisposed()) {
			return;
		}

		mainComposite.getParent().setCursor(
				table.getDisplay().getSystemCursor(SWT.CURSOR_WAIT));

		TableRowCore[] selectedRows = getSelectedRows();
			
		boolean bWas0Rows = table.getItemCount() == 0;
		try {

			if (DEBUGADDREMOVE) {
				debug("--" + " Add " + dataSources.length + " rows to SWT. size(false) == " + size(false));
			}

			// purposefully not included in time check 
			int size = size(false);
			// Bug in Windows (7).  If you add 10 rows by setItemCount,
			// Windows will do some crappy shifting down of the non-row area
			table.setItemCount(size);

			if (size == 1) {
				columnVisibilitiesChanged = true;
			}

		} catch (Exception e) {
			Logger.log(new LogEvent(LOGID, "Error while adding row to Table "
					+ tableID, e));
		}

		if (!columnPaddingAdjusted && table.getItemCount() > 0 && bWas0Rows) {
			TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
			TableItemOrTreeItem item = table.getItem(0);
			// on *nix, the last column expands to fill remaining space.. let's just not touch it
			int len = Constants.isUnix ? tableColumnsSWT.length - 1
					: tableColumnsSWT.length;
			for (int i = 0; i < len; i++) {
				TableColumnCore tc = (TableColumnCore) tableColumnsSWT[i].getData("TableColumnCore");
				if (tc != null) {
					boolean foundOne = false;

					Rectangle bounds = item.getBounds(i);
					int tcWidth = tc.getWidth();
					if (tcWidth != 0 && bounds.width != 0) {
						Object oOldOfs = tableColumnsSWT[i].getData("widthOffset");
						int oldOfs = (oOldOfs instanceof Number) ? ((Number)oOldOfs).intValue() : 0;
						int ofs = tc.getWidth() - bounds.width + oldOfs;
						if (ofs > 0 && ofs != oldOfs) {
							foundOne = true;
							tableColumnsSWT[i].setResizable(true);
							tableColumnsSWT[i].setData("widthOffset", new Long(ofs + oldOfs));
						}
					}
					if (foundOne) {
						tc.triggerColumnSizeChange(0);
					}
				}
			}
			columnPaddingAdjusted = true;
		} 
		if (bWas0Rows) {
			swt_updateColumnVisibilities(false);
		}

		setSelectedRows(selectedRows);
		if (DEBUGADDREMOVE) {
			debug("<< " + size(false));
		}

		boolean bReplacedVisible = false;
		for (Object ds : dataSources) {
			TableRowCore row = getRow((DATASOURCETYPE) ds);
			if (row != null) {
				int i = indexOf(row);
				int iTopIndex = uiGetTopIndex();
				int iBottomIndex = uiGetBottomIndex(iTopIndex);
				if (i >= iTopIndex && i <= iBottomIndex) {
					bReplacedVisible = true;
					break;
				}
			}
		}
		if (bReplacedVisible) {
			visibleRowsChanged();
		}
		
		mainComposite.getParent().setCursor(null);
	}
	
	@Override
	public void reallyAddDataSources(Object[] dataSources) {
		super.reallyAddDataSources(dataSources);

		addDataSourcesToSWT(dataSources, true);
	}

	@Override
	public void uiRemoveRows(TableRowCore[] rows, final Integer[] rowIndexes) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (table == null || table.isDisposed()) {
					return;
				}

				//TableRowCore[] oldSelectedRows = getSelectedRows();
				
				mainComposite.getParent().setCursor(
						table.getDisplay().getSystemCursor(SWT.CURSOR_WAIT));

				try {
					int iTopIndex = uiGetTopIndex();
					int iBottomIndex = uiGetBottomIndex(iTopIndex);
					if (DEBUGADDREMOVE) {
						debug("--- Remove: vis rows " + iTopIndex + " to " + iBottomIndex);
					}
					
					boolean needRefresh = false;
					for (Integer i : rowIndexes) {
						if (i >= iTopIndex && i <= iBottomIndex) {
							needRefresh = true;
							break;
						}
					}

					table.setItemCount(getRowCount());
					fillRowGaps(false);
					
					if (needRefresh || iBottomIndex == table.getItemCount() - 1) {
						table.redraw();
					}
				} finally {
					mainComposite.getParent().setCursor(null);
					
				}
			}
		});
		
	}
	
	// from common.TableView
	public void removeAllTableRows() {

		long lTimeStart = System.currentTimeMillis();

		final TableRowCore[] rows = getRows();


		super.removeAllTableRows();


		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (DEBUGADDREMOVE) {
					debug("removeAll (SWT)");
				}

				if (table != null && !table.isDisposed()) {
					table.removeAll();
				}

				// Image Disposal handled by each cell

				for (int i = 0; i < rows.length; i++) {
					rows[i].delete();
				}
			}
		});

		if (DEBUGADDREMOVE) {
			long lTimeDiff = (System.currentTimeMillis() - lTimeStart);
			if (lTimeDiff > 10) {
				debug("RemovaAll took " + lTimeDiff + "ms");
			}
		}
	}

	/* ParameterListener Implementation */

	public void parameterChanged(String parameterName) {
		if (parameterName == null || parameterName.equals("Graphics Update")) {
			graphicsUpdate = configMan.getIntParameter("Graphics Update");
		}
		if (parameterName == null || parameterName.equals("ReOrder Delay")) {
			reOrderDelay = configMan.getIntParameter("ReOrder Delay");
		}
		if (parameterName == null || parameterName.startsWith("Color")) {
			tableInvalidate();
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.impl.TableViewImpl#tableStructureChanged(boolean, java.lang.Class)
	 */
	public void tableStructureChanged(final boolean columnAddedOrRemoved,
			Class forPluginDataSourceType) {
		if (forPluginDataSourceType == null
				|| forPluginDataSourceType.equals(getDataSourceType())) {
			super.tableStructureChanged(columnAddedOrRemoved, forPluginDataSourceType);
			Utils.execSWTThread(new AERunnable() {
				public void runSupport() {
					if (table.isDisposed()) {
						return;
					}
  				_tableStructureChanged(columnAddedOrRemoved);
  			}
  		});
		}
	}
	
	private void _tableStructureChanged(boolean columnAddedOrRemoved) {

		swt_initializeTableColumns(table);
		refreshTable(false);

		triggerLifeCycleListener(TableLifeCycleListener.EVENT_INITIALIZED);
	}

	// ITableStructureModificationListener
	public void columnOrderChanged(final int[] positions) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				try {
					if (table.isDisposed()) {
						return;
					}
					table.setColumnOrder(positions);
					swt_updateColumnVisibilities(true);
				} catch (NoSuchMethodError e) {
					// Pre SWT 3.1
					// This shouldn't really happen, since this function only gets triggered
					// from SWT >= 3.1
					tableStructureChanged(false, null);
				}
			}
		});
	}

	/** 
	 * The Columns width changed
	 */
	// ITableStructureModificationListener
	public void columnSizeChanged(final TableColumnCore tableColumn, int diff) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				swt_columnSizeChanged(tableColumn);
			}
		});
	}

	public void swt_columnSizeChanged(TableColumnCore tableColumn) {
		int newWidth = tableColumn.getWidth();
		if (table == null || table.isDisposed()) {
			return;
		}

		TableColumnOrTreeColumn column = null;
		TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
		for (int i = 0; i < tableColumnsSWT.length; i++) {
			if (tableColumnsSWT[i].getData("TableColumnCore") == tableColumn) {
				column = tableColumnsSWT[i];
				break;
			}
		}
		if (column == null) {
			return;
		}
		Long lOfs = (Long) column.getData("widthOffset");
		if (lOfs != null) {
			newWidth += lOfs.intValue();
		}
		swt_refreshVisibleRows();
		if (column.isDisposed() || (column.getWidth() == newWidth)) {
			return;
		}

		if (Constants.isUnix) {
			final int fNewWidth = newWidth;
			final TableColumnOrTreeColumn fTableColumn = column;
			column.getDisplay().asyncExec(new AERunnable() {
				public void runSupport() {
					if (!fTableColumn.isDisposed()) {
						fTableColumn.setWidth(fNewWidth);
					}
				}
			});
		} else {
			column.setWidth(newWidth);
		}
	}

	public void columnRefresh(TableColumnCore tableColumn) {
		final String sColumnName = tableColumn.getName();
		runForAllRows(new TableGroupRowVisibilityRunner() {
			public void run(TableRowCore row, boolean bVisible) {
				TableCellCore cell = row.getTableCellCore(sColumnName);
				if (cell != null) {
					cell.refresh(true, bVisible);
				}
			}
		});
	}


	/** Warning: this method may require SWT Thread! 
	 * 
	 * TODO: Make sure callers are okay with that
	 */
	protected TableRowCore getRow(TableItemOrTreeItem item) {
		if (item == null) {
			return null;
		}
		try {
			Object o = item.getData("TableRow");
			if ((o instanceof TableRowCore) && !((TableRowCore) o).isRowDisposed()) {
				return (TableRowCore) o;
			}

			if (item.getParentItem() != null) {
				TableRowCore row = getRow(item.getParentItem());
				return row.linkSubItem(item.getParentItem().indexOf(item));
			}
			
			int iPos = table.indexOf(item);
			//System.out.println(iPos + " has no table row.. associating. " + Debug.getCompressedStackTrace(4));
			Object sortedRows_sync = getRowsSync();
			synchronized (sortedRows_sync) {
				if (iPos >= 0 && iPos < getRowCount()) {
					TableRowSWT row = (TableRowSWT) getRow(iPos);
					//System.out.print(".. associating to " + row);
					if (row != null && !row.isRowDisposed()) {
						row.setTableItem(iPos);
						//System.out.println(", now " + row);
						return row;
					}
					return null;
				}
			}
		} catch (Exception e) {
			Debug.out(e);
		}
		return null;
	}


	public TableRowSWT[] swt_getVisibleRows() {
		if (!isVisible()) {
			return new TableRowSWT[0];
		}
		
		synchronized (this) {
  		if (visibleRows == null) {
  			visibleRowsChanged();
  		}
  		
  		return visibleRows;
		}
	}

	/** For each visible row source, run the code provided by the specified 
	 * parameter.
	 *
	 * @param runner Code to run for each selected row/datasource
	 */
	public void swt_runForVisibleRows(TableGroupRowRunner runner) {
		TableRowSWT[] rows = swt_getVisibleRows();
		if (runner.run(rows)) {
			return;
		}

		for (int i = 0; i < rows.length; i++) {
			runner.run(rows[i]);
		}
	}


	/**
	 * Runs a specified task for a list of table items that the table contains
	 * @param items A list of TableItems that are part of the table view
	 * @param runner A task
	 */
	public void runForTableItems(List<TableItemOrTreeItem> items, TableGroupRowRunner runner) {
		if (table == null || table.isDisposed()) {
			return;
		}

		final Iterator<TableItemOrTreeItem> iter = items.iterator();
		List<TableRowCore> rows_to_use = new ArrayList<TableRowCore>(items.size());
		while (iter.hasNext()) {
			TableItemOrTreeItem tableItem = iter.next();
			if (tableItem.isDisposed()) {
				continue;
			}

			TableRowSWT row = (TableRowSWT) getRow(tableItem);
			if (row != null && !row.isRowDisposed()) {
				rows_to_use.add(row);
			}
		}
		if (rows_to_use.size() > 0) {
			TableRowCore[] rows = rows_to_use.toArray(new TableRowCore[rows_to_use.size()]);
			boolean ran = runner.run(rows);
			if (!ran) {
				for (int i = 0; i < rows.length; i++) {
					TableRowCore row = rows[i];
					runner.run(row);
				}
			}
		}
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#clipboardSelected()
	public void clipboardSelected() {
		String sToClipboard = "";
		for (int j = 0; j < table.getColumnCount(); j++) {
			if (j != 0) {
				sToClipboard += "\t";
			}
			sToClipboard += table.getColumn(j).getText();
		}

		TableRowCore[] rows = getSelectedRows();
		for (TableRowCore row : rows) {
			sToClipboard += "\n";
			TableColumnCore[] visibleColumns = getVisibleColumns();
			for (int j = 0; j < visibleColumns.length; j++) {
				TableColumnCore column = visibleColumns[j];
				if (column.isVisible()) {
  				if (j != 0) {
  					sToClipboard += "\t";
  				}
  				TableCellCore cell = row.getTableCellCore(column.getName());
  				if (cell != null) {
  					sToClipboard += cell.getClipboardText();
  				}
				}
			}
		}
		new Clipboard(getComposite().getDisplay()).setContents(new Object[] {
			sToClipboard
		}, new Transfer[] {
			TextTransfer.getInstance()
		});
	}

	/** Handle sorting of a column based on clicking the Table Header */
	private class ColumnSelectionListener
		implements Listener
	{
		/** Process a Table Header click
		 * @param event event information
		 */
		public void handleEvent(final Event event) {
			int maskNoButton = (event.stateMask & ~SWT.BUTTON_MASK);
			if (maskNoButton != 0) {
				return;
			}
			TableColumnOrTreeColumn column = TableOrTreeUtils.getTableColumnEventItem(event.widget);
			if (column == null) {
				return;
			}
			TableColumnCore tableColumnCore = (TableColumnCore) column.getData("TableColumnCore");
			if (tableColumnCore != null) {
				setSortColumn(tableColumnCore, true);
				columnVisibilitiesChanged = true;
				refreshTable(true);
			}
		}
	}

	/**
	 * Handle movement of a column based on user dragging the Column Header.
	 * SWT >= 3.1
	 */
	private class ColumnMoveListener
		implements Listener
	{
		public void handleEvent(Event event) {
			TableColumnOrTreeColumn column = TableOrTreeUtils.getTableColumnEventItem(event.widget);
			if (column == null) {
				return;
			}

			TableColumnCore tableColumnCore = (TableColumnCore) column.getData("TableColumnCore");
			if (tableColumnCore == null) {
				return;
			}

			TableOrTreeSWT table = column.getParent();

			// Get the 'added position' of column
			// It would have been easier if event (.start, .end) contained the old
			// and new position..
			TableColumnOrTreeColumn[] tableColumns = table.getColumns();
			int iAddedPosition;
			for (iAddedPosition = 0; iAddedPosition < tableColumns.length; iAddedPosition++) {
				if (column.getColumn() == tableColumns[iAddedPosition].getColumn()) {
					break;
				}
			}
			if (iAddedPosition >= tableColumns.length) {
				return;
			}

			// Find out position in the order list
			int iColumnOrder[];
			try {
				iColumnOrder = table.getColumnOrder();
			} catch (NoSuchMethodError e) {
				// Ignore < SWT 3.1
				return;
			}
			for (int i = 0; i < iColumnOrder.length; i++) {
				if (iColumnOrder[i] == iAddedPosition) {
					int iNewPosition = i - (bSkipFirstColumn ? 1 : 0);
					if (tableColumnCore.getPosition() != iNewPosition) {
						if (iNewPosition == -1) {
							iColumnOrder[0] = 0;
							iColumnOrder[1] = iAddedPosition;
							table.setColumnOrder(iColumnOrder);
							iNewPosition = 0;
						}
						//System.out.println("Moving " + tableColumnCore.getName() + " to Position " + i);
						tableColumnCore.setPositionNoShift(iNewPosition);
						tableColumnCore.saveSettings(null);
						TableStructureEventDispatcher.getInstance(tableID).columnOrderChanged(
								iColumnOrder);
					}
					break;
				}
			}
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getColumnNo(int)
	 */
	public int getColumnNo(int iMouseX) {
		int iColumn = -1;
		int itemCount = table.getItemCount();
		if (table.getItemCount() > 0) {
			//Using  table.getTopIndex() instead of 0, cause
			//the first row has no bounds when it's not visible under OS X.
			int topIndex = table.getTopIndex();
			if (topIndex >= itemCount || topIndex < 0) {
				topIndex = itemCount - 1;
			}
			TableItemOrTreeItem ti = table.getItem(topIndex);
			if (ti.isDisposed()) {
				return -1;
			}
			for (int i = bSkipFirstColumn ? 1 : 0; i < table.getColumnCount(); i++) {
				// M8 Fixes SWT GTK Bug 51777:
				//  "TableItem.getBounds(int) returns the wrong values when table scrolled"
				Rectangle cellBounds = ti.getBounds(i);
				//System.out.println("i="+i+";Mouse.x="+iMouseX+";cellbounds="+cellBounds);
				if (iMouseX >= cellBounds.x
						&& iMouseX < cellBounds.x + cellBounds.width
						&& cellBounds.width > 0) {
					iColumn = i;
					break;
				}
			}
		}
		return iColumn;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableView#getRow(int, int)
	 */
	public TableRowCore getRow(int x, int y) {
		int iColumn = getColumnNo(x);
		if (iColumn < 0) {
			return null;
		}

		TableItemOrTreeItem item = table.getItem(new Point(2, y));
		if (item == null) {
			return null;
		}
		return getRow(item);
	}

	public TableCellCore getTableCell(int x, int y) {
		int iColumn = getColumnNo(x);
		if (iColumn < 0) {
			return null;
		}

		TableItemOrTreeItem item = table.getItem(new Point(2, y));
		if (item == null) {
			item = table.getItem(new Point(x, y));
		}

		if (item == null) {
			return null;
		}
		TableRowSWT row = (TableRowSWT) getRow(item);

		if (row == null || row.isRowDisposed()) {
			return null;
		}

		TableColumnOrTreeColumn tcColumn = table.getColumn(iColumn);
		String sCellName = (String) tcColumn.getData("Name");
		if (sCellName == null) {
			return null;
		}

		return row.getTableCellCore(sCellName);
	}

	public TableRowSWT getTableRow(int x, int y, boolean anyX) {
		TableItemOrTreeItem item = table.getItem(new Point(anyX ? 2 : x, y));
		if (item == null) {
			return null;
		}
		return (TableRowSWT) getRow(item);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableColumnByOffset(int)
	 */
	public TableColumnCore getTableColumnByOffset(int x) {
		int iColumn = getColumnNo(x);
		if (iColumn < 0) {
			return null;
		}

		TableColumnOrTreeColumn column = table.getColumn(iColumn);
		return (TableColumnCore) column.getData("TableColumnCore");
	}

	// @see org.gudy.azureus2.core3.util.AEDiagnosticsEvidenceGenerator#generate(org.gudy.azureus2.core3.util.IndentWriter)
	public void generate(IndentWriter writer) {
		super.generate(writer);

		if (tvTabsCommon != null) {
			tvTabsCommon.generate(writer);
		}

		writer.println("Columns:");
		writer.indent();
		try {
			TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
			for (int i = 0; i < tableColumnsSWT.length; i++) {
				final TableColumnCore tc = (TableColumnCore) tableColumnsSWT[i].getData("TableColumnCore");
				if (tc != null) {
					writer.println(tc.getName() + ";w=" + tc.getWidth() + ";w-offset="
							+ tableColumnsSWT[i].getData("widthOffset"));
				}
			}
		} catch (Throwable t) {
		} finally {
			writer.exdent();
		}
	}

	public boolean getSkipFirstColumn() {
		return bSkipFirstColumn;
	}

	// see common.TableView
	public void setRowDefaultHeight(int iHeight) {
		if (ptIconSize == null) {
			ptIconSize = new Point(1, iHeight);
		} else {
			ptIconSize.y = iHeight;
		}
		if (!Constants.isOSX) {
			bSkipFirstColumn = true;
		}
	}

	public int getRowDefaultHeight() {
		if (ptIconSize == null) {
			return 0;
		}
		return ptIconSize.y;
	}

	// from common.TableView
	public void setRowDefaultIconSize(Point size) {
		ptIconSize = size;
		if (!Constants.isOSX) {
			bSkipFirstColumn = true;
		}
	}


	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.impl.TableViewImpl#selectRow(com.aelitis.azureus.ui.common.table.TableRowCore, boolean)
	 */
	public void setRowSelected(final TableRowCore row, boolean selected, boolean trigger) {
		super.setRowSelected(row, selected, trigger);
		
		if (row instanceof TableRowSWT) {
			((TableRowSWT) row).setWidgetSelected(selected);
		}
	}

	protected void updateSelectedRows(TableItemOrTreeItem[] newSelectionArray, boolean trigger) {
		List<TableRowCore> newSelectionList = new ArrayList<TableRowCore>(1);

		//System.out.print("Selected Items: ");
		for (TableItemOrTreeItem item : newSelectionArray) {
			//System.out.print(table.indexOf(item));
			TableRowCore row = getRow(item);
			if (row != null && !row.isRowDisposed()) {
				newSelectionList.add(row);
			}// else { System.out.print("( NO ROW)"); }
			//System.out.print(", ");
		}
		//System.out.println();
		setSelectedRows(newSelectionList.toArray(new TableRowCore[0]), trigger);
	}

	@Override
	public void uiSelectionChanged(final TableRowCore[] newlySelectedRows,
			final TableRowCore[] deselectedRows) {
		Utils.execSWTThread(new AERunnable() {
			
			@Override
			public void runSupport() {
				if (table.isDisposed()) {
					return;
				}
				
				for (TableRowCore row : deselectedRows) {
					if (row instanceof TableRowImpl) {
						TableRowImpl rowImpl = (TableRowImpl) row;
						TableItemOrTreeItem item = rowImpl.getItem();
						if (item != null && !item.isDisposed()) {
							table.deselect(item);
						}
					}
				}

				for (TableRowCore row : newlySelectedRows) {
					if (row instanceof TableRowImpl) {
						TableRowImpl rowImpl = (TableRowImpl) row;
						TableItemOrTreeItem item = rowImpl.getItem();
						if (item != null && !item.isDisposed()) {
							table.select(item);
						}
					}
				}

			}
		});
	}


	@Override
	protected boolean setSortColumn(TableColumnCore newSortColumn,
			boolean allowOrderChange) {
		final TableColumnCore oldSortColumn = getSortColumn();
		
		boolean columnChanged = super.setSortColumn(newSortColumn, allowOrderChange);
		if (columnChanged) {
			Utils.execSWTThread(new AERunnable() {
				public void runSupport() {
					TableColumnCore sortColumn = getSortColumn();
					fixAlignment(oldSortColumn, false);
					fixAlignment(sortColumn, true);
				}
			});
		}
		return columnChanged;
	}

	@Override
	protected void uiChangeColumnIndicator() {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				swt_changeColumnIndicator();
			}
		});
	}

	private void swt_changeColumnIndicator() {
		if (table == null || table.isDisposed()) {
			return;
		}

		try {
			TableColumnCore sortColumn = getSortColumn();
			// can't use TableColumnCore.getPosition, because user may have moved
			// columns around, messing up the SWT column indexes.  
			// We can either use search columnsOrdered, or search table.getColumns()
			TableColumnOrTreeColumn[] tcs = table.getColumns();
			for (int i = 0; i < tcs.length; i++) {
				String sName = (String) tcs[i].getData("Name");
				if (sName != null && sortColumn != null
						&& sName.equals(sortColumn.getName())) {
					table.setSortDirection(sortColumn.isSortAscending() ? SWT.UP
							: SWT.DOWN);
					table.setSortColumn(tcs[i]);
					return;
				}
			}

			table.setSortColumn(null);
		} catch (NoSuchMethodError e) {
			// sWT < 3.2 doesn't have column indicaters
		}
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#isRowVisible(com.aelitis.azureus.ui.common.table.TableRowCore)
	public boolean isRowVisible(TableRowCore row) {
		if (row.isInPaintItem()) {
			return true;
		}
		if (visibleRows == null) {
			return false;
		}
		for (TableRowCore visibleRow : visibleRows) {
			if (row == visibleRow) {
				if (Utils.isThisThreadSWT() && !isVisible()) {
					return false;
				}
				return true;
			}
		}
		return false;
	}

	@Override
	public void visibleRowsChanged() {
		//debug("VRC " + Debug.getCompressedStackTrace());
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				swt_visibleRowsChanged();
			}

		});
	}

	private void swt_visibleRowsChanged() {
		final List<TableRowSWT> newlyVisibleRows = new ArrayList<TableRowSWT>();
		final List<TableRowSWT> nowInVisibleRows;
		synchronized (this) {
  		List<TableItemOrTreeItem> visibleTableItems;
  		if (isVisible()) {
  			visibleTableItems = Utils.getVisibleTableItems(table);
  		} else {
  			visibleTableItems = Collections.emptyList();
  		}
			nowInVisibleRows = new ArrayList<TableRowSWT>(0);
  		if (visibleRows != null) {
  			nowInVisibleRows.addAll(Arrays.asList(visibleRows));
  		}
  		TableRowSWT[] rows = new TableRowSWT[visibleTableItems.size()];
  		int pos = 0;
  		for (TableItemOrTreeItem item : visibleTableItems) {
  			TableRowCore row = getRow(item);
  			if (row instanceof TableRowSWT) {
  				rows[pos++] = (TableRowSWT) row;
  				boolean removed = nowInVisibleRows.remove(row);
  				if (!removed) {
  					newlyVisibleRows.add((TableRowSWT) row);
  				}
  			}
  		}
  
  		if (pos < rows.length) {
  			// Some were null, shrink array
  			TableRowSWT[] temp = new TableRowSWT[pos];
  			System.arraycopy(rows, 0, temp, 0, pos);
  			visibleRows = temp;
  		} else {
  			visibleRows = rows;
  		}
		}
		
		if (DEBUG_ROWCHANGE) {
			System.out.println("visRowsChanged; shown=" + visibleRows.length + "; +"
					+ newlyVisibleRows.size() + "/-" + nowInVisibleRows.size() + " via "
					+ Debug.getCompressedStackTrace(8));
		}
		Utils.getOffOfSWTThread(new AERunnable() {
			
			public void runSupport() {
				boolean bTableUpdate = false;

				for (TableRowSWT row : newlyVisibleRows) {
					row.refresh(true, true);
					row.setShown(true, false);
					if (Constants.isOSX) {
						bTableUpdate = true;
					}
				}

				for (TableRowSWT row : nowInVisibleRows) {
					row.setShown(false, false);
				}

				if (bTableUpdate) {
					Utils.execSWTThread(new AERunnable() {
						public void runSupport() {
							table.update();
						}
					});
				}

			}
		});

	}

	public Image obfusticatedImage(final Image image) {
		if (table.getItemCount() == 0 || !isVisible()) {
			return image;
		}

		TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
		for (int i = 0; i < tableColumnsSWT.length; i++) {
			final TableColumnCore tc = (TableColumnCore) tableColumnsSWT[i].getData("TableColumnCore");

			if (tc != null && tc.isObfusticated()) {
				int iTopIndex = table.getTopIndex();
				int iBottomIndex = Utils.getTableBottomIndex(table, iTopIndex);

				int size = iBottomIndex - iTopIndex + 1;
				if (size <= 0 || iTopIndex < 0) {
					continue;
				}

				for (int j = iTopIndex; j <= iBottomIndex; j++) {
					TableItemOrTreeItem rowSWT = table.getItem(j);
					TableRowSWT row = (TableRowSWT) table.getItem(j).getData("TableRow");
					if (row != null && !row.isRowDisposed()) {
						TableCellSWT cell = row.getTableCellSWT(tc.getName());

						String text = cell.getObfusticatedText();

						if (text != null) {
							final Rectangle columnBounds = rowSWT.getBounds(i);
							if (columnBounds.y + columnBounds.height > clientArea.y
									+ clientArea.height) {
								columnBounds.height -= (columnBounds.y + columnBounds.height)
										- (clientArea.y + clientArea.height);
							}
							if (columnBounds.x + columnBounds.width > clientArea.x
									+ clientArea.width) {
								columnBounds.width -= (columnBounds.x + columnBounds.width)
										- (clientArea.x + clientArea.width);
							}
							
							Point location = Utils.getLocationRelativeToShell(table.getComposite());
							
							columnBounds.x += location.x;
							columnBounds.y += location.y;

							UIDebugGenerator.obfusticateArea(image, columnBounds, text);
						}
					}
				}

				//UIDebugGenerator.offusticateArea(image, columnBounds);
			}
		}

		UISWTViewCore view = tvTabsCommon == null ? null : tvTabsCommon.getActiveSubView();
		if (view instanceof ObfusticateImage) {
			try {
				((ObfusticateImage) view).obfusticatedImage(image);
			} catch (Exception e) {
				Debug.out("Obfuscating " + view, e);
			}
		}
		return image;
	}

	// from common.TableView
	public void setEnableTabViews(boolean enableTabViews) {
		bEnableTabViews = enableTabViews;
	}
	
	public boolean isTabViewsEnabled() {
		return bEnableTabViews;
	}

	public void addMenuFillListener(TableViewSWTMenuFillListener l) {
		tvSWTCommon.addMenuFillListener(l);
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#isDisposed()
	public boolean isDisposed() {
		return mainComposite == null || mainComposite.isDisposed() || table == null
				|| table.isDisposed();
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#setFocus()
	public void setFocus() {
		if (table != null && !table.isDisposed()) {
			table.setFocus();
		}
	}

	// @see org.gudy.azureus2.ui.swt.views.TableViewSWT#addKeyListener(org.eclipse.swt.events.KeyListener)
	public void addKeyListener(KeyListener listener) {
		if (tvSWTCommon == null || isDisposed()) {
			return;
		}
		tvSWTCommon.addKeyListener(listener);
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#removeKeyListener(org.eclipse.swt.events.KeyListener)
	public void removeKeyListener(KeyListener listener) {
		if (tvSWTCommon == null || isDisposed()) {
			return;
		}
		tvSWTCommon.removeKeyListener(listener);
	}
	
	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getKeyListeners()
	 */
	public KeyListener[] getKeyListeners() {
		if (tvSWTCommon == null || isDisposed()) {
			return new KeyListener[0];
		}
		return tvSWTCommon.getKeyListeners();
	}

	// @see com.aelitis.azureus.ui.common.table.TableView#selectAll()
	public void selectAll() {
		if (table != null && !table.isDisposed()) {
			// Used to ensure all rows have index, but I don't see a reason why.
			// Uses a lot of CPU, so kill it :)
			//ensureAllRowsHaveIndex();
			table.selectAll();
			super.selectAll();
		}
	}

	/**
	 * 
	 *
	 * @since 3.0.0.7
	 *
	private void ensureAllRowsHaveIndex() {
		for (int i = 0; i < sortedRows.size(); i++) {
			TableRowSWT row = sortedRows.get(i);
			row.setTableItem(i);
		}
	}
	*/

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#isDragging()
	 */
	public boolean isDragging() {
		return isDragging;
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#createDragSource(int)
	public DragSource createDragSource(int style) {
		final DragSource dragSource = new DragSource(table.getComposite(), style);
		dragSource.addDragListener(new DragSourceAdapter() {
			public void dragStart(DragSourceEvent event) {
				table.setCursor(null);
				isDragging = true;
			}
			
			public void dragFinished(DragSourceEvent event) {
				isDragging = false;
			}
		});
		table.addDisposeListener(new DisposeListener() {
			// @see org.eclipse.swt.events.DisposeListener#widgetDisposed(org.eclipse.swt.events.DisposeEvent)
			public void widgetDisposed(DisposeEvent e) {
				if (!dragSource.isDisposed()) {
					dragSource.dispose();
				}
			}
		});
		return dragSource;
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#createDropTarget(int)
	public DropTarget createDropTarget(int style) {
		final DropTarget dropTarget = new DropTarget(table.getComposite(), style);
		table.addDisposeListener(new DisposeListener() {
			// @see org.eclipse.swt.events.DisposeListener#widgetDisposed(org.eclipse.swt.events.DisposeEvent)
			public void widgetDisposed(DisposeEvent e) {
				if (!dropTarget.isDisposed()) {
					dropTarget.dispose();
				}
			}
		});
		return dropTarget;
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#indexOf(org.eclipse.swt.widgets.Widget)
	public TableRowCore getRow(DropTargetEvent event) {
		TableItemOrTreeItem ti = TableOrTreeUtils.getEventItem(event.item);
		if (ti != null) {
			return (TableRowCore) ti.getData("TableRow");
		}
		return null;
	}

	/**
	 * @return
	 */
	protected TableViewSWTPanelCreator getMainPanelCreator() {
		return mainPanelCreator;
	}

	// @see org.gudy.azureus2.ui.swt.views.TableViewSWT#setMainPanelCreator(org.gudy.azureus2.ui.swt.views.TableViewMainPanelCreator)
	public void setMainPanelCreator(TableViewSWTPanelCreator mainPanelCreator) {
		this.mainPanelCreator = mainPanelCreator;
	}

	public TableCellCore getTableCellWithCursor() {
		Point pt = table.getDisplay().getCursorLocation();
		pt = table.toControl(pt);
		return getTableCell(pt.x, pt.y);
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableRowWithCursor()
	public TableRowCore getTableRowWithCursor() {
		Point pt = table.getDisplay().getCursorLocation();
		pt = table.toControl(pt);
		return getTableRow(pt.x, pt.y, true);
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getTableCellMouseOffset()
	public Point getTableCellMouseOffset(TableCellSWT tableCell) {
		if (tableCell == null) {
			return null;
		}
		Point pt = table.getDisplay().getCursorLocation();
		pt = table.toControl(pt);

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


	/** Note: Callers need to be on SWT Thread */
	public boolean isVisible() {
		if (!Utils.isThisThreadSWT()) {
			return isVisible;
		}
		boolean wasVisible = isVisible;
		isVisible = table != null && !table.isDisposed() && table.isVisible() && !shell.getMinimized();
		if (isVisible != wasVisible) {
			visibleRowsChanged();
			UISWTViewCore view = tvTabsCommon == null ? null : tvTabsCommon.getActiveSubView();
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

	public void showRow(final TableRowCore row) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (isDisposed()) {
    			return;
    		}
				int index = row.getIndex();
				if (index >= 0 && index < table.getItemCount()) {
					table.showItem(table.getItem(index));
				}
			}
		});
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#openFilterDialog()
	 */
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

	public void setFilterText(String s) {
		if (tvSWTCommon != null) {
			tvSWTCommon.setFilterText(s);
		}
	}
	
	public TableViewSWTFilter<?> getSWTFilter() {
		return (TableViewSWTFilter<?>) filter;
	}

	public boolean
	isFiltered(
		DATASOURCETYPE	ds )
	{
		if ( filter == null ){
			return( true );
		}
		
		return( filter.checker.filterCheck( ds, filter.text, filter.regex ));
	}
	
	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#enableFilterCheck(org.eclipse.swt.widgets.Text, org.gudy.azureus2.ui.swt.views.table.TableViewFilterCheck)
	public void enableFilterCheck(Text txtFilter,
			TableViewFilterCheck<DATASOURCETYPE> filterCheck) {
		TableViewSWTFilter<?> filter = getSWTFilter();
		if (filter != null) {
			if (filter.widget != null && !filter.widget.isDisposed()) {
				filter.widget.removeKeyListener(tvSWTCommon);
				filter.widget.removeModifyListener(filter.widgetModifyListener);
			}
		} else{
			this.filter = filter = new TableViewSWTFilter<DATASOURCETYPE>();
		}
		filter.widget = txtFilter;
		if (txtFilter != null) {
			txtFilter.setMessage("Filter");
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
	
	public void disableFilterCheck()
	{
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
	
	public boolean enableSizeSlider(Composite composite, final int min, final int max) {
		try {
			if (sliderArea != null && !sliderArea.isDisposed()) {
				sliderArea.dispose();
			}
			Class<?> claTable = Class.forName("org.eclipse.swt.widgets."
					+ (useTree ? "Tree" : "Table"));
			final Method method = claTable.getDeclaredMethod("setItemHeight", new Class<?>[] {
				int.class
			});
			method.setAccessible(true);

			composite.setLayout(new FormLayout());
			sliderArea = new Label(composite, SWT.NONE);
			((Label)sliderArea).setImage(ImageLoader.getInstance().getImage("zoom"));
			sliderArea.addListener(SWT.MouseUp, new Listener() {
				public void handleEvent(Event event) {
					final Shell shell = new Shell(sliderArea.getShell(), SWT.BORDER);
					Listener l = new Listener() {
						public void handleEvent(Event event) {
							if (event.type == SWT.MouseExit) {
								Control curControl = event.display.getCursorControl();
								Point curPos = event.display.getCursorLocation();
								Point curPosRelShell = shell.toControl(curPos);
								Rectangle bounds = shell.getBounds();
								bounds.x = bounds.y = 0;
								if (!bounds.contains(curPosRelShell)) {
									shell.dispose();
									return;
								}
								if (curControl != null
										&& (curControl == shell || curControl.getParent() == shell)) {
									return;
								}
							}
							shell.dispose();
						}
					};
					shell.setBackgroundMode(SWT.INHERIT_FORCE);
					shell.setBackground(shell.getDisplay().getSystemColor(SWT.COLOR_INFO_BACKGROUND));
					shell.addListener(SWT.MouseExit, l);
					shell.addListener(SWT.Deactivate, l);
					FillLayout fillLayout = new FillLayout();
					fillLayout.marginHeight = 4;
					shell.setLayout(fillLayout);
					final Scale slider = new Scale(shell, SWT.VERTICAL);
					slider.addListener(SWT.MouseExit, l);
					slider.addListener(SWT.Deactivate, l);
					slider.setMinimum(min);
					slider.setMaximum(max);
					slider.setSelection(getRowDefaultHeight());
					try {
						method.invoke(table.getComposite(), new Object[] { slider.getSelection() } );
					} catch (Throwable e1) {
					}
					slider.addSelectionListener(new SelectionListener() {
						public void widgetSelected(SelectionEvent e) {
							setRowDefaultHeight(slider.getSelection());
							try {
								method.invoke(table.getComposite(), new Object[] { slider.getSelection() } );
							} catch (Throwable e1) {
								e1.printStackTrace();
							}
							tableInvalidate();
						}
						
						public void widgetDefaultSelected(SelectionEvent e) {
						}
					});
					Point pt = sliderArea.toDisplay(event.x - 2, event.y - 5);
					int width = Constants.isOSX ? 20 : 50;
					shell.setBounds(pt.x - (width / 2), pt.y, width, 120);
					shell.open();
				}
			});
			
			sliderArea.setLayoutData(Utils.getFilledFormData());
			composite.layout();
		} catch (Throwable t) {
			return false;
		}
		return true;
	}
	
	public void disableSizeSlider() {
		Utils.disposeSWTObjects(new Object[] { sliderArea });
	}
	
	public void setEnabled(final boolean enable) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (!isDisposed()) {
					table.setEnabled(enable);
					/*
					if (enable) {
						Image oldImage = table.getBackgroundImage();
						table.setBackgroundImage(null);
						Utils.disposeSWTObjects(new Object[] { oldImage } );
					} else {
						final Image image = new Image(table.getDisplay(), 50, 50);
						
						GC gc = new GC(image);
						gc.setBackground(ColorCache.getColor(gc.getDevice(), 0xee, 0xee, 0xee));
						gc.fillRectangle(0, 0, 50, 50);
						gc.dispose();
						table.addDisposeListener(new DisposeListener() {
							public void widgetDisposed(DisposeEvent e) {
								Utils.disposeSWTObjects(new Object[] { image } );
							}
						});
						
						table.setBackgroundImage(image);
					}
					*/
				}
			}
		});
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

	public boolean canHaveSubItems() {
		return useTree;
	}
		
	public void setParentDataSource(Object newDataSource) {
		super.setParentDataSource(newDataSource);

		triggerTabViewsDataSourceChanged(true);
	}
	
	public void packColumns() {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (table != null && !table.isDisposed()) {
					table.pack(true);
				}
			}
		});
	}
	
	public int getMaxItemShown() {
		return maxItemShown;
	}
	
	public void setMaxItemShown(int i) {
		maxItemShown  = i;
	}
	
	public int indexOf(TableRowCore row) {
		if (!Utils.isThisThreadSWT()) {
			return super.indexOf(row);
		}
		int i = ((TableRowImpl) row).getRealIndex();
		if (i == -1) {
			i = super.indexOf(row);
			if (i >= 0) {
				row.setTableItem(i);
			}
		}
		return i;
	}


	@Override
	public TableRowCore createNewRow(Object ds) {
		TableRowImpl row = new TableRowImpl(this, table, getVisibleColumns(), ds,
				bSkipFirstColumn);
		return row;
	}

	private int uiGetTopIndex() {
		return ((Number) Utils.execSWTThreadWithObject("uiGetTopIndex", new AERunnableObject() {
			public Object runSupport() {
				 return table.getTopIndex();
			}
		}, 500)).intValue();
	}
	
	@Override
	public int uiGuessMaxVisibleRows() {
		return 0;
	}
	
	private int uiGetBottomIndex(final int iTopIndex) {
		return ((Number) Utils.execSWTThreadWithObject("uiGetBottomIndex", new AERunnableObject() {
			public Object runSupport() {
				return Utils.getTableBottomIndex(table, iTopIndex);
			}
		}, 500)).intValue();
	}

	// @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#getRowSWT(java.lang.Object)
	public TableRowSWT getRowSWT(DATASOURCETYPE dataSource) {
		return (TableRowSWT) getRow(dataSource);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableViewSWT#enableFilterCheck(org.eclipse.swt.widgets.Text, com.aelitis.azureus.ui.common.table.TableViewFilterCheck)
	 */
	public void enableFilterCheck(
			Text txtFilter,
			org.gudy.azureus2.ui.swt.views.table.TableViewFilterCheck<DATASOURCETYPE> filterCheck) {
	}

	@Override
	public void getOffUIThread(AERunnable runnable) {
		Utils.getOffOfSWTThread(runnable);
	}
	
	@Override
	protected void _sortColumn(final boolean bForceDataRefresh, final boolean bFillGapsOnly,
			final boolean bFollowSelected) {
		if (Utils.isThisThreadSWT()) {
			super._sortColumn(bForceDataRefresh, bFillGapsOnly, bFollowSelected);
			return;
		}
		Utils.execSWTThread(new AERunnable() {
			
			@Override
			public void runSupport() {
				_sortColumn(bForceDataRefresh, bFillGapsOnly, bFollowSelected);
			}
		});
	}
	
	public boolean isSingleSelection() {
		return (iTableStyle & SWT.MULTI) > 0;
	}
	
	public void expandColumns() {
		TableColumnOrTreeColumn[] tableColumnsSWT = table.getColumns();
		for (int i = 0; i < tableColumnsSWT.length; i++) {
			TableColumnCore tc = (TableColumnCore) tableColumnsSWT[i].getData("TableColumnCore");
			if (tc != null) {
				int w = tc.getPreferredWidth();
				if (w <= 0) {
					w = tc.getMinWidth();
					if (w <= 0) {
						w = 100;
					}
				}
				tc.setWidth(w);
			}
		}
	}
	
	public void showColumnEditor() {
		if (tvSWTCommon != null) {
			tvSWTCommon.showColumnEditor();
		}
	}
}