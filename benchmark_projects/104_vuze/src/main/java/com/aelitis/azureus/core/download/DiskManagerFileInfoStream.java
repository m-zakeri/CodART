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

import java.io.*;
import java.util.*;

import org.gudy.azureus2.core3.util.AESemaphore;
import org.gudy.azureus2.core3.util.AEThread2;
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

public class 
DiskManagerFileInfoStream
	implements DiskManagerFileInfo
{
	private StreamFactory		stream_factory;
	private File				save_to;
	private byte[]				hash;
	
	private context				current_context;
	
	private Object	lock = this;
	
	public
	DiskManagerFileInfoStream(
		StreamFactory		_stream_factory,
		File				_save_to )
	{
		stream_factory		= _stream_factory;
		save_to				= _save_to;
		
		try{
			hash		= new SHA1Simple().calculateHash( _save_to.getAbsolutePath().getBytes( "UTF-8" ));
			
		}catch( Throwable e ){
			
			Debug.out(e);
		}
	}
	
	public boolean
	isComplete()
	{
		synchronized( lock ){

			return( save_to.exists());
		}
	}
	
	public void
	reset()
	{
		synchronized( lock ){

			if ( current_context != null ){
				
				current_context.destroy( new Exception( "Reset" ));
			}
			
			save_to.delete();
		}
	}
	
	public void 
	setPriority(
		boolean b )
	{
	}
	
	public void 
	setSkipped(
		boolean b )
	{
		throw( new RuntimeException( "Not supported" ));
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
		return( -1 );
	}
	
	public File 
	getFile()
	{
		return( save_to );
	}
		
	public File
	getFile(
		boolean	follow_link )
	{
		return( save_to );
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
		return( -1 );
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
	
		throws DownloadException 
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
		try{
			synchronized( lock ){
				
				if ( current_context == null ){
					
					current_context = new context();
				}
				
				return( current_context.createChannel());
			}
		}catch( Throwable e ){
			
			throw( new DownloadException( "Channel creation failed", e ));
		}
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
	
	protected void
	destroyed(
		context		c )
	{
		synchronized( lock ){
			
			if ( current_context == c ){
				
				current_context = null;
			}
		}
		
		stream_factory.destroyed( c );
	}
	
	protected class
	context
	{
		private RandomAccessFile				raf;
		private StreamFactory.StreamDetails		stream_details;
		
		private boolean				stream_got_eof;
		
		private List<channel>		channels	= new ArrayList<channel>();

		private List<AESemaphore>	waiters 	= new ArrayList<AESemaphore>();
		
		private boolean				context_destroyed;
		
		protected
		context()
		
			throws Exception
		{
			if ( save_to.exists()){
				
				raf = new RandomAccessFile( save_to, "r" );
				
				stream_got_eof = true;
				
			}else{
				
				final File	temp_file = new File( save_to.getAbsolutePath() + "._tmp_" );
				
				raf = new RandomAccessFile( temp_file, "rw" );

				stream_details = stream_factory.getStream( this );
				
				final InputStream stream = stream_details.getStream();
				
				new AEThread2( "DMS:reader", true )
				{
					public void
					run()
					{
						final int BUFF_SIZE = 128*1024;
						
						byte[]	buffer = new byte[BUFF_SIZE];
						
						try{
							while( true ){
								
								int len = stream.read( buffer );
								
								if ( len <= 0 ){
									
									if ( stream_details.hasFailed()){
										
										throw( new IOException( "Stream failed" ));
									}
									
									stream_got_eof	= true;
									
									break;
								}
								
								synchronized( lock ){
									
									raf.seek( raf.length());
									
									raf.write( buffer, 0, len );
									
									for ( AESemaphore waiter: waiters ){
										
										waiter.release();
									}
								}
							}								
						}catch( Throwable e ){
															
							context.this.destroy( e );
							
						}finally{
							
							try{
								stream.close();
																	
							}catch( Throwable e ){
								
							}
							
							Throwable failed = null;
							
							synchronized( lock ){
								
								stream_details = null;
								
								if ( stream_got_eof ){
									
									try{
										raf.close();
										
										save_to.delete();
										
										temp_file.renameTo( save_to );
										
										raf = new RandomAccessFile( save_to, "r" );
										
									}catch( Throwable e ){
																					
										failed = e;
									}
								}
							}
							
							if ( failed != null ){
								
								context.this.destroy( failed );
							}
						}
					}
				}.start();
			}
		}
		
		protected int
		read(
			byte[]		buffer,
			long		offset,
			int			length )
		
			throws IOException
		{
			AESemaphore	sem;
			
			synchronized( lock ){
				
				if ( raf.length() > offset ){
					
					raf.seek( offset );
					
					return( raf.read( buffer, 0, length ));
				}	
				
				if ( stream_details == null ){
					
					if ( stream_got_eof ){
						
						return( -1 );
					}
					
					throw( new IOException( "Premature end of stream (read)" ));
				}
				
				sem = new AESemaphore( "DMS:block" );
				
				waiters.add( sem );
			}
			
			try{
				sem.reserve( 1000 );
			
			}finally{
			
				synchronized( lock ){

					waiters.remove( sem );
				}
			}
			
			return( 0 );
		}
		
		protected channel
		createChannel()
		{
			synchronized( lock ){

				channel c = new channel();
				
				channels.add( c );
				
				return( c );
			}
		}
		
		protected void
		removeChannel(
			channel	c )
		{
			synchronized( lock ){

				channels.remove( c );
			
				if ( channels.size() == 0 && save_to.exists()){
					
					destroy( null );
				}
			}
		}
		
		protected void
		destroy(
			Throwable error )
		{
			if ( error != null ){
				
				Debug.out( error );
			}
			
			synchronized( lock ){

				if ( context_destroyed ){
					
					return;
				}
				
				context_destroyed = true;
				
				if ( channels != null ){
					
					List<channel> channels_copy = new ArrayList<channel>( channels );
					
					for ( channel c: channels_copy ){
						
						c.destroy();
					}
				}
				
				if ( raf != null ){
					
					try{
						raf.close();
						
					}catch( Throwable e ){
					}
					
					raf = null;
				}
				
				if ( stream_details != null ){
					
					try{
						stream_details.getStream().close();
						
					}catch( Throwable e ){
						
					}
					
					stream_details = null;
				}
				
				if ( error != null ){
				
					save_to.delete();
				}
			}
			
			DiskManagerFileInfoStream.this.destroyed( this );
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
				return( DiskManagerFileInfoStream.this );
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
				
				removeChannel( this );
			}
			
			protected class
			request
				implements DiskManagerRequest
			{
				private long		offset;
				private long		length;
				
				private long		position;
				
				private int			max_read_chunk = 128*1024;;
				
				private volatile boolean	request_cancelled;
				
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
						// length can be -1 here meaning 'to the end'
					
					length		= _length==-1?Long.MAX_VALUE:_length;
				}
					
				public void
				setMaximumReadChunkSize(
					int 	size )
				{
					if ( size > 16*1024 ){
					
						max_read_chunk = size;
					}
				}
				
				public long
				getAvailableBytes()
				{
					return( getRemaining());
				}
							
				public long
				getRemaining()
				{
					return( length==Long.MAX_VALUE?length:(offset + length - position ));
				}
				
				public void
				run()
				{
					try{				
						byte[] buffer = new byte[max_read_chunk];
						
						long	rem		= length;
						long	pos 	= offset;
						
						while( rem > 0 ){
							
							if ( request_cancelled ){
								
								throw( new Exception( "Cancelled" ));
								
							}else if ( channel_destroyed ){
								
								throw( new Exception( "Destroyed" ));
							}
							
							int	chunk = (int)Math.min( rem, max_read_chunk );
							
							int	len = read( buffer, pos, chunk );
								
							if ( len == -1 ){
								
								if ( length == Long.MAX_VALUE ){
									
									break;
									
								}else{
									
									throw( new Exception( "Premature end of stream (complete)" ));
								}
							}else if ( len == 0 ){
								
								sendEvent( new event( pos ));
								
							}else{
																
								sendEvent( new event( new PooledByteBufferImpl( buffer, 0, len ), pos, len ));
								
								rem -= len;
								pos	+= len;
							}
						}
					}catch( Throwable e ){
						
						sendEvent( new event( e ));
					}
				}
				
				public void
				cancel()
				{
					request_cancelled = true;
				}
				
				public void
				setUserAgent(
					String		agent )
				{	
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
						long				_offset )
					{
						event_type		= DiskManagerEvent.EVENT_TYPE_BLOCKED;

						event_offset	= _offset;	
						
						channel_position	= _offset;
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
						
						channel_position	= _offset + _length - 1;
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

	public interface
	StreamFactory
	{
		public StreamDetails
		getStream(
			Object		requester )
		
			throws IOException;
		
		public void
		destroyed(
			Object		requester );
		
		public interface
		StreamDetails
		{
			public InputStream
			getStream();
			
			public boolean
			hasFailed();
		}
	}
}
