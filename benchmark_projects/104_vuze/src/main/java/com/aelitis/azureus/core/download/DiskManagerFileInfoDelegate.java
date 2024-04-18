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
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.Arrays;

import org.gudy.azureus2.core3.util.AESemaphore;
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
DiskManagerFileInfoDelegate
	implements DiskManagerFileInfo
{
	private DiskManagerFileInfo		delegate;
	private byte[]					hash;
	
	public
	DiskManagerFileInfoDelegate(
		DiskManagerFileInfo		_delegate )
	
		throws DownloadException
	{
		delegate		= _delegate;
		
		if ( delegate.getDownload() == null ){
			
			throw( new DownloadException( "Not supported" ));
		}
		
		byte[]	delegate_hash = delegate.getDownloadHash();
			
		hash = delegate_hash.clone();
			
		hash[0] ^= 0x01;
	}
	
	public void 
	setPriority(
		boolean b )
	{
		delegate.setPriority( b );
	}
	
	public int 
	getNumericPriorty() 
	{
		return( delegate.getNumericPriorty());
	}
	
	public void 
	setNumericPriority(
		int priority) 
	{
		delegate.setNumericPriority(priority);
	}
	
	public void 
	setSkipped(
		boolean b )
	{
		delegate.setSkipped( b );
	}
	
	public void
	setDeleted(boolean b)
	{
		delegate.setDeleted(b);
	}
	
	public void
	setLink(
		File	link_destination )
	{	
		delegate.setLink( link_destination );
	}
	
	public File
	getLink()
	{
		return( delegate.getLink());
	}
		 	
	public int 
	getAccessMode()
	{
		return( delegate.getAccessMode());
	}
	
	public long 
	getDownloaded()
	{
		return( delegate.getDownloaded());
	}
	
	public long
	getLength()
	{
		return( delegate.getLength());
	}
	
	public File 
	getFile()
	{
		return( delegate.getFile());
	}
	
	public File 
	getFile(
		boolean follow_link ) 
	{
		return( delegate.getFile(follow_link));
	}
	
	public int
	getIndex()
	{
		return( delegate.getIndex());
	}
	
	public int 
	getFirstPieceNumber()
	{
		return( delegate.getFirstPieceNumber());
	}
	
	public long
	getPieceSize()
	{
		return( delegate.getPieceSize());
	}
	
	public int 
	getNumPieces()
	{
		return( delegate.getNumPieces());
	}
		
	public boolean 
	isPriority()
	{
		return( delegate.isPriority());
	}
	
	public boolean 
	isSkipped()
	{
		return( delegate.isSkipped());
	}
	
	public boolean
	isDeleted()
	{
		return( delegate.isDeleted());
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
		return( delegate.createRandomReadRequest( file_offset, length, reverse_order, listener));
	}
	
	private class
	channel
		implements DiskManagerChannel
	{
		private DiskManagerChannel	delegate_channel;
		
		private volatile boolean	channel_destroyed;
		private volatile long		channel_position;
		
		private
		channel()
		
			throws DownloadException
		{
			delegate_channel = delegate.createChannel();
		}
		
		public DiskManagerRequest
		createRequest()
		{
			return( new request());
		}
		
		public DiskManagerFileInfo
		getFile()
		{
			return( DiskManagerFileInfoDelegate.this );
		}
		
		public long 
		getPosition() 
		{
			return( delegate_channel.getPosition());
		}
		
		public boolean 
		isDestroyed() 
		{
			return( delegate_channel.isDestroyed());
		}
		
		public void
		destroy()
		{
			delegate_channel.destroy();
		}
		
		protected class
		request
			implements DiskManagerRequest
		{
			private DiskManagerRequest	delegate_request;
			private volatile boolean	using_delegate;
			
			private long		offset;
			private long		length;
			
			private volatile long	position;
			
			private String		user_agent;

			private int			max_read_chunk = 128*1024;;

			private volatile boolean	cancelled;
			
			
			private CopyOnWriteList<DiskManagerListener>		listeners = new CopyOnWriteList<DiskManagerListener>();
			
			private
			request()
			{
				delegate_request = delegate_channel.createRequest();
			}
			
			public void
			setType(
				int			type )
			{
				if ( type != DiskManagerRequest.REQUEST_READ ){
					
					throw( new RuntimeException( "Not supported" ));
				}
				
				delegate_request.setType( type );
			}
			
			public void
			setOffset(
				long		_offset )
			{
				offset		= _offset;
				
				delegate_request.setOffset( offset ); 
			}
			
			public void
			setLength(
				long		_length )
			{
				if ( _length < 0 ){
					
					throw( new RuntimeException( "Illegal argument" ));
				}
				
				length		= _length;
				
				delegate_request.setLength( length );
			}
				
			public void
			setMaximumReadChunkSize(
				int 	size )
			{
				max_read_chunk = size;
				
				delegate_request.setMaximumReadChunkSize( size );
			}
			
			public void
			setUserAgent(
				String		agent )
			{	
				user_agent	= agent;
				
				delegate_request.setUserAgent( agent );
			}

			public long
			getAvailableBytes()
			{
				if ( using_delegate ){
					
					return( delegate_request.getAvailableBytes());
				}
				
				return( getRemaining());
			}
						
			public long
			getRemaining()
			{
				if ( using_delegate ){
					
					return( delegate_request.getRemaining());
				}
				
				return( offset + length - position );
			}
			
			public void
			run()
			{
				boolean	for_stream = user_agent != null;
				
				if ( for_stream ){
					
					File file = delegate.getFile();
					
					String name = file.getName();
					
					int	dot_pos = name.lastIndexOf('.');
					
					String ext = dot_pos<0?"":name.substring(dot_pos+1);

					for_stream = QTFastStartRAF.isSupportedExtension( ext );
				}
				
				if ( for_stream ){
					
					QTFastStartRAF	raf = null;
					
					try{
						raf = new QTFastStartRAF( getAccessor( max_read_chunk, user_agent ), true );
						
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
							
							position += len;
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
				}else{
					
					using_delegate	= true;
					
					delegate_request.addListener(
						new DiskManagerListener()
						{
							public void
							eventOccurred(
								DiskManagerEvent	event )
							{
								sendEvent( event );
							}
						});
						
					delegate_request.run();
				}
			}
			
			public void
			cancel()
			{
				cancelled = true;
				
				delegate_request.cancel();
			}
						
			protected void
			sendEvent(
				DiskManagerEvent		ev )
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
		
		private QTFastStartRAF.FileAccessor
		getAccessor(
			final int			max_req_size,
			final String		user_agent )
		{
			return( 
				new QTFastStartRAF.FileAccessor()
				{
					private long				seek_position;
					private DiskManagerRequest 	current_request;
					private volatile boolean	closed;
					
					public String
					getName()
					{
						try{
							return( delegate.getDownload().getName() + "/" + delegate.getFile().getName());
							
						}catch( Throwable e ){
							
							Debug.out( e );
							
							return( delegate.getFile().getAbsolutePath());
						}
					}
					
					public long
					getFilePointer()
					
						throws IOException
					{
						return( seek_position );
					}
					
					public void
					seek(
						long		pos )
					
						throws IOException
					{
						seek_position = pos;
					}

					public void
					skipBytes(
						int		num )
					
						throws IOException
					{
						seek_position += num;
					}
					
					public long
					length()
					
						throws IOException
					{
						return( getLength());
					}
					
					public int
					read(
						final byte[]	buffer,
						final int		pos,
						final int		len )
					
						throws IOException
					{
						synchronized( this ){
							
							if ( closed ){
								
								throw( new IOException( "closed" ));
							}
							
							current_request = delegate_channel.createRequest();
						}
						
						current_request.setType( DiskManagerRequest.REQUEST_READ );
						current_request.setOffset( seek_position );
						current_request.setLength( len );
						
						current_request.setMaximumReadChunkSize( max_req_size );
						
						if ( user_agent != null ){
						
							current_request.setUserAgent( user_agent );
						}
						
						final AESemaphore	sem = new AESemaphore( "waiter" );
						final Throwable[]	error = {null};
						
						current_request.addListener(
							new DiskManagerListener()
							{
								private int write_pos 	= pos;
								private int	rem			= len;
								
								public void
								eventOccurred(
									DiskManagerEvent	event )
								{
									int	type = event.getType();
									
									if ( type == DiskManagerEvent.EVENT_TYPE_SUCCESS ){
										
										PooledByteBuffer p_buffer = event.getBuffer();
										
										try{
											ByteBuffer	bb = p_buffer.toByteBuffer();
																					
											bb.position( 0 );
											
											int	read = bb.remaining();

											bb.get( buffer, write_pos, read );
											
											write_pos 	+= read;
											rem			-= read;
											
											if ( rem == 0 ){
												
												sem.release();
											}
										}finally{
											
											p_buffer.returnToPool();
										}
									}else if ( type == DiskManagerEvent.EVENT_TYPE_FAILED ){
									
										error[0] = event.getFailure();
										
										sem.release();
									}
								}
							});
						
						current_request.run();
						
						while( true ){
							
							if ( sem.reserve( 1000 )){
								
								if ( error[0] != null ){
									
									throw( new IOException( Debug.getNestedExceptionMessage( error[0] )));
								}
								
								seek_position += len;
								
								return( len );
								
							}else{
								
								if ( closed ){
									
									throw( new IOException( "Closed" ));
								}
							}
						}
					}
					
					public int
					readInt()
					
						throws IOException
					{
						byte[]	readBuffer = new byte[4];
						
						readFully( readBuffer );
						
						return ((readBuffer[0] << 24) + 
								((readBuffer[1]&0xff) << 16) + 
								((readBuffer[2]&0xff) << 8) + 
								((readBuffer[3]&0xff) << 0));
					}
					
					public long
					readLong()
					
						throws IOException
					{
						byte[]	readBuffer = new byte[8];
						
						readFully( readBuffer );
					  
						return (	((long)readBuffer[0] << 56) +
					                ((long)(readBuffer[1]&0xff) << 48) +
					                ((long)(readBuffer[2]&0xff) << 40) +
					                ((long)(readBuffer[3]&0xff) << 32) +
					                ((long)(readBuffer[4]&0xff) << 24) +
					                ((readBuffer[5]&0xff) << 16) +
					                ((readBuffer[6]&0xff) <<  8) +
					                ((readBuffer[7]&0xff) <<  0));					
					}
					
					public void
					readFully(
						byte[]	buffer )
					
						throws IOException
					{
						read( buffer, 0, buffer.length );
					}
							
					public void
					close()
					
						throws IOException
					{
						synchronized( this ){
						
							closed	= true;
							
							if ( current_request != null ){
								
								current_request.cancel();
							}
						}
					}
				});
		}
	}
}
