/*
 * Created on Aug 6, 2008
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

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.core3.util.ByteArrayHashMap;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.HashWrapper;
import org.gudy.azureus2.core3.util.SystemTime;

import com.aelitis.azureus.core.AzureusCoreFactory;
import com.aelitis.azureus.core.metasearch.Engine;
import com.aelitis.azureus.core.subs.SubscriptionHistory;
import com.aelitis.azureus.core.subs.SubscriptionResult;

public class 
SubscriptionHistoryImpl
	implements SubscriptionHistory
{
	private SubscriptionManagerImpl		manager;
	private SubscriptionImpl			subs;
	
	private boolean		enabled;
	private boolean		auto_dl;
	
	private long		last_scan;
	private long		last_new_result;
	private int			num_unread;
	private int			num_read;
	
	private String			last_error;
	private boolean			auth_failed;
	private int				consec_fails;
	
	private boolean			auto_dl_supported;
	
	private boolean			dl_with_ref	= true;
	
	protected
	SubscriptionHistoryImpl(
		SubscriptionManagerImpl		_manager,
		SubscriptionImpl			_subs )
	{
		manager		= _manager;
		subs		= _subs;
		
		loadConfig();
	}
	
	protected SubscriptionResultImpl[]
	reconcileResults(
		Engine							engine,
		SubscriptionResultImpl[]		latest_results )
	{
		auto_dl_supported	= engine.getAutoDownloadSupported() == Engine.AUTO_DL_SUPPORTED_YES;
		
		int	new_unread 	= 0;
		int new_read	= 0;
					
		if ( last_scan == 0 ){
				
					// first download feed -> mark all existing as read
						
			GlobalManager gm = AzureusCoreFactory.getSingleton().getGlobalManager();
			
			for (int i=0;i<latest_results.length;i++){
					
				SubscriptionResultImpl result = latest_results[i];
				
				result.setReadInternal(true);
				
					// see if we can associate result with existing download
				
				try{
					String hash_str = result.getAssetHash();
					
					if ( hash_str != null ){
						
						byte[] hash = Base32.decode( hash_str );
						
						DownloadManager dm = gm.getDownloadManager( new HashWrapper( hash ));
						
						if ( dm != null ){
							
							log( "Adding existing association on first read for '" + dm.getDisplayName());
							
							subs.addAssociation( hash );
						}
					}
				}catch( Throwable e ){
					
					Debug.printStackTrace(e);
				}
			}
		}
		
		long	now = SystemTime.getCurrentTime();
		
		SubscriptionResultImpl[] result;
		
		int	max_results = manager.getMaxNonDeletedResults();
		
		synchronized( this ){
			
			boolean	got_new_or_changed_result	= false;
			
			SubscriptionResultImpl[] existing_results = manager.loadResults( subs );
					
			ByteArrayHashMap	result_key_map 	= new ByteArrayHashMap();
			ByteArrayHashMap	result_key2_map = new ByteArrayHashMap();
			
			List	new_results = new ArrayList();

			for (int i=0;i<existing_results.length;i++){
				
				SubscriptionResultImpl r = existing_results[i];
				
				result_key_map.put( r.getKey1(), r );
				
				byte[]	key2 = r.getKey2();
				
				if ( key2 != null ){
					
					result_key2_map.put( key2, r );
				}
				
				new_results.add( r );
				
				if ( !r.isDeleted()){
					
					if ( r.getRead()){
						
						new_read++;
						
					}else{
						
						new_unread++;
					}
				}
			}
						
			for (int i=0;i<latest_results.length;i++){

				SubscriptionResultImpl r = latest_results[i];
				
					// we first of all insist on names uniqueness
				
				SubscriptionResultImpl existing = (SubscriptionResultImpl)result_key_map.get( r.getKey1());
				
				if ( existing == null ){
					
						// only if non-unique name do we fall back and use UID to remove duplicate
						// entries where the name has changed
					
					byte[]	key2 = r.getKey2();
					
					if ( key2 != null ){
						
						existing = (SubscriptionResultImpl)result_key2_map.get( key2 );
					}
				}
				
				if ( existing == null ){
					
					last_new_result = now;
					
					new_results.add( r );
					
					result_key_map.put( r.getKey1(), r );
					
					byte[]	key2 = r.getKey2();
					
					if ( key2 != null ){
						
						result_key2_map.put( key2, r );
					}
					
					got_new_or_changed_result = true;
				
					if ( r.getRead()){
						
						new_read++;
						
					}else{
					
						new_unread++;
					}
				}else{
					
					if ( existing.updateFrom( r )){
						
						got_new_or_changed_result = true;
					}
				}
			}
			
				// see if we need to delete any old ones
			
			if ( max_results > 0 && (new_unread + new_read ) > max_results ){
				
				for (int i=0;i<new_results.size();i++){
					
					SubscriptionResultImpl r = (SubscriptionResultImpl)new_results.get(i);
					
					if ( !r.isDeleted()){
						
						if ( r.getRead()){
							
							new_read--;
							
						}else{
							
							new_unread--;
						}
						
						r.deleteInternal();
						
						got_new_or_changed_result = true;
						
						if (( new_unread + new_read ) <= max_results ){
							
							break;
						}
					}
				}
			}
			
			if ( got_new_or_changed_result ){
				
				result = (SubscriptionResultImpl[])new_results.toArray( new SubscriptionResultImpl[new_results.size()]);
				
				manager.saveResults( subs, result );
				
			}else{
				
				result = existing_results;
			}
		
			last_scan 	= now;
			num_unread	= new_unread;
			num_read	= new_read;
		}
		
			// always save config as we have a new scan time
		
		saveConfig();
		
		return( result );
	}
	
	public boolean
	isEnabled()
	{
		return( enabled );
	}
	
	public void
	setEnabled(
		boolean		_enabled )
	{
		if ( _enabled != enabled ){
			
			enabled	= _enabled;
		
			saveConfig();
		}
	}
	
	public boolean
	isAutoDownload()
	{
		return( auto_dl );
	}
	
	public void
	setAutoDownload(
		boolean		_auto_dl )
	{
		if ( _auto_dl != auto_dl ){
			
			auto_dl	= _auto_dl;
		
			saveConfig();
			
			if ( auto_dl ){
				
				downloadNow();
			}
		}
	}
	
	public void 
	setDetails(
		boolean 	_enabled, 
		boolean 	_auto_dl ) 
	{
		if ( enabled != _enabled || auto_dl != _auto_dl ){
			
			enabled	= _enabled;
			auto_dl	= _auto_dl;
			
			saveConfig();
			
			if ( enabled && auto_dl ){
				
				downloadNow();
			}
		}
	}
	
	protected void
	downloadNow()
	{
		try{
			subs.getManager().getScheduler().downloadAsync( subs, false );
			
		}catch( Throwable e ){
			
			log( "Failed to initiate download", e );
		}
	}
	
	public long
	getLastScanTime()
	{
		return( last_scan );
	}
	
	public long 
	getLastNewResultTime() 
	{
		return( last_new_result );
	}
	
	public long
	getNextScanTime()
	{
		Map	schedule = subs.getScheduleConfig();
		
		if ( schedule.size() == 0  ){
			
			log( "Schedule is empty!");
			
			return( Long.MAX_VALUE );
			
		}else{
			
			try{
			
				long	interval_min = ((Long)schedule.get( "interval" )).longValue();
				
				if ( interval_min == Integer.MAX_VALUE || interval_min == Long.MAX_VALUE ){
					
					return( Long.MAX_VALUE );
				}
				
				if ( last_scan == 0 ){
					
						// never scanned, scan immediately
					
					return( SystemTime.getCurrentTime());
					
				}else{
				
					return( last_scan + interval_min*60*1000 );
				}
			}catch( Throwable e ){
				
				log( "Failed to decode schedule " + schedule, e );
				
				return( Long.MAX_VALUE );
			}
		}
	}
	
	public int
	getCheckFrequencyMins()
	{
		Map	schedule = subs.getScheduleConfig();
		
		if ( schedule.size() == 0  ){
			
			return( DEFAULT_CHECK_INTERVAL_MINS );
			
		}else{
			
			try{		
				int	interval_min = ((Long)schedule.get( "interval" )).intValue();
				
				return( interval_min );
				
			}catch( Throwable e ){
								
				return( DEFAULT_CHECK_INTERVAL_MINS );
			}
		}
	}
	
	public int
	getNumUnread()
	{
		return( num_unread );
	}
	
	public int
	getNumRead()
	{
		return( num_read );
	}
	
	public SubscriptionResult[]
	getResults(
		boolean		include_deleted )
	{
		SubscriptionResult[] results;
		
		synchronized( this ){
			
			results = manager.loadResults( subs );
		}
		
		if ( include_deleted ){
			
			return( results );
			
		}else{
			
			List	l = new ArrayList( results.length );
			
			for (int i=0;i<results.length;i++){
				
				if ( !results[i].isDeleted()){
					
					l.add( results[i] );
				}
			}
			
			return((SubscriptionResult[])l.toArray( new SubscriptionResult[l.size()]));
		}
	}
	
	public SubscriptionResult
	getResult(
		String		result_id )
	{
		SubscriptionResult[] results = getResults( true );
		
		for (int i=0;i<results.length;i++){
			
			if ( results[i].getID().equals( result_id )){
				
				return( results[i] );
			}
		}
		
		return( null );
	}
	
	protected void
	updateResult(
		SubscriptionResultImpl 	result )
	{
		byte[]	key = result.getKey1();
		
		boolean	changed = false;

		synchronized( this ){
			
			SubscriptionResultImpl[] results = manager.loadResults( subs );
						
			for (int i=0;i<results.length;i++){
				
				if ( Arrays.equals( results[i].getKey1(), key )){
					
					results[i] = result;
					
					changed	= true;
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
		
		if ( isAutoDownload() && !result.getRead() && !result.isDeleted()){
			
			manager.getScheduler().download( subs, result );		
		}
	}
	

	public void 
	deleteResults(
		String[] result_ids )
	{
		ByteArrayHashMap rids = new ByteArrayHashMap();
		
		for (int i=0;i<result_ids.length;i++){
			
			rids.put( Base32.decode( result_ids[i]), "" );
		}
	
		boolean	changed = false;

		synchronized( this ){
				
			SubscriptionResultImpl[] results = manager.loadResults( subs );

			for (int i=0;i<results.length;i++){
				
				SubscriptionResultImpl result = results[i];
				
				if ( !result.isDeleted() && rids.containsKey( result.getKey1())){
					
					changed = true;
					
					result.deleteInternal();
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
	}
	
	public void
	deleteAllResults()
	{
		boolean	changed = false;
		
		synchronized( this ){
						
			SubscriptionResultImpl[] results = manager.loadResults( subs );

			for (int i=0;i<results.length;i++){
				
				SubscriptionResultImpl result = results[i];
				
				if ( !result.isDeleted()){
					
					changed = true;
				
					result.deleteInternal();
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
	}
	
	public void
	markAllResultsRead()
	{
		boolean	changed = false;
		
		synchronized( this ){
						
			SubscriptionResultImpl[] results = manager.loadResults( subs );

			for (int i=0;i<results.length;i++){
				
				SubscriptionResultImpl result = results[i];
				
				if ( !result.getRead()){
					
					changed = true;
				
					result.setReadInternal( true );
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
	}
	
	public void
	markAllResultsUnread()
	{
		boolean	changed = false;
		
		synchronized( this ){
						
			SubscriptionResultImpl[] results = manager.loadResults( subs );

			for (int i=0;i<results.length;i++){
				
				SubscriptionResultImpl result = results[i];
				
				if ( result.getRead()){
					
					changed = true;
				
					result.setReadInternal( false );
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
	}
	
	public void 
	markResults(
		String[] 		result_ids,
		boolean[]		reads )
	{
		ByteArrayHashMap rid_map = new ByteArrayHashMap();
		
		for (int i=0;i<result_ids.length;i++){
			
			rid_map.put( Base32.decode( result_ids[i]), new Boolean( reads[i] ));
		}
	
		boolean	changed = false;

		List	newly_unread = new ArrayList();
		
		synchronized( this ){
						
			SubscriptionResultImpl[] results = manager.loadResults( subs );

			for (int i=0;i<results.length;i++){
				
				SubscriptionResultImpl result = results[i];
				
				if ( result.isDeleted()){
					
					continue;
				}
				
				Boolean	b_read = (Boolean)rid_map.get( result.getKey1());
				
				if ( b_read != null ){
					
					boolean	read = b_read.booleanValue();
					
					if ( result.getRead() != read ){
						
						changed = true;
					
						result.setReadInternal( read );
						
						if ( !read ){
							
							newly_unread.add( result );
						}
					}
				}
			}
			
			if ( changed ){
				
				updateReadUnread( results );
				
				manager.saveResults( subs, results );
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
		
		if ( isAutoDownload()){
			
			for (int i=0;i<newly_unread.size();i++){
				
				manager.getScheduler().download( subs, (SubscriptionResult)newly_unread.get(i));
			}
		}
	}
	
	public void 
	reset() 
	{
		synchronized( this ){
			
			SubscriptionResultImpl[] results = manager.loadResults( subs );
			
			if ( results.length > 0 ){
				
				results = new SubscriptionResultImpl[0];
								
				manager.saveResults( subs, results );
			}
			
			updateReadUnread( results );
		}
		
		last_error		= null;
		last_new_result	= 0;
		last_scan		= 0;
					
		saveConfig();
	}
	
	protected void
	checkMaxResults(
		int		max_results )
	{
		if ( max_results <= 0 ){
			
			return;
		}
		
		boolean	changed = false;

		synchronized( this ){

			if ((num_unread + num_read ) > max_results ){

				SubscriptionResultImpl[] results = manager.loadResults( subs );
				
				for (int i=0;i<results.length;i++){
					
					SubscriptionResultImpl r = results[i];
					
					if ( !r.isDeleted()){
						
						if ( r.getRead()){
							
							num_read--;
							
						}else{
							
							num_unread--;
						}
						
						r.deleteInternal();
						
						changed = true;
						
						if (( num_unread + num_read ) <= max_results ){
							
							break;
						}
					}
				}
				
				if ( changed ){
					
					manager.saveResults( subs, results );
				}
			}
		}
		
		if ( changed ){
			
			saveConfig();
		}
	}
	
	protected void
	updateReadUnread(
		SubscriptionResultImpl[]	results )
	{
		int	new_unread	= 0;
		int	new_read	= 0;
		
		for (int i=0;i<results.length;i++){
			
			SubscriptionResultImpl result = results[i];
			
			if ( !result.isDeleted()){
				
				if ( result.getRead()){
					
					new_read++;
					
				}else{
					
					new_unread++;
				}
			}
		}
		
		num_read	= new_read;
		num_unread	= new_unread;
	}
	
	protected boolean
	isAutoDownloadSupported()
	{
		return( auto_dl_supported );
	}
	
	protected void
	setFatalError(
		String		_error )
	{
		last_error		= _error;
		consec_fails	= 1024;
	}
	
	protected void
	setLastError(
		String		_last_error,
		boolean		_auth_failed )
	{
		last_error 		= _last_error;
		auth_failed		= _auth_failed;
		
		if ( last_error == null ){
			
			consec_fails = 0;
			
		}else{
			
			consec_fails++;
		}
		
		subs.fireChanged();
	}
	
	public String
	getLastError()
	{
		return( last_error );
	}
	
	public boolean
	isAuthFail()
	{
		return( auth_failed );
	}
	
	public int 
	getConsecFails() 
	{
		return( consec_fails );
	}
	
	public boolean
	getDownloadWithReferer()
	{
		return( dl_with_ref );
	}
	
	public void
	setDownloadWithReferer(
		boolean		b )
	{
		if ( b != dl_with_ref ){
			
			dl_with_ref = b;
			
			saveConfig();
		}
	}
	
	protected void
	loadConfig()
	{
		Map	map = subs.getHistoryConfig();
		
		Long	l_enabled	= (Long)map.get( "enabled" );		
		enabled				= l_enabled==null?true:l_enabled.longValue()==1;
		
		Long	l_auto_dl	= (Long)map.get( "auto_dl" );		
		auto_dl				= l_auto_dl==null?false:l_auto_dl.longValue()==1;
		
		Long	l_last_scan = (Long)map.get( "last_scan" );		
		last_scan			= l_last_scan==null?0:l_last_scan.longValue();
		
		Long	l_last_new 	= (Long)map.get( "last_new" );		
		last_new_result		= l_last_new==null?0:l_last_new.longValue();
		
		Long	l_num_unread 	= (Long)map.get( "num_unread" );		
		num_unread				= l_num_unread==null?0:l_num_unread.intValue();

		Long	l_num_read 	= (Long)map.get( "num_read" );		
		num_read			= l_num_read==null?0:l_num_read.intValue();
		
			// migration - if we've already downloaded this feed then we default to being
			// enabled
		
		Long	l_auto_dl_s	= (Long)map.get( "auto_dl_supported" );		
		auto_dl_supported	= l_auto_dl_s==null?(last_scan>0):l_auto_dl_s.longValue()==1;

		Long	l_dl_with_ref	= (Long)map.get( "dl_with_ref" );		
		dl_with_ref	= l_dl_with_ref==null?true:l_dl_with_ref.longValue()==1;

	}
	
	protected void
	saveConfig()
	{
		Map	map = new HashMap();
		
		map.put( "enabled", new Long( enabled?1:0 ));
		map.put( "auto_dl", new Long( auto_dl?1:0 ));
		map.put( "auto_dl_supported", new Long( auto_dl_supported?1:0));
		map.put( "last_scan", new Long( last_scan ));
		map.put( "last_new", new Long( last_new_result ));
		map.put( "num_unread", new Long( num_unread ));
		map.put( "num_read", new Long( num_read ));
		map.put( "dl_with_ref", new Long( dl_with_ref?1:0 ));

		subs.updateHistoryConfig( map );
	}
	
	protected void
	log(
		String		str )
	{
		subs.log( "History: " + str );
	}
	
	protected void
	log(
		String		str,
		Throwable	e )
	{
		subs.log( "History: " + str, e );
	}
	
	protected String
	getString()
	{
		return( "unread=" + num_unread + ",read=" + num_read+ ",last_err=" + last_error );
	}
}
