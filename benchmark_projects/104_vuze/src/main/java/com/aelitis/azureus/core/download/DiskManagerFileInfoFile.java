/*
 * Created on Feb 11, 2009
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


package com.aelitis.azureus.core.download;

import java.io.File;

import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.SHA1Simple;
import org.gudy.azureus2.plugins.disk.DiskManagerChannel;
import org.gudy.azureus2.plugins.disk.DiskManagerEvent;
import org.gudy.azureus2.plugins.disk.DiskManagerFileInfo;
import org.gudy.azureus2.plugins.disk.DiskManagerListener;
import org.gudy.azureus2.plugins.disk.DiskManagerRandomReadRequest;
import org.gudy.azureus2.plugins.disk.DiskManagerRequest;
import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.download.DownloadException;
import org.gudy.azureus2.plugins.utils.PooledByteBuffer;
import org.gudy.azureus2.pluginsimpl.local.utils.PooledByteBufferImpl;

import com.aelitis.azureus.core.util.CopyOnWriteList;
import com.aelitis.azureus.core.util.QTFastStartRAF;

public class 
DiskManagerFileInfoFile
	implements DiskManagerFileInfo
{
	private byte[]		hash;
	private File		file;
	
	public
	DiskManagerFileInfoFile(
		File		_file )
	{
		file		= _file;
		
		try{
			hash		= new SHA1Simple().calculateHash( file.getAbsolutePath().getBytes( "UTF-8" ));
			
		}catch( Throwable e ){
			
			Debug.out(e);
		}
	}
	
	public void 
	setPriority(
		boolean b )
	{
	}
	
	public int 
	getNumericPriorty() 
	{
		return( 0 );
	}
	
	public void 
	setNumericPriority(
		int priority) 
	{
		throw( new RuntimeException( "Not supported" ));
	}
	
	public void 
	setSkipped(
		boolean b )
	{
		throw( new RuntimeException( "Not supported" ));
	}
	
	public void
	setDeleted(boolean b)
	{
	}
	
	
	public void
	setLink(
		File	link_destination )
	{	
		throw( new RuntimeException( "Not supported" ));
	}
	
	public File
	getLink()
	{
		return( null );
	}
		 	
	public int 
	getAccessMode()
	{
		return( READ );
	}
	
	public long 
	getDownloaded()
	{
		return( getLength());
	}
	
	public long
	getLength()
	{
		return( file.length());
	}
	
	public File 
	getFile()
	{
		return( file );
	}
	
	public File 
	getFile(
		boolean follow_link ) 
	{
		return( file );
	}
	
	public int
	getIndex()
	{
		return( 0 );
	}
	
	public int 
	getFirstPieceNumber()
	{
		return( 0 );
	}
	
	public long
	getPieceSize()
	{
		return( 32*1024 );
	}
	
	public int 
	getNumPieces()
	{
		long	piece_size = getPieceSize();
		
		return((int)(( getLength() + piece_size - 1 ) / piece_size ));
	}
		
	public boolean 
	isPriority()
	{
		return( false );
	}
	
	public boolean 
	isSkipped()
	{
		return( false );
	}
	
	public boolean
	isDeleted()
	{
		return( false );
	}
	
	public byte[] 
	getDownloadHash()
    {
		return( hash );
    }
	
	public Download 
	getDownload()
	
      throws DownloadException
    {
		throw( new DownloadException( "Not supported" ));
    }
	
	public DiskManagerChannel
	createChannel()
	
		throws DownloadException
	{
		return( new channel());
	}
	
	public DiskManagerRandomReadRequest
	createRandomReadRequest(
		long						file_offset,
		long						length,
		boolean						reverse_order,
		DiskManagerListener			listener )
	
		throws DownloadException
	{
		throw( new DownloadException( "Not supported" ));
	}
	
	protected class
	channel
		implements DiskManagerChannel
	{
		private volatile boolean	channel_destroyed;
		private volatile long		channel_position;
		
		public DiskManagerRequest
		createRequest()
		{
			return( new request());
		}
		
		public DiskManagerFileInfo
		getFile()
		{
			return( DiskManagerFileInfoFile.this );
		}
		
		public long 
		getPosition() 
		{
			return( channel_position );
		}
		
		public boolean 
		isDestroyed() 
		{
			return( channel_destroyed );
		}
		
		public void
		destroy()
		{
			channel_destroyed	= true;
		}
		
		protected class
		request
			implements DiskManagerRequest
		{
			private long		offset;
			private long		length;
			
			private long		position;
			
			private int			max_read_chunk = 128*1024;;

			private volatile boolean	cancelled;
			
			private String		user_agent;
			
			private CopyOnWriteList<DiskManagerListener>		listeners = new CopyOnWriteList<DiskManagerListener>();
			
			public void
			setType(
				int			type )
			{
				if ( type != DiskManagerRequest.REQUEST_READ ){
					
					throw( new RuntimeException( "Not supported" ));
				}
			}
			
			public void
			setOffset(
				long		_offset )
			{
				offset		= _offset;
			}
			
			public void
			setLength(
				long		_length )
			{
				if ( _length < 0 ){
					
					throw( new RuntimeException( "Illegal argument" ));
				}
				
				length		= _length;
			}
				
			public void
			setMaximumReadChunkSize(
				int 	size )
			{
				max_read_chunk = size;
			}
			
			public void
			setUserAgent(
				String		agent )
			{	
				user_agent	= agent;
			}

			
			public long
			getAvailableBytes()
			{
				return( getRemaining());
			}
						
			public long
			getRemaining()
			{
				return( offset + length - position );
			}
			
			public void
			run()
			{
				QTFastStartRAF	raf = null;
				
				String name = file.getName();
				
				int	dot_pos = name.lastIndexOf('.');
				
				String ext = dot_pos<0?"":name.substring(dot_pos+1);
				
				try{
					raf = new QTFastStartRAF( file, user_agent != null && QTFastStartRAF.isSupportedExtension( ext ));
					
					raf.seek( offset );
			
					byte[] buffer = new byte[max_read_chunk];
					
					long	rem		= length;
					long	pos 	= offset;
					
					while( rem > 0 ){
						
						if ( cancelled ){
							
							throw( new Exception( "Cancelled" ));
							
						}else if ( channel_destroyed ){
							
							throw( new Exception( "Destroyed" ));
						}
						
						int	chunk = (int)Math.min( rem, max_read_chunk );
						
						int	len = raf.read( buffer, 0, chunk );
												
						sendEvent( new event( new PooledByteBufferImpl( buffer, 0, len ), pos, len ));
						
						rem -= len;
						pos	+= len;
					}
				}catch( Throwable e ){
					
					sendEvent( new event( e ));
					
				}finally{
					
					if ( raf != null ){
						
						try{
							raf.close();
							
						}catch( Throwable e ){
							
							Debug.out( e );
						}
					}
				}
			}
			
			public void
			cancel()
			{
				cancelled = true;
			}
						
			protected void
			sendEvent(
				event		ev )
			{					
				for ( DiskManagerListener l: listeners ){
					
					l.eventOccurred( ev );
				}
			}
			
			public void
			addListener(
				DiskManagerListener	listener )
			{
				listeners.add( listener );
			}
			
			public void
			removeListener(
				DiskManagerListener	listener )
			{
				listeners.remove( listener );
			}
		
			protected class
			event
				implements DiskManagerEvent
			{
				private int					event_type;
				private Throwable			error;
				private PooledByteBuffer	buffer;
				private long				event_offset;
				private int					event_length;
				
				protected
				event(
					Throwable		_error )
				{
					event_type	= DiskManagerEvent.EVENT_TYPE_FAILED;
					error		= _error;
				}
								
				protected
				event(
					PooledByteBuffer	_buffer,
					long				_offset,
					int					_length )
				{
					event_type		= DiskManagerEvent.EVENT_TYPE_SUCCESS;
					buffer			= _buffer;
					event_offset	= _offset;
					event_length	= _length;
					
					channel_position = _offset + _length - 1;
				}
				
				public int
				getType()
				{
					return( event_type );
				}
				
				public DiskManagerRequest
				getRequest()
				{
					return( request.this );
				}
				
				public long
				getOffset()
				{
					return( event_offset );
				}
				
				public int
				getLength()
				{
					return( event_length );
				}
				
				public PooledByteBuffer
				getBuffer()
				{
					return( buffer );
				}
				
				public Throwable
				getFailure()
				{
					return( error );
				}
			}
		}
	}
}
