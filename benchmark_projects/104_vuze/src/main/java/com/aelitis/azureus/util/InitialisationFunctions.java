/*
 * Created on 14-Sep-2006
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

package com.aelitis.azureus.util;

import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.cnetwork.ContentNetworkManagerFactory;
import com.aelitis.azureus.core.content.AzureusPlatformContentDirectory;
import com.aelitis.azureus.core.content.RelatedContentManager;
import com.aelitis.azureus.core.devices.Device;
import com.aelitis.azureus.core.devices.DeviceManager;
import com.aelitis.azureus.core.devices.DeviceManagerFactory;
import com.aelitis.azureus.core.devices.DeviceMediaRenderer;
import com.aelitis.azureus.core.download.DownloadManagerEnhancer;
import com.aelitis.azureus.core.metasearch.MetaSearchManagerFactory;
import com.aelitis.azureus.core.metasearch.MetaSearchManagerListener;
import com.aelitis.azureus.core.peer.cache.CacheDiscovery;
import com.aelitis.azureus.core.subs.Subscription;
import com.aelitis.azureus.core.subs.SubscriptionManagerFactory;
import com.aelitis.azureus.core.torrent.PlatformTorrentUtils;
import com.aelitis.azureus.core.util.AZ3Functions;
import com.aelitis.azureus.core.util.AZ3Functions.provider.TranscodeProfile;
import com.aelitis.azureus.core.util.AZ3Functions.provider.TranscodeTarget;
import com.aelitis.azureus.ui.UIFunctions;
import com.aelitis.azureus.ui.UIFunctionsManager;
import com.aelitis.azureus.ui.swt.shells.RemotePairingWindow;
import com.aelitis.azureus.ui.swt.shells.main.MainWindow;
import com.aelitis.azureus.ui.swt.views.skin.TorrentListViewsUtils;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.disk.DiskManagerFileInfo;
import org.gudy.azureus2.core3.download.DownloadManagerState;
import org.gudy.azureus2.core3.download.DownloadManagerStateAttributeListener;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.download.DownloadManager;
import org.gudy.azureus2.plugins.download.DownloadManagerListener;
import org.gudy.azureus2.plugins.download.DownloadWillBeAddedListener;
import org.gudy.azureus2.plugins.torrent.Torrent;
import org.gudy.azureus2.pluginsimpl.local.PluginCoreUtils;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;

public class InitialisationFunctions
{
	private static final String EXTENSION_PREFIX = "azid";

	public static void earlyInitialisation(AzureusCore core) {
		
		DownloadUtils.initialise();
		
		DownloadManagerEnhancer dme = DownloadManagerEnhancer.initialise(core);

		hookDownloadAddition();

		AzureusPlatformContentDirectory.register();

		CacheDiscovery.initialise( dme );
		
		ContentNetworkManagerFactory.preInitialise();
		
		MetaSearchManagerFactory.preInitialise();
		
		SubscriptionManagerFactory.preInitialise();
		
		DeviceManagerFactory.preInitialise();
		
		NavigationHelper.initialise();
		
		RelatedContentManager.preInitialise( core );

		AZ3Functions.setProvider(
			new AZ3Functions.provider()
			{
				public String getDefaultContentNetworkURL(int type, Object[] params) {
					return ConstantsVuze.getDefaultContentNetwork().getServiceURL(type, params);
				}

				public void 
				subscribeToRSS(
					String		name,
					URL 		url,
					int			interval,
					boolean		is_public,
					String		creator_ref )
				
					throws Exception
				{
					Subscription subs =
						SubscriptionManagerFactory.getSingleton().createSingletonRSS(
						name, url, interval );
					
					if ( !subs.getName().equals( name )){
					
						subs.setName( name );
					}
					
					if ( subs.isPublic() != is_public ){
						
						subs.setPublic( is_public );
					}
					
					if ( !subs.isSubscribed()){
						
						subs.setSubscribed( true );
					}
					if ( creator_ref != null ){
						
						subs.setCreatorRef( creator_ref );
					}
				}
				
				public void 
				openRemotePairingWindow() 
				{
					RemotePairingWindow.open();
				}
				
				public boolean
				canPlay(
					org.gudy.azureus2.core3.download.DownloadManager		dm,
					int														file_index )
				{
					return( PlayUtils.canPlayDS(dm, file_index) || PlayUtils.canStreamDS(dm, file_index));
				}
				
				public void
				play(
					org.gudy.azureus2.core3.download.DownloadManager		dm,
					int														file_index )
				{
					Object ds = dm;
					if (file_index >= 0) {
						DiskManagerFileInfo[] files = dm.getDiskManagerFileInfoSet().getFiles();
						if (file_index < files.length) {
							ds = files[file_index];
						}
					}
					
					if ( PlayUtils.canPlayDS(dm, file_index)){
						TorrentListViewsUtils.playOrStreamDataSource(ds,
								DLReferals.DL_REFERAL_PLAYDM, false, true);
					}
					if ( PlayUtils.canStreamDS(dm, file_index)){
						TorrentListViewsUtils.playOrStreamDataSource(ds,
								DLReferals.DL_REFERAL_PLAYDM, true, false);
					}
				}	
				
				public TranscodeTarget[]
           		getTranscodeTargets()
				{
					List<TranscodeTarget> result = new ArrayList<TranscodeTarget>();
					
					if ( !COConfigurationManager.getStringParameter("ui").equals("az2")){

						try{
							DeviceManager dm = DeviceManagerFactory.getSingleton();
						
							Device[] devices = dm.getDevices();
							
							for ( final Device d: devices ){
								
								if ( d instanceof DeviceMediaRenderer ){
									
									final DeviceMediaRenderer dmr = (DeviceMediaRenderer)d;							
	
									boolean	hide_device = d.isHidden();
									
									if ( COConfigurationManager.getBooleanParameter( "device.sidebar.ui.rend.hidegeneric", true ) ){
																			
										if ( dmr.isNonSimple()){
											
											hide_device = true;
										}
									}
									
									if ( hide_device ){
										
										continue;
									}
									
									result.add( 
										new TranscodeTarget()
										{
											public String
											getName()
											{
												return( d.getName());
											}
											
											public TranscodeProfile[]
											getProfiles()
											{		
												List<TranscodeProfile>	ps = new ArrayList<TranscodeProfile>(); 
	
												com.aelitis.azureus.core.devices.TranscodeProfile[] profs = dmr.getTranscodeProfiles();	
												
												if ( profs.length == 0 ){
													
													if ( dmr.getTranscodeRequirement() == com.aelitis.azureus.core.devices.TranscodeTarget.TRANSCODE_NEVER ){
														
														ps.add(
																new TranscodeProfile()
																{
																	public String
																	getUID()
																	{
																		return( dmr.getID() + "/" + dmr.getBlankProfile().getName());
																	}
																	
																	public String
																	getName()
																	{
																		return( MessageText.getString( "devices.profile.direct" ));
																	}
																});												}
												}else{
												
													for ( final com.aelitis.azureus.core.devices.TranscodeProfile prof: profs ){
											
														ps.add(
															new TranscodeProfile()
															{
																public String
																getUID()
																{
																	return( prof.getUID());
																}
																
																public String
																getName()
																{
																	return( prof.getName());
																}
															});
													}
												}
												
												return( ps.toArray( new TranscodeProfile[ ps.size()]));
											}
										});					
								}
							}
							
						}catch( Throwable e ){
							
							Debug.out( e );
						}
					}
					
					Collections.sort(
						result,
						new Comparator<TranscodeTarget>()
						{
							public int 
							compare(
								TranscodeTarget o1,
								TranscodeTarget o2)
							{
								return( o1.getName().compareTo( o2.getName()));
							}
						});
					
					return( result.toArray( new TranscodeTarget[result.size()]));
				}
				               		

			});
	}

	public static void 
	lateInitialisation(
		AzureusCore core ) 
	{
		ExternalStimulusHandler.initialise(core);
		
		PluginInitializer.getDefaultInterface().getUtilities().createDelayedTask(
			new Runnable()
			{
				public void 
				run() 
				{
					MetaSearchManagerFactory.getSingleton();
					
					SubscriptionManagerFactory.getSingleton();
					
					try{
						RelatedContentManager.getSingleton();
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
					
					try{
						MetaSearchManagerFactory.getSingleton().addListener(
							new MetaSearchManagerListener()
							{
								public void
								searchRequest(
									String		term )
								{
									UIFunctionsManager.getUIFunctions().doSearch( term );
								}
							});
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}).queue();
	}

	protected static void 
	hookDownloadAddition() 
	{
		PluginInterface pi = PluginInitializer.getDefaultInterface();

		DownloadManager	dm = pi.getDownloadManager();
		
			// need to get in early to ensure property present on initial announce
		
		dm.addDownloadWillBeAddedListener(
			new DownloadWillBeAddedListener()
			{
				public void
				initialised(
					Download 	download )
				{
						// unfortunately the has-been-opened state is updated by azureus when a user opens content
						// but is also preserved across torrent export/import (e.g. when downloaded via magnet
						// URL. So reset it here if it is found to be set
					
					org.gudy.azureus2.core3.download.DownloadManager dm = PluginCoreUtils.unwrap( download );
					
					if ( PlatformTorrentUtils.getHasBeenOpened( dm )){
						
						PlatformTorrentUtils.setHasBeenOpened( dm, false );
					}
					
					register( download );
				}
			});
		
		dm.addListener(
			new DownloadManagerListener() 
			{
				public void 
				downloadAdded(
					Download download )
				{
					register( download );
				}

				public void downloadRemoved(Download download) {
				}
			});
	}

	protected static void
	register(
		final Download	download )
	{
			// only add the azid to platform content

		DownloadManagerStateAttributeListener dmsal = new DownloadManagerStateAttributeListener() {
			public void attributeEventOccurred(org.gudy.azureus2.core3.download.DownloadManager dm, String attribute_name, int event_type) {
				try{							
					Torrent t = download.getTorrent();
					if (t == null) {return;}
					if (!PlatformTorrentUtils.isContent(t, true)) {return;}
					DownloadUtils.addTrackerExtension(download, EXTENSION_PREFIX, ConstantsVuze.AZID);	
					
					// allow the tracker to manipulate peer sources for dead/unauthorised torrents
					download.setFlag(Download.FLAG_ALLOW_PERMITTED_PEER_SOURCE_CHANGES, true);
				}
				finally {
					dm.getDownloadState().removeListener(this, DownloadManagerState.AT_TRACKER_CLIENT_EXTENSIONS, DownloadManagerStateAttributeListener.WILL_BE_READ);
				}
			}
		};
		
		PluginCoreUtils.unwrap( download ).getDownloadState().addListener(dmsal, DownloadManagerState.AT_TRACKER_CLIENT_EXTENSIONS, DownloadManagerStateAttributeListener.WILL_BE_READ);				

	}
}
