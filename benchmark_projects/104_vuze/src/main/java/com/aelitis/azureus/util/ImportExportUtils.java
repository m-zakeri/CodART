package com.aelitis.azureus.util;

import java.io.IOException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.gudy.azureus2.core3.util.UrlUtils;
import org.json.simple.JSONArray;

/**
 * Note: There's a similarly defined map processing utility class called
 * {@link MapUtils}.  Since there are differences in implementation, both
 * have been kept until someone goes through each callee and check if it
 * can be switched to use just one of them.
 */
public final class ImportExportUtils {
	
	public final static void
	exportString(
		Map		map,
		String	key,
		String	value )
	
		throws IOException
	{
		if ( value != null ){
	
			map.put( key, value.getBytes( "UTF-8" ));
		}
	}
	
	public final static void
	exportJSONString(
		Map		map,
		String	key,
		String	value )
	
		throws IOException
	{
		if ( value != null ){
	
			map.put( key, value );
		}
	}
	
	public final static String
	importString(
		Map		map,
		String	key,
		String	def )
	
		throws IOException
	{
		String	res = importString( map, key );
		
		if ( res == null ){
			
			res = def;
		}
		
		return( res );
	}
	
	public final static String
	importString(
		Map		map,
		String	key )
	
		throws IOException
	{
		if ( map == null ){
			
			return( null );
		}
		
		Object	obj = map.get( key );
		
		if ( obj instanceof String ){
			
			return((String)obj);
			
		}else if ( obj instanceof byte[]){
			
			return( new String((byte[])obj, "UTF-8" ));
		}
		
		return( null );
	}
	
	public final static long
	importLong(
		Map		map,
		String	key )
	
		throws IOException
	{
		return( importLong( map, key, 0 ));
	}
	
	public final static long
	importLong(
		Map		map,
		String	key,
		long	def )
	
		throws IOException
	{
		if ( map == null ){
			
			return( def );
		}
		
		Object	obj = map.get( key );
		
		if ( obj instanceof Long){
			
			return(((Long)obj).longValue());
			
		}else if ( obj instanceof String ){
			
			return( Long.parseLong((String)obj));
		}
		
		return( def );
	}

	public final static void
	exportLong(
		Map		map,
		String	key,
		long	value )
	{
		map.put( key, value );
	}
	
	public final static void
	exportInt(
		Map		map,
		String	key,
		int		value )
	{
		map.put( key, new Long( value ));
	}
	
	public final static int
	importInt(
		Map		map,
		String	key )
	
		throws IOException
	{
		return((int)importLong( map, key, 0 ));
	}
	
	public final static int
	importInt(
		Map		map,
		String	key,
		int		def )
	
		throws IOException
	{
		return((int)importLong( map, key, def ));
	}
	
	public final static void
	exportFloat(
		Map		map,
		String	key,
		float	value )
	
		throws IOException
	{
		exportString( map, key, String.valueOf( value ));
	}
	
	public final static float
	importFloat(
		Map		map,
		String	key,
		float	def )
	
		throws IOException
	{
		String	str = importString( map, key );
		
		if ( str == null ){
			
			return( def );
		}
		
		return( Float.parseFloat( str ));
	}
	
	public final static void
	exportBoolean(
		Map		map,
		String	key,
		boolean	value )
	
		throws IOException
	{
		map.put( key, new Long( value?1:0 ));
	}
	
	public final static boolean
	importBoolean(
		Map		map,
		String	key )
	
		throws IOException
	{
		return( importBoolean( map, key, false ));
	}
	
	public final static boolean
	importBoolean(
		Map		map,
		String	key,
		boolean	def )
	
		throws IOException
	{
		if ( map == null ){
			
			return( def );
		}
		
		Object	obj = map.get( key );
		
		if ( obj instanceof Long){
			
			return(((Long)obj).longValue() == 1 );
			
		}else if ( obj instanceof Boolean ){
			
			return(((Boolean)obj).booleanValue());
		}
		
		return( def );
	}
	
	public final static void
	exportJSONBoolean(
		Map		map,
		String	key,
		boolean	value )
	
		throws IOException
	{
		map.put( key, new Boolean( value ));
	}
	
	public static final String
	importURL(
		Map		map,
		String	key )
	
		throws IOException
	{
		String url = importString( map, key );
		
		if ( url != null ){
			
			url = url.trim();
			
			if ( url.length() == 0 ){
				
				url = null;
				
			}else{
				
				url = URLDecoder.decode( url, "UTF-8" );
			}
		}
		
		return( url );
	}
	
	public final static void
	exportURL(
		Map		map,
		String	key,
		String	value )
	
		throws IOException
	{
		exportString( map, key, value );
	}
	
	public final static void
	exportJSONURL(
		Map		map,
		String	key,
		String	value )
	
		throws IOException
	{
		exportJSONString( map, key, UrlUtils.encode( value ));
	}
	
	public static final String[]
	importStringArray(
		Map		map,
		String	key )
	
		throws IOException
	{
		List	list = (List)map.get( key );
		
		if ( list == null ){
			
			return( new String[0] );
		}
		
		String[]	res = new String[list.size()];
		
		for (int i=0;i<res.length;i++){
			
			Object obj = list.get(i);
			
			if ( obj instanceof String ){
				
				res[i] = (String)obj;
				
			}else if ( obj instanceof byte[] ){
				
				res[i] = new String((byte[])obj, "UTF-8" );
			}
		}
		
		return( res );
	}
	
	public static final void
	exportStringArray(
		Map			map,
		String		key,
		String[]	data )
	
		throws IOException
	{
		List	l = new ArrayList(data.length);
		
		map.put( key, l );
		
		for (int i=0;i<data.length;i++){
			
			l.add( data[i].getBytes( "UTF-8" ));
		}
	}
	
	public static final void
	exportJSONStringArray(
		Map			map,
		String		key,
		String[]	data )
	
		throws IOException
	{
		List	l = new JSONArray(data.length);
		
		map.put( key, l );
		
		for (int i=0;i<data.length;i++){
			
			l.add( data[i] );
		}
	}
	
	public static final void
	exportIntArray(
		Map			map,
		String		key,
		int[]		values )
	{
		if ( values == null ){
			
			return;
		}
		
		int	num = values.length;
		
		byte[]	bytes 	= new byte[num*4];
		int		pos		= 0;
		
		for (int i=0;i<num;i++){
			
			int	v = values[i];
			
		    bytes[pos++] = (byte)(v >>> 24);
		    bytes[pos++] = (byte)(v >>> 16);
		    bytes[pos++] = (byte)(v >>> 8);
		    bytes[pos++] = (byte)(v);
		}
		
		map.put( key, bytes );
	}
	
	public static final int[]
	importIntArray(
		Map			map,
		String		key )
	{
		byte[]	bytes = (byte[])map.get( key );
		
		if ( bytes == null ){
			
			return( null );
		}
		
		int[]	values = new int[bytes.length/4];
		
		int	pos = 0;
		
		for (int i=0;i<values.length;i++){
			
			values[i] =  
				((bytes[pos++]&0xff) << 24) + 
				((bytes[pos++]&0xff) << 16) + 
				((bytes[pos++]&0xff) << 8) + 
				((bytes[pos++]&0xff)); 
		}
		
		return( values );
	}
}
