/*
 * Created on Feb 10, 2009
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

import org.gudy.azureus2.plugins.PluginEvent;
import org.gudy.azureus2.plugins.PluginEventListener;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.PluginListener;
import org.gudy.azureus2.plugins.PluginManager;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.AzureusCoreRunningListener;
import com.aelitis.azureus.core.AzureusCoreFactory;

public class 
DeviceiTunesManager 
{
	private DeviceManagerImpl		device_manager;
	
	private DeviceiTunes			itunes_device;
	
	protected
	DeviceiTunesManager(
		DeviceManagerImpl		_dm )
	{
		device_manager = _dm;

		AzureusCoreFactory.addCoreRunningListener(new AzureusCoreRunningListener() {
			public void azureusCoreRunning(AzureusCore core) {
				init(core);
			}
		});
	}
	
	private void init(
			AzureusCore azureus_core )
	{
		
		final PluginManager pm = azureus_core.getPluginManager();
		
		final PluginInterface default_pi = pm.getDefaultPluginInterface();
		
		default_pi.addListener(
			new PluginListener()
			{
				public void
				initializationComplete()
				{
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
					
					PluginInterface[] plugins = pm.getPlugins();
					
					for ( PluginInterface pi: plugins ){
						
						if ( pi.getPluginState().isOperational()){
						
							pluginAdded( pi );
						}
					}
				}
				
				public void
				closedownInitiated()
				{	
				}
				
				public void
				closedownComplete()
				{
				}
			});
	}
	
	protected void
	pluginAdded(
		PluginInterface		pi )
	{
		if ( pi.getPluginState().isBuiltIn()){
			
			return;
		}
		
		String plugin_id = pi.getPluginID();
		
		if ( plugin_id.equals( "azitunes" )){
			
			DeviceiTunes new_device;
			
			synchronized( this ){
				
				if ( itunes_device == null ){
					
					itunes_device = new_device = new DeviceiTunes( device_manager, pi );
					
				}else{
					
					return;
				}
			}
			
			device_manager.addDevice( new_device, false );
		}
	}	
	
	protected void
	pluginRemoved(
		PluginInterface		pi )
	{
		String plugin_id = pi.getPluginID();
		
		if ( plugin_id.equals( "azitunes" )){
			
			DeviceiTunes existing_device;

			synchronized( this ){
				
				if ( itunes_device != null ){

					existing_device = itunes_device;
					
					itunes_device = null;
					
				}else{
					
					return;
				}
			}
			
			existing_device.remove();
		}
	}
}
