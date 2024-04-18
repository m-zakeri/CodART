/*
 * Created on 2 juil. 2003
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
package org.gudy.azureus2.ui.swt.views;

import java.util.List;
import java.util.Map;

import org.eclipse.swt.SWT;
import org.eclipse.swt.widgets.Menu;
import org.eclipse.swt.widgets.MenuItem;

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.download.DownloadManagerTPSListener;
import org.gudy.azureus2.core3.torrent.TOTorrent;
import org.gudy.azureus2.core3.tracker.client.TRTrackerAnnouncer;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.TorrentUtils;
import org.gudy.azureus2.plugins.ui.tables.TableManager;
import org.gudy.azureus2.ui.swt.Messages;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.maketorrent.MultiTrackerEditor;
import org.gudy.azureus2.ui.swt.maketorrent.TrackerEditorListener;
import org.gudy.azureus2.ui.swt.plugins.UISWTInstance;
import org.gudy.azureus2.ui.swt.plugins.UISWTViewEvent;
import org.gudy.azureus2.ui.swt.pluginsimpl.UISWTInstanceImpl;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWTMenuFillListener;
import org.gudy.azureus2.ui.swt.views.table.impl.TableViewFactory;
import org.gudy.azureus2.ui.swt.views.table.impl.TableViewSWTImpl;
import org.gudy.azureus2.ui.swt.views.table.impl.TableViewTab;
import org.gudy.azureus2.ui.swt.views.tableitems.tracker.*;

import com.aelitis.azureus.core.tracker.TrackerPeerSource;
import com.aelitis.azureus.ui.common.ToolBarItem;
import com.aelitis.azureus.ui.common.table.*;
import com.aelitis.azureus.ui.selectedcontent.SelectedContent;
import com.aelitis.azureus.ui.selectedcontent.SelectedContentManager;
import com.aelitis.azureus.ui.swt.UIFunctionsManagerSWT;
import com.aelitis.azureus.ui.swt.UIFunctionsSWT;



public class TrackerView 
	extends TableViewTab<TrackerPeerSource>
	implements 	TableLifeCycleListener, TableDataSourceChangedListener, 
				DownloadManagerTPSListener, TableViewSWTMenuFillListener
{
	private static boolean registeredCoreSubViews = false;

	private final static TableColumnCore[] basicItems = {
		new TypeItem(),
		new NameItem(),
		new StatusItem(),
		new PeersItem(),
		new SeedsItem(),
		new LeechersItem(),
		new UpdateInItem(),
		new IntervalItem(),
	};

	public static final String MSGID_PREFIX = "TrackerView";

	DownloadManager manager;
  
	private TableViewSWT<TrackerPeerSource> tv;

	/**
	 * Initialize
	 *
	 */
	public TrackerView() {
		super(MSGID_PREFIX);
	}

	public TableViewSWT<TrackerPeerSource>
	initYourTableView() 
	{
		tv = TableViewFactory.createTableViewSWT(
				TrackerPeerSource.class,
				TableManager.TABLE_TORRENT_TRACKERS, 
				getPropertiesPrefix(), 
				basicItems,
				basicItems[0].getName(), 
				SWT.SINGLE | SWT.FULL_SELECTION | SWT.VIRTUAL );

		tv.addLifeCycleListener(this);
		tv.addMenuFillListener(this);
		tv.addTableDataSourceChangedListener(this, true);
		tv.setEnableTabViews(true);
		
		UIFunctionsSWT uiFunctions = UIFunctionsManagerSWT.getUIFunctionsSWT();
		if (uiFunctions != null) {
			UISWTInstance pluginUI = uiFunctions.getUISWTInstance();
			
			if (pluginUI != null && !registeredCoreSubViews) {

				pluginUI.addView(TableManager.TABLE_TORRENT_TRACKERS, "ScrapeInfoView",
						ScrapeInfoView.class, manager);

				registeredCoreSubViews = true;
			}
		}

		return tv;
	}

	
	public void 
	fillMenu(
		String sColumnName, Menu menu) 
	{
		final Object[] sources = tv.getSelectedDataSources().toArray();
		
		boolean	found_tracker	= false;
		boolean	update_ok 		= false;
		
		for ( Object o: sources ){
	
			TrackerPeerSource ps = (TrackerPeerSource)o;
		
			if ( ps.getType() == TrackerPeerSource.TP_TRACKER ){
				
				found_tracker = true;
			}
			
			int	state = ps.getStatus();
						
			if ( 	( 	state == TrackerPeerSource.ST_ONLINE || 
						state == TrackerPeerSource.ST_QUEUED || 
						state == TrackerPeerSource.ST_ERROR ) &&
					!ps.isUpdating() &&
					ps.canManuallyUpdate()){
				
				update_ok = true;
				
				break;
			}
		}
		
		if ( found_tracker ){
			final MenuItem update_item = new MenuItem( menu, SWT.PUSH);
	
			Messages.setLanguageText(update_item, "GeneralView.label.trackerurlupdate");
			
			update_item.setEnabled( update_ok );
			
			update_item.addListener(
				SWT.Selection, 
				new TableSelectedRowsListener(tv) 
				{
					public void 
					run(
						TableRowCore row )
					{
						for ( Object o: sources ){
							
							TrackerPeerSource ps = (TrackerPeerSource)o;
	
							if ( ps.canManuallyUpdate()){
								
								ps.manualUpdate();
							}
						}
					}
				});
			
			final MenuItem edit_item = new MenuItem( menu, SWT.PUSH);
			
			Messages.setLanguageText(edit_item, "MyTorrentsView.menu.editTracker");
						
			edit_item.addListener(
				SWT.Selection, 
				new TableSelectedRowsListener(tv) 
				{
					public void 
					run(
						TableRowCore row )
					{
						final TOTorrent torrent = manager.getTorrent();

						if (torrent == null) {
							return;
						}

						Utils.execSWTThread(
							new Runnable()
							{
								public void
								run()
								{
									List<List<String>> group = TorrentUtils.announceGroupsToList(torrent);
			
									new MultiTrackerEditor(null,null, group, new TrackerEditorListener() {
										public void trackersChanged(String str, String str2, List<List<String>> _group) {
											TorrentUtils.listToAnnounceGroups(_group, torrent);
			
											try {
												TorrentUtils.writeToFile(torrent);
											} catch (Throwable e2) {
			
												Debug.printStackTrace(e2);
											}
			
											TRTrackerAnnouncer tc = manager.getTrackerClient();
			
											if (tc != null) {
			
												tc.resetTrackerUrl(true);
											}
										}
									}, true);
								}
							});
					}
				});
			
			new MenuItem( menu, SWT.SEPARATOR );
		}
	}
	
	public void 
	addThisColumnSubMenu(
		String columnName, 
		Menu menuThisColumn) 
	{
	}
	
	public void 
	trackerPeerSourcesChanged() 
	{
		Utils.execSWTThread(
			new AERunnable() 
			{
				public void
				runSupport()
				{
					if ( manager == null || tv.isDisposed()){
						
						return;
					}
					
					tv.removeAllTableRows();
					
					addExistingDatasources();
				}
			});
	}
	
	public void 
	tableDataSourceChanged(
		Object newDataSource ) 
	{
	  	if ( manager != null ){
	  		
	  		manager.removeTPSListener( this );
		}
	
		if ( newDataSource == null ){
			
			manager = null;
			
		}else if ( newDataSource instanceof Object[] ){
		
			manager = (DownloadManager)((Object[])newDataSource)[0];
			
		}else{
			
			manager = (DownloadManager)newDataSource;
		}
		
	  	if ( manager != null && !tv.isDisposed()){
	    	
  			manager.addTPSListener( this );
	  		
	    	addExistingDatasources();
	    }
	}
	
	public void 
	tableViewInitialized() 
	{
		if ( manager != null ){

			manager.addTPSListener( this );
			
			addExistingDatasources();
		}
    }

	public void 
	tableViewDestroyed() 
	{
		if ( manager != null ){
			
			manager.removeTPSListener( this );
		}
	}

	private void 
	addExistingDatasources() 
	{
		if ( manager == null || tv.isDisposed()){
			
			return;
		}

		List<TrackerPeerSource> tps = manager.getTrackerPeerSources();
		
		tv.addDataSources( tps.toArray( (new TrackerPeerSource[tps.size()])));
		
		tv.processDataSourceQueue();
	}
	
	public boolean eventOccurred(UISWTViewEvent event) {
	    switch (event.getType()) {
	     
	        
	      case UISWTViewEvent.TYPE_FOCUSGAINED:
	      	String id = "DMDetails_Sources";
	      	if (manager != null) {
	      		if (manager.getTorrent() != null) {
	  					id += "." + manager.getInternalName();
	      		} else {
	      			id += ":" + manager.getSize();
	      		}
	      	}
	  
	      	SelectedContentManager.changeCurrentlySelectedContent(id, new SelectedContent[] {
	      		new SelectedContent(manager)
	      	});
	      	break;
	    }
	    
	    return( super.eventOccurred(event));
	}
	
	public boolean toolBarItemActivated(ToolBarItem item, long activationType,
			Object datasource) {
		if ( ViewUtils.toolBarItemActivated(manager, item, activationType, datasource)){
			return( true );
		}
		return( super.toolBarItemActivated(item, activationType, datasource));
	}

	public void refreshToolBarItems(Map<String, Long> list) {
		ViewUtils.refreshToolBarItems(manager, list);
		super.refreshToolBarItems(list);
	}
}
