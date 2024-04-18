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

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;

import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.AESemaphore;
import org.gudy.azureus2.core3.util.AEThread2;
import org.gudy.azureus2.core3.util.AsyncDispatcher;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.IndentWriter;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.plugins.ipc.IPCInterface;

import com.aelitis.azureus.core.devices.*;
import com.aelitis.azureus.core.devices.DeviceManager.UnassociatedDevice;

public class 
DeviceiTunes
	extends DeviceMediaRendererImpl
	implements DeviceMediaRenderer
{
	private static final String UID = "a5d7869e-1ab9-6098-fef9-88476d988455";
	
	private static final Object	ERRROR_KEY_ITUNES = new Object();
	
	private static final int INSTALL_CHECK_PERIOD	= 60*1000;
	private static final int RUNNING_CHECK_PERIOD	= 30*1000;
	private static final int DEVICE_CHECK_PERIOD	= 10*1000;
	
	private static final int INSTALL_CHECK_TICKS	= INSTALL_CHECK_PERIOD / DeviceManagerImpl.DEVICE_UPDATE_PERIOD;
	private static final int RUNNING_CHECK_TICKS	= RUNNING_CHECK_PERIOD / DeviceManagerImpl.DEVICE_UPDATE_PERIOD;
	private static final int DEVICE_CHECK_TICKS		= DEVICE_CHECK_PERIOD / DeviceManagerImpl.DEVICE_UPDATE_PERIOD;
	
	private static final Object	COPY_ERROR_KEY = new Object();
	
	private PluginInterface		itunes;
	
	private volatile boolean				is_installed;
	private volatile boolean				is_running;
	
	private boolean				copy_outstanding;
	private boolean				copy_outstanding_set;
	private AEThread2			copy_thread;
	private AESemaphore			copy_sem = new AESemaphore( "Device:copy" );
	private AsyncDispatcher		async_dispatcher = new AsyncDispatcher( 5000 );
	
	private long				last_update_fail;
	private int					consec_fails;
	
	protected
	DeviceiTunes(
		DeviceManagerImpl	_manager,
		PluginInterface		_itunes )
	{
		super( _manager, UID, "iTunes", true );
		
		itunes	= _itunes;
	}

	protected
	DeviceiTunes(
		DeviceManagerImpl	_manager,
		Map					_map )
	
		throws IOException
	{
		super( _manager, _map );
	}
	
	protected boolean
	updateFrom(
		DeviceImpl		_other,
		boolean			_is_alive )
	{
		if ( !super.updateFrom( _other, _is_alive )){
			
			return( false );
		}
		
		if ( !( _other instanceof DeviceiTunes )){
			
			Debug.out( "Inconsistent" );
			
			return( false );
		}
		
		DeviceiTunes other = (DeviceiTunes)_other;
		
		itunes = other.itunes;
		
		return( true );
	}
	
	protected void
	initialise()
	{
		super.initialise();
		
		if ( getPersistentBooleanProperty( PP_COPY_OUTSTANDING, false )){
		
			setCopyOutstanding();
		}
		
		addListener( 
			new TranscodeTargetListener()
			{
				public void
				fileAdded(
					TranscodeFile		file )
				{
					if ( file.isComplete() && !file.isCopiedToDevice()){
						
						setCopyOutstanding();
					}
				}
				
				public void
				fileChanged(
					TranscodeFile		file,
					int					type,
					Object				data )
				{
					if ( file.isComplete() && !file.isCopiedToDevice()){
						
						setCopyOutstanding();
					}
				}
				
				public void
				fileRemoved(
					TranscodeFile		file )
				{
					copy_sem.release();
				}
			});
	}
	
	protected String
	getDeviceClassification()
	{
		return( "apple." );
	}
	
	public int
	getRendererSpecies()
	{
		return( RS_ITUNES );
	}
	
	public InetAddress
	getAddress()
	{
		return( null );
	}
	
	public boolean
	canRemove()
	{
			// no user-initiated removal, they need to uninstall the plugin
		
		return( false );
	}
	
	public boolean 
	isLivenessDetectable() 
	{
		return( true );
	}
	
	@Override
	public URL
	getWikiURL()
	{
		try{
			return( new URL( MessageText.getString( "device.wiki.itunes" )) );
			
		}catch( Throwable e ){
			
			Debug.out( e );
			
			return( null );
		}
	}
	
	protected void
	destroy()
	{
		super.destroy();
	}
	
	protected void
	updateStatus(
		int		tick_count )
	{
		super.updateStatus( tick_count );
		
		updateStatusSupport( tick_count );
		
		if ( is_installed && is_running ){
			
			alive();
			
		}else{
			
			dead();
		}
	}
	
	protected void
	updateStatusSupport(
		int		tick_count )
	{
		if ( itunes == null ){
			
			return;
		}
		
		if ( !is_installed ){
			
			if ( tick_count % INSTALL_CHECK_TICKS == 0 ){
				
				updateiTunesStatus();
				
				return;
			}
		}
		
		if ( !is_running ){
			
			if ( tick_count % RUNNING_CHECK_TICKS == 0 ){
				
				updateiTunesStatus();
				
				return;
			}
		}
		
		if ( tick_count % DEVICE_CHECK_TICKS == 0 ){

			updateiTunesStatus();
		}
	}
	
	protected void
	updateiTunesStatus()
	{	
		if ( getManager().isClosing()){
			
			return;
		}
		
		IPCInterface	ipc = itunes.getIPC();
		
		try{
			Map<String,Object> properties = (Map<String,Object>)ipc.invoke( "getProperties", new Object[]{} );

			is_installed = (Boolean)properties.get( "installed" );
			
			boolean	was_running = is_running;
			
			is_running	 = (Boolean)properties.get( "running" );
			
			if ( is_running && !was_running ){
				
				copy_sem.release();
			}
			
			if ( !( is_installed || is_running )){
				
				last_update_fail = 0;
			}
			
			String	info = null;
			
			if ( getCopyToDevicePending() > 0 ){
				
				if ( !is_installed ){
					
					info = MessageText.getString( "device.itunes.install" );
					
				}else if ( !is_running ){
					
					if ( !getAutoStartDevice()){
					
						info = MessageText.getString( "device.itunes.start" );
					}
				}
			}
				
			setInfo( ERRROR_KEY_ITUNES, info );
			
			Throwable error = (Throwable)properties.get( "error" );
			
			if ( error != null ){
				
				throw( error );
			}
			
			/*
			List<Map<String,Object>> sources = (List<Map<String,Object>>)properties.get( "sources" );
			
			if ( sources != null ){
				
				for ( Map<String,Object> source: sources ){
					
					System.out.println( source );
				}
			}
			*/
			
			last_update_fail 	= 0;
			consec_fails		= 0;
			
			setError( ERRROR_KEY_ITUNES, null );
			
		}catch( Throwable e ){
			
			long	now = SystemTime.getMonotonousTime();
			
			consec_fails++;
			
			if ( last_update_fail == 0 ){
				
				last_update_fail = now;
				
			}else if ( now - last_update_fail > 60*1000 && consec_fails >= 3 ){
							
				setError( ERRROR_KEY_ITUNES, MessageText.getString( "device.itunes.install_problem" ));
			}
			
			log( "iTunes IPC failed", e );
		}
	}
	
	public boolean
	canCopyToDevice()
	{
		return( true );
	}
	
	public int
	getCopyToDevicePending()
	{
		synchronized( this ){
		
			if ( !copy_outstanding ){
				
				return( 0 );
			}
		}

		TranscodeFileImpl[] files = getFiles();
		
		int result = 0;
			
		for ( TranscodeFileImpl file: files ){

			if ( file.isComplete() && !file.isCopiedToDevice()){
				
				result++;
			}
		}
		
		return( result );
	}
	
	protected void
	setCopyOutstanding()
	{
		synchronized( this ){
			
			copy_outstanding_set = true;
			
			if ( copy_thread == null ){
				
				copy_thread = 
					new AEThread2( "Device:copier", true )
					{
						public void
						run()
						{
							performCopy();
						}
					};
									
				copy_thread.start();
			}
			
			copy_sem.release();
		}
	}
	
	public boolean
	canAutoStartDevice()
	{
		return( true );
	}
	
	public boolean
	getAutoStartDevice()
	{
		return( getPersistentBooleanProperty( PP_AUTO_START, PR_AUTO_START_DEFAULT ));
	}
	
	public void
	setAutoStartDevice(
		boolean		auto )
	{
		setPersistentBooleanProperty( PP_AUTO_START, auto );
		
		if ( auto ){
			
			copy_sem.release();
		}
	}
	
	public boolean
	canAssociate()
	{
		return( false );
	}
	
	public boolean
	canRestrictAccess()
	{
		return( false );
	}
	
	public void
	associate(
		UnassociatedDevice	assoc )
	{
	}
	
	protected void
	performCopy()
	{
		synchronized( this ){

			copy_outstanding = true;
		
			async_dispatcher.dispatch(
				new AERunnable()
				{
					public void
					runSupport()
					{
						setPersistentBooleanProperty( PP_COPY_OUTSTANDING, true );
					}
				});
		}
		
		while( true ){
			
			if ( copy_sem.reserve( 60*1000 )){
				
				while( copy_sem.reserveIfAvailable());
			}
						
			boolean	auto_start = getAutoStartDevice();
			
			synchronized( this ){

				if ( itunes == null || ( !is_running && !( auto_start && is_installed ))){
					
					if ( !( copy_outstanding || copy_outstanding_set )){
						
						copy_thread = null;
						
						break;
					}
					
					continue;
				}

				copy_outstanding_set = false;
			}
						
			TranscodeFileImpl[] files = getFiles();
				
			List<TranscodeFileImpl>	to_copy = new ArrayList<TranscodeFileImpl>();
				
			boolean	borked_exist = false;
			
			for ( TranscodeFileImpl file: files ){
					
				if ( file.isComplete() && !file.isCopiedToDevice()){
					
					if ( file.getCopyToDeviceFails() < 3 ){
					
						to_copy.add( file );
						
					}else{
						
						borked_exist = true;
					}
				}
			}
				
			if ( borked_exist ){
				
				setError( COPY_ERROR_KEY, MessageText.getString( "device.error.copyfail2") );
			}
			
			synchronized( this ){

				if ( to_copy.size() == 0 && !copy_outstanding_set && !borked_exist ){
						
					copy_outstanding = false;
					
					async_dispatcher.dispatch(
						new AERunnable()
						{
							public void
							runSupport()
							{
								setError( COPY_ERROR_KEY, null );

								setPersistentBooleanProperty( PP_COPY_OUTSTANDING, false );
							}
						});
					
					copy_thread = null;
					
					break;
				}
			}
			
			for ( TranscodeFileImpl transcode_file: to_copy ){
				
				try{
					File	file = transcode_file.getTargetFile().getFile();
					
					try{
						IPCInterface	ipc = itunes.getIPC();
						
						if ( !is_running ){
							
							log( "Auto-starting iTunes" );
						}

						Map<String,Object> result = (Map<String,Object>)ipc.invoke( "addFileToLibrary", new Object[]{ file } );
		
						Throwable error = (Throwable)result.get( "error" );
						
						if ( error != null ){
							
							throw( error );
						}
						
						is_running = true;
						
						log( "Added file '" + file + ": " + result );
						
						transcode_file.setCopiedToDevice( true );
						
					}catch( Throwable e ){
						
						transcode_file.setCopyToDeviceFailed();
						
						log( "Failed to copy file " + file, e );
					}
				}catch( TranscodeException e ){

					// file has been deleted
				}
			}
		}
	}
	
	public boolean 
	isBrowsable()
	{
		return( false );
	}
	
	public browseLocation[] 
	getBrowseLocations() 
	{
		return null;
	}
	
	protected void
	getDisplayProperties(
		List<String[]>	dp )
	{
		super.getDisplayProperties( dp );
		
		if ( itunes == null ){
			
			addDP( dp, "devices.comp.missing", "<null>" );

		}else{
			
			updateiTunesStatus();
			
			addDP( dp, "devices.installed", is_installed );
				
			addDP( dp, "MyTrackerView.status.started", is_running );
			
			addDP( dp, "devices.copy.pending", copy_outstanding );
			
			addDP( dp, "devices.auto.start", getAutoStartDevice());
		}
	}
	
	public String
	getStatus()
	{
		if ( is_running ){
			
			return( MessageText.getString( "device.itunes.status.running" ));
			
		}else if ( is_installed ){
			
			return( MessageText.getString( "device.itunes.status.notrunning" ));

		}else{
			
			return( MessageText.getString( "device.itunes.status.notinstalled" ));
		}     
	}
	
	public void
	generate(
		IndentWriter		writer )
	{
		super.generate( writer );
		
		try{
			writer.indent();
	
			writer.println( "itunes=" + itunes + ", installed=" + is_installed + ", running=" + is_running + ", auto_start=" + getAutoStartDevice());
			writer.println( "copy_os=" + copy_outstanding + ", last_fail=" + new SimpleDateFormat().format( new Date( last_update_fail )));
			
		}finally{
			
			writer.exdent();
		}
	}
}
