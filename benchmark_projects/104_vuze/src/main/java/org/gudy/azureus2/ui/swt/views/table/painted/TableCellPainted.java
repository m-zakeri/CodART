package org.gudy.azureus2.ui.swt.views.table.painted;

import org.eclipse.swt.graphics.*;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;

import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.plugins.ui.Graphic;
import org.gudy.azureus2.plugins.ui.tables.TableColumn;
import org.gudy.azureus2.plugins.ui.tables.TableRow;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.pluginsimpl.UISWTGraphicImpl;
import org.gudy.azureus2.ui.swt.views.table.TableRowSWT;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;
import org.gudy.azureus2.ui.swt.views.table.impl.TableCellSWTBase;

import com.aelitis.azureus.ui.common.table.TableColumnCore;
import com.aelitis.azureus.ui.common.table.TableRowCore;

public class TableCellPainted
	extends TableCellSWTBase
{
	private static final boolean DEBUG_CELLPAINT = false;

	private Rectangle bounds;

	private String text = "";

	private int marginWidth;

	private int marginHeight;

	private boolean redrawScheduled;

	private Color colorFG;

	private Color colorBG;

	public TableCellPainted(TableRowSWT row, TableColumnCore column, int pos) {
		super(row, column);
		tableColumn.invokeCellAddedListeners(TableCellPainted.this);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getDataSource()
	 */
	public Object getDataSource() {
		if (isDisposed()) {
			return null;
		}
		TableRowCore row = tableRow;
		TableColumnCore col = tableColumn;

		if (row == null || col == null) {
			return (null);
		}
		return row.getDataSource(col.getUseCoreDataSource());
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getTableColumn()
	 */
	public TableColumn getTableColumn() {
		return tableColumn;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getTableRow()
	 */
	public TableRow getTableRow() {
		return tableRow;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getTableID()
	 */
	public String getTableID() {
		return tableRow.getTableID();
	}

	@SuppressWarnings("null")
	public static boolean stringEquals(String s0, String s1) {
		boolean s0Null = s0 == null;
		boolean s1Null = s1 == null;
		if (s0Null || s1Null) {
			return s0Null == s1Null;
		}
		return s0.equals(s1);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getText()
	 */
	public String getText() {
		if (hasFlag(FLAG_SORTVALUEISTEXT) && sortValue instanceof String) {
			return (String) sortValue;
		}

		return text;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getSortValue()
	 */
	public Comparable<?> getSortValue() {
		Comparable<?> value = super.getSortValue();
		return value == null ? "" : value;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#isShown()
	 */
	public boolean isShown() {
		return !isDisposed() && tableRow.getView().isColumnVisible(tableColumn);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getMaxLines()
	 */
	public int getMaxLines() {
		// TODO
		return 1;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getWidth()
	 */
	public int getWidth() {
		if (isDisposed()) {
			return -1;
		}
		return tableColumn.getWidth() - 2 - (getMarginWidth() * 2);
	}

	public int getWidthRaw() {
		if (isDisposed()) {
			return -1;
		}
		return tableColumn.getWidth() - 2;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getHeight()
	 */
	public int getHeight() {
		if (bounds == null) {
			return tableRow.getView().getRowDefaultHeight();
		}
		return bounds.height - (getMarginHeight() * 2);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getMarginHeight()
	 */
	public int getMarginHeight() {
		return marginHeight;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#setMarginHeight(int)
	 */
	public void setMarginHeight(int height) {
		marginHeight = height;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getMarginWidth()
	 */
	public int getMarginWidth() {
		return marginWidth;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#setMarginWidth(int)
	 */
	public void setMarginWidth(int width) {
		marginWidth = width;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getBackgroundGraphic()
	 */
	public Graphic getBackgroundGraphic() {
		// WARNING: requires SWT Thread!
		return new UISWTGraphicImpl(getBackgroundImage());
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableCellCore#locationChanged()
	 */
	public void locationChanged() {
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.impl.TableCellSWTBase#setCursorID(int)
	 */
	@Override
	public boolean setCursorID(int cursorID) {
		if (!super.setCursorID(cursorID)) {
			return false;
		}
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (isDisposed() || tableRow == null) {
					return;
				}
				if (isMouseOver()) {
					TableViewSWT<?> view = (TableViewSWT<?>) tableRow.getView();
					if (view != null) {
						Composite composite = view.getComposite();
						if (composite != null && !composite.isDisposed()) {
							composite.setCursor(composite.getDisplay().getSystemCursor(
									getCursorID()));
						}
					}
				}
			}
		});
		return true;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableCellCore#redraw()
	 */
	public void redraw() {

		if (!tableRow.isVisible() || redrawScheduled) {
			return;
		}
		redrawScheduled = true;
		if (DEBUG_CELLPAINT) {
			System.out.println(SystemTime.getCurrentTime() + "r"
					+ tableRow.getIndex() + "c" + tableColumn.getPosition()
					+ "} cellredraw via " + Debug.getCompressedStackTrace());
		}
		Utils.execSWTThread(new AERunnable() {

			public void runSupport() {
				if (isDisposed()) {
					return;
				}
				redrawScheduled = false;
				if (DEBUG_CELLPAINT) {
					System.out.println(SystemTime.getCurrentTime() + "r"
							+ tableRow.getIndex() + "c" + tableColumn.getPosition()
							+ "] cellredraw @ " + bounds);
				}
				if (bounds != null && tableRow != null) {
					TableViewPainted view = (TableViewPainted) tableRow.getView();
					if (view != null) {
						view.swt_updateCanvasImage(bounds, false);
					}
				}
			}
		});
	}

	public boolean setForeground(Color color) {
		// Don't need to set when not visible
		if (isInvisibleAndCanRefresh()) {
			return false;
		}

		if (color == colorFG || (color != null && color.equals(colorFG))
				|| (colorFG != null && colorFG.equals(color))) {
			return false;
		}

		colorFG = color;
		setFlag(FLAG_VISUALLY_CHANGED_SINCE_REFRESH);

		return true;
	}

	public Point getSize() {
		if (bounds == null) {
			return new Point(0, 0);
		}
		return new Point(bounds.width - (marginWidth * 2), bounds.height
				- (marginHeight * 2));
	}

	public Rectangle getBounds() {
		if (bounds == null) {
			return new Rectangle(0, 0, 0, 0);
		}
		return new Rectangle(bounds.x + marginWidth, bounds.y + marginHeight,
				bounds.width - (marginWidth * 2), bounds.height - (marginHeight * 2));
	}

	public Rectangle getBoundsRaw() {
		if (bounds == null) {
			return null;
		}
		return new Rectangle(bounds.x, bounds.y, bounds.width, bounds.height);
	}

	public Rectangle getBoundsOnDisplay() {
		if (isDisposed() || tableRow == null) {
			return null;
		}
		Rectangle bounds = getBoundsRaw();
		if (bounds == null) {
			return null;
		}
		TableViewPainted tv = ((TableViewPainted) tableRow.getView());
		if (tv == null) {
			return null;
		}
		Composite c = tv.getTableComposite();
		if (c == null || c.isDisposed()) {
			return null;
		}
		Point pt = c.toDisplay(bounds.x, bounds.y);
		bounds.x = pt.x;
		bounds.y = pt.y;
		bounds.height = getHeight();
		bounds.width = getWidthRaw();
		return bounds;
	}

	public Image getBackgroundImage() {
		if (bounds == null || bounds.isEmpty()) {
			return null;
		}

		Image image = new Image(Display.getDefault(), bounds.width
				- (marginWidth * 2), bounds.height - (marginHeight * 2));

		GC gc = new GC(image);
		gc.setForeground(getBackgroundSWT());
		gc.setBackground(getBackgroundSWT());
		gc.fillRectangle(0, 0, bounds.width, bounds.height);
		gc.dispose();

		return image;
	}

	public Color getForegroundSWT() {
		return colorFG;
	}

	public Color getBackgroundSWT() {
		return colorBG;
	}

	public void setBoundsRaw(Rectangle bounds) {
		this.bounds = bounds;
	}

	@Override
	public boolean uiSetText(String text) {
		boolean bChanged = !stringEquals(this.text, text);
		if (bChanged) {
			this.text = text;
		}
		return bChanged;
	}
}
