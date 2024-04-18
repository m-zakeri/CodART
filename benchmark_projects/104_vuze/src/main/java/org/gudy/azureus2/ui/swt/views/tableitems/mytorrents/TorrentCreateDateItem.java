/*
 * Created on 05-May-2006
 * Created by Paul Gardner
 * Copyright (C) 2006 Aelitis, All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 * 
 * AELITIS, SAS au capital de 46,603.30 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */

package org.gudy.azureus2.ui.swt.views.tableitems.mytorrents;

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.ui.swt.views.table.utils.TableColumnCreator;
import org.gudy.azureus2.ui.swt.views.tableitems.ColumnDateSizer;

import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.ui.tables.TableCell;
import org.gudy.azureus2.plugins.ui.tables.TableColumnInfo;

public class TorrentCreateDateItem
	extends ColumnDateSizer
{
	public static final Class DATASOURCE_TYPE = Download.class;

	public static final String COLUMN_ID = "torrent_created";

	public void fillTableColumnInfo(TableColumnInfo info) {
		info.addCategories(new String[] { CAT_TIME, CAT_CONTENT });
		info.setProficiency(TableColumnInfo.PROFICIENCY_INTERMEDIATE);
	}

	public TorrentCreateDateItem(String sTableID) {
		super(DATASOURCE_TYPE, COLUMN_ID, TableColumnCreator.DATE_COLUMN_WIDTH, sTableID);
		
		setMultiline(false);
		
		setRefreshInterval(INTERVAL_INVALID_ONLY);

		setShowTime( false );
	}

	/**
	 * @param tableID
	 * @param b
	 */
	public TorrentCreateDateItem(String tableID, boolean v) {
		this(tableID);
		setVisible(v);
	}

	public void refresh(TableCell cell, long timestamp) {
		DownloadManager dm = (DownloadManager) cell.getDataSource();
		timestamp = (dm == null) ? 0 : dm.getTorrentCreationDate();
		super.refresh(cell, timestamp*1000);
		//cell.setText(DisplayFormatters.formatDate(timestamp));
	}
}
