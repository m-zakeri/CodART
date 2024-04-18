/*
 * Created on Dec 19, 2006
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
 * AELITIS, SAS au capital de 63.529,40 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */


package com.aelitis.azureus.core.content;

import java.io.InputStream;
import java.net.URL;
import java.util.Map;

import org.gudy.azureus2.core3.torrent.TOTorrent;
import org.gudy.azureus2.core3.torrent.TOTorrentFactory;
import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.plugins.disk.DiskManagerFileInfo;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.download.DownloadAttributeListener;
import org.gudy.azureus2.plugins.torrent.Torrent;
import org.gudy.azureus2.plugins.torrent.TorrentAttribute;
import org.gudy.azureus2.plugins.utils.resourcedownloader.ResourceDownloader;
import org.gudy.azureus2.plugins.utils.resourcedownloader.ResourceDownloaderFactory;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;
import org.gudy.azureus2.pluginsimpl.local.torrent.TorrentImpl;
import org.gudy.azureus2.pluginsimpl.local.utils.resourcedownloader.ResourceDownloaderFactoryImpl;

import com.aelitis.azureus.core.torrent.PlatformTorrentUtils;
import com.aelitis.azureus.core.util.CopyOnWriteList;
import com.aelitis.azureus.util.ConstantsVuze;

/**
 * Used in UPnP for something
 * 
 */
public class 
AzureusPlatformContentDirectory
	implements AzureusContentDirectory
{
	private static boolean registered = false;
	
	private static TorrentAttribute	ta_category;
	
	public static synchronized void
	register()
	{
		if ( !registered ){
		
			registered = true;
			
			ta_category = PluginInitializer.getDefaultInterface().getTorrentManager().getAttribute( TorrentAttribute.TA_CATEGORY );
			
			AzureusContentDirectoryManager.registerDirectory( new AzureusPlatformContentDirectory());
		}
	}
	
	private static CopyOnWriteList<AzureusContentDirectoryListener>	listeners = new CopyOnWriteList<AzureusContentDirectoryListener>();
	
	public AzureusContent
	lookupContent(
		Map		attributes )
	{
		byte[]	hash = (byte[])attributes.get( AT_BTIH );
		
		if ( hash == null ){
			
			return( null );
		}
		
		String	url_str = ConstantsVuze.getDefaultContentNetwork().getTorrentDownloadService( Base32.encode( hash ), null );
		
		ResourceDownloaderFactory rdf = ResourceDownloaderFactoryImpl.getSingleton();
		
		try{
			ResourceDownloader rd = rdf.create( new URL( url_str ));
		
			InputStream	is = rd.download();
			
			try{		
				TOTorrent	torrent = TOTorrentFactory.deserialiseFromBEncodedInputStream( is );
			
				return( new AzureusPlatformContent( new TorrentImpl( torrent )));
				
			}finally{
				
				is.close();
			}
			
		}catch( Throwable e ){
			
			e.printStackTrace();
			
			return( null );
		}
	}
	
	public AzureusContentDownload 
	lookupContentDownload(
		Map 		attributes ) 
	{
		byte[]	hash = (byte[])attributes.get( AT_BTIH );
				
		try{
			final Download download = PluginInitializer.getDefaultInterface().getDownloadManager().getDownload(hash);
		
			if ( download == null ){
				
				return( null );
			}
			
			return( 
				new AzureusContentDownload()
				{
					public Download
					getDownload()
					{
						return( download );
					}
					
					public Object
					getProperty(
						String		name )
					{
						return( null );
					}
				});
			
		}catch( Throwable e ){
			
			return( null );
		}
	}
	
	public AzureusContentFile 
	lookupContentFile(
		Map 		attributes) 
	{
		byte[]	hash 	= (byte[])attributes.get( AT_BTIH );
		int		index	= ((Integer)attributes.get( AT_FILE_INDEX )).intValue();
		
		try{

			Download download = PluginInitializer.getDefaultInterface().getDownloadManager().getDownload(hash);
		
			if ( download == null ){
				
				return( null );
			}
			
			Torrent	t_torrent = download.getTorrent();
			
			if ( t_torrent == null ){
				
				return( null );
			}

			String ud_key = "AzureusPlatformContentDirectory" + ":" + index;
			
			AzureusContentFile acf = (AzureusContentFile)download.getUserData( ud_key );
			
			if ( acf != null ){
				
				return( acf );
			}		
			
			final TOTorrent torrent = ((TorrentImpl)t_torrent).getTorrent();
			
			final DiskManagerFileInfo	file = download.getDiskManagerFileInfo(index);

			if ( PlatformTorrentUtils.isContent( torrent, false )){
			
				acf =
					new AzureusContentFile()
					{
						public DiskManagerFileInfo
						getFile()
						{
							return( file );
						}
						
						public Object
						getProperty(
							String		name )
						{
							try{
								if ( name.equals( PT_DURATION )){
									
									long duration = PlatformTorrentUtils.getContentVideoRunningTime( torrent );
									
									if ( duration > 0 ){
										
											// secs -> millis
										
										return( new Long( duration*1000 ));
									}
								}else if ( name.equals( PT_VIDEO_WIDTH )){
		
									int[] res = PlatformTorrentUtils.getContentVideoResolution(torrent);
									
									if ( res != null ){
										
										return(new Long( res[0]));
									}								
								}else if ( name.equals( PT_VIDEO_HEIGHT )){
		
									int[] res = PlatformTorrentUtils.getContentVideoResolution(torrent);
									
									if ( res != null ){
										
										return(new Long( res[1] ));
									}
								}else if ( name.equals( PT_DATE )){
		
									return( new Long( file.getDownload().getCreationTime()));
									
								}else if ( name.equals( PT_CATEGORIES )){

									try{
										String cat = file.getDownload().getCategoryName();
										
										if ( cat != null && cat.length() > 0 ){
											
											if ( !cat.equalsIgnoreCase( "Categories.uncategorized" )){
											
												return( new String[]{ cat });
											}
										}
									}catch( Throwable e ){
										
									}
									
									return( new String[0] );
									
								}else if ( name.equals( PT_PERCENT_DONE )){
									
									long	size = file.getLength();
									
									return( new Long( size==0?100:(1000*file.getDownloaded()/size )));
									
								}else if ( name.equals( PT_ETA )){							
								
									return( getETA( file ));
								}
							}catch( Throwable e ){							
							}
							
							return( null );
						}
					};
			}else{
				acf =
						new AzureusContentFile()
						{
							public DiskManagerFileInfo
							getFile()
							{
								return( file );
							}
							
							public Object
							getProperty(
								String		name )
							{
								try{
									if ( name.equals( PT_DATE )){
	
										return( new Long( file.getDownload().getCreationTime()));
										
									}else if ( name.equals( PT_CATEGORIES )){

										try{
											String cat = file.getDownload().getCategoryName();
											
											if ( cat != null && cat.length() > 0 ){
												
												if ( !cat.equalsIgnoreCase( "Categories.uncategorized" )){
												
													return( new String[]{ cat });
												}
											}
										}catch( Throwable e ){
											
										}
										
										return( new String[0] );
										
									}else if ( name.equals( PT_PERCENT_DONE )){
										
										long	size = file.getLength();
										
										return( new Long( size==0?100:(1000*file.getDownloaded()/size )));
	
									}else if ( name.equals( PT_ETA )){							
									
										return( getETA( file ));
									}
								}catch( Throwable e ){							
								}
								
								return( null );
							}
						};
			}
			
			download.setUserData( ud_key, acf );
			
			final AzureusContentFile f_acf = acf;
			
			download.addAttributeListener(
				new DownloadAttributeListener()
				{
					public void 
					attributeEventOccurred(
						Download 			download,
						TorrentAttribute 	attribute, 
						int 				eventType ) 
					{
						fireChanged( f_acf );
					}
				},
				ta_category,
				DownloadAttributeListener.WRITTEN );
			
			return( acf );
			
		}catch( Throwable e ){
			
			return( null );
		}
	}
	
	protected long
	getETA(
		DiskManagerFileInfo		file )
	{
		try{
			if ( file.getDownloaded() == file.getLength()){
				
				return( 0 );
			}
			
			if ( file.isDeleted() || file.isSkipped()){
				
				return( Long.MAX_VALUE );
			}
		
			long eta = file.getDownload().getStats().getETASecs();
			
			if ( eta < 0 ){
				
				return( Long.MAX_VALUE );
			}
			
			return( eta );
			
		}catch( Throwable e ){
			
			return( Long.MAX_VALUE );
		}
	}
	
	public static void
	fireChanged(
		AzureusContentFile	acf )
	{
		for ( AzureusContentDirectoryListener l: listeners ){
			
			l.contentChanged( acf, AzureusContentFile.PT_CATEGORIES );
		}
	}
	
	public void 
	addListener(
		AzureusContentDirectoryListener listener ) 
	{
		listeners.add( listener );
	}
	
	public void 
	removeListener(
		AzureusContentDirectoryListener listener )
	{
		listeners.remove( listener );
	}
	
	protected class
	AzureusPlatformContent
		implements AzureusContent
	{
		private Torrent	torrent;
		
		protected
		AzureusPlatformContent(
			Torrent		_torrent )
		{
			torrent	= _torrent;
		}
		
		public Torrent
		getTorrent()
		{
			return( torrent );
		}
	}
}
