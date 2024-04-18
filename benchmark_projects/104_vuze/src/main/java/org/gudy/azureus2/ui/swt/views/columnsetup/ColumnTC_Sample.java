/**
 * Created on Jan 3, 2009
 *
 * Copyright 2008 Vuze, Inc.  All rights reserved.
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License only.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA 
 */

package org.gudy.azureus2.ui.swt.views.columnsetup;

import org.eclipse.swt.graphics.GC;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.widgets.Composite;

import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.plugins.ui.tables.*;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.views.table.TableCellSWT;
import org.gudy.azureus2.ui.swt.views.table.TableCellSWTPaintListener;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;
import org.gudy.azureus2.ui.swt.views.table.impl.FakeTableCell;
import org.gudy.azureus2.ui.swt.views.table.utils.CoreTableColumn;

import com.aelitis.azureus.ui.common.table.*;

/**
 * @author TuxPaper
 * @created Jan 3, 2009
 *
 */
public class ColumnTC_Sample
	extends CoreTableColumn
	implements TableCellAddedListener
{
	public static final String COLUMN_ID = "TableColumnSample";

	public ColumnTC_Sample(String tableID) {
		super(COLUMN_ID, tableID);
		setPosition(POSITION_INVISIBLE);
		setRefreshInterval(INTERVAL_LIVE);
		setWidth(120);
	}

	// @see org.gudy.azureus2.plugins.ui.tables.TableCellAddedListener#cellAdded(org.gudy.azureus2.plugins.ui.tables.TableCell)
	public void cellAdded(final TableCell cell) {
		Utils.execSWTThread(new AERunnable() {
			public void runSupport() {
				if (cell.isDisposed()) {
					return;
				}
				TableColumnCore column = (TableColumnCore) cell.getDataSource();
				TableViewSWT<?> tv = (TableViewSWT<?>) ((TableCellCore) cell).getTableRowCore().getView();
				TableColumnSetupWindow tvs = (TableColumnSetupWindow) tv.getParentDataSource();
				TableRowCore sampleRow = (TableRowCore) tvs.getSampleRow();

				cell.addListeners(new Cell(cell, column, tv.getTableComposite(), sampleRow));
			}
		});
	}

	public class Cell
		implements TableCellRefreshListener, TableCellSWTPaintListener,
		TableCellVisibilityListener, TableCellDisposeListener
	{
		private final TableColumnCore column;
		private FakeTableCell sampleCell;

		public Cell(TableCell parentCell, TableColumnCore column, Composite c, TableRowCore sampleRow) {
			this.column = column;
			if (sampleRow == null) {
				return;
			}
			Object ds = sampleRow.getDataSource(true);
			sampleCell = new FakeTableCell(column, ds);

			Rectangle bounds = ((TableCellSWT)parentCell).getBounds();
			sampleCell.setControl(c, bounds, false);
		}
		
		public void dispose(TableCell cell) {
			sampleCell = null;
		}

		// @see org.gudy.azureus2.ui.swt.views.table.TableCellSWTPaintListener#cellPaint(org.eclipse.swt.graphics.GC, org.gudy.azureus2.ui.swt.views.table.TableCellSWT)
		public void cellPaint(GC gc, TableCellSWT cell) {
			if (sampleCell == null) {
				return;
			}
			Rectangle bounds = cell.getBounds();
			sampleCell.setCellArea(bounds);
			try {
				sampleCell.doPaint(gc);
			} catch (Throwable e) {
				Debug.out(e);
			}
		}

		// @see org.gudy.azureus2.plugins.ui.tables.TableCellVisibilityListener#cellVisibilityChanged(org.gudy.azureus2.plugins.ui.tables.TableCell, int)
		public void cellVisibilityChanged(TableCell cell, int visibility) {
			if (sampleCell == null) {
				return;
			}
			try {
				column.invokeCellVisibilityListeners(sampleCell, visibility);
			} catch (Throwable e) {
				Debug.out(e);
			}
		}

		// @see org.gudy.azureus2.plugins.ui.tables.TableCellRefreshListener#refresh(org.gudy.azureus2.plugins.ui.tables.TableCell)
		public void refresh(TableCell cell) {
			if (sampleCell == null) {
				return;
			}
			if (!cell.isShown()) {
				return;
			}
			sampleCell.refresh(true, true, true);
			cell.setSortValue(sampleCell.getSortValue());
			cell.invalidate();
			if (cell instanceof TableCellSWT) {
				((TableCellSWT) cell).redraw();
			}
			//cell.setText(sampleCell.getText());
		}

	}
}
