/*
 * Created on Feb 4, 2009
 * Created by Paul Gardner
 * 
 * Copyright 2009 Vuze, Inc.  All rights reserved.
 * 
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
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */


package com.aelitis.azureus.core.devices.impl;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.gudy.azureus2.core3.category.Category;
import org.gudy.azureus2.core3.category.CategoryListener;
import org.gudy.azureus2.core3.category.CategoryManager;
import org.gudy.azureus2.core3.category.CategoryManagerListener;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.global.GlobalManagerAdapter;
import org.gudy.azureus2.core3.global.GlobalManagerListener;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.plugins.*;
import org.gudy.azureus2.plugins.disk.DiskManagerFileInfo;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.torrent.TorrentAttribute;
import org.gudy.azureus2.pluginsimpl.local.PluginCoreUtils;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.AzureusCoreFactory;
import com.aelitis.azureus.core.devices.*;
import com.aelitis.azureus.core.util.CopyOnWriteList;

public class 
TranscodeManagerImpl
	implements TranscodeManager
{
	private DeviceManagerImpl		device_manager;
	private AzureusCore				azureus_core;
	
	private TranscodeProviderVuze	vuzexcode_provider;
	
	private CopyOnWriteList<TranscodeManagerListener>	listeners = new CopyOnWriteList<TranscodeManagerListener>();
	
	private TranscodeQueueImpl		queue = new TranscodeQueueImpl( this );
	
	private AESemaphore	init_sem 	= new AESemaphore( "TM:init" );

	private boolean hooked_categories;
	
	private Map<Category,Object[]> 	category_map = new HashMap<Category, Object[]>();
	private CategoryListener		category_listener;
	private GlobalManagerListener	category_dl_listener;
	private TorrentAttribute		category_ta;
	
	protected
	TranscodeManagerImpl(
		DeviceManagerImpl		_dm )
	{
		device_manager	= _dm;
		
		azureus_core = AzureusCoreFactory.getSingleton();
		
		PluginInterface default_pi = PluginInitializer.getDefaultInterface();
		
		category_ta = default_pi.getTorrentManager().getPluginAttribute( "xcode.cat.done" );
		
		final AESemaphore	plugin_sem 	= new AESemaphore( "TM:plugin" );

		default_pi.addListener(
			new PluginListener()
			{
				public void
				initializationComplete()
				{
					try{
						PluginInterface default_pi = PluginInitializer.getDefaultInterface();
						
						default_pi.addEventListener(
							new PluginEventListener()
							{
								public void 
								handleEvent(
									PluginEvent ev )
								{
									int	type = ev.getType();
									
									if ( type == PluginEvent.PEV_PLUGIN_OPERATIONAL ){
										
										pluginAdded((PluginInterface)ev.getValue());
									}
									if ( type == PluginEvent.PEV_PLUGIN_NOT_OPERATIONAL ){
										
										pluginRemoved((PluginInterface)ev.getValue());
									}
								}
							});
						
						PluginInterface[] plugins = default_pi.getPluginManager().getPlugins();
						
						for ( PluginInterface pi: plugins ){
							
							if ( pi.getPluginState().isOperational()){
							
								pluginAdded( pi );
							}
						}
					}finally{
						
						plugin_sem.releaseForever();
					}
				}
				
				public void
				closedownInitiated()
				{
					plugin_sem.releaseForever();
					
						// we don't want things hanging around for init if we're closing
					
					init_sem.releaseForever();
				}
				
				public void
				closedownComplete()
				{
				}
			});
		
		if ( !plugin_sem.reserve( 30*1000 )){
			
			Debug.out( "Timeout waiting for init" );
			
			AEDiagnostics.dumpThreads();
		}
	}
	
	protected void
	initialise()
	{
		queue.initialise();
		
		init_sem.releaseForever();
	}
	
	protected void
	pluginAdded(
		PluginInterface		pi )
	{
		if ( pi.getPluginState().isBuiltIn()){
			
			return;
		}
		
		String plugin_id = pi.getPluginID();
		
		if ( plugin_id.equals( "vuzexcode" )){
			
			boolean		added		= false;
			boolean		updated		= false;
			
			TranscodeProviderVuze provider	= null;
			
			synchronized( this ){
				
				if ( vuzexcode_provider == null ){
					
					provider = vuzexcode_provider = new TranscodeProviderVuze( this, pi );
			
					added = true;
					
				}else if ( pi != vuzexcode_provider ){
					
					provider = vuzexcode_provider;
					
					vuzexcode_provider.update( pi );
					
					updated = true;
				}
			}
			
			if ( added ){
				
				for ( TranscodeManagerListener listener: listeners ){
					
					try{
						listener.providerAdded( provider );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}else if ( updated ){
				
				for ( TranscodeManagerListener listener: listeners ){
					
					try{
						listener.providerUpdated( provider );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}
		}
	}
	
	protected void
	pluginRemoved(
		PluginInterface		pi )
	{
		String plugin_id = pi.getPluginID();
		
		if ( plugin_id.equals( "vuzexcode" )){
			
			TranscodeProviderVuze provider	= null;

			synchronized( this ){
				
				if ( vuzexcode_provider != null ){

					provider = vuzexcode_provider;
					
					vuzexcode_provider.destroy();
					
					vuzexcode_provider = null;
				}
			}
			
			if ( provider != null ){
				
				for ( TranscodeManagerListener listener: listeners ){
					
					try{
						listener.providerRemoved( provider );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}
		}
	}
	
	protected void
	updateStatus(
		int	tick_count )
	{
		if ( queue != null ){
			
			queue.updateStatus( tick_count );
			
			if ( !hooked_categories ){
				
				hooked_categories = true;
				
				CategoryManager.addCategoryManagerListener(
					new CategoryManagerListener()
					{
						public void
						categoryAdded(
							Category category )
						{
						}
							
						public void
						categoryRemoved(
							Category category )
						{
						}
						
						public void
						categoryChanged(
							Category category )
						{
							checkCategories();
						}
					});
				
				checkCategories();
			}
		}
	}
	
	private void
	checkCategories()
	{
		Category[] cats = CategoryManager.getCategories();
		
		Map<Category,Object[]> active_map = new HashMap<Category, Object[]>();
		
		for ( Category cat: cats ){
			
			String target = cat.getStringAttribute( Category.AT_AUTO_TRANSCODE_TARGET );
			
			if ( target != null ){
				
				String device_id = null;
				
				if ( target.endsWith( "/blank" )){
					
					device_id = target.substring( 0, target.length() - 6 );
				}
				
				DeviceMediaRenderer		target_dmr			= null;
				TranscodeProfile		target_profile 		= null;
				
				for ( DeviceImpl device: device_manager.getDevices()){
				
					if ( !( device instanceof DeviceMediaRenderer )){
						
						continue;
					}
					
					DeviceMediaRenderer dmr = (DeviceMediaRenderer)device;
					
					if ( device_id != null ){
						
						if ( device.getID().equals( device_id )){
							
							target_dmr		 	= dmr;
							target_profile		= device.getBlankProfile();
							
							break;
						}
					}else{
						
						TranscodeProfile[] profs = device.getTranscodeProfiles();
						
						for ( TranscodeProfile prof: profs ){
							
							if ( prof.getUID().equals( target )){
								
								target_dmr	= dmr;
								target_profile	= prof;
								
								break;
							}
						}
					}
				}
			
				if ( target_dmr != null ){
					
					active_map.put( cat, new Object[]{ target_dmr, target_profile });					
				}
			}
		}
		
		Map<Category,Object[]> to_process = new HashMap<Category, Object[]>();
		
		synchronized( category_map ){
			
			if ( category_listener == null ){
				
				category_listener = 
					new CategoryListener()
					{
						public void	
						downloadManagerAdded(
							Category 			cat, 
							DownloadManager 	manager )
						{
							Object[]	details;
							
							synchronized( category_map ){

								details = category_map.get( cat );
							}
							
							if ( details != null ){
								
								processCategory( cat, details, manager );
							}
						}
					
						public void	
						downloadManagerRemoved(
							Category 			cat, 
							DownloadManager 	removed )
						{							
						}
					};
			}
			
			Iterator<Category>	it = category_map.keySet().iterator();
			
			while( it.hasNext()){
				
				Category c = it.next();
				
				if ( !active_map.containsKey( c )){
					
					c.removeCategoryListener( category_listener );
					
					it.remove();
				}
			}
			
			for ( final Category c: active_map.keySet()){
				
				if ( !category_map.containsKey( c )){
					
					to_process.put( c, active_map.get(c));
					
					c.addCategoryListener( category_listener );
					
					category_map.put( c, active_map.get(c));
					
					if ( c.getType() == Category.TYPE_UNCATEGORIZED ){
						
						if ( category_dl_listener == null ){
						
								// new downloads don't get a category-change event fired when added
								// we also want to delay things a bit to allow other components
								// to set an initial category. there's no hurry anyways
							
							category_dl_listener = 
								new GlobalManagerAdapter()
								{
									public void
									downloadManagerAdded(
										final DownloadManager	dm )
									{
										new DelayedEvent( 
											"TM:cat-check",
											10*1000,
											new AERunnable()
											{
												public void
												runSupport()
												{
													Category dm_c = dm.getDownloadState().getCategory();
													
													if ( dm_c == null || dm_c == c ){
														
															// still uncategorised
													
														Object[]	details;
														
														synchronized( category_map ){
	
															details = category_map.get( c );
														}
														
														if ( details != null ){
															
															processCategory( c, details, dm );
														}
													}
												}
											});
									}
									public void
									downloadManagerRemoved(
										DownloadManager	dm )
									{
									}
								};
						
								
							azureus_core.getGlobalManager().addListener( category_dl_listener, false );
						}
					}
				}
			}
		}
		
		if ( to_process.size() > 0 ){
			
			List<DownloadManager> downloads = azureus_core.getGlobalManager().getDownloadManagers();
			
			for ( Map.Entry<Category, Object[]> entry: to_process.entrySet()){
				
				Category 	c 		= entry.getKey();
				Object[]	details = entry.getValue();
				
				List<DownloadManager> list = c.getDownloadManagers( downloads );
				
				for( DownloadManager dm: list ){
					
					processCategory( c, details, dm );
				}
			}
		}
	}
	
	private void
	processCategory(
		Category		cat,
		Object[]		details,
		DownloadManager	dm )
	{
		Download download = PluginCoreUtils.wrap( dm );
		
		if ( download.getFlag( Download.FLAG_LOW_NOISE )){
			
			return;
		}
		
		String str = download.getAttribute( category_ta );
		
		String cat_name = cat.getName();
		
		if ( cat.getType() == Category.TYPE_UNCATEGORIZED ){
			
			cat_name = "<none>";
		}
		
		String	cat_tag = cat_name + ";";
		
		if ( str != null && str.contains( cat_tag )){
			
			return;
		}
		
		try{
			DeviceMediaRenderer		device 	= (DeviceMediaRenderer)details[0];
			TranscodeProfile		profile	= (TranscodeProfile)details[1];
						
			log( "Category " + cat_name + " - adding " + download.getName() + " to " + device.getName() + "/" + profile.getName());
			
			DiskManagerFileInfo[] dm_files = download.getDiskManagerFileInfo();
			
			int	num_added = 0;
			
			for ( DiskManagerFileInfo dm_file: dm_files ){
				
					// limit number of files we can add to avoid crazyness
				
				if ( num_added > 64 ){
					
					break;
				}
				
					// could be smarter here and check extension or whatever
				
				if ( dm_files.length == 1 || dm_file.getLength() >= 128*1024 ){
					
					try{
						queue.add( device, profile, dm_file, false  );
					
						num_added++;
						
					}catch( Throwable e ){
						
						log( "    add failed", e );
					}
				}
			}
		}finally{
			
			download.setAttribute( category_ta, str==null?cat_tag:(str+cat_tag));
		}
	}
	
	public TranscodeProvider[]
	getProviders()
	{
		TranscodeProviderVuze	vp = vuzexcode_provider;

		if ( vp == null ){
		
			return( new TranscodeProvider[0] );
		}
		
		return( new TranscodeProvider[]{ vp });
	}
	
	protected TranscodeProfile
	getProfileFromUID(
		String		uid )
	{
		for ( TranscodeProvider provider: getProviders()){
			
			TranscodeProfile profile = provider.getProfile( uid );
			
			if ( profile != null ){
				
				return( profile );
			}
		}
		
		return( null );
	}
	
	public TranscodeQueueImpl
	getQueue() 
	{
		if ( !init_sem.reserve(30*1000)){
			
			Debug.out( "Timeout waiting for init" );
			
			AEDiagnostics.dumpThreads();
		}
		
		return( queue );
	}
	
	protected DeviceManagerImpl
	getManager()
	{
		return( device_manager );
	}
	
	protected TranscodeTarget
	lookupTarget(
		String		target_id )
	
		throws TranscodeException
	{
		Device device = device_manager.getDevice( target_id );
		
		if ( device instanceof TranscodeTarget ){
			
			return((TranscodeTarget)device);
		}
		
		throw( new TranscodeException( "Transcode target with id " + target_id + " not found" ));
	}
	
	protected DiskManagerFileInfo
	lookupFile(
		byte[]		hash,
		int			index )
	
		throws TranscodeException
	{
		try{
			Download download = PluginInitializer.getDefaultInterface().getDownloadManager().getDownload( hash );
			
			if ( download == null ){
				
				throw( new TranscodeException( "Download with hash " + ByteFormatter.encodeString( hash ) + " not found" ));
			}
		
			return( download.getDiskManagerFileInfo()[index]);
			
		}catch( Throwable e ){
			
			throw( new TranscodeException( "Download with hash " + ByteFormatter.encodeString( hash ) + " not found", e ));

		}
	}
	
	protected void
	close()
	{
		queue.close();
	}
	
	public void
	addListener(
		TranscodeManagerListener		listener )
	{
		listeners.add( listener );
	}
	
	public void
	removeListener(
		TranscodeManagerListener		listener )
	{
		listeners.remove( listener );
	}
	
	protected void
	log(
		String	str )
	{
		device_manager.log( "Trans: " + str );
	}
	
	protected void
	log(
		String		str,
		Throwable	e )
	{
		device_manager.log( "Trans: " + str, e );
	}
	
	public void
	generate(
		IndentWriter		writer )
	{
		writer.println( "Transcode Manager: vuze provider=" + vuzexcode_provider );
		
		queue.generate( writer );
	}
}
