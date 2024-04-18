package com.aelitis.azureus.core.subs.impl;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;
import java.util.regex.Pattern;

import com.aelitis.azureus.core.metasearch.Result;
import com.aelitis.azureus.util.ImportExportUtils;

public class 
SubscriptionResultFilter
{
	
	private String[] 	textFilters;
	private Pattern[]	textFilterPatterns;
	
	private String[] 	excludeTextFilters;
	private Pattern[]	excludeTextFilterPatterns;
	
	private String regexFilter;	// unused
	
	private long minSeeds = -1;
	private long minSize = -1;
	private long maxSize = -1;
	private String categoryFilter = null;
	
	public String
	getString()
	{
		String	res = addString( "", "+", getString(textFilters));
	
		res = addString( res, "-", getString(excludeTextFilters));
		
		res = addString( res, "regex=", regexFilter );

		res = addString( res, "cat=", categoryFilter );

		return( res );
	}
	
	private String
	addString(
		String	existing,
		String	key,
		String	rest )
	{
		if ( rest == null || rest.length() == 0 ){
			
			return( existing );
		}
		
		String str = key + rest;
		
		if ( existing == null || existing.length() == 0){
			
			return( str );
		}
		
		return( existing + "," + str );
	}
		
	private String
	getString(
		String[]		strs )
	{
		String	res = "";
		
		for( int i=0;i<strs.length;i++){
			res += (i==0?"":"&") + strs[i]; 
		}
		
		return( res );
	}
	
	public SubscriptionResultFilter(Map filters) {
		try {
			textFilters = importStrings(filters,"text_filter"," ");
			
			textFilterPatterns = getPatterns( textFilters );
			
			excludeTextFilters = importStrings(filters,"text_filter_out"," ");
			
			excludeTextFilterPatterns = getPatterns( excludeTextFilters );

			
			regexFilter = ImportExportUtils.importString(filters, "text_filter_regex");
			
			minSize = ImportExportUtils.importLong(filters,"min_size",-1l);
			
			maxSize = ImportExportUtils.importLong(filters,"max_size",-1l);
			
			minSeeds = ImportExportUtils.importLong(filters, "min_seeds",-1l);
			
			String rawCategory = ImportExportUtils.importString(filters,"category");
			if(rawCategory != null) {
				categoryFilter = rawCategory.toLowerCase();
			}
			
		} catch(Exception e) {
			//Invalid filters array
		}
	}

	private static Pattern[] NO_PATTERNS = {};
	
	private Pattern[]
	getPatterns(
		String[]	strs )
	{
		if ( strs.length == 0 ){
			
			return( NO_PATTERNS );
		}
		
		Pattern[] pats = new Pattern[strs.length];
		
		for (int i=0;i<strs.length;i++){
		
			try{
				pats[i] = Pattern.compile( strs[i].trim());
				
			}catch( Throwable e ){
				
				System.out.println( "Failed to compile pattern '" + strs[i] );
			}
		}		
		
		return( pats );
	}
	
	private String[] importStrings(Map filters,String key,String separator) throws IOException {
		String rawStringFilter = ImportExportUtils.importString(filters,key);
		if(rawStringFilter != null) {
			StringTokenizer st = new StringTokenizer(rawStringFilter,separator);
			String[] stringFilter = new String[st.countTokens()];
			for(int i = 0 ; i < stringFilter.length ; i++) {
				stringFilter[i] = st.nextToken().toLowerCase();
			}
			return stringFilter;
		}
		return new String[0];
	}
	
	public Result[] filter(Result[] results) {
		List<Result> filteredResults = new ArrayList<Result>(results.length);
		for(int i = 0 ; i < results.length ; i++) {
			Result result = results[i];
			
			String name = result.getName();
			//Results need a name, or they are by default invalid
			if(name == null) {
				continue;
			}
			name = name.toLowerCase();
			
			boolean valid = true;
			for(int j = 0 ; j < textFilters.length ; j++) {
				
				//If one of the text filters do not match, let's not keep testing the others
				// and mark the result as not valid
				if(name.indexOf(textFilters[j]) == -1) {
					
						// double check against reg-expr if exists
					
					Pattern p = textFilterPatterns[j];
					
					if ( p == null  || !p.matcher( name ).find()){
					
						valid = false;
					
						break;
					}
				}
			}
			
			//if invalid after name check, let's get to the next result
			if(!valid) {
				continue;
			}
			
			for(int j = 0 ; j < excludeTextFilters.length ; j++) {
				
				//If one of the text filters do not match, let's not keep testing the others
				// and mark the result as not valid
				if(name.indexOf(excludeTextFilters[j]) != -1) {
					valid = false;
					break;
				}else{
					Pattern p = excludeTextFilterPatterns[j];
					
					if ( p != null  && p.matcher( name ).find()){
						valid = false;
						break;
					}
				}
			}
			
			//if invalid after name check, let's get to the next result
			if(!valid) {
				continue;
			}
			
			long size = result.getSize();
			
			if(minSize > -1) {
				if(minSize > size) {
					continue;
				}
			}
			
			if(maxSize > -1) {
				if(maxSize < size) {
					continue;
				}
			}
			
			if(minSeeds > -1) {
				if(minSeeds < result.getNbSeeds()) {
					continue;
				}
			}
			
			if(categoryFilter != null) {
				String category = result.getCategory();
				if(category == null || !category.equalsIgnoreCase(categoryFilter)) {
					continue;
				}
			}
			
			
			//All filters are ok, let's add the results to the filtered results
			filteredResults.add(result);
			
		}
		
		Result[] fResults = (Result[]) filteredResults.toArray(new Result[filteredResults.size()]);
		
		return fResults;
	}
}