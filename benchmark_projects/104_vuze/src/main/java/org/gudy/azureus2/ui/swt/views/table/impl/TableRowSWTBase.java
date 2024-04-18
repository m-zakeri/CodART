package org.gudy.azureus2.ui.swt.views.table.impl;

import java.util.*;

import org.eclipse.swt.graphics.*;
import org.eclipse.swt.widgets.Display;

import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.plugins.ui.tables.*;
import org.gudy.azureus2.pluginsimpl.local.PluginCoreUtils;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.mainwindow.Colors;
import org.gudy.azureus2.ui.swt.views.table.TableCellSWT;
import org.gudy.azureus2.ui.swt.views.table.TableRowSWT;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;

import com.aelitis.azureus.ui.common.table.TableCellCore;
import com.aelitis.azureus.ui.common.table.TableRowCore;
import com.aelitis.azureus.ui.common.table.TableView;
import com.aelitis.azureus.ui.swt.utils.ColorCache;

@SuppressWarnings("rawtypes")
public abstract class TableRowSWTBase
	implements TableRowSWT
{
	public static boolean DEBUG_ROW_PAINT = false;

	protected Object lock;

	private final TableViewSWT tv;

	private final TableRowCore parentRow;

	private final Object coreDataSource;

	private int lastIndex = -1;

	protected Map<String, TableCellCore> mTableCells;

	private boolean bDisposed;

	private Object pluginDataSource;

	protected boolean wasShown = false;

	private boolean bSetNotUpToDateLastRefresh;

	private ArrayList<TableRowMouseListener> mouseListeners;

	private Map<String, Object> dataList;

	private int alpha = 255;

	private int fontStyle;

	private boolean expanded;


	public TableRowSWTBase(Object lock, TableRowCore parentRow, TableViewSWT tv,
			Object dataSource) {
		this.lock = lock;
		this.parentRow = parentRow;
		this.tv = tv;
		this.coreDataSource = dataSource;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#invalidate()
	 */
	public void invalidate() {
		invalidate(false);
	}
	public void invalidate(boolean mustRefersh) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return;
  		}
  
  		for (TableCellCore cell : mTableCells.values()) {
  			if (cell != null) {
  				cell.invalidate(mustRefersh);
  			}
  		}
		}
	}

	public boolean doesAnyCellHaveFlag(int flag) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return false;
  		}
  
  		for (TableCellCore cell : mTableCells.values()) {
  			if ((cell instanceof TableCellSWTBase)
  					&& ((TableCellSWTBase) cell).hasFlag(flag)) {
  				return true;
  			}
  		}
  		return false;
		}
	}


	public void setCellFlag(int flag) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return;
  		}
  
  		for (TableCellCore cell : mTableCells.values()) {
  			if (cell != null) {
  				((TableCellSWTBase) cell).setFlag(flag);
  			}
  		}
		}
	}

	public void clearCellFlag(int flag, boolean subRows) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return;
  		}
  
  		for (TableCellCore cell : mTableCells.values()) {
  			if (cell != null) {
  				((TableCellSWTBase) cell).clearFlag(flag);
  			}
  		}
  		if (subRows) {
  			TableRowCore[] subRowsWithNull = getSubRowsWithNull();
  			for (TableRowCore row : subRowsWithNull) {
  				((TableRowSWTBase) row).clearCellFlag(flag, false);
  			}
  		}
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#delete()
	 */
	public void delete() {
		synchronized (lock) {

			if (bDisposed) {
				return;
			}

			if (mTableCells != null) {
  			for (TableCellCore cell : mTableCells.values()) {
  				try {
  					if (cell != null) {
  						cell.dispose();
  					}
  				} catch (Exception e) {
  					Debug.out(e);
  				}
  			}
			}

			setHeight(0);
			
			bDisposed = true;
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#refresh(boolean)
	 */
	public List refresh(boolean bDoGraphics) {
		if (bDisposed) {
			return Collections.EMPTY_LIST;
		}

		boolean bVisible = isVisible();

		return refresh(bDoGraphics, bVisible);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#locationChanged(int)
	 */
	public void locationChanged(int iStartColumn) {
		if (bDisposed || !isVisible()) {
			return;
		}
		synchronized (lock) {
			if (mTableCells == null) {
				return;
			}

  		for (TableCellCore cell : mTableCells.values()) {
  			if (cell != null && cell.getTableColumn().getPosition() > iStartColumn) {
  				cell.locationChanged();
  			}
  		}
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#getDataSource(boolean)
	 */
	public Object getDataSource(boolean bCoreObject) {
		if (bDisposed) {
			return null;
		}

		if (bCoreObject) {
			return coreDataSource;
		}

		if (pluginDataSource != null) {
			return pluginDataSource;
		}

		pluginDataSource = PluginCoreUtils.convert(coreDataSource, bCoreObject);

		return pluginDataSource;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#getIndex()
	 */
	public int getIndex() {
		if (bDisposed) {
			return -1;
		}

		if (lastIndex >= 0) {
			if (parentRow != null) {
				return lastIndex;
			}
			TableRowCore row = tv.getRowQuick(lastIndex);
			if (row == this) {
				return lastIndex;
			}
		}

		// don't set directly to lastIndex, so setTableItem will eventually do
		// its job
		return tv.indexOf(this);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#getTableCellCore(java.lang.String)
	 */
	public TableCellCore getTableCellCore(String name) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return null;
  		}
  
  		return mTableCells.get(name);
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#isVisible()
	 */
	public boolean isVisible() {
		return tv.isRowVisible(this);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#setTableItem(int)
	 */
	public boolean setTableItem(int newIndex) {
		return setTableItem(newIndex, true);
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#setTableItem(int, boolean)
	 */
	public boolean setTableItem(int newIndex, boolean isVisible) {
		if (bDisposed) {
			System.out.println("XXX setTI: bDisposed from "
					+ Debug.getCompressedStackTrace());
			return false;
		}
		boolean changedIndex = lastIndex != newIndex;
		if (changedIndex) {
			//System.out.println("row " + newIndex + " from " + lastIndex + ";" + getView().isRowVisible(this) + ";" + Debug.getCompressedStackTrace());
			lastIndex = newIndex;
		}

		setShown(isVisible, changedIndex);

		return changedIndex;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#setSelected(boolean)
	 */
	public void setSelected(boolean selected) {
		TableView tableView = getView();
		if (tableView instanceof TableViewSWT) {
			((TableViewSWT<?>) tableView).setRowSelected(this, selected, true);
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#isRowDisposed()
	 */
	public boolean isRowDisposed() {
		return bDisposed;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#setUpToDate(boolean)
	 */
	public void setUpToDate(boolean upToDate) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return;
  		}
  
  		for (TableCellCore cell : mTableCells.values()) {
  			if (cell != null) {
  				cell.setUpToDate(upToDate);
  			}
  		}
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#refresh(boolean, boolean)
	 */
	public List<TableCellCore> refresh(boolean bDoGraphics, boolean bVisible) {
		// If this were called from a plugin, we'd have to refresh the sorted column
		// even if we weren't visible
		List<TableCellCore> list = Collections.EMPTY_LIST;

		if (bDisposed) {
			return list;
		}

		if (!bVisible) {
			if (!bSetNotUpToDateLastRefresh) {
				setUpToDate(false);
				bSetNotUpToDateLastRefresh = true;
			}
			return list;
		}

		bSetNotUpToDateLastRefresh = false;

		//System.out.println(SystemTime.getCurrentTime() + "refresh " + getIndex() + ";vis=" + bVisible + " via " + Debug.getCompressedStackTrace(8));

		tv.invokeRefreshListeners(this);

		// Make a copy of cells so we don't lock while refreshing
		Collection<TableCellCore> lTableCells = null;
		synchronized (lock) {
			if (mTableCells != null) {
				lTableCells = new ArrayList<TableCellCore>(mTableCells.values());
			}
		}

		if (lTableCells != null) {
  		for (TableCellCore cell : lTableCells) {
  			if (cell == null || cell.isDisposed()) {
  				continue;
  			}
  			TableColumn column = cell.getTableColumn();
  			//System.out.println(column);
  			if (column != tv.getSortColumn()
  					&& !tv.isColumnVisible(column)) {
  				//System.out.println("skip " + column);
  				continue;
  			}
  			boolean cellVisible = bVisible && cell.isShown();
				boolean changed = cell.refresh(bDoGraphics, bVisible, cellVisible);
  			if (changed) {
  				if (list == Collections.EMPTY_LIST) {
  					list = new ArrayList<TableCellCore>(lTableCells.size());
  				}
  				list.add(cell);
  			}
  
  		}
		}

		//System.out.println();
		return list;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#getView()
	 */
	public TableView getView() {
		return tv;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#addMouseListener(org.gudy.azureus2.plugins.ui.tables.TableRowMouseListener)
	 */
	public void addMouseListener(TableRowMouseListener listener) {
		synchronized (lock) {

			if (mouseListeners == null) {
				mouseListeners = new ArrayList<TableRowMouseListener>(1);
			}

			mouseListeners.add(listener);

		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#removeMouseListener(org.gudy.azureus2.plugins.ui.tables.TableRowMouseListener)
	 */
	public void removeMouseListener(TableRowMouseListener listener) {
		synchronized (lock) {

			if (mouseListeners == null) {
				return;
			}

			mouseListeners.remove(listener);

		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#invokeMouseListeners(org.gudy.azureus2.plugins.ui.tables.TableRowMouseEvent)
	 */
	public void invokeMouseListeners(TableRowMouseEvent event) {
		ArrayList<TableRowMouseListener> listeners = mouseListeners;
		if (listeners == null) {
			return;
		}

		for (int i = 0; i < listeners.size(); i++) {
			try {
				TableRowMouseListener l = listeners.get(i);

				l.rowMouseTrigger(event);

			} catch (Throwable e) {
				Debug.printStackTrace(e);
			}
		}
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#isMouseOver()
	 */
	public boolean isMouseOver() {
		return tv.getTableRowWithCursor() == this;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#isExpanded()
	 */
	public boolean isExpanded() {
		return expanded;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#setExpanded(boolean)
	 */
	public void setExpanded(boolean b) {
		expanded = b;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#getParentRowCore()
	 */
	public TableRowCore getParentRowCore() {
		return parentRow;
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#isInPaintItem()
	 */
	public boolean isInPaintItem() {
		return false;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#getDataSource()
	 */
	public Object getDataSource() {
		return getDataSource(false);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#getTableID()
	 */
	public String getTableID() {
		return tv.getTableID();
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setForeground(org.eclipse.swt.graphics.Color)
	 */
	public abstract boolean setForeground(Color c);

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#setForeground(int, int, int)
	 */
	public void setForeground(int red, int green, int blue) {
		setForeground2(red, green, blue);
	}
	
	public boolean setForeground2(int red, int green, int blue) {
		if (red < 0 || green < 0 || blue < 0) {
			return setForeground((Color) null);
		}
		return setForeground(new RGB(red, green, blue));
	}

	private boolean setForeground(final RGB rgb) {
		Color colorFG = getForeground();
		boolean changed = colorFG == null || colorFG.isDisposed()
				|| !colorFG.getRGB().equals(rgb);
		if (changed) {
			Utils.execSWTThread(new AERunnable() {
				public void runSupport() {
					setForeground(ColorCache.getColor(Display.getCurrent(), rgb));
				}
			});
		}
		return changed;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#setForeground(int[])
	 */
	public void setForeground(int[] rgb) {
		setForeground2(rgb);
	}

	public boolean setForeground2(int[] rgb) {
		if (rgb == null || rgb.length < 3) {
			return setForeground((Color) null);
		}
		return setForeground2(rgb[0], rgb[1], rgb[2]);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#setForegroundToErrorColor()
	 */
	public void setForegroundToErrorColor() {
		this.setForeground(Colors.colorError);
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#isValid()
	 */
	public boolean isValid() {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return true;
  		}
  
  		boolean valid = true;
  		for (TableCell cell : mTableCells.values()) {
  			if (cell != null && cell.isValid()) {
  				return false;
  			}
  		}
  
 		return valid;
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#getTableCell(java.lang.String)
	 */
	public TableCell getTableCell(String field) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return null;
  		}
  
  		return mTableCells.get(field);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#isSelected()
	 */
	public boolean isSelected() {
		return getView().isSelected(this);
	}

	public boolean isFocused() {
		return getView().getFocusedRow() == this;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#getData(java.lang.String)
	 */
	public Object getData(String id) {
		synchronized (this) {
			return dataList == null ? null : dataList.get(id);
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.plugins.ui.tables.TableRow#setData(java.lang.String, java.lang.Object)
	 */
	public void setData(String id, Object data) {
		synchronized (this) {
			if (dataList == null) {
				dataList = new HashMap<String, Object>(1);
			}
			if (data == null) {
				dataList.remove(id);
			} else {
				dataList.put(id, data);
			}
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setIconSize(org.eclipse.swt.graphics.Point)
	 */
	public abstract boolean setIconSize(Point pt);
	
	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getForeground()
	 */
	public abstract Color getForeground();

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getBackground()
	 */
	public abstract Color getBackground();

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getTableCellSWT(java.lang.String)
	 */
	public TableCellSWT getTableCellSWT(String name) {
		synchronized (lock) {
  		if (bDisposed || mTableCells == null) {
  			return null;
  		}
  
  		TableCellCore cell = mTableCells.get(name);
  		if (cell instanceof TableCellSWT) {
  			return (TableCellSWT) cell;
  		}
  		return null;
		}
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getBounds()
	 */
	public abstract Rectangle getBounds();

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setBackgroundImage(org.eclipse.swt.graphics.Image)
	 */
	public abstract void setBackgroundImage(Image image);

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getFontStyle()
	 */
	public int getFontStyle() {
		return fontStyle;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setFontStyle(int)
	 */
	public boolean setFontStyle(int style) {
		if (fontStyle == style) {
			return false;
		}

		fontStyle = style;
		invalidate();

		return true;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#getAlpha()
	 */
	public int getAlpha() {
		return alpha;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setAlpha(int)
	 */
	public boolean setAlpha(int alpha) {
		if (alpha == this.alpha) {
			return false;
		}
		this.alpha = alpha;
		return true;
	}

	/* (non-Javadoc)
	 * @see org.gudy.azureus2.ui.swt.views.table.TableRowSWT#setWidgetSelected(boolean)
	 */
	public abstract void setWidgetSelected(boolean selected);


	public void setShown(boolean b, boolean force) {
		if (bDisposed) {
			return;
		}

		if (b == wasShown && !force) {
			return;
		}
		wasShown = b;

		Collection<TableCellCore> lTableCells = null;
		synchronized (lock) {
			if (mTableCells != null) {
				lTableCells = new ArrayList<TableCellCore>(mTableCells.values());
			}
		}

		if (lTableCells != null) {
  		for (TableCellCore cell : lTableCells) {
  			if (cell != null) {
  				cell.invokeVisibilityListeners(b
  						? TableCellVisibilityListener.VISIBILITY_SHOWN
  						: TableCellVisibilityListener.VISIBILITY_HIDDEN, true);
  			}
  		}
		}

		/* Don't need to refresh; paintItem will trigger a refresh on
		 * !cell.isUpToDate()
		 *
		if (b) {
			refresh(b, true);
		}
		/**/
	}

	/* (non-Javadoc)
	 * @see com.aelitis.azureus.ui.common.table.TableRowCore#redraw()
	 */
	public void redraw() {
		redraw(false);
	}

	/*
	public abstract void setSubItemCount(int length);

	public abstract int getSubItemCount();

	public abstract TableRowCore linkSubItem(int indexOf);

	public abstract void setSubItems(Object[] datasources);

	public abstract TableRowCore[] getSubRowsWithNull();

	public abstract void removeSubRow(Object datasource);
	*/
}
