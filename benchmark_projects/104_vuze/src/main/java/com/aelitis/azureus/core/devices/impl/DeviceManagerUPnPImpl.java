/*
 * Created on Jan 27, 2009
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

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.URL;
import java.util.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.plugins.PluginEvent;
import org.gudy.azureus2.plugins.PluginEventListener;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.PluginListener;
import org.gudy.azureus2.plugins.ipc.IPCInterface;
import org.gudy.azureus2.plugins.torrent.TorrentAttribute;
import org.gudy.azureus2.plugins.tracker.web.TrackerWebPageRequest;
import org.gudy.azureus2.plugins.utils.UTTimer;
import org.gudy.azureus2.plugins.utils.resourcedownloader.ResourceDownloaderFactory;
import org.gudy.azureus2.plugins.utils.xml.simpleparser.SimpleXMLParserDocument;
import org.gudy.azureus2.plugins.utils.xml.simpleparser.SimpleXMLParserDocumentException;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;
import org.gudy.azureus2.pluginsimpl.local.ipc.IPCInterfaceImpl;

import com.aelitis.azureus.core.content.AzureusContentDownload;
import com.aelitis.azureus.core.content.AzureusContentFile;
import com.aelitis.azureus.core.content.AzureusContentFilter;
import com.aelitis.azureus.core.devices.DeviceMediaRenderer;
import com.aelitis.azureus.core.devices.DeviceManager.UnassociatedDevice;
import com.aelitis.azureus.core.util.UUIDGenerator;
import com.aelitis.net.upnp.UPnP;
import com.aelitis.net.upnp.UPnPAdapter;
import com.aelitis.net.upnp.UPnPDevice;
import com.aelitis.net.upnp.UPnPFactory;
import com.aelitis.net.upnp.UPnPListener;
import com.aelitis.net.upnp.UPnPRootDevice;
import com.aelitis.net.upnp.UPnPRootDeviceListener;
import com.aelitis.net.upnp.UPnPSSDPListener;
import com.aelitis.net.upnp.UPnPService;
import com.aelitis.net.upnp.services.UPnPOfflineDownloader;
import com.aelitis.net.upnp.services.UPnPWANConnection;

public class 
DeviceManagerUPnPImpl 
{
	private final static Object KEY_ROOT_DEVICE = new Object();
		
	private DeviceManagerImpl		manager;
	private PluginInterface			plugin_interface;
	private UPnP 					upnp;
	private TorrentAttribute		ta_category;
	
	private volatile IPCInterface			upnpav_ipc;
	
	private Map<InetAddress,String>		unassociated_devices = new HashMap<InetAddress, String>();
	
	private Set<String>					access_logs	= new HashSet<String>();
	
	protected
	DeviceManagerUPnPImpl(
		DeviceManagerImpl		_manager )
	{
		manager	= _manager;
	}
	
	protected void
	initialise()
	{
		plugin_interface = PluginInitializer.getDefaultInterface();
		
		ta_category = plugin_interface.getTorrentManager().getAttribute( TorrentAttribute.TA_CATEGORY );
		
		plugin_interface.addListener(
				new PluginListener()
				{
					public void
					initializationComplete()
					{
							// startup can take a while as adding the upnp listener can sync call back device added and result
							// in device details loading etc
						
						new AEThread2( "DMUPnPAsyncStart", true )
						{
							public void
							run()
							{
								startUp();
							}
						}.start();
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
	
	protected DeviceManagerImpl
	getManager()
	{
		return( manager );
	}
	
	protected TorrentAttribute
	getCategoryAttibute()
	{
		return( ta_category );
	}
	
	protected void
	startUp()
	{
		UPnPAdapter adapter = 
			new UPnPAdapter()
			{
				public SimpleXMLParserDocument
				parseXML(
					String	data )
				
					throws SimpleXMLParserDocumentException
				{
					return( plugin_interface.getUtilities().getSimpleXMLParserDocumentFactory().create( data ));
				}
				
				public ResourceDownloaderFactory
				getResourceDownloaderFactory()
				{
					return( plugin_interface.getUtilities().getResourceDownloaderFactory());
				}
				
				public UTTimer
				createTimer(
					String	name )
				{
					return( plugin_interface.getUtilities().createTimer( name ));
				}
				
				public void
				createThread(
					String				name,
					final Runnable		runnable )
				{
					plugin_interface.getUtilities().createThread( name, runnable );
				}
				
				public Comparator
				getAlphanumericComparator()
				{
					return( plugin_interface.getUtilities().getFormatters().getAlphanumericComparator( true ));
				}

				public void
				log(
					Throwable	e )
				{
					Debug.printStackTrace(e);
				}
				
				public void
				trace(
					String	str )
				{
					// System.out.println( str );
				}
				
				public void
				log(
					String	str )
				{
					// System.out.println( str );
				}
				
				public String
				getTraceDir()
				{
					return( plugin_interface.getPluginDirectoryName());
				}
			};
		
		try{
			upnp = UPnPFactory.getSingleton( adapter, null );
			
			
			upnp.addRootDeviceListener(
				new UPnPListener()
				{
					public boolean
					deviceDiscovered(
						String		USN,
						URL			location )
					{
						return( true );
					}
					
					public void
					rootDeviceFound(
						UPnPRootDevice		device )
					{
						handleDevice( device, true );
					}
				});
		
			upnp.getSSDP().addListener(
				new UPnPSSDPListener()
				{
					private Map<InetAddress,Boolean>	liveness_map = new HashMap<InetAddress, Boolean>();
					
					public void
					receivedResult(
						NetworkInterface	network_interface,
						InetAddress			local_address,
						InetAddress			originator,
						String				USN,
						URL					location,
						String				ST,
						String				AL )
					{
					}
					
					public void
					receivedNotify(
						NetworkInterface	network_interface,
						InetAddress			local_address,
						InetAddress			originator,
						String				USN,
						URL					location,
						String				NT,
						String				NTS )
					{
						alive( originator, NTS.indexOf( "byebye") == -1 );
					}

					public String[]
					receivedSearch(
						NetworkInterface	network_interface,
						InetAddress			local_address,
						InetAddress			originator,
						String				ST )
					{
						alive( originator, true );
						
						return( null );
					}
					
					public void
					interfaceChanged(
						NetworkInterface	network_interface )
					{
					}
					
					private void
					alive(
						InetAddress		address,
						boolean			alive )
					{
						synchronized( liveness_map ){
						
							Boolean	b = liveness_map.get( address );
							
							if ( b != null && b == alive ){
								
								return;
							}
							
							liveness_map.put( address, alive );
						}
												
						DeviceImpl[] devices = manager.getDevices();

						for ( DeviceImpl d: devices ){
												
							if ( d instanceof DeviceMediaRendererImpl ){
									
								DeviceMediaRendererImpl r = (DeviceMediaRendererImpl)d;
									
								InetAddress device_address = r.getAddress();
									
								if ( device_address != null && device_address.equals( address )){
										
									if ( r.isAlive() != alive ){
										
										if ( alive ){
											
											r.alive();
											
										}else{
											
											r.dead();
										}
									}
								}
							}
						}
					}
				});
			
		}catch( Throwable e ){
			
			manager.log( "UPnP device manager failed", e );
		}
		
		try{			
			plugin_interface.addEventListener(
					new PluginEventListener()
					{
						public void 
						handleEvent(
							PluginEvent ev )
						{
							int	type = ev.getType();
							
							if ( 	type == PluginEvent.PEV_PLUGIN_OPERATIONAL ||
									type == PluginEvent.PEV_PLUGIN_NOT_OPERATIONAL ){
								
								PluginInterface pi = (PluginInterface)ev.getValue();
			
								if ( pi.getPluginID().equals( "azupnpav" )){
				
									if ( type == PluginEvent.PEV_PLUGIN_OPERATIONAL ){
									
										upnpav_ipc = pi.getIPC();

										addListener( pi );
										
									}else{
										
										upnpav_ipc = null;
									}
								}
							}
						}
					});
			
			PluginInterface pi = plugin_interface.getPluginManager().getPluginInterfaceByID( "azupnpav" );

			if ( pi == null ){
				
				manager.log( "No UPnPAV plugin found" );
				
			}else{
				
				upnpav_ipc = pi.getIPC();
				
				addListener( pi );
			}			
		}catch( Throwable e ){
			
			manager.log( "Failed to hook into UPnPAV", e );
		}
		
		manager.UPnPManagerStarted();
	}
	
	protected void
	addListener(
		PluginInterface	pi )
	{
		try{			
			IPCInterface my_ipc = 
				new IPCInterfaceImpl(
					new Object()
					{
						public Map<String,Object>
						browseReceived(
							TrackerWebPageRequest		request,
							Map<String,Object>			browser_args )
						{
							Map headers = request.getHeaders();
							
							String user_agent 	= (String)headers.get( "user-agent" );
							String client_info 	= (String)headers.get( "x-av-client-info" );
							
							InetSocketAddress client_address = request.getClientAddress2();
													
							boolean	handled = false;
														
							if ( user_agent != null ){
								
								String lc_agent = user_agent.toLowerCase();
								
								if ( lc_agent.contains( "playstation 3")){
									
									handlePS3( client_address );
									
									handled = true;
									
								}else if ( lc_agent.contains( "xbox")){
								
									handleXBox( client_address );
									
									handled = true;
									
								}else if ( lc_agent.contains( "nintendo wii")){
								
									handleWii( client_address );
																		
									handled = true;
								}

							}
							
							if ( client_info != null ){
							
								String	lc_info = client_info.toLowerCase();
								
								if ( lc_info.contains( "playstation 3")){
									
									handlePS3( client_address );
									
									handled = true;
								}
							}
							
							if ( !handled ){
								
								handled = manager.browseReceived( request, browser_args );
							}
							
							if ( !handled ){
								
								String	 source = (String)browser_args.get( "source" );
								
								if ( source != null && source.equalsIgnoreCase( "http" )){
									
									handleBrowser( client_address );
																		
									handled = true;
								}
							}
							
							/**
							System.out.println( 
									"Received browse: " + request.getClientAddress() +
									", agent=" + user_agent +
									", info=" + client_info +
									", handled=" + handled + ", " + request.getURL());
									System.out.println("\n\n");
								/**/

							
							DeviceImpl[] devices = manager.getDevices();
							
							final List<DeviceMediaRendererImpl>	browse_devices = new ArrayList<DeviceMediaRendererImpl>();
							
							boolean	restrict_access = false;
							
							for ( DeviceImpl device: devices ){
							
								if ( device instanceof DeviceMediaRendererImpl ){
								
									DeviceMediaRendererImpl renderer = (DeviceMediaRendererImpl)device;
									
									InetAddress device_address = renderer.getAddress();
									
									try{
										if ( device_address != null ){
														
												// just test on IP, should be OK
											
											if ( device_address.equals( client_address.getAddress())){
					
												if ( renderer.canFilterFilesView()){
												
													boolean	skip = false;
													
													if ( renderer.canRestrictAccess()){
														
														String restriction = renderer.getAccessRestriction().trim();
														
														if ( restriction.length() > 0 ){
															
															String x = client_address.getAddress().getHostAddress();
															
															skip = true;
															
															String[] ips = restriction.split( "," );
															
															for ( String ip: ips ){
																
																if ( ip.startsWith( "-" )){
																	
																	ip = ip.substring(1);
																	
																	if ( ip.equals( x )){
																		
																		break;
																	}
																}else{
																	
																	if ( ip.startsWith( "+" )){
																		
																		ip = ip.substring(1);
																	}
																	
																	if ( ip.equals( x )){
																	
																		skip = false;
																		
																		break;
																	}
																}
															}
														}
													}
													
													if ( skip ){
													
														restrict_access = true;
														
														String	host = client_address.getAddress().getHostAddress();
														
														synchronized( access_logs){
															
															if ( !access_logs.contains( host )){
																
																access_logs.add( host );
															
																manager.log( "Ignoring browse from " + host + " due to access restriction for '" + renderer.getName() + "'" );
															}
														}
													}
														
													browse_devices.add( renderer );
													
													renderer.browseReceived();
												}
											}
										}
									}catch( Throwable e ){
										
										Debug.out( e );
									}
								}
							}
							
							Map<String,Object> result = new HashMap<String, Object>();
							
							if ( browse_devices.size() > 0 ){
								
								synchronized( unassociated_devices ){
									
									unassociated_devices.remove( client_address.getAddress() );
								}
								
								final boolean f_restrict_access = restrict_access;
								
								result.put(
									"filter",
									new AzureusContentFilter()
									{
										public boolean
										isVisible(
											AzureusContentDownload	download,
											Map<String,Object>		browse_args )
										{
											if ( f_restrict_access ){
												
												return( false );
											}
											
											boolean	visible = false;
											
											for ( DeviceUPnPImpl device: browse_devices ){
												
												if ( device.isVisible( download )){
													
													visible	= true;
												}
											}
											
											return( visible );
										}
										
										public boolean
										isVisible(
											AzureusContentFile		file,
											Map<String,Object>		browse_args )
										{
											if ( f_restrict_access ){
												
												return( false );
											}
											
											boolean	visible = false;
											
											for ( DeviceUPnPImpl device: browse_devices ){
												
												if ( device.isVisible( file )){
													
													visible	= true;
												}
											}
											
											return( visible );
										}
									});
							}else{
								
								if ( request.getHeader().substring(0,4).equalsIgnoreCase( "POST" )){
									
									synchronized( unassociated_devices ){
									
										unassociated_devices.put( client_address.getAddress(), user_agent );
									}
								}
							}
								
							return( result );
						}
					});
			
			if ( upnpav_ipc.canInvoke( "addBrowseListener", new Object[]{ my_ipc })){
								
				DeviceImpl[] devices = manager.getDevices();
				
				for ( DeviceImpl device: devices ){
				
					if ( device instanceof DeviceUPnPImpl ){
					
						DeviceUPnPImpl u_d = (DeviceUPnPImpl)device;

						u_d.resetUPNPAV();
					}
				}
				
				upnpav_ipc.invoke( "addBrowseListener", new Object[]{ my_ipc });

			}else{
				
				manager.log( "UPnPAV plugin needs upgrading" );
			}
		}catch( Throwable e ){
			
			manager.log( "Failed to hook into UPnPAV", e );
		}
	}
	
	protected void
	injectDiscoveryCache(
		Map		cache )
	{
		try{
			upnp.injectDiscoveryCache( cache );
			
		}catch( Throwable e ){
	
			Debug.out( e );
		}
	}
	
	public UnassociatedDevice[]
	getUnassociatedDevices()
	{
		List<UnassociatedDevice> result = new ArrayList<UnassociatedDevice>();
		
		Map<InetAddress,String> ud;
		
		synchronized( unassociated_devices ){

			ud = new HashMap<InetAddress,String>( unassociated_devices );
		}
		
		DeviceImpl[] devices = manager.getDevices();

		for ( final Map.Entry<InetAddress, String> entry: ud.entrySet()){
			
			InetAddress	address = entry.getKey();
			
			boolean already_assoc = false;

			for ( DeviceImpl d: devices ){
								
				if ( d instanceof DeviceMediaRendererImpl ){
					
					DeviceMediaRendererImpl r = (DeviceMediaRendererImpl)d;
					
					InetAddress device_address = r.getAddress();
					
					if ( d.isAlive() && device_address != null && device_address.equals( address )){
						
						already_assoc = true;
						
						break;
					}
				}
			}
			
			if ( !already_assoc ){
				
				result.add(
					new UnassociatedDevice()
					{
						public InetAddress
						getAddress()
						{
							return( entry.getKey());
						}
						
						public String
						getDescription()
						{
							return( entry.getValue());
						}
					});
			}
		}
		
		return( result.toArray( new UnassociatedDevice[result.size()]));
	}
	
	public PluginInterface
	getPluginInterface()
	{
		return( plugin_interface );
	}
	
	protected IPCInterface
	getUPnPAVIPC()
	{
		return( upnpav_ipc );
	}
	
	public void
	search()
	{	
		if ( upnp != null ){
	
			// if the user has removed items we need to re-inject them

			UPnPRootDevice[] devices = upnp.getRootDevices();
			
			for ( UPnPRootDevice device: devices ){
				
				handleDevice( device, false );
			}
			
			String[] STs = {
				"upnp:rootdevice",
				"urn:schemas-upnp-org:device:MediaRenderer:1"
			};
			
			upnp.search( STs );
		}
	}
	
	protected void
	handleXBox(
		InetSocketAddress	address )
	{
		// normally we can detect the xbox renderer and things work automagically. However, on
		// occasion we receive the browse before detection and if the device's IP has changed
		// we need to associate its new address here otherwise association of browse to device
		// fails
		
		DeviceImpl[] devices = manager.getDevices();
		
		boolean	found = false;
		
		for ( DeviceImpl device: devices ){
			
			if ( device instanceof DeviceMediaRendererImpl ){
				
				DeviceMediaRendererImpl renderer = (DeviceMediaRendererImpl)device;
				
				if ( device.getRendererSpecies() == DeviceMediaRenderer.RS_XBOX ){

					found = true;
					
					if (!device.isAlive()){
				
						renderer.setAddress( address.getAddress());
						
						device.alive();
					}
				}
			}
		}
		
		if ( !found ){
			
			manager.addDevice( new DeviceMediaRendererImpl( manager, "Xbox 360" ));
		}
	}
	
	protected void
	handlePS3(
		InetSocketAddress	address )
	{
		handleGeneric( address, "ps3", "PS3" );
	}

	protected void
	handleWii(
		InetSocketAddress	address )
	{
		handleGeneric( address, "wii", "Wii" );
	}
	
	protected void
	handleBrowser(
		InetSocketAddress	address )
	{
		handleGeneric( address, "browser", "Browser" );
	}
	
	protected DeviceMediaRenderer
	handleGeneric(
		InetSocketAddress	address,
		String				unique_name,
		String				display_name )
	{
		String uid;
		
		synchronized( this ){
			
			uid = COConfigurationManager.getStringParameter( "devices.upnp.uid." + unique_name, "" );
			
			if ( uid.length() == 0 ){
				
				uid = UUIDGenerator.generateUUIDString();
				
				COConfigurationManager.setParameter( "devices.upnp.uid." + unique_name, uid );
				
				COConfigurationManager.save();
			}
		}
		
		DeviceMediaRendererImpl newDevice = new DeviceMediaRendererImpl( manager, uid, unique_name, false, display_name );
		DeviceMediaRendererImpl device = (DeviceMediaRendererImpl)manager.addDevice( newDevice );
		
		device.setAddress( address.getAddress());
		
		device.alive();

		return device;
	}
	
	protected void
	handleDevice(
		UPnPRootDevice		root_device,
		boolean				update_if_found )
	{
		if ( !manager.getAutoSearch()){
			
			if ( !manager.isExplicitSearch()){
				
				return;
			}
		}
		
		handleDevice( root_device.getDevice(), update_if_found );
	}
	
	protected void
	handleDevice(
		UPnPDevice	device,
		boolean		update_if_found )
	{
		UPnPService[] 	services = device.getServices();
		
		List<DeviceUPnPImpl>	new_devices = new ArrayList<DeviceUPnPImpl>();
		
		List<UPnPWANConnection>	igd_services = new ArrayList<UPnPWANConnection>();
		
		for ( UPnPService service: services ){
				
			String	service_type = service.getServiceType();
				
			if ( 	service_type.equalsIgnoreCase( "urn:schemas-upnp-org:service:WANIPConnection:1") || 
					service_type.equalsIgnoreCase( "urn:schemas-upnp-org:service:WANPPPConnection:1")){
				
				UPnPWANConnection	wan_service = (UPnPWANConnection)service.getSpecificService();
				
				igd_services.add( wan_service );				

			}else if ( service_type.equals( "urn:schemas-upnp-org:service:ContentDirectory:1" )){
				
				new_devices.add( new DeviceContentDirectoryImpl( manager, device, service ));
				
			}else if ( service_type.equals( "urn:schemas-upnp-org:service:VuzeOfflineDownloaderService:1" )){
				
					// ignore local offline downloader
				
				try{
					PluginInterface od_pi = plugin_interface.getPluginManager().getPluginInterfaceByID( "azofflinedownloader" );
	
					if ( od_pi != null ){
					
						String	local_usn = (String)od_pi.getIPC().invoke( "getUSN", new Object[0] );
					
						String	od_usn = device.getRootDevice().getUSN();
						
							// we end up with "::upnp:rootdevice" on the end of this - remove
						
						int	pos = od_usn.indexOf( "::upnp:rootdevice" );
						
						if ( pos > 0 ){
							
							od_usn = od_usn.substring( 0, pos );
						}
						
						if ( od_usn.equals( local_usn )){
							
							continue;
						}
					}
				}catch( Throwable e ){
					
					Debug.out( e );
				}
				
				UPnPOfflineDownloader downloader = (UPnPOfflineDownloader)service.getSpecificService();

				if ( downloader != null ){
					
					new_devices.add( new DeviceOfflineDownloaderImpl( manager, device, downloader ));
				}
			}
		}
		
		if ( igd_services.size() > 0 ){
			
			new_devices.add( new DeviceInternetGatewayImpl( manager, device, igd_services ));
		}
		
		if ( device.getDeviceType().equals( "urn:schemas-upnp-org:device:MediaRenderer:1" )){
				
			new_devices.add( new DeviceMediaRendererImpl( manager, device ));
		}
		
		for ( final DeviceUPnPImpl new_device: new_devices ){
				
			final DeviceImpl actual_device;
			
			DeviceImpl existing = manager.getDevice( new_device.getID());
			
			if ( !update_if_found && existing != null ){
					
				actual_device = existing;
				
			}else{
			
					// grab the actual device as the 'addDevice' call will update an existing one
					// with same id
			
				actual_device = manager.addDevice( new_device );
			}
			
			UPnPRootDevice current_root = device.getRootDevice();
			
			UPnPRootDevice existing_root = (UPnPRootDevice)actual_device.getTransientProperty( KEY_ROOT_DEVICE );
			
			if ( current_root != existing_root ){
				
				actual_device.setTransientProperty( KEY_ROOT_DEVICE, current_root );
				
				current_root.addListener(
					new UPnPRootDeviceListener()
					{
						public void
						lost(
							UPnPRootDevice	root,
							boolean			replaced )
						{
							if ( !replaced ){
								
								actual_device.dead();
							}
						}
					});
			}
		}
		
		for (UPnPDevice d: device.getSubDevices()){
			
			handleDevice( d, update_if_found );
		}
	}
}