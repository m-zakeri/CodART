/*
 * Created on Aug 14, 2012
 * Created by Paul Gardner
 * 
 * Copyright 2012 Vuze, Inc.  All rights reserved.
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


package com.aelitis.azureus.core.pairing.impl.swt;

import java.net.InetAddress;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.eclipse.swt.graphics.Image;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.SimpleTimer;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.core3.util.TimeFormatter;
import org.gudy.azureus2.core3.util.TimerEvent;
import org.gudy.azureus2.core3.util.TimerEventPerformer;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.ui.UIInstance;
import org.gudy.azureus2.plugins.ui.UIManagerListener;
import org.gudy.azureus2.plugins.ui.config.BooleanParameter;
import org.gudy.azureus2.plugins.ui.config.Parameter;
import org.gudy.azureus2.plugins.ui.config.ParameterListener;
import org.gudy.azureus2.plugins.ui.menus.MenuItem;
import org.gudy.azureus2.plugins.ui.menus.MenuItemListener;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.plugins.UISWTInstance;
import org.gudy.azureus2.ui.swt.plugins.UISWTStatusEntry;
import org.gudy.azureus2.ui.swt.plugins.UISWTStatusEntryListener;

import com.aelitis.azureus.core.networkmanager.admin.NetworkAdmin;
import com.aelitis.azureus.core.networkmanager.admin.NetworkAdminNetworkInterface;
import com.aelitis.azureus.core.networkmanager.admin.NetworkAdminNetworkInterfaceAddress;
import com.aelitis.azureus.core.networkmanager.admin.NetworkAdminPropertyChangeListener;
import com.aelitis.azureus.core.util.AZ3Functions;
import com.aelitis.azureus.ui.UIFunctions;
import com.aelitis.azureus.ui.UIFunctionsManager;
import com.aelitis.azureus.ui.common.updater.UIUpdater;
import com.aelitis.azureus.ui.swt.imageloader.ImageLoader;

public class 
PMSWTImpl 
{
	private UISWTStatusEntry 	status;
	
	private volatile Set<String>	local_addresses = new HashSet<String>();
	
	private Image	icon_idle;
	private Image	icon_green;
	private Image	icon_red;
	
	private int		last_update_count;
	private Image	last_image;
	private String	last_tooltip_text	= "";
	
	private long	last_image_expiry_mono;
	private long	last_image_expiry_uc_min;
	
	public void
	initialise(
		final PluginInterface			pi,
		final BooleanParameter			icon_enable )
	{
		final NetworkAdmin na = NetworkAdmin.getSingleton();
		
		na.addPropertyChangeListener(
			new NetworkAdminPropertyChangeListener()
			{
				public void 
				propertyChanged(
					String property) 
				{
					if ( property == NetworkAdmin.PR_NETWORK_INTERFACES ){
						
						updateLocalAddresses( na );
					}
				}
			});
		
		updateLocalAddresses( na );
		
		pi.getUIManager().addUIListener(
				new UIManagerListener()
				{
					public void
					UIAttached(
						final UIInstance		instance )
					{
						if ( instance instanceof UISWTInstance ){
							
							UIFunctions uif = UIFunctionsManager.getUIFunctions();
							
							if ( uif != null ){
								
								uif.getUIUpdater().addListener(
									new UIUpdater.UIUpdaterListener()
									{
										public void 
										updateComplete(
											int count )
										{
											last_update_count	= count;
											
											updateStatus( true );
										}
									});
							}
							
							Utils.execSWTThread(
								new AERunnable() 
								{
									public void 
									runSupport() 
									{
										ImageLoader imageLoader = ImageLoader.getInstance();
	
										icon_idle 	= imageLoader.getImage( "pair_sb_idle" );
										icon_green 	= imageLoader.getImage( "pair_sb_green" );
										icon_red	= imageLoader.getImage( "pair_sb_red" );
				
										UISWTInstance	ui_instance = (UISWTInstance)instance;
										
										status	= ui_instance.createStatusEntry();
											
										last_tooltip_text = MessageText.getString( "pairing.ui.icon.tip" );
										
										status.setTooltipText( last_tooltip_text );
										
										status.setImageEnabled( true );
										
										status.setImage( icon_idle );
										
										last_image	= icon_idle;
										
										boolean	is_visible = icon_enable.getValue();
										
										status.setVisible( is_visible );
										
										if ( is_visible ){
											
											updateStatus( false );
										}
										
										final MenuItem mi_show =
											pi.getUIManager().getMenuManager().addMenuItem(
																status.getMenuContext(),
																"pairing.ui.icon.show" );
										
										mi_show.setStyle( MenuItem.STYLE_CHECK );
										mi_show.setData( new Boolean( is_visible ));
										
										mi_show.addListener(
												new MenuItemListener()
												{
													public void
													selected(
														MenuItem			menu,
														Object 				target )
													{
														icon_enable.setValue( false );
													}
												});
										
										icon_enable.addListener(
												new ParameterListener()
												{
													public void 
													parameterChanged(
														Parameter param )
													{
														boolean is_visible = icon_enable.getValue();
														
														status.setVisible( is_visible );
														
														mi_show.setData( new Boolean( is_visible ));
														
														if ( is_visible ){
															
															updateStatus( false );
														}
													}
												});
											
			
										final AZ3Functions.provider az3 = AZ3Functions.getProvider();

										if ( az3 != null ){
											
											MenuItem mi_pairing =
												pi.getUIManager().getMenuManager().addMenuItem(
																	status.getMenuContext(),
																	"MainWindow.menu.pairing" );
				
											mi_pairing.addListener(
												new MenuItemListener()
												{
													public void
													selected(
														MenuItem			menu,
														Object 				target )
													{
														az3.openRemotePairingWindow();
													}
												});
										}
										
										MenuItem mi_sep =
											pi.getUIManager().getMenuManager().addMenuItem(
																status.getMenuContext(),
																"" );
			
										mi_sep.setStyle( MenuItem.STYLE_SEPARATOR );
										
										MenuItem mi_options =
											pi.getUIManager().getMenuManager().addMenuItem(
																status.getMenuContext(),
																"MainWindow.menu.view.configuration" );
			
										mi_options.addListener(
											new MenuItemListener()
											{
												public void
												selected(
													MenuItem			menu,
													Object 				target )
												{
													UIFunctions uif = UIFunctionsManager.getUIFunctions();
			
													if ( uif != null ){
			
														uif.openView( UIFunctions.VIEW_CONFIG, "Pairing" );
													}
												}
											});
										
										
										UISWTStatusEntryListener click_listener = 
											new UISWTStatusEntryListener()
										{
												public void 
												entryClicked(
													UISWTStatusEntry entry )
												{
													UIFunctions uif = UIFunctionsManager.getUIFunctions();
													
													if ( uif != null ){
			
														uif.openView( UIFunctions.VIEW_CONFIG, "Pairing" );
													}
												}
											};
											
										status.setListener( click_listener );
									}
								});
						}
								
					}
					
					public void
					UIDetached(
						UIInstance		instance )
					{
						
					}
				});
	}
	
	private void
	updateLocalAddresses(
		NetworkAdmin		network_admin )
	{
		NetworkAdminNetworkInterface[] interfaces = network_admin.getInterfaces();
						
		Set<String>	ias = new HashSet<String>();
		
		for ( NetworkAdminNetworkInterface intf: interfaces ){
			
			NetworkAdminNetworkInterfaceAddress[] addresses = intf.getAddresses();
			
			for ( NetworkAdminNetworkInterfaceAddress address: addresses ){
				
				InetAddress ia = address.getAddress();
				
				ias.add( ia.getHostAddress());
			}
		}
		
		local_addresses = ias;
	}
	
	private Map<String,RemoteHistory>	history_map	= new HashMap<String, RemoteHistory>();
		
	public void
	recordRequest(
		final String		name,
		final String		ip,
		final boolean		good )
	{	
		Utils.execSWTThread(
			new AERunnable() 
			{
				public void 
				runSupport() 
				{						
					RemoteHistory entry = history_map.get( name );
						
					if ( entry == null ){
							
						entry = new RemoteHistory();
							
						history_map.put( name, entry );
					}
						
					entry.addRequest( ip, good );
					
					updateStatus( false );
				}
			});
	}
	
	private void
	updateStatus(
		boolean		update_completed )
	{
		final int RECORD_EXPIRY		= 60*60*1000;
		final int GOOD_EXPIRY		= 1*1000;
		final int BAD_EXPIRY		= 5*60*1000;
		final int MAX_IPS_PER_TYPE	= 10;
		final int MAX_TYPES			= 10;
	
		if ( status == null ){
			
			return;
		}
		
		long	now_mono = SystemTime.getMonotonousTime();
		
		if ( update_completed ){
		
			if ( last_image != icon_idle && last_update_count >= last_image_expiry_uc_min ){
				
				if ( now_mono >= last_image_expiry_mono ){
					
					last_image = icon_idle;
										
					status.setImage( icon_idle );
				}
			}
		}
			
		StringBuffer	tooltip_text = new StringBuffer( 256 );
		
		tooltip_text.append( MessageText.getString( "pairing.ui.icon.tip" ));
			
		long newest_bad_mono	= -1;
		long newest_good_mono	= -1;

		Iterator<Map.Entry<String,RemoteHistory>>	it = history_map.entrySet().iterator();
		
		String	oldest_type			= null;
		long	oldest_type_mono	= Long.MAX_VALUE;
		
		int	records_added = 0;
		
		while( it.hasNext()){
			
			Map.Entry<String,RemoteHistory> entry = it.next();
			
			String			name 	= entry.getKey();
			RemoteHistory	history = entry.getValue();
			
			String	oldest_ip		= null;
			long	oldest_ip_mono	= Long.MAX_VALUE;
							
			Map<String,RemoteHistoryEntry> records = history.getEntries();
			
			Iterator<Map.Entry<String,RemoteHistoryEntry>>	record_it = records.entrySet().iterator();
			
			StringBuffer	tt_ip_details = new StringBuffer( 256 );
			
			while( record_it.hasNext()){
				
				Map.Entry<String,RemoteHistoryEntry>	record = record_it.next();
				
				String				ip 	= record.getKey();
				RemoteHistoryEntry 	e 	= record.getValue();
				
				long e_mono = e.getLastReceivedMono();
				
				if ( e_mono < oldest_ip_mono ){
					
					oldest_ip_mono 	= e_mono;
					oldest_ip		= ip;
				}
				
				long age = now_mono - e_mono;
				
				if ( age > RECORD_EXPIRY ){
					
					record_it.remove();
					
				}else{
					
					String age_str = TimeFormatter.format( age/1000 );
					
					tt_ip_details.append( "\n        " );
					
					if ( local_addresses.contains( ip )){
						
						tt_ip_details.append( MessageText.getString( "DHTView.db.local" ) + " (" + ip + ")" );
						
					}else{
						
						tt_ip_details.append( ip );
					}
					
					if ( e.wasLastGood()){
						
						tt_ip_details.append( " OK" );
						
						newest_good_mono 	= Math.max( newest_good_mono, e_mono );
						
					}else{
						
						tt_ip_details.append( " " + MessageText.getString( "label.access.denied" ));
						
						newest_bad_mono 	= Math.max( newest_bad_mono, e_mono );
					}
					
					tt_ip_details.append( " - " + age_str + " ago");
				}
			}
			
			if ( records.size() == 0 ){
				
				it.remove();
				
			}else{
				
				if ( oldest_ip_mono < oldest_type_mono ){
					
					oldest_type_mono 	= oldest_ip_mono;
					oldest_type			= name;
				}
			
				if ( records.size() >= MAX_IPS_PER_TYPE ){
					
					records.remove( oldest_ip );
					
				}else{
					
					tooltip_text.append( "\n    " + name );
					tooltip_text.append( tt_ip_details );
					
					records_added++;
				}
			}
		}
		
		if ( history_map.size() > MAX_TYPES ){
			
			history_map.remove( oldest_type );
		}
		
		if ( records_added == 0 ){
			
			tooltip_text.append( "\n    " + MessageText.getString( "pairing.ui.icon.tip.no.recent" ));
		}
		
		if ( !tooltip_text.equals( last_tooltip_text )){
			
			last_tooltip_text = tooltip_text.toString();
			
			status.setTooltipText( last_tooltip_text );
		}
		
		Image	target_image = null;
		
		long	age_newest_bad = now_mono - newest_bad_mono;
	
		if ( newest_bad_mono >= 0 && age_newest_bad <= BAD_EXPIRY ){
			
			target_image = icon_red;
			
			last_image_expiry_mono 		= newest_bad_mono + BAD_EXPIRY;
		}else{
			
			long	age_newest_good = now_mono - newest_good_mono;

			if ( newest_good_mono >= 0 && age_newest_good <= GOOD_EXPIRY ){
				
				target_image = icon_green;
				
				last_image_expiry_mono 		= age_newest_good + GOOD_EXPIRY;
			}
		}
		
		if ( target_image != null && target_image != last_image ){
			
			last_image = target_image;
			
			last_image_expiry_uc_min	= last_update_count + 2;
			
			status.setImage( target_image );
		}
	}
	
	private static class
	RemoteHistory
	{
		private Map<String,RemoteHistoryEntry>	map = new HashMap<String, RemoteHistoryEntry>();
			
		private void
		addRequest(
			String		ip,
			boolean		good )
		{
			RemoteHistoryEntry entry = map.get( ip );
			
			if ( entry == null ){
				
				entry = new RemoteHistoryEntry();
				
				map.put( ip, entry );
			}
			
			entry.update( good );
		}
		
		private Map<String,RemoteHistoryEntry>
		getEntries()
		{
			return( map );
		}
	}
	
	private static class
	RemoteHistoryEntry
	{
		private long		last_received_mono;
		private long		last_received_rtc;
		
		private int			request_count;
		private boolean		last_was_good;
		
		private long
		getLastReceivedMono()
		{
			return( last_received_mono );
		}
		
		private long
		getLastReceivedRTC()
		{
			return( last_received_rtc );
		}
		
		private int
		getRequestCount()
		{
			return( request_count );
		}
		
		private boolean
		wasLastGood()
		{
			return( last_was_good );
		}
		
		private void
		update(
			boolean	good )
		{
			last_received_mono	= SystemTime.getMonotonousTime();
			last_received_rtc	= SystemTime.getCurrentTime();
			
			request_count++;
			
			last_was_good	= good;
		}
	}
}
