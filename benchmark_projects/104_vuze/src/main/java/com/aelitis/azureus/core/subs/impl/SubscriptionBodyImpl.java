/*
 * Created on Jul 15, 2008
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


package com.aelitis.azureus.core.subs.impl;

import java.io.File;
import java.io.IOException;
import java.security.Signature;
import java.util.*;

import org.gudy.azureus2.core3.util.BEncoder;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.SHA1Simple;

import com.aelitis.azureus.core.security.CryptoECCUtils;
import com.aelitis.azureus.core.subs.Subscription;
import com.aelitis.azureus.core.subs.SubscriptionException;
import com.aelitis.azureus.core.vuzefile.VuzeFile;
import com.aelitis.azureus.core.vuzefile.VuzeFileComponent;
import com.aelitis.azureus.core.vuzefile.VuzeFileHandler;

public class 
SubscriptionBodyImpl 
{
	private static final int SIMPLE_ID_LENGTH				= 10;

	protected static byte[]
	encode(
		byte[]		hash,
		int			version,
		int			size )
	{
		int hash_len = hash.length;
		
		byte[]	result = new byte[ hash_len + 4 + 4 ];
		
		System.arraycopy( hash, 0, result, 0, hash_len );
		System.arraycopy( SubscriptionImpl.intToBytes(version), 0, result, hash_len, 4 );
		System.arraycopy( SubscriptionImpl.intToBytes(size), 0, result, hash_len+4, 4 );

		return( result );
	}
	
	protected static byte[]
	sign(
		byte[]		private_key,
		byte[]		hash,
		int			version,
		int			size )
	
		throws Exception
	{
		Signature signature = CryptoECCUtils.getSignature( CryptoECCUtils.rawdataToPrivkey( private_key ));
		
		// key for signature is hash + version + size so we have some
		// control over auto-update process and prevent people from injecting
		// potentially huge bogus updates
	
		signature.update( encode( hash, version, size ));

		return( signature.sign());
	}
	
	protected static boolean
	verify(
		byte[]		public_key,
		byte[]		hash,
		int			version,
		int			size,
		byte[]		sig )
	{
		try{
			Signature signature = CryptoECCUtils.getSignature( CryptoECCUtils.rawdataToPubkey( public_key ));
	
			signature.update( encode( hash, version, size ));
	
			return( signature.verify( sig ));
			
		}catch( Throwable e ){
			
			Debug.out( e );
			
			return( false );
		}
	}
	
	protected static byte[]
	deriveShortID(
		byte[]		public_key,
		Map			singleton_details )
	{
		if ( singleton_details != null ){
			
			return( deriveSingletonShortID( singleton_details ));
							
		}else{
		
			byte[]	hash = new SHA1Simple().calculateHash( public_key );

			byte[]	short_id = new byte[SIMPLE_ID_LENGTH];

			System.arraycopy( hash, 0, short_id, 0, SIMPLE_ID_LENGTH );
		
			return( short_id );
		}
	}
	
	protected static byte[]
  	deriveSingletonShortID(
  		Map			singleton_details )
  	{
  		byte[]	short_id = new byte[SIMPLE_ID_LENGTH];

  		byte[] 	explicit_sid = new SHA1Simple().calculateHash((byte[])singleton_details.get( "key" ));
  			
  		System.arraycopy( explicit_sid, 0, short_id, 0, SIMPLE_ID_LENGTH );
  		
  		return( short_id );
  	}
	
	private SubscriptionManagerImpl		manager;
	
	private String	name;
	private boolean	is_public;
	private byte[]	public_key;
	private int		version;
	private int		az_version;
	private String	json;
	private Map		singleton_details;
	
	
	
	private byte[]	hash;
	private byte[]	sig;
	private int		sig_data_size;
	
	private Map		map;

		// load constructor
	
	protected 
	SubscriptionBodyImpl(
		SubscriptionManagerImpl	_manager,
		SubscriptionImpl		_subs )
			
		throws SubscriptionException
	{
		manager	= _manager;

		try{
			File vuze_file = manager.getVuzeFile( _subs );
	
			VuzeFile	vf = VuzeFileHandler.getSingleton().loadVuzeFile( vuze_file.getAbsolutePath());
	
			if ( vf == null ){
				
				throw( new IOException( "Failed to load vuze file '" + vuze_file + "'" ));
			}
					
			load(  vf.getComponents()[0].getContent(), false );
			
		}catch( Throwable e ){
			
			rethrow( e );
		}
	}
	
		// import constructor
	
	protected 
	SubscriptionBodyImpl(
		SubscriptionManagerImpl	_manager,
		Map						_map )
	
		throws IOException
	{
		manager	= _manager;

		load( _map, true );
	}
	
	protected void
	load(
		Map			_map,
		boolean		_verify )
	
		throws IOException
	{
		map		= _map;
		
		hash 	= (byte[])map.get( "hash" );
		sig	 	= (byte[])map.get( "sig" );
		Long	l_size	= (Long)map.get( "size" );
		
		Map	details = (Map)map.get( "details" );
		
		if ( details == null || hash == null || sig == null || l_size == null ){
			
			throw( new IOException( "Invalid subscription - details missing" ));
		}
		
		sig_data_size	= l_size.intValue();
		
		name		= new String((byte[])details.get( "name" ), "UTF-8" );
		public_key	= (byte[])details.get( "public_key" );
		version		= ((Long)details.get( "version" )).intValue();
		is_public	= ((Long)details.get( "is_public" )).intValue()==1; 
		json		= new String((byte[])details.get( "json"), "UTF-8" );
		
		singleton_details = (Map)details.get( "sin_details" );
		
		Long l_az_version	= (Long)details.get( "az_version" );
		
		az_version = l_az_version==null?Subscription.AZ_VERSION:l_az_version.intValue();
		
		if ( _verify ){
			
				// verify
			
			byte[] contents = BEncoder.encode( details );
			
			byte[] actual_hash = new SHA1Simple().calculateHash( contents );
	
			if ( !Arrays.equals( actual_hash, hash )){
				
					// backwards compat for pre-az_version
							
				Map details_copy = new HashMap( details );
				
				details_copy.remove( "az_version" );
				
				contents = BEncoder.encode( details_copy );
				
				actual_hash = new SHA1Simple().calculateHash( contents );
			}
			
			if ( !Arrays.equals( actual_hash, hash )){

				throw( new IOException( "Hash mismatch" ));
			}
			
			if ( sig_data_size != contents.length ){
				
				throw( new IOException( "Signature data length mismatch" ));
			}
			
			if ( !verify( public_key, hash, version, sig_data_size, sig )){
					
				throw( new IOException( "Signature verification failed" ));
			}
		}
	}
	
		// create constructor
	
	protected
	SubscriptionBodyImpl(
		SubscriptionManagerImpl	_manager,
		String					_name,
		boolean					_is_public,
		String					_json_content,
		byte[]					_public_key,
		int						_version,
		int						_az_version,
		Map						_singleton_details )
	
		throws IOException
	{
		manager		= _manager;
		
		name		= _name;
		is_public	= _is_public;
		public_key	= _public_key;
		version		= _version;
		az_version	= _az_version;
		json		= _json_content;
		
		singleton_details	= _singleton_details;
		
		map			= new HashMap();
		
		Map details = new HashMap();
			
		map.put( "details", details );
		
		details.put( "name", name.getBytes( "UTF-8" ));
		details.put( "is_public", new Long( is_public?1:0 ));
		details.put( "public_key", public_key );
		details.put( "version", new Long( version ));
		details.put( "az_version", new Long( az_version ));
		details.put( "json", _json_content.getBytes( "UTF-8" ));
		
		if ( singleton_details != null ){
			
			details.put( "sin_details", singleton_details );
		}
	}
	
	protected void
	updateDetails(
		SubscriptionImpl		subs,
		Map						details )
	
		throws IOException
	{
		is_public	= subs.isPublic();
		version		= subs.getVersion();
		az_version	= subs.getAZVersion();
		name		= subs.getName();
		
		details.put( "name",name.getBytes( "UTF-8" ));
		details.put( "is_public", new Long( is_public?1:0 ));
		details.put( "version", new Long( version ));
		details.put( "az_version", new Long( az_version ));
		
		if ( json != null ){
		
			details.put( "json", json.getBytes( "UTF-8" ));
		}
		
		if ( singleton_details != null ){
			
			details.put( "sin_details", singleton_details );
		}
	}
	
	protected String
	getName()
	{
		return( name );
	}
	
	protected byte[]
	getPublicKey()
	{
		return( public_key );
	}
	
	public byte[]
	getShortID()
	{
		return( deriveShortID( public_key, singleton_details ));
	}
	
	protected boolean
	isPublic()
	{
		return( is_public );
	}
	
	protected String
	getJSON()
	{
		return( json );
	}
	
	protected Map
	getSingletonDetails()
	{
		return( singleton_details );
	}
	
	protected void
	setJSON(
		String		_json )
	{
		json	= _json;
	}
	
	protected int
	getVersion()
	{
		return( version );
	}
	
	protected int
	getAZVersion()
	{
		return( az_version );
	}
	
		// derived data
	
	protected byte[]
	getHash()
	{
		return( hash );
	}

	protected byte[]
	getSig()
	{
		return( sig );
	}
	
	protected int
	getSigDataSize()
	{
		return( sig_data_size );
	}
	
	protected void
	writeVuzeFile(
		SubscriptionImpl		subs )
	
		throws SubscriptionException
	{
		try{
			File file = manager.getVuzeFile( subs );
							
			Map	details = (Map)map.get( "details" );
			
			updateDetails( subs, details );
			
			byte[] contents = BEncoder.encode( details );
					
			byte[] new_hash = new SHA1Simple().calculateHash( contents );
			
			byte[] old_hash	= (byte[])map.get( "hash" );
			
				// backward compat from before az_version was introduced
			
			if ( old_hash != null && !Arrays.equals( old_hash, new_hash )){
					
				Map details_copy = new HashMap( details );
				
				details_copy.remove( "az_version" );
				
				contents = BEncoder.encode( details_copy );
				
				new_hash = new SHA1Simple().calculateHash( contents );
			}
			
			if ( old_hash == null || !Arrays.equals( old_hash, new_hash )){
				
				byte[]	private_key = subs.getPrivateKey();
				
				if ( private_key == null ){
					
					throw( new SubscriptionException( "Only the originator of a subscription can modify it" ));
				}
							
				map.put( "size", new Long( contents.length ));
				
				try{				
					map.put( "hash", new_hash );
					map.put( "sig", sign( private_key, new_hash, version, contents.length ));
					
				}catch( Throwable e ){
					
					throw( new SubscriptionException( "Crypto failed: " + Debug.getNestedExceptionMessage(e)));
				}
			}
			
			File	backup_file	= null;
			
			if ( file.exists()){
				
				backup_file = new File( file.getParent(), file.getName() + ".bak" );
				
				backup_file.delete();
				
				if ( !file.renameTo( backup_file )){
					
					throw( new SubscriptionException( "Backup failed" ));
				}
			}
			
			try{
				VuzeFile	vf = VuzeFileHandler.getSingleton().create();
				
				vf.addComponent( VuzeFileComponent.COMP_TYPE_SUBSCRIPTION, map );
				
				vf.write( file );
			
				hash			= new_hash;
				sig				= (byte[])map.get( "sig" );
				sig_data_size	= contents.length;
				
			}catch( Throwable e ){
				
				if ( backup_file != null ){
					
					backup_file.renameTo( file );
				}
				
				throw( new SubscriptionException( "File write failed: " + Debug.getNestedExceptionMessage(e)));
			}
		}catch( Throwable e ){
			
			rethrow( e );
		}
	}
	
	protected void
	rethrow(
		Throwable e )
	
		throws SubscriptionException
	{
		if ( e instanceof SubscriptionException ){
			
			throw((SubscriptionException)e);
		}
		
		throw( new SubscriptionException( "Operation failed", e ));
	}
}
