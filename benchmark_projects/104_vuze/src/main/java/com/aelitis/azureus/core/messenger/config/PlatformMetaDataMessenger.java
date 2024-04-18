/*
 * Created on December 4, 2009
 * Created by Olivier Chalouhi
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

import java.util.*;

import com.aelitis.azureus.core.messenger.PlatformMessengerException;

public class 
PlatformMetaDataMessenger 
{
	
	private static final PlatformMessengerConfig	dispatcher = 
			new PlatformMessengerConfig( "metadata", false );

	private static final String OP_LOOKUP		= "lookup";
	private static final String OP_SEARCH		= "search";
	private static final String OP_SUBMIT		= "submit";


	public static Association 
	getAssociation(
		String hash)
	
		throws PlatformMessengerException
	{
		Map reply = dispatcher.syncInvoke(	OP_LOOKUP, getParameter( hash ) ); 

		Association assoc = getAssociation( reply );
		
		if ( assoc == null ){
			
			throw( new PlatformMessengerException( "Invalid reply: " + reply ));
		}
		
		return assoc;
	}
	
	private static Association getAssociation(Map reply) {
		try {
			Map result = (Map) reply.get("result");
			return getAssociationFromMap(result);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}

	private static Association getAssociationFromMap(Map assoc) {
		try {
			String title = (String) assoc.get("title");
			String db =  (String)  assoc.get("db");
			String db_id =  (String)  assoc.get("db_id");
			String hash =  (String)  assoc.get("hash");
			String type =  (String)  assoc.get("type");
			
			if(type == null) {
				EmptyAssociation result = new EmptyAssociation();
				result.hash = hash;
				return result;
			}
			
			if("movie".equals(type)) {
				String quality = (String)  assoc.get("quality");
				String language = (String)  assoc.get("language");
				MovieAssociation association = new MovieAssociation();
				association.db = db;
				association.db_id = db_id;
				association.title = title;
				association.quality = VideoQuality.fromString(quality);
				association.language = new Locale(language);
				association.hash = hash;
				return association;
			}
			if("tv".equals(type)) {
				String quality = (String)  assoc.get("quality");
				String language = (String)  assoc.get("language");
				TvShowAssociation association = new TvShowAssociation();
				association.db = db;
				association.db_id = db_id;
				association.title = title;
				association.quality = VideoQuality.fromString(quality);
				association.language = new Locale(language);
				association.hash = hash;
				return association;
			}
			if("music".equals(type)) {
				String quality = (String)  assoc.get("quality");
				MusicAssociation association = new MusicAssociation();
				association.db = db;
				association.db_id = db_id;
				association.title = title;
				association.quality = AudioQuality.fromString(quality);
				association.hash = hash;
				return association;
			}
			
			
			return null;
		
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
	
	private static Map<String,Association> getAssociations(Map reply) {
		try {
			Map<String,Map> result = (Map<String,Map>) reply.get("results");
			Map<String,Association> results = new HashMap<String, Association>();
			for(String key : result.keySet()) {
				results.put(key, getAssociationFromMap(result.get(key)));
			}
			return results;
		} catch (Exception e) {
			e.printStackTrace();
			return new HashMap<String,Association>();
		}
	}
	
	public static Map<String,Association>
   	getAssociations(
   		String[]		hashes )
   	
   		throws PlatformMessengerException
   	{
		Map<String,Association> result = new HashMap<String, Association>();
		if( hashes.length == 0 ){
			
			return result;
		}


   		Map reply = dispatcher.syncInvoke(	OP_LOOKUP, getParameters(hashes) ); 

   		return( getAssociations( reply ));
   	}
	
	public static void 
	addSubmission(Association assoc)
	
		throws PlatformMessengerException
	{
		Map<String,Object> parameters = new HashMap<String,Object>();
		
		Map<String,Object> submission = new HashMap<String,Object>();
		submission.put("hash",assoc.hash);
		submission.put("db", assoc.db);
		submission.put("db_id",assoc.db_id);
		if(assoc instanceof MovieAssociation) {
			submission.put("type", "movie");
			submission.put("quality", ((MovieAssociation)assoc).quality.quality);
			submission.put("language", ((MovieAssociation)assoc).language.getLanguage());
		}
		if(assoc instanceof TvShowAssociation) {
			submission.put("type", "tv");
			submission.put("quality", ((MovieAssociation)assoc).quality.quality);
			submission.put("language", ((MovieAssociation)assoc).language.getLanguage());
		}
		if(assoc instanceof MusicAssociation) {
			submission.put("type", "music");
			submission.put("quality", ((MovieAssociation)assoc).quality.quality);
		}
		
		parameters.put("submission", submission);
		
		dispatcher.syncInvoke(	OP_SUBMIT, parameters ); 

	}
	
	public static SearchResult[]
	search(String title) throws PlatformMessengerException {
		Map<String,String> parameters = new HashMap<String, String>();
		parameters.put("title", title);
		Map reply = dispatcher.syncInvoke(	OP_SEARCH, parameters );
		List<Map> results = (List<Map>)reply.get("results");
		SearchResult[] searchResults = new SearchResult[results.size()];
		int i = 0;
		for(Map result : results) {
			SearchResult searchResult = new SearchResult();
			searchResult.title = (String)result.get("title");
			searchResult.db = (String)result.get("db");
			searchResult.db_id = (String)result.get("db_id");
			searchResults[i++] = searchResult;
		}
		
		return searchResults;
		
	}
	
	public static class SearchResult {
		String title;
		String db;
		String db_id;
		
		@Override
		public String toString() {
			return db + "." + db_id + " : " + title;
		}
		
	}
	
	protected static Map
	getParameter(
		String		hash )
	{
		Map parameters = new HashMap();
		
		parameters.put( "hash",  hash );

		return( parameters );
	}
	
	protected static Map
	getParameters(
		String[]		hashes )
	{
		Map parameters = new HashMap();
		
		parameters.put( "hashes", hashes);

		return( parameters );
	}
	
	public static abstract class Association {
		public String hash;
	    public String db;
	    public String db_id;

	    //Cached but not stored
	    public String title;
	    
	    @Override
	    public String toString() {
	    	return hash + " > " + db + "." + db_id + " : " + title;
	    }
	}
	
	public static class EmptyAssociation extends Association {

	}
	
	public static abstract class VideoAssociation extends Association {
		 public VideoQuality quality;
		 public Locale language;
	}
	
	public static class MovieAssociation extends VideoAssociation {
		
	}
	
	public static class TvShowAssociation extends VideoAssociation {
		
	}
	
	public static class MusicAssociation extends Association {
		public AudioQuality quality;
	}
	
	public static enum VideoQuality {
		LOW("low"),DVD("dvd"),HD_720p("720p"),HD_1080p("1080p");
		
		String quality;
		
		private VideoQuality(String quality) {
			this.quality = quality;
		}
		
		public static VideoQuality fromString(String quality) {
			quality = quality.toLowerCase();
			if(LOW.quality.equals(quality)) return LOW;
			if(DVD.quality.equals(quality)) return DVD;
			if(HD_720p.quality.equals(quality)) return HD_720p;
			if(HD_1080p.quality.equals(quality)) return HD_1080p;
			return null;
		}
	}
	
	public static enum AudioQuality {
		LOW("low"),HIGH("high"),LOSSLESS("lossless");
		
		String quality;
		
		private AudioQuality(String quality) {
			this.quality = quality;
		}
		
		public static AudioQuality fromString(String quality) {
			quality = quality.toLowerCase();
			if(LOW.quality.equals(quality)) return LOW;
			if(HIGH.quality.equals(quality)) return HIGH;
			if(LOSSLESS.quality.equals(quality)) return LOSSLESS;
			return null;
		}
		
	}
	
	public static void main(String[] args) throws Exception {
		SearchResult[] results = search("Dark Knight");
		for(SearchResult result : results) {
			System.out.println(result);
		}
		
		MovieAssociation assoc = new MovieAssociation();
		assoc.db = "tmdb";
		assoc.db_id = "155";
		assoc.hash = "test";
		assoc.quality = VideoQuality.DVD;
		assoc.language = new Locale("en");
		addSubmission(assoc);
		
		Association assocL = getAssociation("test");
		System.out.println(assocL);
		
	}

}
