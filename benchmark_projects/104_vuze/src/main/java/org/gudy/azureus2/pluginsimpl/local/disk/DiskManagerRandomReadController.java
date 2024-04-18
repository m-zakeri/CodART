/*
 * Created on Oct 10, 2012
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


package org.gudy.azureus2.pluginsimpl.local.disk;

import java.util.*;

import org.gudy.azureus2.core3.disk.DiskManager;
import org.gudy.azureus2.core3.disk.DiskManagerFileInfoListener;
import org.gudy.azureus2.core3.disk.DiskManagerPiece;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.peer.PEPeer;
import org.gudy.azureus2.core3.peer.PEPeerManager;
import org.gudy.azureus2.core3.peer.PEPiece;
import org.gudy.azureus2.core3.torrent.TOTorrent;
import org.gudy.azureus2.core3.torrent.TOTorrentFile;
import org.gudy.azureus2.core3.util.AERunnable;
import org.gudy.azureus2.core3.util.AESemaphore;
import org.gudy.azureus2.core3.util.AsyncDispatcher;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.DirectByteBuffer;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.plugins.disk.DiskManagerEvent;
import org.gudy.azureus2.plugins.disk.DiskManagerListener;
import org.gudy.azureus2.plugins.disk.DiskManagerRandomReadRequest;
import org.gudy.azureus2.plugins.download.DownloadException;
import org.gudy.azureus2.plugins.utils.PooledByteBuffer;
import org.gudy.azureus2.pluginsimpl.local.download.DownloadImpl;
import org.gudy.azureus2.pluginsimpl.local.utils.PooledByteBufferImpl;

import com.aelitis.azureus.core.peermanager.piecepicker.PiecePicker;

public class 
DiskManagerRandomReadController 
{
	private static Map<DownloadImpl, DiskManagerRandomReadController>	controller_map = new HashMap<DownloadImpl, DiskManagerRandomReadController>();
	
	public static DiskManagerRandomReadRequest
	createRequest(
		DownloadImpl				download,
		DiskManagerFileInfoImpl		file,
		long						file_offset,
		long						length,
		boolean						reverse_order,
		DiskManagerListener			listener )
	
		throws DownloadException
	{
		DiskManagerRandomReadController controller;
		
		synchronized( controller_map ){
			
			controller = controller_map.get( download );
			
			if ( controller == null ){
				
				controller = new DiskManagerRandomReadController( download );
				
				controller_map.put( download, controller );
			}
		}
		
		return( controller.addRequest( file, file_offset, length, reverse_order, listener ));
	}
	
	private DownloadImpl		download;
	
	private List<DiskManagerRandomReadRequestImpl>	requests = new ArrayList<DiskManagerRandomReadRequestImpl>();
	
	private AsyncDispatcher	dispatcher = new AsyncDispatcher();
	
	private
	DiskManagerRandomReadController(
		DownloadImpl		_download )
	{
		download	= _download;
	}
	
	private DiskManagerRandomReadRequest
	addRequest(
		DiskManagerFileInfoImpl		file,
		long						file_offset,
		long						length,
		boolean						reverse_order,
		DiskManagerListener			listener )
	{
		DiskManagerRandomReadRequestImpl request = new DiskManagerRandomReadRequestImpl( file, file_offset, length, reverse_order, listener );
		
		synchronized( requests ){
			
			requests.add( request );
		}
		
		dispatcher.dispatch(
			new AERunnable()
			{
				public void
				runSupport()
				{
					executeRequest();
				}
			});
		
		return( request );
	}

	private void
	executeRequest()
	{
		DiskManagerRandomReadRequestImpl	request;
	
		synchronized( requests ){
			
			if ( requests.isEmpty()){
				
				return;
			}
			
			request = requests.remove( 0 );
		}
		
		if ( request.isCancelled()){
			
			return;
		}
		
		boolean 					set_force_start = false;
		DiskManagerFileInfoListener	info_listener	= null;
		
		org.gudy.azureus2.core3.disk.DiskManagerFileInfo core_file		= request.getFile().getCore();

		DownloadManager core_download = core_file.getDownloadManager();

		int			prev_hint_piece	= -1;
		int			curr_hint_piece = -1;

		try{
			
			if ( core_download.getTorrent() == null ){
				
				throw( new DownloadException( "Torrent invalid" ));
			}
			
			if ( core_download.isDestroyed()){
				
				Debug.out( "Download has been removed" );
				
				throw( new DownloadException( "Download has been removed" ));
			}
					
			TOTorrentFile	tf = core_file.getTorrentFile();
			
			TOTorrent 	torrent = tf.getTorrent();
			
			TOTorrentFile[]	tfs = torrent.getFiles();
										
			long	core_file_start_byte = 0;
			
			for (int i=0;i<core_file.getIndex();i++){
					
				core_file_start_byte += tfs[i].getLength();
			}
			
			long download_byte_start 	= core_file_start_byte + request.getOffset();
			long download_byte_end		= download_byte_start + request.getLength();
			
			int piece_size	= (int)tf.getTorrent().getPieceLength();
			
			if ( core_file.getDownloaded() != core_file.getLength()){
				
				if ( core_file.isSkipped()){
					
					core_file.setSkipped( false );
				}
				
				boolean	force_start = download.isForceStart();
				
				if ( !force_start ){
										
					download.setForceStart( true );
					
					set_force_start = true;
				}
			}
			
			boolean	is_reverse = request.isReverse();
			
			final AESemaphore	wait_sem = new AESemaphore( "rr:waiter" );
			
			info_listener = new 
				DiskManagerFileInfoListener()
				{
					public void
					dataWritten(
						long	offset,
						long	length )
					{
						wait_sem.release();
					}
					
					public void
					dataChecked(
						long	offset,
						long	length )
					{	
					}
				};
				
			long 		start_time 		= SystemTime.getMonotonousTime();
			boolean		has_started		= false;
						
			core_file.addListener( info_listener );
			
			//System.out.println( "Request starts" );
			
			while( download_byte_start < download_byte_end ){
				
				if ( request.isCancelled()){
					
					throw( new Exception( "request cancelled" ));
				}
				
				//System.out.println( "Request current: " + download_byte_start + " -> " + download_byte_end );

				long	now = SystemTime.getMonotonousTime();
				
				int	piece_start 		= (int)( download_byte_start / piece_size );
				int	piece_start_offset	= (int)( download_byte_start % piece_size );
				
				int	piece_end	 		= (int)( ( download_byte_end - 1 ) / piece_size );
				int	piece_end_offset 	= (int)( ( download_byte_end - 1 ) % piece_size ) + 1;	

				//System.out.println( "    piece details: " + piece_start + "/" + piece_start_offset + " -> " + piece_end + "/" + piece_end_offset );
				
				DiskManagerPiece[] pieces = null;
				
				DiskManager disk_manager = core_download.getDiskManager();
				
				if ( disk_manager != null ){
					
					pieces = disk_manager.getPieces();					
				}
				
				long	avail_start;
				long	avail_end;
				
				if ( pieces == null ){
					
					if ( core_file.getDownloaded() == core_file.getLength()){
						
						avail_start = download_byte_start;
						avail_end	= download_byte_end;
						
					}else{
						
						if ( now - start_time < 10000 && !has_started ){
							
							wait_sem.reserve( 250 );
							
							continue;
						}
						
						throw( new Exception( "download stopped" ));
					}
				}else{
					
					has_started = true;

					if ( is_reverse ){
						
						long	min_done = download_byte_end;
						
						for ( int i=piece_end; i>= piece_start; i-- ){
						
							int	p_start = i==piece_start?piece_start_offset:0;
							int	p_end 	= i==piece_end?piece_end_offset:piece_size;
							
							DiskManagerPiece piece = pieces[i];
							
							boolean[] done = piece.getWritten();
							
							if ( done == null ){
								
								if ( piece.isDone()){
									
									min_done = i*piece_size;
									
									continue;
									
								}else{
									
									break;
								}
							}
							
							int	block_size = piece.getBlockSize( 0 );
							
							int	first_block = p_start/block_size;
							int	last_block 	= (p_end-1)/block_size;
														
							for ( int j=last_block;j>=first_block;j--){
								
								if ( done[j] ){
									
									min_done = i*piece_size + j*block_size;
									
								}else{
									
									break;
								}
							}
						}
						
						avail_start = Math.max( download_byte_start, min_done );
						avail_end	= download_byte_end;
					}else{
						
						long	max_done = download_byte_start;
						
						for ( int i=piece_start; i <= piece_end; i++ ){
						
							int	p_start = i==piece_start?piece_start_offset:0;
							int	p_end 	= i==piece_end?piece_end_offset:piece_size;
							
							DiskManagerPiece piece = pieces[i];
							
							boolean[] done = piece.getWritten();
							
							if ( done == null ){
								
								if ( piece.isDone()){
									
									max_done = (i+1)*piece_size;
									
									continue;
									
								}else{
									
									break;
								}
							}
							
							int	block_size = piece.getBlockSize( 0 );
							
							int	first_block = p_start/block_size;
							int	last_block 	= (p_end-1)/block_size;
														
							for ( int j=first_block;j<=last_block;j++){
								
								if ( done[j] ){
									
									max_done = i*piece_size + (j+1)*block_size;
									
								}else{
									
									break;
								}
							}
						}
						
						avail_start = download_byte_start;
						avail_end	= Math.min( download_byte_end, max_done );			
					}
				}
				
				//System.out.println( "    avail: " + avail_start + " -> " + avail_end );
						
				int max_chunk = 128*1024;
								
				if ( avail_end > avail_start ){
					
					long length = avail_end - avail_start;
					
					if ( length > max_chunk ){
												
						if ( is_reverse ){
						
							avail_start = avail_end - max_chunk;
							
						}else{
							
							avail_end	= avail_start + max_chunk;
						}
					}
					
					//System.out.println( "got data: " + avail_start + " -> " + avail_end );
					
					long	read_offset = avail_start - core_file_start_byte;
					int		read_length	= (int)( avail_end - avail_start );
					
					DirectByteBuffer buffer = core_file.read( read_offset, read_length );
					
					request.dataAvailable( buffer, read_offset, read_length );
						
					if ( is_reverse ){
						
						download_byte_end = avail_start;
						
					}else{
						
						download_byte_start = avail_end;
					}
					
					continue;
				}
				
				PEPeerManager pm = core_download.getPeerManager();
				
				if ( pm == null ){
					
					if ( now - start_time < 10000 && !has_started ){
						
						wait_sem.reserve( 250 );
						
						continue;
					}
					
					throw( new Exception( "download stopped" ));
					
				}else{
					
					has_started = true;
				}
				
				PiecePicker picker = pm.getPiecePicker();
				
				picker.setReverseBlockOrder( is_reverse );
				
				int	hint_piece;
				int	hint_offset;
				int	hint_length;
				
				if ( piece_start == piece_end ){
					
					hint_piece	= piece_start;
					hint_offset = piece_start_offset;
					hint_length	= piece_end_offset - piece_start_offset;
					
				}else{
					
					if ( is_reverse ){
					
						hint_piece 	= piece_end;
						hint_offset = 0;
						hint_length	= piece_end_offset;
	
					}else{
					
						hint_piece	= piece_start;
						hint_offset = piece_start_offset;
						hint_length	= piece_size - piece_start_offset;
					}
				}
				
				if ( curr_hint_piece == -1 ){
					
					int[] existing = picker.getGlobalRequestHint();
					
					if ( existing != null ){
						
						curr_hint_piece = existing[0];
					}
				}
				
				//System.out.println( "hint: " + hint_piece + "/" + hint_offset + "/" + hint_length + ": curr=" + curr_hint_piece + ", prev=" + prev_hint_piece );
				
				picker.setGlobalRequestHint( hint_piece, hint_offset, hint_length );
				
				if ( hint_piece != curr_hint_piece ){
					
					prev_hint_piece = curr_hint_piece;
					
					curr_hint_piece = hint_piece;
				}			
				
				if ( prev_hint_piece != -1  ){
				
					clearHint( pm, prev_hint_piece );
				}
				
				wait_sem.reserve( 250 );
			}
		}catch( Throwable e ){
			
			request.failed( e );
			
		}finally{
			
			PEPeerManager pm = core_download.getPeerManager();
			
			if ( pm != null ){

				PiecePicker picker = pm.getPiecePicker();
				
				if ( picker != null ){
					
					picker.setReverseBlockOrder( false );
					
					picker.setGlobalRequestHint( -1, 0, 0 );
					
					if ( curr_hint_piece != -1  ){
						
						clearHint( pm, curr_hint_piece );
					}
				}
			}
			
			if ( set_force_start ){
				
				download.setForceStart( false );
			}
			
			if ( info_listener != null ){
				
				core_file.removeListener( info_listener );
			}
		}
	}
	
	private void
	clearHint(
		PEPeerManager	pm,
		int				hint_piece )
	{
		PEPiece piece = pm.getPiece( hint_piece );
		
		if ( piece != null && piece.getReservedBy() != null ){
		
			piece.setReservedBy( null );
			
			//System.out.println( "clearing res by for " + hint_piece );
		}
		
		List<PEPeer> peers = pm.getPeers();
		
		for ( PEPeer peer: peers ){
			
			int[] res = peer.getReservedPieceNumbers();
			
			if ( res != null ){
				
				for ( int i: res ){
					
					if ( i == hint_piece ){
						
						peer.removeReservedPieceNumber( hint_piece );
						
						//System.out.println( "removing res by on " + peer.getIp() + " for " + hint_piece );
					}
				}
			}
		}
	}
	private class
	DiskManagerRandomReadRequestImpl
		implements DiskManagerRandomReadRequest
	{
		private DiskManagerFileInfoImpl		file;
		private long						file_offset;
		private long						length;
		private boolean						reverse_order;
		private DiskManagerListener			listener;
		
		private volatile boolean	cancelled;
		private boolean				failed;
		
		private
		DiskManagerRandomReadRequestImpl(
			DiskManagerFileInfoImpl		_file,
			long						_file_offset,
			long						_length,
			boolean						_reverse_order,
			DiskManagerListener			_listener )
		{
			file			= _file;
			file_offset		= _file_offset;
			length			= _length;
			reverse_order	= _reverse_order;
			listener		= _listener;
		}
		
		public DiskManagerFileInfoImpl
		getFile()
		{
			return( file );
		}
		
		public long
		getOffset()
		{
			return( file_offset );
		}
		
		public long
		getLength()
		{
			return( length );
		}
		
		public boolean
		isReverse()
		{
			return( reverse_order );
		}
		
		private boolean
		isCancelled()
		{
			return( cancelled );
		}
		
		public void
		cancel()
		{
			synchronized( requests ){
				
				requests.remove( this );
			
				cancelled = true;
			}
							
			failed( new Exception( "request cancelled" ));
		}
		
		private void
		dataAvailable(
			DirectByteBuffer		buffer,
			final long				offset,
			final int				length )
		{
			final PooledByteBuffer p_buffer = new PooledByteBufferImpl( buffer );
			
			listener.eventOccurred(
				new DiskManagerEvent()
				{
					public int
					getType()
					{
						return( EVENT_TYPE_SUCCESS );
					}
					
					public long
					getOffset()
					{
						return( offset );
					}
					
					public int
					getLength()
					{
						return( length );
					}
					
					public PooledByteBuffer
					getBuffer()
					{
						return( p_buffer );
					}
					
					public Throwable
					getFailure()
					{
						return( null );
					}
				});
		}
		
		private void
		failed(
			final Throwable e )
		{
			Debug.out(e );
			
			synchronized( requests ){
				
				if ( failed ){
					
					return;
				}
				
				failed = true;
			}
			
			listener.eventOccurred(
				new DiskManagerEvent()
				{
					public int
					getType()
					{
						return( EVENT_TYPE_FAILED );
					}
					
					public long
					getOffset()
					{
						return( -1 );
					}
					
					public int
					getLength()
					{
						return( -1 );
					}
					
					public PooledByteBuffer
					getBuffer()
					{
						return( null );
					}
					
					public Throwable
					getFailure()
					{
						return( e );
					}
				});
		}
	}
}
