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

import org.gudy.azureus2.core3.util.Debug;

import com.aelitis.azureus.core.metasearch.Engine;
import com.aelitis.azureus.core.metasearch.Result;
import com.aelitis.azureus.core.metasearch.SearchLoginException;
import com.aelitis.azureus.core.metasearch.SearchParameter;
import com.aelitis.azureus.core.subs.*;
import com.aelitis.azureus.util.JSONUtils;

public class 
SubscriptionDownloader 
{
	private SubscriptionManagerImpl		manager;
	private SubscriptionImpl			subs;
	
	protected
	SubscriptionDownloader(
		SubscriptionManagerImpl	_manager,
		SubscriptionImpl		_subs )
	
		throws SubscriptionException
	{
		manager	= _manager;
		subs	= _subs;
	}
	
	protected void
	download()
	
		throws SubscriptionException
	{
		log( "Downloading" );
		
		Map map = JSONUtils.decodeJSON( subs.getJSON());
		
		Long 	engine_id 	= (Long)map.get( "engine_id" );
		String	search_term	= (String)map.get( "search_term" );
		Map		filters		= (Map)map.get( "filters" );

		Engine engine = manager.getEngine( subs, map, false );
		
		if ( engine == null ){
			
			throw( new SubscriptionException( "Download failed, search engine " + engine_id + " not found" ));
		}
		
		List	sps = new ArrayList();
		
		if ( search_term != null ){
			
			sps.add( new SearchParameter( "s", search_term ));
		
			log( "    Using search term '" + search_term + "' for engine " + engine.getString());
		}
		
		/*
		if ( mature != null ){
			
			sps.add( new SearchParameter( "m", mature.toString()));
		}
		*/
		
		SearchParameter[] parameters = (SearchParameter[])sps.toArray(new SearchParameter[ sps.size()] );

		
		SubscriptionHistoryImpl history = (SubscriptionHistoryImpl)subs.getHistory();
		
		try{	
			Map	context = new HashMap();
			
			context.put( Engine.SC_SOURCE, 	"subscription" );
			
			Result[] results = engine.search( parameters, context, -1, -1, null, null );
		
			log( "    Got " + results.length + " results" );
			
			SubscriptionResultFilter result_filter = new SubscriptionResultFilter(filters );

			results = result_filter.filter( results );
			
			log( "    Post-filter: " + results.length + " results" );

			SubscriptionResultImpl[]	s_results = new SubscriptionResultImpl[results.length];
			
			for( int i=0;i<results.length;i++){
				
				SubscriptionResultImpl	s_result = new SubscriptionResultImpl( history, results[i] );
				
				s_results[i] = s_result;
			}
			
			SubscriptionResultImpl[] all_results = history.reconcileResults( engine, s_results );
						
			checkAutoDownload( all_results );
			
			history.setLastError( null, false );
			
		}catch( Throwable e ){
			
			log( "    Download failed", e);
			
			history.setLastError( Debug.getNestedExceptionMessage( e ),e instanceof SearchLoginException );
			
			throw( new SubscriptionException( "Search failed", e ));
		}
	}
	
	protected void
	checkAutoDownload(
		SubscriptionResultImpl[]	results )
	{
		if ( !subs.getHistory().isAutoDownload()){
			
			return;
		}
		
		for (int i=0;i<results.length;i++){
			
			SubscriptionResultImpl	result = results[i];
			
			if ( result.isDeleted() || result.getRead()){
				
				continue;
			}
						
			manager.getScheduler().download( subs, result );
		}
	}
	
	protected void
	log(
		String		str )
	{
		manager.log( str );
	}
	
	protected void
	log(
		String		str,
		Throwable	e )
	{
		manager.log( str, e );
	}
}
