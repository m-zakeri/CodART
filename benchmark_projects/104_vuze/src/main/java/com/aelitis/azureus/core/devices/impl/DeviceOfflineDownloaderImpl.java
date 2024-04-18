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
import java.net.InetAddress;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;

import org.gudy.azureus2.core3.disk.DiskManager;
import org.gudy.azureus2.core3.disk.DiskManagerFileInfo;
import org.gudy.azureus2.core3.disk.DiskManagerPiece;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.core3.global.GlobalManagerAdapter;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.peer.PEPeer;
import org.gudy.azureus2.core3.peer.PEPeerManager;
import org.gudy.azureus2.core3.torrent.TOTorrent;
import org.gudy.azureus2.core3.torrent.TOTorrentAnnounceURLSet;
import org.gudy.azureus2.core3.torrent.TOTorrentFactory;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.peers.Peer;
import org.gudy.azureus2.pluginsimpl.local.PluginCoreUtils;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.devices.*;
import com.aelitis.azureus.core.security.CryptoManagerFactory;
import com.aelitis.azureus.core.torrent.PlatformTorrentUtils;
import com.aelitis.azureus.core.util.CopyOnWriteList;
import com.aelitis.azureus.util.DownloadUtils;
import com.aelitis.net.upnp.UPnPDevice;
import com.aelitis.net.upnp.UPnPException;
import com.aelitis.net.upnp.UPnPRootDevice;
import com.aelitis.net.upnp.services.UPnPOfflineDownloader;

public class 
DeviceOfflineDownloaderImpl
	extends DeviceUPnPImpl
	implements DeviceOfflineDownloader
{
	public static final int	UPDATE_MILLIS	= 30*1000;
	public static final int UPDATE_TICKS	= UPDATE_MILLIS/DeviceManagerImpl.DEVICE_UPDATE_PERIOD;
	
	public static final int	UPDATE_SPACE_MILLIS	= 3*60*1000;
	public static final int UPDATE_SPACE_TICKS	= UPDATE_SPACE_MILLIS/DeviceManagerImpl.DEVICE_UPDATE_PERIOD;
	
	public static final String	client_id = ByteFormatter.encodeString( CryptoManagerFactory.getSingleton().getSecureID());
	
	private static final Object	ERROR_KEY_OD = new Object();

	private volatile UPnPOfflineDownloader		service;
	private volatile String						service_ip;
	private volatile String						manufacturer;
	
	private long	start_time = SystemTime.getMonotonousTime();
	
	private volatile boolean		update_space_outstanding 	= true;
	private volatile long			space_on_device				= -1;
	
	private volatile boolean					closing;
	
	private AsyncDispatcher	dispatcher = new AsyncDispatcher();
	
	final FrequencyLimitedDispatcher	freq_lim_updater = 
		new FrequencyLimitedDispatcher(
			new AERunnable()
			{
				public void
				runSupport()
				{
					updateDownloads();
				}
			},
			5*1000 );
	
	private boolean								start_of_day	= true;
	private int									consec_errors	= 0;
	private int									consec_success	= 0;
	
	private Map<String,OfflineDownload>			offline_downloads	= new HashMap<String, OfflineDownload>(); 
	private Map<String,TransferableDownload>	transferable 		= new LinkedHashMap<String,TransferableDownload>();
	private TransferableDownload				current_transfer;
	private boolean								is_transferring;
	
	
	private CopyOnWriteList<DeviceOfflineDownloaderListener>	listeners = new CopyOnWriteList<DeviceOfflineDownloaderListener>();		
	
	protected
	DeviceOfflineDownloaderImpl(
		DeviceManagerImpl			_manager,
		UPnPDevice					_device,
		UPnPOfflineDownloader		_service )
	{
		super( _manager, _device, Device.DT_OFFLINE_DOWNLOADER );
		
		setService( _service );
	}
	
	protected
	DeviceOfflineDownloaderImpl(
		DeviceManagerImpl	_manager,
		Map					_map )
	
		throws IOException
	{
		super(_manager, _map );
		
		manufacturer = getPersistentStringProperty( PP_OD_MANUFACTURER, "?" );
	}
	
	protected boolean
	updateFrom(
		DeviceImpl		_other,
		boolean			_is_alive )
	{
		if ( !super.updateFrom( _other, _is_alive )){
			
			return( false );
		}
		
		if ( !( _other instanceof DeviceOfflineDownloaderImpl )){
			
			Debug.out( "Inconsistent" );
			
			return( false );
		}
		
		DeviceOfflineDownloaderImpl other = (DeviceOfflineDownloaderImpl)_other;
			
		if ( service == null && other.service != null ){
			
			setService( other.service );
			
			updateDownloads();
		}
		
		return( true );
	}
	
	protected void
	setService(
		UPnPOfflineDownloader	_service )
	{
		service	= _service;
		
		UPnPRootDevice root = service.getGenericService().getDevice().getRootDevice();
		
		service_ip = root.getLocation().getHost();
		
		try{
			service_ip = InetAddress.getByName( service_ip ).getHostAddress();
			
		}catch( Throwable e ){
			
			Debug.out( e );
		}
		
		Map cache = root.getDiscoveryCache();
		
		if ( cache != null ){
			
			setPersistentMapProperty( PP_OD_UPNP_DISC_CACHE, cache );
		}
		
		manufacturer = root.getDevice().getManufacturer();
		
		setPersistentStringProperty( PP_OD_MANUFACTURER, manufacturer );
		
		updateDownloads();
	}
	
	protected void 
	UPnPInitialised() 
	{
		super.UPnPInitialised();
		
		if ( service == null ){
		
			Map	cache = getPersistentMapProperty( PP_OD_UPNP_DISC_CACHE, null );
		
			if ( cache != null ){
			
				getUPnPDeviceManager().injectDiscoveryCache( cache );
			}
		}
	}
	
	protected void 
	updateStatus(
		int tick_count ) 
	{
		super.updateStatus( tick_count );
		
		update_space_outstanding |= tick_count % UPDATE_SPACE_TICKS == 0;

		if ( tick_count % UPDATE_TICKS == 0 ){
							
			updateDownloads();
		}
	}
	
	protected void
	checkConfig()
	{
		freq_lim_updater.dispatch();
	}
	
	protected void
	updateDownloads()
	{
		dispatcher.dispatch(
			new AERunnable()
			{
				public void
				runSupport()
				{
					if ( dispatcher.getQueueSize() == 0 ){
					
						updateDownloadsSupport();
					}
				}
			});
	}
	
	protected void
	updateDownloadsSupport()
	{
		AzureusCore core = getManager().getAzureusCore();
		
		if ( core == null || closing ){
			
				// not yet initialised or closing
			
			return;
		}

		boolean warn_if_dead = SystemTime.getMonotonousTime() - start_time > 3*60*1000;
		
		if ( !isAlive() || service == null  ){
			
				// no usable service
			
			if ( warn_if_dead ){
			
				setError( ERROR_KEY_OD, MessageText.getString( "device.od.error.notfound" ));
			}
			
			return;
		}

		String	error_status 	= null;
		boolean	force_status	= false;
		
		Map<String,DownloadManager>			new_offline_downloads 	= new HashMap<String,DownloadManager>();
		Map<String,TransferableDownload>	new_transferables 		= new HashMap<String,TransferableDownload>();
		
		try{	
			if ( update_space_outstanding ){
			
				try{
					space_on_device = service.getFreeSpace( client_id );
					
					update_space_outstanding = false;
					
				}catch( Throwable e ){
					
					error_status = MessageText.getString( "device.od.error.opfailexcep", new String[]{ "GetFreeSpace", Debug.getNestedExceptionMessage( e )});

					log( "Failed to get free space", e );

				}
			}
			
			if ( space_on_device == 0 ){
				
				error_status 	= MessageText.getString( "device.od.error.nospace" );
				force_status	= true;
			}

			Map<String,byte[]>	old_cache 	= (Map<String,byte[]>)getPersistentMapProperty( PP_OD_STATE_CACHE, new HashMap<String,byte[]>());
			
			Map<String,byte[]>	new_cache 	= new HashMap<String, byte[]>();
			
			GlobalManager gm = core.getGlobalManager();
			
			if ( start_of_day ){
				
				start_of_day = false;
				
				Map<String,Map> xfer_cache = getPersistentMapProperty( PP_OD_XFER_CACHE, new HashMap<String,Map>());
				
				if ( xfer_cache.size() > 0 ){
					
					List<DownloadManager> initial_downloads = gm.getDownloadManagers();
					
					for ( DownloadManager download: initial_downloads ){
	
						if ( download.isForceStart()){
							
							TOTorrent torrent = download.getTorrent();
							
							if ( torrent == null ){
								
								continue;
							}
							
							try{
								byte[] hash = torrent.getHash();
								
								String	hash_str = ByteFormatter.encodeString( hash );
								
								Map m = xfer_cache.get( hash_str );
									
								if ( m != null ){
									
									if ( m.containsKey( "f" )){
										
										log( download, "Resetting force-start" );
										
										download.setForceStart( false );
									}
								}
							}catch( Throwable e ){
								
								Debug.printStackTrace(e);
							}
						}
					}
				}
				
				gm.addListener(
					new GlobalManagerAdapter()
					{
						public void
						downloadManagerAdded(
							DownloadManager	dm )
						{
							freq_lim_updater.dispatch();
						}
							
						public void
						downloadManagerRemoved( 
							DownloadManager	dm )
						{
							freq_lim_updater.dispatch();
						}
					},
					false );
			}
			
			DeviceManager manager = getManager();
				
			DeviceOfflineDownloaderManager dodm = manager.getOfflineDownlaoderManager();
			
			List<DownloadManager> downloads;
			
			if ( dodm.isOfflineDownloadingEnabled() && isEnabled()){

				List<DownloadManager> initial_downloads = gm.getDownloadManagers();

				List<DownloadManager> relevant_downloads = new ArrayList<DownloadManager>( initial_downloads.size());
			
					// remove uninteresting ones
				
				for ( DownloadManager download: initial_downloads ){
				
					int	state = download.getState();
										
					if ( state == DownloadManager.STATE_SEEDING ){
							// state == DownloadManager.STATE_ERROR ){	removed - might be out of disk space and fixable
						
						continue;
					}
					
						// don't include 'stopping' here as we go through stopping on way to queued

					if ( state == DownloadManager.STATE_STOPPED ){
						
							// don't remove from downloader if simply paused
						
						if ( !download.isPaused()){
														
							continue;
						}
					}
					
						// if it is complete then of no interest
					
					if ( download.isDownloadComplete( false )){
							
						continue;
					}
					
					relevant_downloads.add( download );
				}
			
				downloads = new ArrayList<DownloadManager>( relevant_downloads.size());
			
				if ( dodm.getOfflineDownloadingIsAuto()){
					
					boolean	include_private = dodm.getOfflineDownloadingIncludePrivate();
					
					if ( include_private ){
						
						downloads.addAll( relevant_downloads );
						
					}else{
						
						for ( DownloadManager download: relevant_downloads ){
							
							TOTorrent torrent = download.getTorrent();
							
							if ( !TorrentUtils.isReallyPrivate( torrent )){
								
								downloads.add( download );
							}
						}
					}
				}else{
					
						// manual, just use the tagged downloads
					
					for ( DownloadManager download: relevant_downloads ){

						if ( dodm.isManualDownload( PluginCoreUtils.wrap( download ))){
							
							downloads.add( download );
						}
					}
				}
			}else{
				
				downloads = new ArrayList<DownloadManager>();
			}
			
			Map<DownloadManager,byte[]>	download_map = new HashMap<DownloadManager, byte[]>();
			
			for ( DownloadManager download: downloads ){
											
				TOTorrent torrent = download.getTorrent();
	
				if ( torrent == null ){
					
					continue;
				}
				
				try{
					byte[] hash = torrent.getHash();
					
					String	hash_str = ByteFormatter.encodeString( hash );
					
					DiskManager disk = download.getDiskManager();
					
					if ( disk == null ){
						
						byte[] existing = old_cache.get( hash_str );
						
						if ( existing != null ){
							
							new_cache.put( hash_str, existing );
							
							download_map.put( download, existing );
							
						}else{
							
								// assume not yet started and just use the non-skipped files
							
							DiskManagerFileInfo[] files = download.getDiskManagerFileInfo();
							
							byte[] needed = new byte[( torrent.getNumberOfPieces() + 7 ) / 8];

							int	hits = 0;

							for ( DiskManagerFileInfo file: files ){
								
								if ( file.isSkipped()){
									
									continue;
								}
								
								int	first_piece 	= file.getFirstPieceNumber();
								int	last_piece		= first_piece + file.getNbPieces() - 1;
																
								int	needed_pos		= first_piece/8;
								int	current_byte	= 0;
																
								for ( int pos=first_piece;pos<=last_piece;pos++ ){
									
									current_byte = current_byte << 1;
																			
									current_byte += 1;
										
									hits++;
									
									if (( pos %8 ) == 7 ){
										
										needed[needed_pos++] |= (byte)current_byte;
										
										current_byte = 0;
									}
								}
								
								if ( current_byte != 0 ){
									
									needed[needed_pos++] |= (byte)(current_byte << (8 - (last_piece % 8)));
								}
							}
							
							if ( hits > 0 ){
									
								new_cache.put( hash_str, needed );
									
								download_map.put( download, needed );
							}
						}
					}else{
					
						DiskManagerPiece[] pieces = disk.getPieces();
						
						byte[] needed = new byte[( pieces.length + 7 ) / 8];
						
						int	needed_pos		= 0;
						int	current_byte	= 0;
						int	pos 			= 0;
						
						int	hits = 0;
						
						for ( DiskManagerPiece piece: pieces ){
							
							current_byte = current_byte << 1;
							
							if ( piece.isNeeded() && !piece.isDone()){
								
								current_byte += 1;
								
								hits++;
							}
							
							if (( pos %8 ) == 7 ){
								
								needed[needed_pos++] = (byte)current_byte;
								
								current_byte = 0;
							}
							pos++;
						}
						
						if (( pos % 8 ) != 0 ){
							
							needed[needed_pos++] = (byte)(current_byte << (8 - (pos % 8)));
						}
						
						if ( hits > 0 ){
							
							new_cache.put( hash_str, needed );
							
							download_map.put( download, needed );
						}
					}
				}catch( Throwable e ){
					
					Debug.out( e );
				}
			}
			
				// store this so we have consistent record for downloads that queue/pause etc and therefore lose accessible piece details
			
			setPersistentMapProperty( PP_OD_STATE_CACHE, new_cache );
			
				// sort by download priority
			
			List<Map.Entry<DownloadManager, byte[]>> entries = new ArrayList<Map.Entry<DownloadManager,byte[]>>( download_map.entrySet());
			
			Collections.sort(
				entries,
				new Comparator<Map.Entry<DownloadManager, byte[]>>()
				{
					public int 
					compare(
						Map.Entry<DownloadManager, byte[]> o1,
						Map.Entry<DownloadManager, byte[]> o2) 
					{
						return( o1.getKey().getPosition() - o2.getKey().getPosition());
					} 
				});
				
			String	download_hashes = "";
			
			Iterator<Map.Entry<DownloadManager, byte[]>> it = entries.iterator();
			
			while( it.hasNext()){
				
				Map.Entry<DownloadManager, byte[]> entry = it.next();
				
				DownloadManager	download = entry.getKey();
				
				try{
					String hash = ByteFormatter.encodeString( download.getTorrent().getHash());
					
					download_hashes += ( download_hashes.length()==0?"":"," ) + hash;
					
					new_offline_downloads.put( hash, download );
					
				}catch( Throwable e ){
					
					log( download, "Failed to get download hash", e );
					
					it.remove();
				}
			}
			
			try{
				String[] set_dl_results = service.setDownloads( client_id, download_hashes );
				
				String	set_dl_result	= set_dl_results[0].trim();
				String	set_dl_status 	= set_dl_results[1];
				
				if ( !set_dl_status.equals( "OK" )){
					
					error_status = MessageText.getString( "device.od.error.opfailstatus", new String[]{ "SetDownloads", set_dl_status });

					throw( new Exception( "Failing result returned: " + set_dl_status ));
				}
				
				String[]	bits = Constants.PAT_SPLIT_COMMA.split(set_dl_result);
				
				int	num_bits = set_dl_result.length()==0?0:bits.length;
				
				if ( num_bits != entries.size()){
					
					log( "SetDownloads returned an invalid number of results (hashes=" + new_offline_downloads.size() + ",result=" + set_dl_result + ")");
					
				}else{
					
					it = entries.iterator();
					
					int	pos = 0;
					
					while( it.hasNext()){
						
						Map.Entry<DownloadManager, byte[]> entry = it.next();
						
						DownloadManager	download = entry.getKey();
						
						try{
							TOTorrent torrent = download.getTorrent();
	
							String hash_str = ByteFormatter.encodeString( torrent.getHash());
							
							int	status = Integer.parseInt( bits[ pos++ ]);
		
							boolean	do_update = false;
						
							if ( status == 0 ){
							
								do_update = true;
							
							}else if ( status == 1 ){
							
									// need to add the torrent
							
								try{
										// for vuze content add in the azid
									
									if ( PlatformTorrentUtils.isContent( torrent, true )){
										
										String ext = DownloadUtils.getTrackerExtensions( PluginCoreUtils.wrap( download ));
										
										if ( ext != null && ext.length() > 0 ){
											
											try{
												
												if ( ext.startsWith( "&" )){
													
													ext = ext.substring(1);
												}
											
												torrent = TOTorrentFactory.deserialiseFromMap( torrent.serialiseToMap());
												
												torrent.setAnnounceURL( appendToURL( torrent.getAnnounceURL(), ext ));
												
												TOTorrentAnnounceURLSet[] sets = torrent.getAnnounceURLGroup().getAnnounceURLSets();
												
												for ( TOTorrentAnnounceURLSet set: sets ){
													
													URL[] urls = set.getAnnounceURLs();
													
													for (int i=0;i<urls.length;i++){
														
														urls[i] = appendToURL( urls[i], ext );
													}
												}
												
												torrent.getAnnounceURLGroup().setAnnounceURLSets( sets );
												
											}catch( Throwable e ){
												
												log( "Torrent modification failed", e );
											}
										}
									}
									
									String add_result = 
										addTorrent( 										
											hash_str,
											ByteFormatter.encodeStringFully( BEncoder.encode( torrent.serialiseToMap())));
									
									log( download, "AddDownload succeeded" );
									
									if ( add_result.equals( "OK" )){
										
										do_update = true;
										
									}else{
										
										error_status = MessageText.getString( "device.od.error.opfailstatus", new String[]{ "AddDownload", add_result });
									
										throw( new Exception( "Failed to add download: " + add_result ));
									}
								}catch( Throwable e ){
									
										// TODO: prevent continual attempts to add same torrent?
									
									error_status = MessageText.getString( "device.od.error.opfailexcep", new String[]{ "AddDownload", Debug.getNestedExceptionMessage( e )});

									log( download, "Failed to add download", e );
								}
							}else{
							
								error_status = MessageText.getString( "device.od.error.opfailstatus", new String[]{ "SetDownloads", String.valueOf( status )});

								log( download, "SetDownloads: error status returned - " + status );
							}
					
							if ( do_update ){
					
								try{
									byte[]	required_map = entry.getValue();
									
									String	required_bitfield = ByteFormatter.encodeStringFully( required_map );
									
									String[] update_results = 
										service.updateDownload( 
											client_id, 
											hash_str,
											required_bitfield );
										
									String	have_bitfield	= update_results[0];
									String	update_status 	= update_results[1];
									
									if ( !update_status.equals( "OK" )){
										
										error_status = MessageText.getString( "device.od.error.opfailstatus", new String[]{ "UpdateDownload", update_status });

										throw( new Exception( "UpdateDownload: Failing result returned: " + update_status ));
									}
												
									int		useful_piece_count 	= 0;
									
									if ( have_bitfield.length() > 0 ){
										
										byte[]	have_map = ByteFormatter.decodeString( have_bitfield );
										
										if ( have_map.length != required_map.length ){
											
											throw( new Exception( "UpdateDownload: Returned bitmap length invalid" ));
										}
										
										for ( int i=0;i<required_map.length;i++){
											
											int x = ( required_map[i] & have_map[i] )&0xff;
											
											if ( x != 0 ){
													
												for (int j=0;j<8;j++){
													
													if ((x&0x01) != 0 ){
														
														useful_piece_count++;
													}
													
													x >>= 1;
												}
											}
										}
										
										if ( useful_piece_count > 0 ) {
										
											long	piece_size	= torrent.getPieceLength();

											new_transferables.put( hash_str, new TransferableDownload( download, hash_str, have_map, useful_piece_count * piece_size ));
										}
									}
									
									if ( useful_piece_count > 0 ){
									
										log( download, "They have " + useful_piece_count + " pieces that we don't" );
									}
									
								}catch( Throwable e ){
							
									error_status = MessageText.getString( "device.od.error.opfailexcep", new String[]{ "UpdateDownload", Debug.getNestedExceptionMessage( e )});

									log( download, "UpdateDownload failed", e );
								}
							}
						}catch( Throwable e ){
						
							log( download, "Processing failed", e );
						}
					}
				}
				
			}catch( Throwable e ){
				
				error_status = MessageText.getString( "device.od.error.opfailexcep", new String[]{ "SetDownloads", Debug.getNestedExceptionMessage( e )});
				
				log( "SetDownloads failed", e );
			}
		}finally{
			
			updateTransferable( new_transferables );
			
			List<OfflineDownload>	new_ods = new ArrayList<OfflineDownload>();
			List<OfflineDownload>	del_ods = new ArrayList<OfflineDownload>();
			List<OfflineDownload>	cha_ods = new ArrayList<OfflineDownload>();
			
			synchronized( offline_downloads ){
			
				for (Map.Entry<String,DownloadManager> entry: new_offline_downloads.entrySet()){
				
					String key = entry.getKey();
					
					if ( !offline_downloads.containsKey( key )){
						
						OfflineDownload new_od = new OfflineDownload( entry.getValue());
						
						offline_downloads.put( key, new_od );
						
						new_ods.add( new_od );
					}
				}
				
				Iterator<Map.Entry<String,OfflineDownload>> it = offline_downloads.entrySet().iterator();
				
				while( it.hasNext()){
					
					Map.Entry<String,OfflineDownload>	entry = it.next();
					
					String 			key 	= entry.getKey();
					OfflineDownload	od		= entry.getValue();
					
					if ( new_offline_downloads.containsKey( key )){
						
						TransferableDownload new_td = transferable.get( key );
						
						TransferableDownload existing_td = od.getTransferable();
						
						if ( new_td != existing_td ){
							
							if ( !new_ods.contains( od )){
								
								cha_ods.add( od );
							}
							
							od.setTransferable( new_td );
						}
					}else{
						
						it.remove();
						
						del_ods.add( od );
					}
				}
			}
			
			for ( OfflineDownload od: new_ods ){
				
				for ( DeviceOfflineDownloaderListener listener: listeners ){
					
					try{
						listener.downloadAdded( od );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}
			
			for ( OfflineDownload od: cha_ods ){
				
				for ( DeviceOfflineDownloaderListener listener: listeners ){
					
					try{
						listener.downloadChanged( od );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}
			
			for ( OfflineDownload od: del_ods ){
				
				for ( DeviceOfflineDownloaderListener listener: listeners ){
					
					try{
						listener.downloadRemoved( od );
						
					}catch( Throwable e ){
						
						Debug.out( e );
					}
				}
			}
			
			updateError( error_status, force_status );
		}
	}

	private String
	addTorrent(
		String		hash_str,
		String		torrent_data )
	
		throws UPnPException
	{
		int	chunk_size = 40*1024;
		
		int	length = torrent_data.length();
		
		if ( length < chunk_size ){
		
			return( service.addDownload( client_id,	hash_str, torrent_data ));
			
		}else{
			
			String status = "";
			
			int	rem = length;
			
			for( int i=0; i<length; i+=chunk_size ){
			
				int	size = Math.min( rem, chunk_size );
				
				status = service.addDownloadChunked(
					client_id,	
					hash_str,
					torrent_data.substring( i, i+size ),
					i,
					length );
					
				rem -= size;
			}
			
			return( status );
		}
	}
	
	protected void
	updateError(
		String	str,
		boolean	force )
	{
		if ( str == null ){
			
			setError( ERROR_KEY_OD, null );
			
			consec_errors = 0;
			
			consec_success++;
			
		}else{
			
				// if device isn't connectable then replace the error with something more
				// user-friendly
			
			try{
			
				if ( !service.getGenericService().isConnectable()){
					
					str = MessageText.getString( "device.od.error.notfound" );
				}
			}catch( Throwable e ){
				
				Debug.out( e );
			}
			
			consec_errors++;
			
			consec_success = 0;
			
			if ( consec_errors > 2 || force ){
				
				setError( ERROR_KEY_OD, str );
			}
		}
	}
	
	protected URL
	appendToURL(
		URL			url,
		String		ext )
	
		throws MalformedURLException
	{
		String url_str = url.toExternalForm();
		
		if ( url_str.indexOf( '?' ) == -1 ){
			
			url_str += "?" + ext;
			
		}else{
			
			url_str += "&" + ext;
		}
		
		return( new URL( url_str ));
	}
	
	protected void
	updateTransferable(
		Map<String,TransferableDownload>	map )
	{
			// remove non-transferable entries
		
		Iterator<Map.Entry<String,TransferableDownload>>	it = transferable.entrySet().iterator();
		
		while( it.hasNext()){
			
			Map.Entry<String,TransferableDownload> entry = it.next();
			
			if ( !map.containsKey( entry.getKey())){
					
				TransferableDownload existing = entry.getValue();
				
				if ( existing == current_transfer ){
					
					current_transfer.deactivate();
						
					current_transfer = null;
				}
				
				it.remove();
			}
		}
		
			// add in new ones
		
		for ( TransferableDownload td: map.values()){
			
			String hash = td.getHash();
			
			if ( !transferable.containsKey( hash )){
				
				transferable.put( hash, td );
			}
		}
		
		if ( transferable.size() == 0 ){
			
			if ( is_transferring ){
			
				is_transferring = false;
				
				setBusy( false );
			}
			
			return;
		}
		
		if ( !is_transferring ){
		
			is_transferring = true;
			
			setBusy( true );
		}
		
			// check current
		
		if ( current_transfer != null && transferable.size() > 0 ){
			
				// rotate through them in case something's stuck for whatever reason
			
			long	now = SystemTime.getMonotonousTime();
			
			long	runtime = now - current_transfer.getStartTime();
						
			if ( runtime >= 30*1000 ){
				
				boolean	rotate = false;

				PEPeerManager pm = current_transfer.getDownload().getPeerManager();
				
				if ( pm == null ){
					
					rotate = true;
					
				}else{
					
					if ( runtime > 3*60*1000 ){
					
						List<PEPeer> peers = pm.getPeers( service_ip );
						
						if ( peers.size() == 0 ){
							
							rotate = true;
							
						}else{
						
							PEPeer peer = peers.get(0);
							
							if ( peer.getStats().getDataReceiveRate() < 1024 ){
								
								rotate = true;
							}
						}
					}
				}
				
				if ( rotate ){
					
					current_transfer.deactivate();
					
					current_transfer = null;
				}
			}
		}
		
		if ( current_transfer == null ){
			
			Iterator<TransferableDownload> it2 = transferable.values().iterator();
			
			current_transfer = it2.next();
			
			it2.remove();
			
			transferable.put( current_transfer.getHash(), current_transfer );
		}
		
		if ( current_transfer != null ){
			
			if ( !current_transfer.isActive()){
				
				current_transfer.activate();
			}
			
			if ( current_transfer.isForced()){
				
				Map<String,Map> xfer_cache = new HashMap<String,Map>();
				
				Map m = new HashMap();
				
				m.put( "f", new Long(1));
				
				xfer_cache.put( current_transfer.getHash(), m );
				
				setPersistentMapProperty( PP_OD_XFER_CACHE, xfer_cache );
			}
			
			DownloadManager	download = current_transfer.getDownload();
			
			int	data_port = current_transfer.getDataPort();
			
			if ( data_port <= 0 ){
								
				try{
					String[] start_results = service.startDownload( client_id, current_transfer.getHash());
					
					String start_status = start_results[1];
					
					if ( !start_status.equals( "OK" )){
						
						throw( new Exception( "Failing result returned: " + start_status ));
					}
					
					data_port = Integer.parseInt( start_results[0] );
					
					log( download, "StartDownload succeeded - data port=" + data_port );

				}catch( Throwable e ){
					
					log( download, "StartDownload failed", e );
				}
			}
			
			if ( data_port > 0 ){
				
				current_transfer.setDataPort( data_port );
			}
			
			final TransferableDownload transfer = current_transfer;

			dispatcher.dispatch(
				new AERunnable()
				{
					private final int[]	count = { 0 };
					
					public void
					runSupport()
					{
						count[0]++;
						
						if ( current_transfer != transfer || !transfer.isActive()){
							
							return;
						}
						
						PEPeerManager pm = transfer.getDownload().getPeerManager();
						
						if ( pm == null ){
							
							return;
						}
						
						List<PEPeer> peers = pm.getPeers( service_ip );
								
						if ( peers.size() > 0 ){
			
							return;
						}
						
						Map	user_data = new LightHashMap();
												
						user_data.put( Peer.PR_PRIORITY_CONNECTION, new Boolean( true ));
						
						pm.addPeer( service_ip, transfer.getDataPort(), 0, false, user_data );
						
						if ( count[0] < 3 ){
							
							final AERunnable target = this;
							
							SimpleTimer.addEvent(
								"OD:retry",
								SystemTime.getCurrentTime()+5*1000,
								new TimerEventPerformer()
								{
									public void 
									perform(
										org.gudy.azureus2.core3.util.TimerEvent event ) 
									{
										dispatcher.dispatch( target );
									};
								});
						}
					}
				});
		}
	}
	
	protected void
	close()
	{
		super.close();
	
		final AESemaphore sem = new AESemaphore( "DOD:closer" );
		
		dispatcher.dispatch(
			new AERunnable()
			{
				public void 
				runSupport() 
				{
					try{
						closing	= true;
						
						if ( service != null ){
							
							try{
								service.activate( client_id );
								
							}catch( Throwable e ){
								
							}
						}
					}finally{
						
						sem.release();
					}
				}
			});
		
		sem.reserve(250);
	}
	
	public boolean
	isEnabled()
	{
		return( getPersistentBooleanProperty( PP_OD_ENABLED, false ));
	}
	
	public void
	setEnabled(
		boolean	b )
	{
		setPersistentBooleanProperty( PP_OD_ENABLED, b );
		
		if ( b ){
			
			freq_lim_updater.dispatch();
		}
	}

	@Override
	public boolean 
	isAlive() 
	{
		if ( super.isAlive()){
			
				// more restrictive test here to sync alive state with 'appears to be offline'
				// error messages
			
			return( service.getGenericService().isConnectable());
		}
		
		return( false );
	}
	
	public boolean
	hasShownFTUX()
	{
		return( getPersistentBooleanProperty( PP_OD_SHOWN_FTUX, false ));
	}
	
	public void
	setShownFTUX()
	{
		setPersistentBooleanProperty( PP_OD_SHOWN_FTUX, true );
	}
	
	public String
	getManufacturer()
	{
		return( manufacturer );
	}
	
	public long
	getSpaceAvailable(
		boolean		force )
	
		throws DeviceManagerException
	{
		if ( space_on_device >= 0 && !force ){
			
			return( space_on_device );
		}
		
		if ( service == null ){
			
			throw( new DeviceManagerException( "Device is not online" ));
		}
		
		try{
			space_on_device = service.getFreeSpace( client_id );
			
			update_space_outstanding = false;

			return( space_on_device );
			
		}catch( Throwable e ){
			
			throw( new DeviceManagerException( "Failed to read available space", e ));
		}
	}
	
	public int
	getTransferingCount()
	{
		return( transferable.size());
	}
	
	public DeviceOfflineDownload[]
 	getDownloads()
	{
		synchronized( offline_downloads ){
			
			return( offline_downloads.values().toArray( new DeviceOfflineDownload[ offline_downloads.size()]));
		}
	}
 		
 	public void
 	addListener(
 		DeviceOfflineDownloaderListener		listener )
 	{
 		listeners.add( listener );
 	}
 	
 	public void
 	removeListener(
 		DeviceOfflineDownloaderListener		listener )
 	{
 		listeners.remove( listener );
 	}
	       
	protected void
	getDisplayProperties(
		List<String[]>	dp )
	{
		super.getDisplayProperties( dp );
		
		String	space_str = "";
		
		if ( space_on_device >= 0 ){
			
			space_str = DisplayFormatters.formatByteCountToKiBEtc( space_on_device );
		}
		
		addDP( dp, "azbuddy.enabled", isEnabled());
		addDP( dp, "device.od.space", space_str );
	}
	
	protected void
	log(
		DownloadManager		download,	
		String				str )
	{
		log( download.getDisplayName() + ": " + str );
	}
	
	protected void
	log(
		DownloadManager		download,	
		String				str,
		Throwable			e )
	{
		log( download.getDisplayName() + ": " + str, e );
	}
	
	protected void
	log(
		String	str )
	{
		super.log( "OfflineDownloader: " + str );
	}
	
	protected void
	log(
		String		str,
		Throwable	e )
	{
		super.log( "OfflineDownloader: " + str, e );
	}
	
	protected class
	OfflineDownload
		implements DeviceOfflineDownload
	{
		private DownloadManager		core_download;
		private Download			download;
		
		private TransferableDownload	transferable;
		
		protected
		OfflineDownload(
			DownloadManager		_core_download )
		{
			core_download	= _core_download;
			download		= PluginCoreUtils.wrap( core_download );
		}
		
		public Download
		getDownload()
		{
			return( download );
		}
		
		public boolean
		isTransfering()
		{
			return( transferable != null );
		}
		
		public long
		getCurrentTransferSize()
		{
			TransferableDownload t = transferable;
			
			if ( t == null ){
				
				return( 0 );
			}
			
			return( t.getCurrentTransferSize());
		}
		
		public long
		getRemaining()
		{
			TransferableDownload t = transferable;
			
			if ( t == null ){
				
				return( 0 );
			}
			
			return( t.getRemaining());
		}
		
		protected void
		setTransferable(
			TransferableDownload		td )
		{
			transferable = td;
		}
	
		protected TransferableDownload
		getTransferable()
		{
			return( transferable );
		}
	}
	
	protected class
	TransferableDownload
	{
		private DownloadManager		download;
		private String				hash_str;
		private byte[]				have_map;
		
		private boolean				active;
		private long				start_time;	
		private boolean				forced;
		
		private int					data_port;
		
		private long				transfer_size;
		
		private volatile long		last_calc;
		private volatile long		last_calc_time;
		
		protected
		TransferableDownload(
			DownloadManager		_download,
			String				_hash_str,
			byte[]				_have_map,
			long				_transfer_size_estimate )
		{
			download		= _download;
			hash_str		= _hash_str;
			have_map		= _have_map;
			
				// not totally accurate, in general will be > required as based purely on piece
				// size as opposed to blocks. however, we need an initial estimate as the download
				// may not yet be running and therefore we can't get accurate size now
			
			transfer_size 	= _transfer_size_estimate;
			
			last_calc		= transfer_size;
		}
		
		protected long
		calcDiff()
		{
			long	now = SystemTime.getMonotonousTime();
			
			if ( now - last_calc_time < 2*1000 ){
				
				return( last_calc );
			}
			
			DiskManager disk = download.getDiskManager();

			if ( disk == null ){
				
				return( last_calc );
			}
			
			DiskManagerPiece[] pieces = disk.getPieces();
			
			int	pos		= 0;
			int	current	= 0;
			
			long remaining = 0;
			
			for ( int i=0; i<pieces.length; i++ ){
			
				if ( i % 8 == 0 ){
					
					current = have_map[pos++]&0xff;
				}
				
				if (( current & 0x80 ) != 0 ){
					
					DiskManagerPiece piece = pieces[i];
					
					boolean[] written = piece.getWritten();
					
					if ( written == null ){
						
						if ( !piece.isDone()){
					
							remaining += piece.getLength();
						}
					}else{
						
						for (int j=0;j<written.length;j++){
							
							if ( !written[j] ){
								
								remaining += piece.getBlockSize( j );
							}
						}
					}
				}
				
				current <<= 1;
			}
			
			last_calc		= remaining;
			last_calc_time 	= now;
			
			return( last_calc );
		}
		
		protected long
		getCurrentTransferSize()
		{
			return( transfer_size );
		}
		
		protected long
		getRemaining()
		{
			return( calcDiff());
		}
		
		protected long
		getStartTime()
		{
			return( start_time );
		}
		
		protected boolean
		isForced()
		{
			return( forced );
		}
		
		protected boolean
		isActive()
		{
			return( active );
		}
		
		protected int
		getDataPort()
		{
			return( data_port );
		}
		
		protected void
		setDataPort(
			int		dp )
		{
			data_port = dp;
		}
		
		protected void
		activate()
		{
			active		= true;		
			start_time 	= SystemTime.getMonotonousTime();
			
			if ( download.isForceStart()){

				log( download, "Activating for transfer" );
				
			}else{
				
				log( download, "Activating for transfer; setting force-start" );

				forced = true;
								
				download.setForceStart( true );
			}
		}
		
		protected void
		deactivate()
		{
			active = false;
			
			if ( forced ){

				log( download, "Deactivating for transfer; resetting force-start" );
	
				download.setForceStart( false );
				
			}else{
				
				log( download, "Deactivating for transfer" );
			}
			
			data_port	= 0;
		}
		
		protected DownloadManager
		getDownload()
		{
			return( download );
		}
		
		protected String
		getHash()
		{
			return( hash_str );
		}
		
		protected byte[]
		getHaveMap()
		{
			return( have_map );
		}
	}
}
