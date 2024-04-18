/*
 * Created on Jun 20, 2008
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


package com.aelitis.azureus.core.metasearch.impl.plugin;

import java.util.Date;
import java.util.Map;

import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.LightHashMap;
import org.gudy.azureus2.plugins.utils.search.SearchResult;

import com.aelitis.azureus.core.metasearch.*;

public class 
PluginResult 
	extends Result
{
	private static final Object NULL_OBJECT = PluginResult.class;
	
	private SearchResult			result;
	private String					search_term;
	
	private Map		property_cache = new LightHashMap();
	
	protected
	PluginResult(
		PluginEngine		_engine,
		SearchResult		_result,
		String				_search_term )
	{
		super( _engine );
		
		result			= _result;
		search_term		= _search_term;
	}
	
	public Date
	getPublishedDate()
	{
		return((Date)getResultProperty( SearchResult.PR_PUB_DATE ));
	}
	
	public String 
	getCategory()
	{
		return(getStringProperty( SearchResult.PR_CATEGORY ));
	}
	
	public void 
	setCategory(
		String category )
	{	
	}
	
	public String 
	getContentType()
	{
		return(getStringProperty( SearchResult.PR_CONTENT_TYPE ));

	}
	
	public void 
	setContentType(
		String contentType )
	{	
	}
	
	public String 
	getName()
	{
		return(getStringProperty( SearchResult.PR_NAME ));
	}
	
	public long 
	getSize()
	{
		return(getLongProperty( SearchResult.PR_SIZE ));
	}
	
	public int 
	getNbPeers()
	{
		return(getIntProperty( SearchResult.PR_LEECHER_COUNT ));
	}
	
	public int 
	getNbSeeds()
	{
		return(getIntProperty( SearchResult.PR_SEED_COUNT ));
	}
	
	public int 
	getNbSuperSeeds()
	{
		return(getIntProperty( SearchResult.PR_SUPER_SEED_COUNT ));
	}
	
	public int 
	getComments()
	{
		return(getIntProperty( SearchResult.PR_COMMENTS ));
	}
	
	public int 
	getVotes()
	{
		return(getIntProperty( SearchResult.PR_VOTES ));
	}
	
	public int 
	getVotesDown()
	{
		return(getIntProperty( SearchResult.PR_VOTES_DOWN ));
	}
	
	public boolean 
	isPrivate()
	{
		return( getBooleanProperty( SearchResult.PR_PRIVATE ));
	}
	
	
	public String 
	getDRMKey()
	{
		return(getStringProperty( SearchResult.PR_DRM_KEY ));
	}
	
	public String 
	getDownloadLink()
	{
		return(getStringProperty( SearchResult.PR_DOWNLOAD_LINK ));
	}
	
	public String 
	getDownloadButtonLink()
	{
		return(getStringProperty( SearchResult.PR_DOWNLOAD_BUTTON_LINK ));
	}
	
	public String 
	getCDPLink()
	{
		return( getStringProperty( SearchResult.PR_DETAILS_LINK ));

	}
	
	public String 
	getPlayLink()
	{
		return(getStringProperty( SearchResult.PR_PLAY_LINK ));
	}
	
	public String 
	getUID() 
	{
		return(getStringProperty( SearchResult.PR_UID ));
	}
	
	public String 
	getHash() 
	{
		byte[] hash = getByteArrayProperty( SearchResult.PR_HASH );
		
		if ( hash == null ){
			
			return( null );
		}
		
		return( Base32.encode( hash ));
	}
	
	public float 
	getRank() 
	{
		if (((PluginEngine)getEngine()).useAccuracyForRank()){
			
			return( applyRankBias( getAccuracy()));
		}
		
		long	l_rank = getLongProperty( SearchResult.PR_RANK );

			// if we have seeds/peers just use the usual mechanism
		
		if ( getLongProperty( SearchResult.PR_SEED_COUNT ) >= 0 && getLongProperty( SearchResult.PR_LEECHER_COUNT ) >= 0 ){
			
			l_rank = Long.MIN_VALUE;
		}
		
		if ( l_rank == Long.MIN_VALUE ){
			
			return( super.getRank());
		}
		
		float rank = l_rank;
		
		if ( rank > 100 ){
			
			rank = 100;
			
		}else if ( rank < 0 ){
			
			rank = 0;
		}
		
		return( applyRankBias( rank / 100 ));
	}
	
	public float 
	getAccuracy()
	{
		long	l_accuracy = getLongProperty( SearchResult.PR_ACCURACY );
		
		if ( l_accuracy == Long.MIN_VALUE ){
			
			return( -1 );
		}
		
		float accuracy = l_accuracy;
		
		if ( accuracy > 100 ){
			
			accuracy = 100;
			
		}else if ( accuracy < 0 ){
			
			accuracy = 0;
		}
		
		return( accuracy / 100 );
	}

	public String 
	getSearchQuery()
	{
		return( search_term );
	}
	
	protected int
	getIntProperty(
		int		name )
	{
		return((int)getLongProperty( name ));
	}
	
	protected long
	getLongProperty(
		int		name )
	{
		return( getLongProperty( name, Long.MIN_VALUE ));
	}
	
	protected long
	getLongProperty(
		int		name,
		long	def )
	{
		try{
			Long	l = (Long)getResultProperty( name );
			
			if ( l == null ){
				
				return( def );
			}
			
			return( l.longValue());
			
		}catch( Throwable e ){
			
			Debug.out( "Invalid value returned for Long property " + name );
			
			return( def );
		}
	}
	
	protected boolean
	getBooleanProperty(
		int		name )
	{
		return( getBooleanProperty( name, false ));
	}
	
	protected boolean
	getBooleanProperty(
		int		name,
		boolean	def )
	{
		try{
			Boolean	b = (Boolean)getResultProperty( name );
			
			if ( b == null ){
				
				return( def );
			}
			
			return( b.booleanValue());
			
		}catch( Throwable e ){
			
			Debug.out( "Invalid value returned for Boolean property " + name );
			
			return( def );
		}
	}
	
	protected String
	getStringProperty(
		int		name )
	{
		return( getStringProperty( name, "" ));
	}
	
	protected String
	getStringProperty(
		int		name,
		String	def )
	{
		try{
			String	l = (String)getResultProperty( name );
			
			if ( l == null ){
				
				return( def );
			}
			
			return( unescapeEntities( removeHTMLTags( l )));
			
		}catch( Throwable e ){
			
			Debug.out( "Invalid value returned for String property " + name );
			
			return( def );
		}
	}
	
	protected byte[]
	getByteArrayProperty(
		int		name )
	{
		try{
			return((byte[])getResultProperty( name ));
				
		}catch( Throwable e ){
			
			Debug.out( "Invalid value returned for byte[] property " + name );
			
			return( null );
		}
	}
	
	protected synchronized Object
	getResultProperty(
		int		prop )
	{
		Integer i_prop = new Integer( prop );
		
		Object	res = property_cache.get( i_prop );
		
		if ( res == null ){
			
			res = result.getProperty( prop );
			
			if ( res == null ){
				
				res = NULL_OBJECT;
			}
			
			property_cache.put( i_prop, res );
		}
		
		if ( res == NULL_OBJECT ){
			
			return( null );
		}
		
		return( res );
	}
}
