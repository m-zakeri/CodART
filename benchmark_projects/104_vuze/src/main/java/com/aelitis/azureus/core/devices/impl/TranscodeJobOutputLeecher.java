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


package com.aelitis.azureus.core.devices.impl;

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

import com.aelitis.azureus.core.devices.TranscodeException;
import com.aelitis.azureus.core.devices.TranscodeJob;
import com.aelitis.azureus.core.util.CopyOnWriteList;

public class 
TranscodeJobOutputLeecher
	implements DiskManagerFileInfo
{	
	private TranscodeJobImpl		job;
	private TranscodeFileImpl		file;
	
	private File	save_to;
	private byte[]	hash;
	
	public
	TranscodeJobOutputLeecher(
		TranscodeJobImpl		_job,
		TranscodeFileImpl		_file )
	
		throws TranscodeException
	{
		job		= _job;
		file	= _file;
		
		save_to = file.getCacheFile();
		
		try{
			hash = new SHA1Simple().calculateHash( save_to.getAbsolutePath().getBytes( "UTF-8" ));
			
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
		if ( file.isComplete()){
			
			try{
				return( file.getTargetFile().getLength());
				
			}catch( Throwable e ){
				
				return( -1 );
			}
		}else{
			
			return( -1 );
		}
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
		return( new Channel());
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
	Channel
		implements DiskManagerChannel
	{
		private volatile boolean		channel_destroyed;
		private volatile long			channel_position;
		
		private RandomAccessFile		raf;
		
		public DiskManagerRequest
		createRequest()
		{
			return( new request());
		}
		
		public DiskManagerFileInfo
		getFile()
		{
			return( TranscodeJobOutputLeecher.this );
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
			synchronized( this ){
				
				channel_destroyed	= true;
				
				if ( raf != null ){
					
					try{
						raf.close();
						
					}catch( Throwable e ){
					}
					
					raf = null;
				}
			}
		}
		
		protected int
		read(
			byte[]		buffer,
			long		offset,
			int			length )
		
			throws IOException
		{
			synchronized( this ){
				
				if ( channel_destroyed ){
					
					throw( new IOException( "Channel destroyed" ));
				}
				
				if ( raf == null ){
					
					if ( save_to.exists()){
						
						raf = new RandomAccessFile( save_to, "r" );
						
					}else{
						
						int state = job.getState();
						
						if ( state == TranscodeJob.ST_REMOVED ){
							
							throw( new IOException( "Job has been removed" ));
							
						}else if ( 	state == TranscodeJob.ST_FAILED ||
									state == TranscodeJob.ST_CANCELLED ){
							
							throw( new IOException( "Job has failed or been cancelled" ));
							
						}else if ( 	state == TranscodeJob.ST_COMPLETE ){
							
							throw( new IOException( "Job is complete but file missing" ));
						}

							// fall through and return 0 read
					}
				}
				
				if ( raf != null ){
					
					if ( raf.length() > offset ){
						
						raf.seek( offset );
						
						return( raf.read( buffer, 0, length ));
						
					}else{
					
							// data not yet available or file complete
						
						if ( file.isComplete()){
							
							return( -1 );
						}
					}
				}
			}
			
			try{
				Thread.sleep( 500 );
				
			}catch( Throwable e ){
				
				throw( new IOException( "Interrupted" ));
			}
	
			return( 0 );
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
					
					channel_position = _offset;
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
