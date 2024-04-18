/*
 * Created on Nov 26, 2008
 * Created by Paul Gardner
 * 
 * Copyright 2008 Vuze, Inc.  All rights reserved.
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


package com.aelitis.azureus.core.messenger.config;

import java.util.Map;

import org.gudy.azureus2.core3.util.AESemaphore;

import com.aelitis.azureus.core.messenger.PlatformMessage;
import com.aelitis.azureus.core.messenger.PlatformMessenger;
import com.aelitis.azureus.core.messenger.PlatformMessengerException;
import com.aelitis.azureus.core.messenger.PlatformMessengerListener;

public class 
PlatformMessengerConfig 
{
	private String 		listener_id;
	private boolean		send_azid;
	
	protected
	PlatformMessengerConfig(
		String		_listener_id,
		boolean		_send_azid )
	{
		listener_id		= _listener_id;
		send_azid		= _send_azid;
	}
	
	protected Map
	syncInvoke(
		String 						operationID, 
		Map 						parameters )
	
		throws PlatformMessengerException
	{
		PlatformMessage message = 
			new PlatformMessage( 
					"AZMSG", 
					listener_id,
					operationID, 
					parameters, 
					0 );

		if ( !send_azid ){
		
			message.setSendAZID( false );
		}
		
		final AESemaphore sem = new AESemaphore( "PlatformMessengerConfig:syncInvoke" );
		
		final Object[] result = { null };
		
		PlatformMessenger.queueMessage( 
			message, 
			new PlatformMessengerListener()
			{
				public void 
				messageSent(
					PlatformMessage 	message ) 
				{
				}
	
				public void 
				replyReceived(
					PlatformMessage 	message, 
					String 				replyType,
					Map 				reply )
				{
					try{
						if ( replyType.equals( PlatformMessenger.REPLY_EXCEPTION )){
							
							String		e_message 	= (String)reply.get( "message" );

							if ( e_message != null ){
								
								result[0] = new PlatformMessengerException( e_message );

							}else{
								
								String		text 	= (String)reply.get( "text" );
								
								Throwable	e 		= (Throwable)reply.get( "Throwable" );
								
								if ( text == null && e == null ){
									
									result[0] = new PlatformMessengerException( "Unknown error" );
									
								}else if ( text == null ){
									
									result[0] = new PlatformMessengerException( "Failed to send RPC", e );
									
								}else if ( e == null ){
									
									result[0] = new PlatformMessengerException( text );
									
								}else{
									
									result[0] = new PlatformMessengerException( text, e );
								}
							}
						}else{
							
							result[0] = reply;
						}
					}finally{
						
						sem.release();
					}
				}
			});
		
		sem.reserve();
		
		if ( result[0] instanceof PlatformMessengerException ){
			
			throw((PlatformMessengerException)result[0]);
		}
		
		return((Map)result[0]);
	}
}
