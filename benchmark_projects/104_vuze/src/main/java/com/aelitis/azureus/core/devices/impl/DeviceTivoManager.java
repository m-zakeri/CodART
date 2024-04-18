/*
 * Created on Jul 24, 2009
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

import java.util.*;
import java.io.IOException;
import java.net.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.AESemaphore;
import org.gudy.azureus2.core3.util.AEThread2;
import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.DelayedEvent;
import org.gudy.azureus2.core3.util.RandomUtils;
import org.gudy.azureus2.core3.util.SimpleTimer;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.core3.util.TimerEvent;
import org.gudy.azureus2.core3.util.TimerEventPerformer;
import org.gudy.azureus2.core3.util.TimerEventPeriodic;
import org.gudy.azureus2.platform.PlatformManagerFactory;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.tracker.Tracker;
import org.gudy.azureus2.plugins.tracker.web.TrackerWebContext;
import org.gudy.azureus2.plugins.tracker.web.TrackerWebPageGenerator;
import org.gudy.azureus2.plugins.tracker.web.TrackerWebPageRequest;
import org.gudy.azureus2.plugins.tracker.web.TrackerWebPageResponse;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;

import com.aelitis.azureus.core.devices.Device;
import com.aelitis.azureus.core.devices.DeviceManagerException;
import com.aelitis.azureus.core.networkmanager.admin.NetworkAdmin;


public class 
DeviceTivoManager 
{
	private static final String		LF				= "\n";
	private static final int		CONTROL_PORT	= 2190;
	
	private DeviceManagerImpl		device_manager;
	private PluginInterface 		plugin_interface;
	
	private boolean	is_enabled;
	private String	uid;
	private String	server_name	= "Vuze";
	
	private Searcher	current_search;
	
	private volatile boolean	manager_destroyed;
	
	protected
	DeviceTivoManager(
		DeviceManagerImpl		_dm )
	{
		device_manager = _dm;
	}
	
	protected void
	startUp()
	{
		plugin_interface = PluginInitializer.getDefaultInterface();

		if ( COConfigurationManager.getStringParameter("ui").equals("az2")){
			
			is_enabled = false;
			
		}else{
		
			is_enabled = COConfigurationManager.getBooleanParameter( "devices.tivo.enabled", true );
		}
		
		uid = COConfigurationManager.getStringParameter( "devices.tivo.uid", null );
		
		if ( uid == null ){
			
			byte[] bytes = new byte[8];
			
			RandomUtils.nextBytes( bytes );
			
			uid = Base32.encode( bytes );
			
			COConfigurationManager.setParameter( "devices.tivo.uid", uid );
		}
				
			// set up default server name
		
		try{
			String cn = PlatformManagerFactory.getPlatformManager().getComputerName();
			
			if ( cn != null && cn.length() > 0 ){
			
				server_name += " on " + cn;
			}
		}catch( Throwable e ){
		}

			// try to use the media server's name
		
		try{
			server_name = (String)device_manager.getUPnPManager().getUPnPAVIPC().invoke( "getServiceName", new Object[]{});
							
		}catch( Throwable e ){
		}
		
		boolean	found_tivo = false;
		
		for ( Device device: device_manager.getDevices()){
			
			if ( device instanceof DeviceTivo ){
				
				found_tivo = true;
				
				break;
			}
		}
			
		if ( found_tivo || device_manager.getAutoSearch()){
			
			search( found_tivo, false );
		}
	}
	
	protected boolean
	isEnabled()
	{
		return( is_enabled );
	}
	
	protected void
	setEnabled(
		boolean	enabled )
	{
		COConfigurationManager.setParameter( "devices.tivo.enabled", enabled );
		
		if ( enabled ){
			
			search( false, true );
			
		}else{
			
			for ( Device device: device_manager.getDevices()){
				
				if ( device instanceof DeviceTivo ){
		
					device.remove();
				}
			}
		}
	}
	
	protected void
	search()
	{
		search( false, false );
	}
	
	protected void
	search(
		boolean		persistent,
		boolean		async )
	{
		try{
			synchronized( this ){
				
				if ( current_search == null ){
					
					current_search = new Searcher( persistent, async );
					
				}else{
					
					if ( !current_search.wakeup()){
						
						current_search = new Searcher( persistent, async );
					}
				}
			}
		}catch( Throwable e ){
			
			Debug.out( e );
		}
	}
	
	protected byte[]
	encodeBeacon(
		boolean		is_broadcast,
		int			my_port )
	
		throws IOException
	{
		String beacon = 
			"tivoconnect=1" + LF +
			"swversion=1" + LF +	
			"method=" + (is_broadcast?"broadcast":"connected") + LF +
			"identity=" + uid + LF +
			"machine=" + server_name + LF +
			"platform=pc" + LF +
			"services=TiVoMediaServer:" + my_port + "/http";

		return( beacon.getBytes( "ISO-8859-1" ));
	}
	
	protected Map<String,String>
	decodeBeacon(
		byte[]		buffer,
		int			length )
		
		throws IOException
	{
		String str = new String( buffer, 0, length, "ISO-8859-1" );
		
		String[]	lines = str.split( LF );
		
		Map<String,String>	map = new HashMap<String, String>();
		
		for (String line:lines ){
			
			int pos = line.indexOf( '=' );
			
			if ( pos > 0 ){
				
				map.put( line.substring( 0, pos ).trim().toLowerCase(), line.substring( pos+ 1 ).trim());
			}
		}
		
		return( map );
	}
	
	protected boolean
	receiveBeacon(
		InetAddress	sender,
		byte[]		buffer,
		int			length )
	{
		if ( is_enabled ){
			
			try{
				Map<String,String>	map = decodeBeacon( buffer, length );
				
				String id = map.get( "identity" );
				
				if ( id == null || id.equals( uid )){
					
					return( false );
				}
				
				String platform = map.get( "platform" );
				
				if ( platform != null && platform.toLowerCase().startsWith( "tcd/")){
					
					String classification = "tivo." + platform.substring( 4 ).toLowerCase();
					
					foundTiVo( sender, id, classification, (String)map.get( "machine" ));
					
					return( true );
				}
			}catch( Throwable e ){
				
				log( "Failed to decode beacon", e );
			}
		}
		
		return( false );
	}
	
	protected DeviceTivo
	foundTiVo(
		InetAddress		address,
		String			uid,
		String			classification,
		String			machine )
	{
		uid	= "tivo:" + uid;
		
		DeviceImpl[] devices = device_manager.getDevices();
				
		for ( DeviceImpl device: devices ){
			
			if ( device instanceof DeviceTivo ){
				
				DeviceTivo tivo = (DeviceTivo)device;
				
				if ( device.getID().equals( uid )){
				
					if ( classification != null ){
						
						String existing_classification = device.getClassification();
						
						if ( !classification.equals( existing_classification )){
							
							device.setPersistentStringProperty( DeviceImpl.PP_REND_CLASSIFICATION,classification );
						}
					}
					
					tivo.found( this, address, server_name, machine );
					
					return( tivo );
				}
			}
		}
		
			// unfortunately we can't deduce the series from the browse request so start off with a series 3
			// this will be corrected later if we receive a beacon which *does* contain the series details
		
		if ( classification == null ){
			
			classification = "tivo.series3";
		}
		
		DeviceTivo new_device = new DeviceTivo( device_manager, uid, classification );
		
		DeviceTivo result = (DeviceTivo)device_manager.addDevice( new_device );
		
			// possible race here so handle case where device already present
		
		if ( result == new_device ){
		
			new_device.found( this, address, server_name, machine );
		}
		
		return( result );
	}
	
	protected void
	log(
		String		str )
	{
		if ( device_manager == null ){
			
			System.out.println( str );
			
		}else{
			
			device_manager.log( "TiVo: " + str );
		}
	}
	
	protected void
	log(
		String		str,
		Throwable 	e )
	{
		if ( device_manager == null ){
			
			System.out.println( str );
			
			e.printStackTrace();
			
		}else{
		
			device_manager.log( "TiVo: " + str, e );
		}
	}
	
	protected class
	Searcher
	{
		private static final int	LIFE_MILLIS = 10*1000;
		
		private long start = SystemTime.getMonotonousTime();
		
		private int		tcp_port;
		
		private DatagramSocket 		control_socket;
		private TrackerWebContext 	twc;
		private TimerEventPeriodic	timer_event;
		
		private volatile boolean		persistent;
		
		private volatile boolean		search_destroyed;
		
		protected
		Searcher(
			boolean		_persistent,
			boolean		_async )
		
			throws DeviceManagerException
		{
			try{
				int	last_port = COConfigurationManager.getIntParameter( "devices.tivo.net.tcp.port", 0 );
				
				if ( last_port > 0 ){
					
					try{
						ServerSocket ss = new ServerSocket( last_port );
					
						ss.setReuseAddress( true );
						
						ss.close();
						
					}catch( Throwable e ){
						
						last_port = 0;
					}
				}
				
				twc = plugin_interface.getTracker().createWebContext( last_port, Tracker.PR_HTTP );
				
				tcp_port = twc.getURLs()[0].getPort();

				COConfigurationManager.setParameter( "devices.tivo.net.tcp.port", tcp_port );
				
				twc.addPageGenerator(
					new TrackerWebPageGenerator()
					{
						public boolean 
						generate(
							TrackerWebPageRequest 	request,
							TrackerWebPageResponse 	response )
						
							throws IOException 
						{
							String	id = (String)request.getHeaders().get( "tsn" );
							
							if ( id == null ){
								
								id = (String)request.getHeaders().get( "tivo_tcd_id" );	
							}
							
							if ( id != null && is_enabled ){
								
								persistent = true;
								
								DeviceTivo tivo = foundTiVo( request.getClientAddress2().getAddress(), id, null, null );
								
								return( tivo.generate( request, response ));
							}
							
							return( false );
						}
					});
								
				control_socket  = new DatagramSocket( null );
					
				control_socket.setReuseAddress( true );
					
				try{
					control_socket.setSoTimeout( 60*1000 );
					
				}catch( Throwable e ){
				}
				
				InetAddress bind = NetworkAdmin.getSingleton().getSingleHomedServiceBindAddress();
				
				control_socket.bind( new InetSocketAddress( bind, CONTROL_PORT ));
		
				timer_event = 
					SimpleTimer.addPeriodicEvent(
						"Tivo:Beacon",
						60*1000,
						new TimerEventPerformer()
						{
							public void 
							perform(
								TimerEvent 	event )
							{
								if ( !( manager_destroyed || search_destroyed )){
								
									sendBeacon();
								}
								
									// see if time to auto-shutdown searching
								
								if ( !persistent ){
								
									synchronized( DeviceTivoManager.this ){
									
										if ( SystemTime.getMonotonousTime() - start >= LIFE_MILLIS ){
											
											log( "Terminating search, no devices found" );
											
											current_search = null;
											
											destroy();
										}
									}
								}
							}
						});	
				
				final AESemaphore start_sem = new AESemaphore( "TiVo:CtrlListener" );
				
				new AEThread2( "TiVo:CtrlListener", true )
				{
					public void
					run()
					{
						start_sem.release();
						
						long	successful_accepts 	= 0;
						long	failed_accepts		= 0;
		
						while( !( manager_destroyed || search_destroyed )){
							
							try{
								byte[] buf = new byte[8192];
								
								DatagramPacket packet = new DatagramPacket(buf, buf.length );
												
								control_socket.receive( packet );
									
								successful_accepts++;
								
								failed_accepts	 = 0;
								
								if ( receiveBeacon( packet.getAddress(), packet.getData(), packet.getLength())){
									
									persistent = true;
								}
								
							}catch( SocketTimeoutException e ){
															
							}catch( Throwable e ){
								
								if ( control_socket != null && !search_destroyed && !manager_destroyed ){
								
									failed_accepts++;
								
									log( "UDP receive on port " + CONTROL_PORT + " failed", e );
								}
								
								if (( failed_accepts > 100 && successful_accepts == 0 ) || failed_accepts > 1000 ){
									
									log( "    too many failures, abandoning" );
		
									break;
								}
							}
						}				
					}
				}.start();
					
				if ( _async ){
					
					new DelayedEvent( 
						"search:delay", 
						5000,
						new AERunnable()
						{
							public void
							runSupport()
							{
								sendBeacon();
							}
						});	
				}else{
					
					start_sem.reserve( 5000 );
				
					sendBeacon();
				}

				log( "Initiated device search" );
				
			}catch( Throwable e ){
			
				log( "Failed to initialise search", e );

				destroy();
				
				throw( new DeviceManagerException( "Creation failed",e ));
			}
		}
		
		protected void
		sendBeacon()
		{
			if ( is_enabled ){
				
				try{
					byte[] 	bytes = encodeBeacon( true, tcp_port );
					
					control_socket.send( new DatagramPacket( bytes, bytes.length, InetAddress.getByName( "255.255.255.255" ), CONTROL_PORT ));
					
				}catch( Throwable e ){
					
					log( "Failed to send beacon", e );
				}
			}
		}
		
		protected boolean
		wakeup()
		{
			synchronized( DeviceTivoManager.this ){
				
				if ( search_destroyed ){
					
					return( false );
				}
				
				start = SystemTime.getMonotonousTime();
			}
			
			sendBeacon();
			
			return( true );
		}
		
		protected void
		destroy()
		{
			search_destroyed = true;
			
			if ( twc != null ){
				
				twc.destroy();
				
				twc = null;
			}
			
			if ( timer_event != null ){
				
				timer_event.cancel();
				
				timer_event = null;
			}
			
			if ( control_socket != null ){
				
				try{
					control_socket.close();
					
				}catch( Throwable e ){
				}
				
				control_socket = null;
			}
		}
	}
}
