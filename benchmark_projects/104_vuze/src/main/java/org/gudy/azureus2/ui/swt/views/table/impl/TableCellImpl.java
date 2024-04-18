/*
 * File    : TableCellImpl.java
 * Created : 24 nov. 2003
 * By      : Olivier
 * Originally PluginItem.java, and changed to be more generic.
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

import java.util.Comparator;

import org.eclipse.swt.SWT;
import org.eclipse.swt.graphics.*;
import org.eclipse.swt.widgets.Item;

import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.logging.LogEvent;
import org.gudy.azureus2.core3.logging.LogIDs;
import org.gudy.azureus2.core3.logging.Logger;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Constants;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.plugins.ui.Graphic;
import org.gudy.azureus2.plugins.ui.tables.TableColumn;
import org.gudy.azureus2.plugins.ui.tables.TableRow;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.components.*;
import org.gudy.azureus2.ui.swt.plugins.UISWTGraphic;
import org.gudy.azureus2.ui.swt.pluginsimpl.UISWTGraphicImpl;
import org.gudy.azureus2.ui.swt.views.table.*;
import org.gudy.azureus2.ui.swt.views.table.utils.TableColumnSWTUtils;

import com.aelitis.azureus.ui.common.table.TableColumnCore;
import com.aelitis.azureus.ui.common.table.TableRowCore;


/** TableCellImpl represents one cell in the table.  
 * Table access is provided by BufferedTableItem.  
 * TableCellImpl is stored in and accessed by TableRowCore.
 * Drawing control gets passed to listeners.
 *
 * For plugins, this object is the implementation to TableCell.
 *
 * This object is needed to split core code from plugin code.
 */
public class TableCellImpl 
	extends TableCellSWTBase
{
	private static final LogIDs LOGID = LogIDs.GUI;
	
	private static final boolean canUseQuickDraw = Constants.isWindows;
	
	
  private BufferedTableItem bufferedTableItem;
	
  // Getting the cell's bounds can be slow.  QUICK_WIDTH uses TableColumn's width
	private static final boolean QUICK_WIDTH = true;

  public TableCellImpl(TableRowCore _tableRow, TableColumnCore _tableColumn,
      int position, BufferedTableItem item) {
  	super(_tableRow, _tableColumn);

  	if (item != null) {
    	bufferedTableItem = item;
    } else {
    	createBufferedTableItem(position);
    }

    tableColumn.invokeCellAddedListeners(TableCellImpl.this);
    //bDebug = (position == 1) && tableColumn.getTableID().equalsIgnoreCase("Peers");
  }

  /**
   * Initialize
   *  
   * @param _tableRow
   * @param _tableColumn
   * @param position
   */
  public TableCellImpl(TableRowSWT _tableRow, TableColumnCore _tableColumn,
                       int position) {
  	this(_tableRow, _tableColumn, position, null);
  }
  
  private void createBufferedTableItem(int position) {
    BufferedTableRow bufRow = (BufferedTableRow)tableRow;
    if (tableColumn.getType() == TableColumnCore.TYPE_GRAPHIC) {
      bufferedTableItem = new BufferedGraphicTableItem1(bufRow, position) {
        public void refresh() {
          TableCellImpl.this.refresh();
        }
        public void invalidate() {
        	clearFlag(FLAG_VALID);
        	redraw();
        }
        protected void quickRedrawCell(TableOrTreeSWT table, Rectangle dirty, Rectangle cellBounds) {
        	TableItemOrTreeItem item = row.getItem();
					boolean ourQuickRedraw = canUseQuickDraw && tableRow != null
							&& !tableRow.isMouseOver() && !tableRow.isSelected();
					if (ourQuickRedraw) {
      			TableCellImpl.this.quickRedrawCell2(table, item, dirty, cellBounds);
      		} else {
      			super.quickRedrawCell(table, dirty, cellBounds);
      		}
        }
      };
    	setOrientationViaColumn();
    } else {
			bufferedTableItem = new BufferedTableItemImpl(bufRow, position) {
				public void refresh() {
					TableCellImpl.this.refresh();
				}

				public void invalidate() {
					clearFlag(FLAG_VALID);
				}

				protected void quickRedrawCell(TableOrTreeSWT table, Rectangle dirty,
						Rectangle cellBounds) {
					TableItemOrTreeItem item = row.getItem();
					boolean ourQuickRedraw = canUseQuickDraw && tableRow != null
							&& !tableRow.isMouseOver() && !tableRow.isSelected();
					if (ourQuickRedraw) {
						TableCellImpl.this.quickRedrawCell2(table, item, dirty, cellBounds);
					} else {
						super.quickRedrawCell(table, dirty, cellBounds);
					}
				}
			};
    }
  }

	protected void quickRedrawCell2(TableOrTreeSWT table,
			TableItemOrTreeItem tableItemOrTreeItem, Rectangle dirty,
			Rectangle cellBounds) {
		if (bufferedTableItem.isInPaintItem()) {
			return;
		}
		Rectangle bounds = new Rectangle(0, 0, cellBounds.width, cellBounds.height);
		Point pt = new Point(cellBounds.x, cellBounds.y);
		Image img = new Image(table.getDisplay(), bounds);

		int colPos = bufferedTableItem.getPosition();

		Item item = tableItemOrTreeItem.getItem();
		table.setData("inPaintInfo", new InPaintInfo(item, colPos, bounds));
		table.setData("fullPaint", Boolean.TRUE);

		GC gc = new GC(img);
		try {
			TableViewSWTImpl<?> tv = (TableViewSWTImpl<?>) tableRow.getView();
			TableViewSWT_EraseItem.eraseItem(null, gc, tableItemOrTreeItem, colPos,
					false, bounds, tv, true);
			//gc.setBackground(ColorCache.getRandomColor());
			//gc.fillRectangle(bounds);

			Color fg = getForegroundSWT();
			if (fg != null) {
				gc.setForeground(fg);
			}
			gc.setBackground(getBackgroundSWT());

			TableViewSWT_PaintItem.paintItem(gc, (TableRowSWT) tableRow, colPos,
					tableRow.getIndex(), bounds, tv, true);
		} finally {
			gc.dispose();
		}

		gc = new GC(table.getComposite());
		try {
			//System.out.println("draw " + bounds);
			gc.drawImage(img, pt.x, pt.y);
		} finally {
			img.dispose();
			gc.dispose();
		}

		table.setData("inPaintInfo", null);
		table.setData("fullPaint", Boolean.FALSE);
	}

	protected void quickRedrawCell(TableOrTreeSWT table,
			TableItemOrTreeItem tableItemOrTreeItem, Rectangle dirty,
			Rectangle cellBounds) {
		if (bufferedTableItem.isInPaintItem()) {
			return;
		}
		
		int colPos = bufferedTableItem.getPosition();

		Item item = tableItemOrTreeItem.getItem();
		table.setData("inPaintInfo", new InPaintInfo(item, colPos, cellBounds));
		table.setData("fullPaint", Boolean.TRUE);

		GC gc = new GC(table.getComposite());
		try {
			TableViewSWTImpl<?> tv = (TableViewSWTImpl<?>) tableRow.getView();
			TableViewSWT_EraseItem.eraseItem(null, gc, tableItemOrTreeItem,
					bufferedTableItem.getPosition(), true, cellBounds, tv, true);

			Color fg = getForegroundSWT();
			if (fg != null) {
				gc.setForeground(fg);
			}
			gc.setBackground(getBackgroundSWT());
			
			TableViewSWT_PaintItem.paintItem(gc, (TableRowSWT) tableRow,
					bufferedTableItem.getPosition(), tableRow.getIndex(), cellBounds, tv, true);
		} finally {
			gc.dispose();
		}

		table.setData("inPaintInfo", null);
		table.setData("fullPaint", Boolean.FALSE);
	}

	protected void pluginError(Throwable e) {
    String sTitleLanguageKey = (tableColumn==null?"?":tableColumn.getTitleLanguageKey());

    String sPosition = (bufferedTableItem == null) 
      ? "null" 
      : "" + bufferedTableItem.getPosition() + 
        " (" + MessageText.getString(sTitleLanguageKey) + ")";
    Logger.log(new LogEvent(LOGID, "Table Cell Plugin for Column #" + sPosition
				+ " generated an exception ", e));
  }

	protected void pluginError(String s) {
    String sTitleLanguageKey = (tableColumn==null?"?":tableColumn.getTitleLanguageKey());

		String sPosition = "r"
				+ tableRow.getIndex()
				+ (bufferedTableItem == null ? "null" : "c"
						+ bufferedTableItem.getPosition() + " ("
						+ MessageText.getString(sTitleLanguageKey) + ")");
		Logger.log(new LogEvent(LOGID, LogEvent.LT_ERROR,
				"Table Cell Plugin for Column #" + sPosition + ":" + s + "\n  "
						+ Debug.getStackTrace(true, true)));
  }
  
  /* Public API */
  ////////////////
  
  public Object getDataSource() {
		// if we've been disposed then row/col are null
	  
	TableRowCore	row = tableRow;
	TableColumnCore	col	= tableColumn;
	
	if ( row == null || col == null){
		return( null );
	}
	
    return row.getDataSource(col.getUseCoreDataSource());
  }
  
  public TableColumn getTableColumn() {
    return tableColumn;
  }

  public TableRow getTableRow() {
    return tableRow;
  }

  public String getTableID() {
    return tableRow.getTableID();
  }
  
  public Color getForegroundSWT() {
		if (isDisposed()) {
			return null;
		}

    return bufferedTableItem.getForeground();
  }
  
  public Color getBackgroundSWT() {
		if (isDisposed()) {
			return null;
		}

		return bufferedTableItem.getBackground();
	}

  
  public boolean setForeground(Color color) {
		if (isDisposed()) {
			return false;
		}

  	// Don't need to set when not visible
  	if (isInvisibleAndCanRefresh())
  		return false;

    boolean set = bufferedTableItem.setForeground(color);
    if (set) {
    	setFlag(FLAG_VISUALLY_CHANGED_SINCE_REFRESH);
    }
    return set;
  }

  @Override
  public boolean uiSetText(String text) {
  	return bufferedTableItem.setText(text);
  }
  
  @Override
  public boolean setGraphic(Graphic img) {
  	boolean changed = super.setGraphic(img);
  	if (changed && img != null) {
    	Image imgSWT = ((UISWTGraphic)img).getImage();
    	((BufferedGraphicTableItem)bufferedTableItem).setGraphic(imgSWT);
  	}
  	return changed;
  }

  public String getText() {
  	if (hasFlag(FLAG_SORTVALUEISTEXT) && sortValue instanceof String)
  		return (String)sortValue;
  	if (bufferedTableItem == null) {
  		return null;
  	}
    return bufferedTableItem.getText();
  }

  public boolean isShown() {
  	if (bufferedTableItem == null) {
  		return false;
  	}

    return bufferedTableItem.isShown()
				&& tableRow.getView().isColumnVisible(tableColumn);
  }
  
  public Comparable<?> getSortValue() {
  	Comparable<?> v = super.getSortValue();
  	if (v == null) {
      if (bufferedTableItem != null)
        return bufferedTableItem.getText();
      return "";
  	}
    return v;
  }
  
	// @see org.gudy.azureus2.plugins.ui.tables.TableCell#getMaxLines()
	public int getMaxLines() {
		if (bufferedTableItem == null) {
			// use 1 in case some plugin borks on div by zero
			return 1;
		}
		return bufferedTableItem.getMaxLines();
	}
  
  /* Start TYPE_GRAPHIC Functions */

	public Point getSize() {
    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return null;
    return ((BufferedGraphicTableItem)bufferedTableItem).getSize();
  }

	public int getWidthRaw() {
		return tableColumn.getWidth() - 2;
	}
	
  public int getWidth() {
  	if (isDisposed()) {
  		return -1;
  	}
  	if (QUICK_WIDTH) {
  		return tableColumn.getWidth() - 2 - (getMarginWidth() * 2);
  	} else {
    	Point pt = null;
    	
      if (bufferedTableItem instanceof BufferedGraphicTableItem) {
      	pt = ((BufferedGraphicTableItem)bufferedTableItem).getSize();
      } else {
      	Rectangle bounds = bufferedTableItem.getBounds();
      	if (bounds != null) {
      		pt = new Point(bounds.width, bounds.height);
      	}
      }
      if (pt == null)
        return -1;
      return pt.x;
  	}
  }

  public int getHeight() {
  	return bufferedTableItem.getHeight();
  }

  /* (non-Javadoc)
   * @see org.gudy.azureus2.plugins.ui.tables.TableCell#setFillCell(boolean)
   */
  public void setFillCell(boolean bFillCell) {
  	super.setFillCell(bFillCell);
		if (isDisposed()) {
			return;
		}

    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return;
    
    if (bFillCell)
    	((BufferedGraphicTableItem)bufferedTableItem).setOrientation(SWT.FILL);
    else
    	setOrientationViaColumn();
    setFlag(FLAG_VISUALLY_CHANGED_SINCE_REFRESH);
  }

	public void setMarginHeight(int height) {
		if (isDisposed()) {
			return;
		}

    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return;
    ((BufferedGraphicTableItem)bufferedTableItem).setMargin(-1, height);
    setFlag(FLAG_VISUALLY_CHANGED_SINCE_REFRESH);
  }

  public void setMarginWidth(int width) {
		if (isDisposed()) {
			return;
		}

    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return;
    ((BufferedGraphicTableItem)bufferedTableItem).setMargin(width, -1);
    setFlag(FLAG_VISUALLY_CHANGED_SINCE_REFRESH);
  }

	public int getMarginHeight() {
    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return 0;
    return ((BufferedGraphicTableItem)bufferedTableItem).getMarginHeight();
  }

  public int getMarginWidth() {
    if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
      return 0;
    return ((BufferedGraphicTableItem)bufferedTableItem).getMarginWidth();
  }

  /* End TYPE_GRAPHIC Functions */


	/* Start of Core-Only function */
  //////////////////////////////////
	
	public void redraw() {
		if (!tableRow.isVisible()) {
			return;
		}
		if (bufferedTableItem != null) {
			bufferedTableItem.redraw();
		}
	}
	
  public void invalidate(final boolean bMustRefresh) {
  	super.invalidate(bMustRefresh);
  	if (bMustRefresh) {
  		if (bufferedTableItem != null) {
  			bufferedTableItem.invalidate();
  		}
  	}
  }
  

  public void dispose() {
  	super.dispose();

    if (bufferedTableItem != null) {
			//bufferedTableItem.setForeground(null);
			bufferedTableItem.dispose();
		}
    
    bufferedTableItem = null;
  }
  
  public boolean needsPainting() {
		if (isDisposed()) {
			return false;
		}

  	if (cellSWTPaintListeners != null || tableColumn.hasCellOtherListeners("SWTPaint")) {
  		return true;
  	}
  	if (bufferedTableItem == null) {
  		return false;
  	}
    return bufferedTableItem.needsPainting();
  }
  
  public void locationChanged() {
  	if (bufferedTableItem != null) {
  		bufferedTableItem.locationChanged();
  	}
  }

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	public String toString() {
		return "TableCell {"
				+ (tableColumn == null ? "disposed" : tableColumn.getName())
				+ ","
				+ (tableRow == null ? "" : "r" + tableRow.getIndex())
				+ (bufferedTableItem == null ? "c?" : "c"
						+ bufferedTableItem.getPosition()) + "," + getText() + ","
				+ getSortValue() + "}";
	}

	/* Comparable Implementation */
  
  public static final Comparator TEXT_COMPARATOR = new TextComparator();
  private static class TextComparator implements Comparator {
		public int compare(Object arg0, Object arg1) {
			return arg0.toString().compareToIgnoreCase(arg1.toString());
		}
  }
  

	public Rectangle getBounds() {
		if (isDisposed()) {
			return new Rectangle(0, 0, 0, 0);
		}
		Rectangle bounds = bufferedTableItem.getBounds();
		if (bounds == null) {
			return new Rectangle(0, 0, 0, 0);
		}
    return bounds;
	}

	private void setOrientationViaColumn() {
		if (!(bufferedTableItem instanceof BufferedGraphicTableItem))
			return;
		
		int align = tableColumn.getAlignment();
		BufferedGraphicTableItem ti = (BufferedGraphicTableItem) bufferedTableItem;
		ti.setOrientation(TableColumnSWTUtils.convertColumnAlignmentToSWT(align));
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableCell#getBackgroundGraphic()
	 */
	public Graphic getBackgroundGraphic() {
		if (bufferedTableItem == null) {
			return null;
		}
  	return new UISWTGraphicImpl(bufferedTableItem.getBackgroundImage());
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableCellSWT#getBackgroundImage()
	 */
	public Image getBackgroundImage() {
		if (bufferedTableItem == null) {
			return null;
		}
  	return bufferedTableItem.getBackgroundImage();
	}
	
	public BufferedTableItem getBufferedTableItem() {
		return bufferedTableItem;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableCellCore#setCursorID(int)
	 */
	public boolean setCursorID(int cursorID) {
		if (!super.setCursorID(cursorID)) {
			return false;
		}
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (isMouseOver()) {
					bufferedTableItem.setCursor(getCursorID());
				}
			}
		});
		return true;
	}
	
	public boolean isMouseOver() {
		if (bufferedTableItem == null) {
			return false;
		}
		if (!tableRow.isVisible()) {
			return false;
		}
		return bufferedTableItem.isMouseOver();
	}
	
	public Rectangle getBoundsOnDisplay() {
		Rectangle bounds = getBounds();
		Point pt = ((TableViewSWT<?>) tableRow.getView()).getTableOrTreeSWT().toDisplay(bounds.x, bounds.y);
		bounds.x = pt.x;
		bounds.y = pt.y;
		return bounds;
	}
	
	@Override
	public boolean refresh(boolean bDoGraphics, boolean bRowVisible,
			boolean bCellVisible) {
		return super.refresh(bDoGraphics, bRowVisible, bCellVisible);
	}

}
