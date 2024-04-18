/*
 * Created on Jan 28, 2009
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

import java.io.IOException;
import java.io.InputStream;
import java.net.InetAddress;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.IndentWriter;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.plugins.disk.DiskManagerFileInfo;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.download.DownloadAttributeListener;
import org.gudy.azureus2.plugins.download.DownloadManager;
import org.gudy.azureus2.plugins.download.DownloadManagerListener;
import org.gudy.azureus2.plugins.ipc.IPCInterface;
import org.gudy.azureus2.plugins.torrent.Torrent;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;
import org.gudy.azureus2.plugins.torrent.TorrentAttribute;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.AzureusCoreRunningListener;
import com.aelitis.azureus.core.AzureusCoreFactory;
import com.aelitis.azureus.core.content.AzureusContentDownload;
import com.aelitis.azureus.core.content.AzureusContentFile;
import com.aelitis.azureus.core.content.AzureusPlatformContentDirectory;
import com.aelitis.azureus.core.devices.TranscodeException;
import com.aelitis.azureus.core.devices.TranscodeFile;
import com.aelitis.azureus.core.devices.TranscodeJob;
import com.aelitis.azureus.core.devices.TranscodeProfile;
import com.aelitis.azureus.core.devices.TranscodeTarget;
import com.aelitis.azureus.core.devices.TranscodeTargetListener;
import com.aelitis.azureus.core.devices.DeviceManager.UnassociatedDevice;
import com.aelitis.azureus.core.download.DiskManagerFileInfoStream;
import com.aelitis.azureus.core.torrent.PlatformTorrentUtils;
import com.aelitis.azureus.core.util.UUIDGenerator;
import com.aelitis.azureus.util.PlayUtils;
import com.aelitis.net.upnp.UPnPDevice;
import com.aelitis.net.upnp.UPnPDeviceImage;
import com.aelitis.net.upnp.UPnPRootDevice;

public abstract class 
DeviceUPnPImpl
	extends DeviceImpl
	implements TranscodeTargetListener, DownloadManagerListener
{
	private static final Object UPNPAV_FILE_KEY = new Object();
		
	private static final Map<String,AzureusContentFile>	acf_map = new WeakHashMap<String,AzureusContentFile>();
	
	protected static String
	getDisplayName(
		UPnPDevice		device )
	{
		UPnPDevice	root = device.getRootDevice().getDevice();
		
		String fn = root.getFriendlyName();
		
		if ( fn == null || fn.length() == 0 ){
			
			fn = device.getFriendlyName();
		}
		
		String	dn = root.getModelName();
		
		if ( dn == null || dn.length() == 0 ){
		
			dn = device.getModelName();
		}
		
		if ( dn != null && dn.length() > 0 ){
			
			if ( !fn.contains( dn ) && ( !dn.contains( "Azureus" ) || dn.contains( "Vuze" ))){
			
				fn += " (" + dn + ")";
			}
		}
		
		return( fn );
	}
	
	private final String MY_ACF_KEY;

	
	private final DeviceManagerUPnPImpl	upnp_manager;
	private volatile UPnPDevice		device_may_be_null;
	
	private IPCInterface		upnpav_ipc;
	private TranscodeProfile	dynamic_transcode_profile;
	private Map<String,AzureusContentFile>	dynamic_xcode_map;
	
	
	protected
	DeviceUPnPImpl(
		DeviceManagerImpl		_manager,
		UPnPDevice				_device,
		int						_type )
	{
		super( _manager, _type, _type + "/" + _device.getRootDevice().getUSN(), getDisplayName( _device ), false );
		
		upnp_manager		= _manager.getUPnPManager();
		setUPnPDevice(_device);
		
		MY_ACF_KEY = getACFKey();
	}	
	
	protected
	DeviceUPnPImpl(
		DeviceManagerImpl	_manager,
		int					_type,
		String				_classification )

	{
		super( _manager, _type, UUIDGenerator.generateUUIDString(), _classification, true );
		
		upnp_manager		= _manager.getUPnPManager();
		
		MY_ACF_KEY = getACFKey();
	}
	
	protected
	DeviceUPnPImpl(
		DeviceManagerImpl	_manager,
		int					_type,
		String				_uuid,
		String				_classification,
		boolean				_manual,
		String				_name )

	{
		super( _manager, _type, _uuid==null?UUIDGenerator.generateUUIDString():_uuid, _classification, _manual, _name );
		
		upnp_manager		= _manager.getUPnPManager();
		
		MY_ACF_KEY = getACFKey();
	}
	
	protected
	DeviceUPnPImpl(
		DeviceManagerImpl	_manager,
		int					_type,
		String				_uuid,
		String				_classification,
		boolean				_manual )

	{
		super( _manager, _type, _uuid, _classification, _manual );
		
		upnp_manager		= _manager.getUPnPManager();
		
		MY_ACF_KEY = getACFKey();
	}
	
	protected
	DeviceUPnPImpl(
		DeviceManagerImpl	_manager,
		Map					_map )
	
		throws IOException
	{
		super(_manager, _map );
		
		upnp_manager		= _manager.getUPnPManager();
		
		MY_ACF_KEY = getACFKey();
	}
	
	protected String
	getACFKey()
	{
		return( "DeviceUPnPImpl:device:" + getID());
	}
	
	@Override
	protected boolean
	updateFrom(
		DeviceImpl		_other,
		boolean			_is_alive )
	{
		if ( !super.updateFrom( _other, _is_alive )){
			
			return( false );
		}
		
		if ( !( _other instanceof DeviceUPnPImpl )){
			
			Debug.out( "Inconsistent" );
			
			return( false );
		}
		
		DeviceUPnPImpl other = (DeviceUPnPImpl)_other;
		
		setUPnPDevice(other.device_may_be_null);
		
		return( true );
	}
	
	@Override
	protected void
	initialise()
	{
		super.initialise();
	}
	
	protected void
	UPnPInitialised()
	{
	}
	
	@Override
	protected void
	destroy()
	{
		super.destroy();
	}
	
	protected DeviceManagerUPnPImpl
	getUPnPDeviceManager()
	{
		return( upnp_manager );
	}
	
	protected UPnPDevice
	getUPnPDevice()
	{
		return( device_may_be_null );
	}
	
	protected void
	setUPnPDevice(
			UPnPDevice device)
	{
		device_may_be_null = device;
		if (device != null) {
			// triggers any address change logic
			setAddress(getAddress());
		}
	}
	
	public boolean
	isBrowsable()
	{
		return( true );
	}
	
	public browseLocation[]
	getBrowseLocations()
	{
		List<browseLocation>	locs = new ArrayList<browseLocation>();
	
		UPnPDevice device = device_may_be_null;
		
		if ( device != null ){
			
			URL		presentation = getPresentationURL( device );

			if ( presentation != null ){
					
				locs.add( new browseLocationImpl( "device.upnp.present_url", presentation ));
			}
			
			int userMode = COConfigurationManager.getIntParameter("User Mode");
			
			if ( userMode > 1 ){
			
				locs.add( new browseLocationImpl( "device.upnp.desc_url", device.getRootDevice().getLocation()));
			}
		}
		
		return( locs.toArray( new browseLocation[ locs.size() ]));
	}
	
	public boolean
	canFilterFilesView()
	{
		return( true );
	}
	
	public void
	setFilterFilesView(
		boolean	filter )
	{
		boolean	existing = getFilterFilesView();
		
		if ( existing != filter ){
		
			setPersistentBooleanProperty( PP_FILTER_FILES, filter );
		
			IPCInterface ipc = upnpav_ipc;
			
			if ( ipc != null ){
				
				try{
					ipc.invoke( "invalidateDirectory", new Object[]{});

				}catch( Throwable e ){
				}
			}
		}
	}
	
	public boolean
	getFilterFilesView()
	{
		return( getPersistentBooleanProperty( PP_FILTER_FILES, true ));
	}
	
	public boolean
	isLivenessDetectable()
	{
		return( true );
	}
	
	protected URL
	getLocation()
	{
		UPnPDevice device = device_may_be_null;
		
		if ( device != null ){
			
			UPnPRootDevice root = device.getRootDevice();
			
			return( root.getLocation());
		}
		
		return( null );
	}
	
	public boolean
	canAssociate()
	{
		return( true );
	}
	
	public void
	associate(
		UnassociatedDevice	assoc )
	{
		if ( isAlive()){
			
			return;
		}
		
		setAddress( assoc.getAddress());
		
		alive();
	}
	
	public InetAddress
	getAddress()
	{
		try{

			UPnPDevice device = device_may_be_null;
	
			if ( device != null ){
				
				UPnPRootDevice root = device.getRootDevice();
				
				URL location = root.getLocation();
				
				return( InetAddress.getByName( location.getHost() ));
				
			}else{
				
				InetAddress address = (InetAddress)getTransientProperty( TP_IP_ADDRESS );
				
				if ( address != null ){
					
					return( address );
				}
				
				String last = getPersistentStringProperty( PP_IP_ADDRESS );
				
				if ( last != null && last.length() > 0 ){
					
					return( InetAddress.getByName( last ));
				}
			}
		}catch( Throwable e ){
			
			Debug.printStackTrace(e);
		
		}
		
		return( null );
	}
	
	public void
	setAddress(
		InetAddress	address )
	{
		setTransientProperty( TP_IP_ADDRESS, address );
		
		setPersistentStringProperty( PP_IP_ADDRESS, address.getHostAddress());
	}
	
	public boolean
	canRestrictAccess()
	{
		return( true );
	}
	
	public String
	getAccessRestriction()
	{
		return( getPersistentStringProperty( PP_RESTRICT_ACCESS, "" ));
	}
	
	public void
	setAccessRestriction(
		String		str )
	{
		setPersistentStringProperty( PP_RESTRICT_ACCESS, str );
	}
	
	protected URL
	getStreamURL(
		TranscodeFileImpl		file )
	{
		return( getStreamURL( file, null ));
	}
	
	protected URL
	getStreamURL(
		TranscodeFileImpl		file,
		String					host )
	{
		browseReceived();
		
		return( super.getStreamURL( file, host ));
	}
	
	protected String
	getMimeType(
		TranscodeFileImpl		file )
	{
		browseReceived();
		
		return( super.getMimeType(file));
	}
	
	protected void
	browseReceived()
	{
		IPCInterface ipc = upnp_manager.getUPnPAVIPC();
		
		if ( ipc == null ){
			
			return;
		}
		
		TranscodeProfile default_profile = getDefaultTranscodeProfile();
		
		if ( default_profile == null ){
			
			TranscodeProfile[] profiles = getTranscodeProfiles();
			
			for ( TranscodeProfile p: profiles ){
				
				if ( p.isStreamable()){
					
					default_profile = p;
					
					break;
				}
			}
		}
		
		synchronized( this ){
			
			if ( upnpav_ipc != null ){
				
				return;
			}
			
			upnpav_ipc = ipc;
			
			if ( default_profile != null && default_profile.isStreamable()){
				
				dynamic_transcode_profile	= default_profile;
			}
		}
		
		if ( dynamic_transcode_profile != null && this instanceof TranscodeTarget ){
			
			// In theory this is a plugin, so there should be a core..
			// However, check just in case
			AzureusCoreFactory.addCoreRunningListener(new AzureusCoreRunningListener() {
			
				public void azureusCoreRunning(AzureusCore core) {
					
					DownloadManager dm = PluginInitializer.getDefaultInterface().getDownloadManager();
					
					dm.addListener( DeviceUPnPImpl.this, true );
				}
			});
		}
				
		addListener( this );

		TranscodeFile[]	transcode_files = getFiles();
		
		for ( TranscodeFile file: transcode_files ){
			
			fileAdded( file, false );
		}
	}
	
	protected void
	resetUPNPAV()
	{		
		Set<String>	to_remove = new HashSet<String>();
		
		synchronized( this ){
			
			if ( upnpav_ipc == null ){
				
				return;
			}
			
			upnpav_ipc = null;
			
			dynamic_transcode_profile = null;
			
			dynamic_xcode_map = null;
		 
			DownloadManager dm = PluginInitializer.getDefaultInterface().getDownloadManager();

			dm.removeListener( this );
			
			removeListener( this );
			
			TranscodeFileImpl[]	transcode_files = getFiles();
			
			for ( TranscodeFileImpl file: transcode_files ){

				file.setTransientProperty( UPNPAV_FILE_KEY, null );
				
				to_remove.add( file.getKey());
			}
		}
		
		synchronized( acf_map ){
			
			for (String key: to_remove ){
			
				acf_map.remove( key );
			}
		}
	}
	
	public void
	downloadAdded(
		Download	download )
	{
		Torrent torrent = download.getTorrent();
		
		if ( torrent != null && PlatformTorrentUtils.isContent( torrent, false )){
								
			addDynamicXCode( download.getDiskManagerFileInfo()[0]);
		}
	}
	
	public void
	downloadRemoved(
		Download	download )
	{
		Torrent torrent = download.getTorrent();
		
		if ( torrent != null && PlatformTorrentUtils.isContent( torrent, false )){
								
			removeDynamicXCode( download.getDiskManagerFileInfo()[0]);
		}
	}
		
	protected void
	addDynamicXCode(
		final DiskManagerFileInfo		source )
	{
		final TranscodeProfile profile = dynamic_transcode_profile;
		
		IPCInterface			ipc	= upnpav_ipc;
		
		if ( profile == null || ipc == null ){
			
			return;
		}
		
		try{
			TranscodeFileImpl transcode_file = allocateFile( profile, false, source, false );
			
			AzureusContentFile acf = (AzureusContentFile)transcode_file.getTransientProperty( UPNPAV_FILE_KEY );

			if ( acf != null ){
				
				return;
			}
			
			final String tf_key = transcode_file.getKey();

			synchronized( acf_map ){
				
				acf = acf_map.get( tf_key );
			}
			
			if ( acf != null ){
				
				return;
			}
			
			final DiskManagerFileInfo stream_file = 
				new DiskManagerFileInfoStream( 
					new DiskManagerFileInfoStream.StreamFactory()
					{
						private List<Object>	current_requests = new ArrayList<Object>();
						
						public StreamDetails 
						getStream(
							Object		request )
						
							throws IOException 
						{						
							try{
								TranscodeJobImpl job = getManager().getTranscodeManager().getQueue().add(
										(TranscodeTarget)DeviceUPnPImpl.this,
										profile, 
										source, 
										false,
										true,
										TranscodeTarget.TRANSCODE_UNKNOWN );
									
								synchronized( this ){
								
									current_requests.add( request );
								}
								
								while( true ){
									
									InputStream is = job.getStream( 1000 );
									
									if ( is != null ){
										
										return( new StreamWrapper( is, job ));
									}
									
									int	state = job.getState();
									
									if ( state == TranscodeJobImpl.ST_FAILED ){
										
										throw( new IOException( "Transcode failed: " + job.getError()));
										
									}else if ( state == TranscodeJobImpl.ST_CANCELLED ){
										
										throw( new IOException( "Transcode failed: job cancelled" ));
	
									}else if ( state == TranscodeJobImpl.ST_COMPLETE ){
										
										throw( new IOException( "Job complete but no stream!" ));
									}
									
									synchronized( this ){
										
										if ( !current_requests.contains( request )){
											
											break;
										}
									}
									
									System.out.println( "waiting for stream" );
									
								}
								
								IOException error = new IOException( "Stream request cancelled" );
								
								job.failed( error );
								
								throw( error );
								
							}catch( IOException e ){
								
								throw( e );
								
							}catch( Throwable e ){
								
								throw( new IOException( "Failed to add transcode job: " + Debug.getNestedExceptionMessage(e)));
								
							}finally{
								
								synchronized( this ){
								
									current_requests.remove( request );
								}
							}
						}
						
						public void 
						destroyed(
							Object request ) 
						{
							synchronized( this ){
								
								current_requests.remove( request );
							}
						}
					},
					transcode_file.getCacheFile());
										
			acf =	new AzureusContentFile()
					{	
					   	public DiskManagerFileInfo
					   	getFile()
					   	{
					   		return( stream_file );
					   	}
					   	
						public Object
						getProperty(
							String		name )
						{
								// TODO: duration etc

							if ( name.equals( MY_ACF_KEY )){
								
								return( new Object[]{ DeviceUPnPImpl.this, tf_key });
								
							}else if ( name.equals( PT_PERCENT_DONE )){
								
								return( new Long(1000));
								
							}else if ( name.equals( PT_ETA )){
								
								return( new Long(0));
							}
							
							return( null );
						}
					};
			
			synchronized( acf_map ){

				acf_map.put( tf_key, acf );
			}
					
			transcode_file.setTransientProperty( UPNPAV_FILE_KEY, acf );

			syncCategories( transcode_file, true );
					
			synchronized( this ){
				
				if ( dynamic_xcode_map == null ){
					
					dynamic_xcode_map = new HashMap<String,AzureusContentFile>();
				}
				
				dynamic_xcode_map.put( tf_key, acf );
			}
			
			ipc.invoke( "addContent", new Object[]{ acf });
			
		}catch( Throwable e ){
			
			Debug.out( e );
		}
	}
	
	protected void
	removeDynamicXCode(
		final DiskManagerFileInfo		source )
	{
		final TranscodeProfile profile = dynamic_transcode_profile;
		
		IPCInterface			ipc	= upnpav_ipc;
		
		if ( profile == null || ipc == null ){
			
			return;
		}
		
		try{
			TranscodeFileImpl transcode_file = lookupFile( profile, source );

				// if the file completed transcoding then we leave the result around for
				// the user to re-use
			
			if ( transcode_file != null && !transcode_file.isComplete()){
				
				AzureusContentFile acf = null;
				
				synchronized( this ){
	
					if ( dynamic_xcode_map != null ){
					
						acf = dynamic_xcode_map.get( transcode_file.getKey());
					}
				}
				
				transcode_file.delete( true );
				
				if ( acf != null ){
				
					ipc.invoke( "removeContent", new Object[]{ acf });
				}
				
				synchronized( acf_map ){
					
					acf_map.remove( transcode_file.getKey());
				}
			}
		}catch( Throwable e ){
			
			Debug.out( e );
		}
	}
	
	protected boolean
	setupStreamXCode(
		TranscodeFileImpl		transcode_file )
	{
		final TranscodeJobImpl	job = transcode_file.getJob();
		
		if ( job == null ){
			
				// may have just completed, say things are OK as caller can continue
			
			return( transcode_file.isComplete());
		}
		
		final String tf_key = transcode_file.getKey();

		AzureusContentFile	acf;
		
		synchronized( acf_map ){
			
			acf = acf_map.get( tf_key );
		}
		
		if ( acf != null ){
			
			return( true );
		}
		
		IPCInterface			ipc	= upnpav_ipc;

		if ( ipc == null ){
			
			return( false );
		}
		
		if ( transcode_file.getDurationMillis() == 0 ){
			
			return( false );
		}
		
		try{
			final DiskManagerFileInfo stream_file = 
				new TranscodeJobOutputLeecher( job, transcode_file );
										
			acf =	new AzureusContentFile()
					{	
					   	public DiskManagerFileInfo
					   	getFile()
					   	{
					   		return( stream_file );
					   	}
					   	
						public Object
						getProperty(
							String		name )
						{
								// TODO: duration etc
	
							if ( name.equals( MY_ACF_KEY )){
								
								return( new Object[]{ DeviceUPnPImpl.this, tf_key });
								
							}else if ( name.equals( PT_PERCENT_DONE )){
								
								return( new Long(1000));
								
							}else if ( name.equals( PT_ETA )){
								
								return( new Long(0));
							}
							
							return( null );
						}
					};
			
			synchronized( acf_map ){
	
				acf_map.put( tf_key, acf );
			}
		
			ipc.invoke( "addContent", new Object[]{ acf });

			log( "Set up stream-xcode for " + transcode_file.getName());
			
			return( true );
			
		}catch( Throwable e ){
			
			return( false );
		}
	}
	
	protected boolean
	isVisible(
		AzureusContentDownload		file )
	{
		if ( getFilterFilesView() || file == null ){
			
			return false;
		}
		
		Download download = file.getDownload();
		
		if ( download == null){
			
			return false;
		}
		
		if ( download.isComplete()){
			
			return true;
		}
		
		int numFiles = download.getDiskManagerFileCount();
		
		for ( int i = 0; i < numFiles; i++){
			
			DiskManagerFileInfo fileInfo = download.getDiskManagerFileInfo(i);
			
			if ( fileInfo == null || fileInfo.isDeleted() || fileInfo.isSkipped()){
				
				continue;
			}
			
			if ( fileInfo.getLength() == fileInfo.getDownloaded()){
				
				return true;
				
			}else if ( PlayUtils.canUseEMP( fileInfo )){
			
				return( true );
			}
		}
		
		return false;
	}
	
	protected boolean
	isVisible(
		AzureusContentFile		file )
	{			
		if ( getFilterFilesView()){
		
			Object[] x = (Object[])file.getProperty( MY_ACF_KEY );
			
			if ( x != null && x[0] == this ){
					
				String	tf_key = (String)x[1];
					
				return( getTranscodeFile( tf_key ) != null );
				
			}else{
				
				return( false );
			}
		}else{
			
			if ( file == null ){
				
				return( false );
			}
			
			DiskManagerFileInfo fileInfo = file.getFile();
			
			if ( fileInfo == null || fileInfo.isDeleted() || fileInfo.isSkipped()){
				
				return( false );
			}
			
			if ( fileInfo.getLength() == fileInfo.getDownloaded()){
				
				return( true );
				
			}else if ( PlayUtils.canUseEMP( fileInfo )){
			
				return( true );
			}
		}
		
		return( false );
	}
	
	public void
	fileAdded(
		TranscodeFile		_transcode_file )
	{
		fileAdded( _transcode_file, true );
	}
	
	public void
	fileAdded(
		TranscodeFile		_transcode_file,
		boolean				_new_file )
	{
		TranscodeFileImpl	transcode_file = (TranscodeFileImpl)_transcode_file;
		
		IPCInterface ipc = upnpav_ipc;
		
		synchronized( this ){
			
			if ( ipc == null ){

				return;
			}
			
			if ( !transcode_file.isComplete()){
				
				syncCategories( transcode_file, _new_file );

				return;
			}
			
			AzureusContentFile acf = (AzureusContentFile)transcode_file.getTransientProperty( UPNPAV_FILE_KEY );
			
			if ( acf != null ){
				
				return;
			}

			final String tf_key	= transcode_file.getKey();

			synchronized( acf_map ){
				
				acf = acf_map.get( tf_key );
			}
			
			if ( acf != null ){
				
				return;
			}

			try{
				final DiskManagerFileInfo 	f 		= transcode_file.getTargetFile();
							
				acf = 
					new AzureusContentFile()
					{
						public DiskManagerFileInfo
					    getFile()
						{
							return( f );
						}
						
						public Object
						getProperty(
							String		name )
						{						
							if(  name.equals( MY_ACF_KEY )){
								
								return( new Object[]{ DeviceUPnPImpl.this, tf_key });
								
							}else if ( name.equals( PT_CATEGORIES )){
								
								TranscodeFileImpl	tf = getTranscodeFile( tf_key );

								if ( tf != null ){
									
									return( tf.getCategories());
								}
							
								return( new String[0] );
								
							} else if (name.equals(PT_TITLE)) {
								
								
								TranscodeFileImpl	tf = getTranscodeFile( tf_key );

								if ( tf != null ){
									
									return( tf.getName());
								}
							
								
							}else{
								
								TranscodeFileImpl	tf = getTranscodeFile( tf_key );
								
								if ( tf != null ){
									
									long	res = 0;
									
									if ( name.equals( PT_DURATION )){
										
										res = tf.getDurationMillis();
										
									}else if ( name.equals( PT_VIDEO_WIDTH )){
										
										res = tf.getVideoWidth();
										
									}else if ( name.equals( PT_VIDEO_HEIGHT )){
										
										res = tf.getVideoHeight();
										
									}else if ( name.equals( PT_DATE )){

										res = tf.getCreationDateMillis();
										
									}else if ( name.equals( PT_PERCENT_DONE )){

										if ( tf.isComplete()){
											
											res = 1000;
											
										}else{
											
											TranscodeJob job = tf.getJob();
											
											if ( job == null ){
												
												res = 0;
												
											}else{
												
												res = 10*job.getPercentComplete();
											}
										}
										
										return( res );
										
									}else if ( name.equals( PT_ETA )){

										if ( tf.isComplete()){
											
											res = 0;
											
										}else{
											
											TranscodeJob job = tf.getJob();
											
											if ( job == null ){
												
												res = Long.MAX_VALUE;
												
											}else{
												
												res = job.getETASecs();
											}
										}
										
										return( res );
									}
									
									if ( res > 0 ){
										
										return( new Long( res ));
									}
								}
							}
							
							return( null );
						}
					};
				
				transcode_file.setTransientProperty( UPNPAV_FILE_KEY, acf );

				synchronized( acf_map ){

					acf_map.put( tf_key, acf );
				}	
				
				syncCategories( transcode_file, _new_file );
					
				try{
					ipc.invoke( "addContent", new Object[]{ acf });
				
				}catch( Throwable e ){
					
					Debug.out( e );
				}		
			}catch( TranscodeException e ){
				
				// file deleted
			}
		}
	}
	
	protected void
	syncCategories(
		TranscodeFileImpl		tf,
		boolean					inherit_from_download )
	{
		try{
			Download dl = tf.getSourceFile().getDownload();
			
			if ( dl != null ){
				
					// only overwrite categories with the downloads ones if none already set
				
				if ( inherit_from_download ){
				
					setCategories( tf, dl );
				}
				
				final String tf_key = tf.getKey();
				
				dl.addAttributeListener(
					new DownloadAttributeListener()
					{
						public void 
						attributeEventOccurred(
							Download 			download,
							TorrentAttribute 	attribute, 
							int 				eventType) 
						{
							TranscodeFileImpl tf = getTranscodeFile( tf_key );
							
							if ( tf != null ){
								
								setCategories( tf, download );
							}
						}
					},
					upnp_manager.getCategoryAttibute(),
					DownloadAttributeListener.WRITTEN );
			}
		}catch( Throwable e ){
			
		}
	}
	
	protected void
	setCategories(
		TranscodeFileImpl		tf,
		Download				dl )
	{
		String	cat = dl.getCategoryName();
		
		if ( cat != null && cat.length() > 0 && !cat.equals( "Categories.uncategorized" )){
			
			tf.setCategories( new String[]{ cat });
			
		}else{
			
			tf.setCategories( new String[0] );
		}
	}
	
	public void
	fileChanged(
		TranscodeFile		file,
		int					type,
		Object				data )
	{
		if ( file.isComplete()){
			
			fileAdded( file, false );
		}
		
		if ( type == TranscodeTargetListener.CT_PROPERTY ){
			
			if ( data == TranscodeFile.PT_CATEGORY ){
				
				AzureusContentFile	acf;
				
				synchronized( acf_map ){
				
					acf = acf_map.get(((TranscodeFileImpl)file).getKey());
				}
				
				if ( acf != null ){
					
					AzureusPlatformContentDirectory.fireChanged( acf );
				}
			}
		}
	}
	
	public void
	fileRemoved(
		TranscodeFile		file )
	{
		IPCInterface ipc = upnp_manager.getUPnPAVIPC();
		
		if ( ipc == null ){
			
			return;
		}

		synchronized( this ){

			AzureusContentFile acf = (AzureusContentFile)file.getTransientProperty( UPNPAV_FILE_KEY );

			if ( acf == null ){
		
				return;
			}
			
			file.setTransientProperty( UPNPAV_FILE_KEY, null );

			try{
				ipc.invoke( "removeContent", new Object[]{ acf });
			
				
			}catch( Throwable e ){
				
				Debug.out( e );
			}
		}
		
		synchronized( acf_map ){

			acf_map.remove( ((TranscodeFileImpl)file).getKey());
		}	
	}
	
	protected URL
	getPresentationURL(
		UPnPDevice		device )
	{
		String	presentation = device.getRootDevice().getDevice().getPresentation();
		
		if ( presentation != null ){
			
			try{
				URL url = new URL( presentation );
				
				return( url );

			}catch( Throwable e ){				
			}
		}
		
		return( null );
	}
	
	protected void
	getDisplayProperties(
		List<String[]>	dp )
	{
		super.getDisplayProperties( dp );
		
		UPnPDevice device = device_may_be_null;
		
		if ( device != null ){
			
			UPnPRootDevice root = device.getRootDevice();
			
			URL location = root.getLocation();
			
			addDP( dp, "dht.reseed.ip", location.getHost() + ":" + location.getPort()); 
	
			String	model_details 	= device.getModelName();
			String	model_url		= device.getModelURL();
			
			if ( model_url != null && model_url.length() > 0 ){
				model_details += " (" + model_url + ")";
			}
			
			String	manu_details 	= device.getManufacturer();
			String	manu_url		= device.getManufacturerURL();
			
			if ( manu_url != null && manu_url.length() > 0 ){
				manu_details += " (" + manu_url + ")";
			}
			
			addDP( dp, "device.model.desc", device.getModelDescription());
			addDP( dp, "device.model.name", model_details );
			addDP( dp, "device.model.num", device.getModelNumber());
			addDP( dp, "device.manu.desc", manu_details );
			
		}else{
			
			InetAddress ia = getAddress();
			
			if ( ia != null ){
				
				addDP( dp, "dht.reseed.ip", ia.getHostAddress()); 
			}
		}
		addDP( dp, "!Is Liveness Detectable!", isLivenessDetectable());
		if ( isManual() ){
			
			addDP( dp, "azbuddy.ui.table.online",  isAlive() );
		
			addDP( dp, "device.lastseen", getLastSeen()==0?"":new SimpleDateFormat().format(new Date( getLastSeen() )));
		}
	}
	
	public void
	generate(
		IndentWriter		writer )
	{
		super.generate( writer );
		
		try{
			writer.indent();
			
			UPnPDevice device = device_may_be_null;
			
			if ( device == null ){
				
				writer.println( "upnp_device=null" );
				
			}else{
				
				writer.println( "upnp_device=" + device.getFriendlyName());
			}
	
			writer.println( "dyn_xcode=" + (dynamic_transcode_profile==null?"null":dynamic_transcode_profile.getName()));
		}finally{
			
			writer.exdent();
		}
	}
	
	protected static class
	StreamWrapper
		implements DiskManagerFileInfoStream.StreamFactory.StreamDetails
	{
		private InputStream		is;
		private TranscodeJob	job;
		
		protected
		StreamWrapper(
			InputStream		_is,
			TranscodeJob	_job )
		{
			is		= _is;
			job		= _job;
		}
		
		public InputStream
		getStream()
		{
			return( is );
		}
		
		public boolean
		hasFailed()
		{
			long start = SystemTime.getMonotonousTime();
		
			while( true ){
				
				int state = job.getState();
							
					// timing issues - we can get here during teh fail process so
					// hang around a little if we're still running
				
				if ( state == TranscodeJobImpl.ST_RUNNING ){
					
					if ( SystemTime.getMonotonousTime() - start > 5*1000 ){
						
						return( true );
						
					}else{
						
						try{
							Thread.sleep(250);
							
							continue;
							
						}catch( Throwable e ){
							
							return( true );
						}
					}
				}
				
				if ( 	state == TranscodeJobImpl.ST_FAILED ||
						state == TranscodeJobImpl.ST_CANCELLED ||
						state == TranscodeJobImpl.ST_REMOVED ||
						state == TranscodeJobImpl.ST_STOPPED ){
					
						// might have completed and then been removed
					
					TranscodeFile tf = job.getTranscodeFile();
					
					if ( tf != null && tf.isComplete()){
						
						return( false );
					}
					
					return( true );
				}
			}
		}
	}

	@Override
	public String getImageID() {
		String imageID = super.getImageID();
		// commented out existing imageid check so upnp device image overrides
		if (/*imageID == null && */ device_may_be_null != null && isAlive()) {
			UPnPDeviceImage[] images = device_may_be_null.getImages();
			if (images.length > 0) {
				URL location = getLocation();
				if (location != null) {
					String url = "http://" + location.getHost() + ":" + location.getPort();
					String imageUrl = images[0].getLocation(); 
					for (UPnPDeviceImage imageInfo : images) {
						String mime = imageInfo.getLocation();
						if (mime != null && mime.contains("png")) {
							imageUrl = imageInfo.getLocation();
							break;
						}
					}
					if (!imageUrl.startsWith("/")) {
						url += "/";
					}
					url += imageUrl;
					return url;
				}
			}
		}
		return imageID;
	}
}
