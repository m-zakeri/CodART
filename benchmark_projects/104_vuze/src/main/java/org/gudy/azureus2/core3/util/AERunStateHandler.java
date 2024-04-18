/*
 * Created on Sep 18, 2012
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


package org.gudy.azureus2.core3.util;

import java.util.Iterator;

import org.gudy.azureus2.core3.config.COConfigurationManager;

import com.aelitis.azureus.core.util.CopyOnWriteList;

public class 
AERunStateHandler 
{
	public static final long		RS_DELAYED_UI			= 0x00000001;
	public static final long		RS_UDP_NET_ONLY			= 0x00000002;
	public static final long		RS_DHT_SLEEPING			= 0x00000004;
	
	public static final long		RS_ALL_ACTIVE			= 0x00000000;
	public static final long		RS_ALL_LOW				= 0xffffffff;
	
	private static boolean	start_low = COConfigurationManager.getBooleanParameter( "Start In Low Resource Mode" );
	
	private static long	current_mode = start_low?RS_ALL_LOW:RS_ALL_ACTIVE;
	
	private static AsyncDispatcher	dispatcher = new AsyncDispatcher(2500);
	
	private static CopyOnWriteList<RunStateChangeListener>	listeners = new CopyOnWriteList<RunStateChangeListener>();
	
	public static boolean
	isDelayedUI()
	{
		return( ( current_mode & RS_DELAYED_UI ) != 0 );
	}
	
	public static boolean
	isUDPNetworkOnly()
	{
		return( ( current_mode & RS_UDP_NET_ONLY ) != 0 );
	}
	
	public static boolean
	isDHTSleeping()
	{
		return( ( current_mode & RS_DHT_SLEEPING ) != 0 );
	}
	
	public static long
	getResourceMode()
	{
		return( current_mode );
	}
	
	public static void
	setResourceMode(
		final long		new_mode )
	{
		synchronized( dispatcher ){
			
			if ( new_mode == current_mode ){
				
				return;
			}
		
			current_mode = new_mode;
			
			final Iterator<RunStateChangeListener> it = listeners.iterator();
			
			dispatcher.dispatch(
				new AERunnable()
				{
					public void
					runSupport()
					{
						while( it.hasNext()){
							
							try{								
								it.next().runStateChanged( new_mode );
								
							}catch( Throwable e ){
								
								Debug.out( e );
							}
						}
						
					}
				});
		}
	}
	
	public static void
	addListener(
		final RunStateChangeListener	l,
		boolean							fire_now )
	{
		synchronized( dispatcher ){

			listeners.add( l );
			
			if ( fire_now ){
				
				dispatcher.dispatch(
					new AERunnable()
					{
						public void
						runSupport()
						{
							try{
								l.runStateChanged( current_mode );

							}catch( Throwable e ){
								
								Debug.out( e );
							}
						}
					});
			}
		}
	}
	
	public static void
	removeListener(
		RunStateChangeListener	l )
	{
		synchronized( dispatcher ){

			listeners.remove( l );
		}
	}
	
	public interface
	RunStateChangeListener
	{
		public void
		runStateChanged(
			long		run_state );
	}
}
