/*
 * Created on Aug 7, 2008
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

import java.util.*;

import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.DisplayFormatters;
import org.gudy.azureus2.core3.util.SHA1Simple;
import org.gudy.azureus2.plugins.utils.search.SearchResult;

import com.aelitis.azureus.core.metasearch.Result;
import com.aelitis.azureus.core.subs.SubscriptionResult;
import com.aelitis.azureus.util.JSONUtils;

public class 
SubscriptionResultImpl 
	implements SubscriptionResult
{
	final private SubscriptionHistoryImpl	history;
	
	private byte[]		key1;
	private byte[]		key2;
	private boolean		read;
	private boolean		deleted;
	
	private String		result_json;
	
	protected
	SubscriptionResultImpl(
		SubscriptionHistoryImpl		_history,
		Result						result )
	{
		history = _history;
		
		Map	map = result.toJSONMap();
		
		result_json 	= JSONUtils.encodeToJSON( map );
		read			= false;
		
		String	key1_str =  result.getEngine().getId() + ":" + result.getName();
		
		try{
			byte[] sha1 = new SHA1Simple().calculateHash( key1_str.getBytes( "UTF-8" ));
			
			key1 = new byte[10];
			
			System.arraycopy( sha1, 0, key1, 0, 10 );
			
		}catch( Throwable e ){
			
			Debug.printStackTrace(e);
		}
		
		String	uid = result.getUID();
		
		if ( uid != null && uid.length() > 0 ){
		
			String	key2_str = result.getEngine().getId() + ":" + uid;
			
			try{
				byte[] sha1 = new SHA1Simple().calculateHash( key2_str.getBytes( "UTF-8" ));
				
				key2 = new byte[10];
				
				System.arraycopy( sha1, 0, key2, 0, 10 );
				
			}catch( Throwable e ){
				
				Debug.printStackTrace(e);
			}
		}
	}
	
	protected 
	SubscriptionResultImpl(
		SubscriptionHistoryImpl		_history,
		Map							map )
	{
		history = _history;
		
		key1		= (byte[])map.get( "key" );
		key2		= (byte[])map.get( "key2" );
		
		read		= ((Long)map.get( "read")).intValue()==1;
		
		Long	l_deleted = (Long)map.get( "deleted" );
		
		if ( l_deleted != null ){
			
			deleted	= true;
			
		}else{
		
			try{
				result_json	= new String((byte[])map.get( "result_json" ), "UTF-8" );
				
			}catch( Throwable e ){
				
				Debug.printStackTrace(e);
			}
		}
	}
	
	protected boolean
	updateFrom(
		SubscriptionResultImpl	other )
	{
		if ( deleted ){
			
			return( false );
		}
		
		if ( getJSON().equals( other.getJSON())){
			
			return( false );
			
		}else{
			
			key2		= other.getKey2();
			result_json = other.getJSON();
			
			return( true );
		}
	}
	
	public String
	getID()
	{
		return( Base32.encode( key1 ));
	}
	
	protected byte[]
	getKey1()
	{
		return( key1 );
	}
	
	protected byte[]
	getKey2()
	{
   		return( key2 );
   	}
	
	public boolean
	getRead()
	{
		return( read );
	}
	
	public void
	setRead(
		boolean	_read )
	{
		if ( read != _read ){
			
			read	= _read;
			
			history.updateResult( this );
		}
	}
	
	protected void
	setReadInternal(
		boolean	_read )
	{
		read	= _read;
	}
	
	public void
	delete()
	{
		if ( !deleted ){
			
			deleted	= true;
			
			history.updateResult( this );
		}
	}
	
	protected void
	deleteInternal()
	{
		deleted = true;
	}
	
	public boolean
	isDeleted()
	{
		return( deleted );
	}
	
	protected Map
	toBEncodedMap()
	{
		Map		map	= new HashMap();
		
		map.put( "key", key1 );
		
		if ( key2 != null ){
			map.put( "key2", key2 );
		}
		
		map.put( "read", new Long(read?1:0));
		
		if ( deleted ){
			
			map.put( "deleted", new Long(1));
			
		}else{
		
			try{
				map.put( "result_json", result_json.getBytes( "UTF-8" ));
				
			}catch( Throwable e ){
				
				Debug.printStackTrace(e);
			}
		}
		
		return( map );
	}
	
	public Map
	toJSONMap()
	{
		Map	map = JSONUtils.decodeJSON( result_json );
		
		map.put( "subs_is_read", new Boolean( read ));
		map.put( "subs_id", getID());
		
		Result.adjustRelativeTerms( map );
		
			// migration - trim digits
		
		String size = (String)map.get( "l" );

		if ( size != null ){
			
			size = DisplayFormatters.trimDigits( size, 3 );
			
			map.put( "l", size );
		}
		
		return( map );
	}
	
	private String
	getJSON()
	{
		return( result_json );
	}
	
	public String 
	getDownloadLink() 
	{
		Map map = toJSONMap();
		
		String	link = (String)map.get( "dbl" );
		
		if ( link == null ){
			
			link = (String)map.get( "dl" );
		}		
		
		return( link );
	}
	
	public String 
	getPlayLink() 
	{
		return((String)toJSONMap().get( "pl" ));
	}
	
	public String 
	getAssetHash() 
	{
		return((String)toJSONMap().get( "h" ));
	}
	
	public Map<Integer,Object>
	toPropertyMap()
	{
		Map map = toJSONMap();
		
		Map<Integer,Object>	result = new HashMap<Integer, Object>();
		
		String title = (String)map.get( "n" );
		
		result.put( SearchResult.PR_UID, getID());
		result.put( SearchResult.PR_NAME, title );
		
		String pub_date = (String)map.get( "ts" );
		if ( pub_date != null ){	
			result.put( SearchResult.PR_PUB_DATE, new Date( Long.parseLong( pub_date )));
		}
		
		String size = (String)map.get( "lb" );
		if ( size != null ){	
			result.put( SearchResult.PR_SIZE, Long.parseLong( size ));
		}
		
		String	link = (String)map.get( "dbl" );
		
		if ( link == null ){
			
			link = (String)map.get( "dl" );
		}		
		
		if ( link != null ){
			result.put( SearchResult.PR_DOWNLOAD_LINK, link );
		}
		
		String	hash = (String)map.get( "h" );
		if ( hash != null ){
			result.put( SearchResult.PR_HASH, Base32.decode( hash ));
		}
		
		String	seeds = (String)map.get( "s" );
		if ( seeds != null ){
			result.put( SearchResult.PR_SEED_COUNT, Long.parseLong(seeds) );
		}
		
		String	peers = (String)map.get( "p" );
		if ( peers != null ){
			result.put( SearchResult.PR_LEECHER_COUNT, Long.parseLong(peers) );
		}
		
		String	rank = (String)map.get( "r" );
		if ( rank != null ){
			result.put( SearchResult.PR_RANK, (long)(100*Float.parseFloat( rank )));
		}
		
		return( result );
	}
}
