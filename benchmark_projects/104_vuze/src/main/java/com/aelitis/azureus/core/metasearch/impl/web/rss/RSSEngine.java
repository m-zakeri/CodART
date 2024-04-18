package com.aelitis.azureus.core.metasearch.impl.web.rss;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.core3.util.UrlUtils;
import org.gudy.azureus2.plugins.utils.StaticUtilities;
import org.gudy.azureus2.plugins.utils.xml.rss.RSSChannel;
import org.gudy.azureus2.plugins.utils.xml.rss.RSSFeed;
import org.gudy.azureus2.plugins.utils.xml.rss.RSSItem;
import org.gudy.azureus2.plugins.utils.xml.simpleparser.SimpleXMLParserDocumentAttribute;
import org.gudy.azureus2.plugins.utils.xml.simpleparser.SimpleXMLParserDocumentNode;
import org.json.simple.JSONObject;

import com.aelitis.azureus.core.metasearch.Engine;
import com.aelitis.azureus.core.metasearch.Result;
import com.aelitis.azureus.core.metasearch.ResultListener;
import com.aelitis.azureus.core.metasearch.SearchException;
import com.aelitis.azureus.core.metasearch.SearchParameter;
import com.aelitis.azureus.core.metasearch.impl.EngineImpl;
import com.aelitis.azureus.core.metasearch.impl.MetaSearchImpl;
import com.aelitis.azureus.core.metasearch.impl.web.FieldMapping;
import com.aelitis.azureus.core.metasearch.impl.web.WebEngine;
import com.aelitis.azureus.core.metasearch.impl.web.WebResult;

public class 
RSSEngine 
	extends WebEngine 
{
	private Pattern seed_leecher_pat = Pattern.compile("([0-9]+)\\s+(seed|leecher)s", Pattern.CASE_INSENSITIVE);

	public static EngineImpl
	importFromBEncodedMap(
		MetaSearchImpl		meta_search,
		Map					map )
	
		throws IOException
	{
		return( new RSSEngine( meta_search, map ));
	}
	
	public static Engine
	importFromJSONString(
		MetaSearchImpl		meta_search,
		long				id,
		long				last_updated,
		float				rank_bias,
		String				name,
		JSONObject			map )
	
		throws IOException
	{
		return( new RSSEngine( meta_search, id, last_updated, rank_bias, name, map ));
	}
	
		// explicit constructor
	
	public 
	RSSEngine(
		MetaSearchImpl		meta_search,
		long 				id,
		long 				last_updated,
		float				rank_bias,
		String 				name,
		String 				searchURLFormat,
		boolean				needs_auth,
		String				auth_method,
		String				login_url,
		String[]			required_cookies )
	{
		super( 	meta_search, 
				Engine.ENGINE_TYPE_RSS, 
				id,
				last_updated,
				rank_bias,
				name,
				searchURLFormat,
				"GMT",
				false,
				"EEE, d MMM yyyy HH:mm:ss Z",
				new FieldMapping[0],
				needs_auth,
				auth_method,
				login_url,
				required_cookies );		
	}
	
	protected 
	RSSEngine(
		MetaSearchImpl		meta_search,
		Map					map )
	
		throws IOException
	{
		super( meta_search, map );
	}
	
		// json 
	
	protected 
	RSSEngine(
		MetaSearchImpl		meta_search,
		long				id,
		long				last_updated,
		float				rank_bias,
		String				name,
		JSONObject			map )
	
		throws IOException
	{
		super( meta_search, Engine.ENGINE_TYPE_REGEX, id, last_updated, rank_bias, name, map );
	}
	
	
	public Map 
	exportToBencodedMap()
	
		throws IOException
	{
		return( exportToBencodedMap( false ));
	}
	
	public Map 
	exportToBencodedMap(
		boolean	generic )
	
		throws IOException
	{
		Map	res = new HashMap();
				
		super.exportToBencodedMap( res, generic );
		
		return( res );
	}
	
	public boolean
	supportsField(
		int		field_id )
	{
			// don't know about optional fields (such as direct download - be optimistic)
		
		switch( field_id ){
			case FIELD_NAME:
			case FIELD_DATE:
			case FIELD_CATEGORY:
			case FIELD_COMMENTS:
			case FIELD_CDPLINK:
			case FIELD_TORRENTLINK:
			case FIELD_DOWNLOADBTNLINK:
			{
				return( true );
			}
		}
	
		return( false );
	}
	
	public int 
	getAutoDownloadSupported() 
	{
			// unknown until a successful feed download has occurred so that we know the
			// status of the feed tag
		
		return((int)getLocalLong( LD_AUTO_DL_SUPPORTED, AUTO_DL_SUPPORTED_UNKNOWN ));
	}
	
	protected Result[] 
	searchSupport(
		SearchParameter[] 	searchParameters, 
		Map					searchContext,
		int 				desired_max_matches,
		int					absolute_max_matches,
		String 				headers, 
		ResultListener 		listener) 
	
		throws SearchException 
	{
		debugStart();
		
		boolean	only_if_mod = !searchContext.containsKey( Engine.SC_FORCE_FULL );
		
		pageDetails page_details = super.getWebPageContent( searchParameters, searchContext, headers, only_if_mod );
		
		String	page = page_details.getContent();
		
		if ( listener != null ){
			
			listener.contentReceived( this, page );
		}
			
		if ( page == null || page.length() == 0 ){
			
			return( new Result[0]);
		}
		
		try {
			ByteArrayInputStream bais = new ByteArrayInputStream( page.getBytes("UTF-8"));
			
			RSSFeed rssFeed = StaticUtilities.getRSSFeed( bais );
			
			RSSChannel[] channels = rssFeed.getChannels();
			
			List results = new ArrayList();
			
			for ( int i=0; i<channels.length; i++ ){
				
				RSSChannel channel = channels[i];
				
				SimpleXMLParserDocumentNode[] channel_kids = channel.getNode().getChildren();
				
				int	auto_dl_state = AUTO_DL_SUPPORTED_YES;
				
				for ( int j=0; j<channel_kids.length; j++ ){

					SimpleXMLParserDocumentNode child = channel_kids[j];

					String	lc_full_child_name 	= child.getFullName().toLowerCase();

					if ( lc_full_child_name.equals( "vuze:auto_dl_enabled" )){
						
						if ( !child.getValue().equalsIgnoreCase( "true" )){
							
							auto_dl_state = AUTO_DL_SUPPORTED_NO;
						}
					}
				}			
				
				setLocalLong( LD_AUTO_DL_SUPPORTED, auto_dl_state );
				
				RSSItem[] items = channel.getItems();

				for ( int j=0 ; j<items.length; j++ ){
					
					RSSItem item = items[j];
					
					WebResult result = new WebResult(this,getRootPage(),getBasePage(),getDateParser(),"");
					
					result.setPublishedDate(item.getPublicationDate());
					
					result.setNameFromHTML(item.getTitle());
					
					URL cdp_link = item.getLink();
					
					if ( cdp_link != null ){
					
						result.setCDPLink(cdp_link.toExternalForm());
					}
					
					String uid = item.getUID();
					
					if ( uid != null ){
						
						result.setUID( uid );
					}
					
					boolean got_seeds_peers = false;
					
					SimpleXMLParserDocumentNode node = item.getNode();
					
					if ( node != null ){
						
						SimpleXMLParserDocumentNode[] children = node.getChildren();
						
						boolean vuze_feed = false;
						
						for ( int k=0; k<children.length; k++ ){
														
							SimpleXMLParserDocumentNode child = children[k];
							
							String	lc_full_child_name 	= child.getFullName().toLowerCase();
							
							if ( lc_full_child_name.startsWith( "vuze:" )){
								
								vuze_feed = true;
								
								break;
							}
						}
						
						for ( int k=0; k<children.length; k++ ){
							
							SimpleXMLParserDocumentNode child = children[k];
							
							String	lc_child_name 		= child.getName().toLowerCase();
							String	lc_full_child_name 	= child.getFullName().toLowerCase();
							
							String	value = child.getValue();
							
							if (lc_child_name.equals( "enclosure" )){
								
								SimpleXMLParserDocumentAttribute typeAtt = child.getAttribute("type");
								
								if( typeAtt != null && typeAtt.getValue().equalsIgnoreCase( "application/x-bittorrent")) {
									
									SimpleXMLParserDocumentAttribute urlAtt = child.getAttribute("url");
									
									if( urlAtt != null ){
										
										result.setTorrentLink(urlAtt.getValue());
									}
									
									SimpleXMLParserDocumentAttribute lengthAtt = child.getAttribute("length");
									
									if (lengthAtt != null){
										
										result.setSizeFromHTML(lengthAtt.getValue());
									}
								}
							}else if(lc_child_name.equals( "category" )) {
																
								result.setCategoryFromHTML( value );
								
							}else if(lc_child_name.equals( "comments" )){
								
								result.setCommentsFromHTML( value );
								
							}else if ( lc_child_name.equals( "link" ) || lc_child_name.equals( "guid" )) {
								
								String lc_value = value.toLowerCase();
																
								try{
									URL url = new URL(value);

									if ( 	lc_value.endsWith( ".torrent" ) ||
											lc_value.startsWith( "magnet:" ) ||
											lc_value.startsWith( "bc:" ) ||
											lc_value.startsWith( "bctp:" ) ||
											lc_value.startsWith( "dht:" )){
										
										
										result.setTorrentLink(value);
										
									}else if ( lc_child_name.equals( "link" ) && !vuze_feed ){
									
										long	test = getLocalLong( LD_LINK_IS_TORRENT, 0 );
									
										if ( test == 1 ){
										
											result.setTorrentLink( value );
											
										}else if ( test == 0 || SystemTime.getCurrentTime() - test > 60*1000 ){
										
											if ( linkIsToTorrent( url )){
											
												result.setTorrentLink(value);
												
												setLocalLong( LD_LINK_IS_TORRENT, 1 );
												
											}else{
												
												setLocalLong( LD_LINK_IS_TORRENT, SystemTime.getCurrentTime());
											}
										}
									}
								}catch( Throwable e ){
									
										// see if this is an atom feed 
										//  <link rel="alternate" type="application/x-bittorrent" href="http://asdasd/ 
									
									SimpleXMLParserDocumentAttribute typeAtt = child.getAttribute( "type" );
									
									if ( typeAtt != null && typeAtt.getValue().equalsIgnoreCase("application/x-bittorrent")) {
									
										SimpleXMLParserDocumentAttribute hrefAtt = child.getAttribute( "href" );
										
										if ( hrefAtt != null ){
											
											String	href = hrefAtt.getValue().trim();
											
											try{
												
												result.setTorrentLink( new URL( href ).toExternalForm() );
												
											}catch( Throwable f ){
												
											}
										}
									}
								}
							}else if ( lc_child_name.equals( "content" ) && rssFeed.isAtomFeed()){
								
								SimpleXMLParserDocumentAttribute srcAtt = child.getAttribute( "src" );
								
								String	src = srcAtt==null?null:srcAtt.getValue();
											
								if ( src != null ){
									
									boolean	is_dl_link = false;
									
									SimpleXMLParserDocumentAttribute typeAtt = child.getAttribute( "type" );
									
									if ( typeAtt != null && typeAtt.getValue().equalsIgnoreCase("application/x-bittorrent")) {

										is_dl_link = true;
									}
									
									if ( !is_dl_link ){
									
										is_dl_link = src.toLowerCase().indexOf( ".torrent" ) != -1;
									}
										
									if ( is_dl_link ){
										
										try{
											new URL( src );
										
											result.setTorrentLink( src );
											
										}catch( Throwable e ){
										}
									}
								}
							}else if ( lc_full_child_name.equals( "vuze:size" )){
								
								result.setSizeFromHTML( value );
								
							}else if ( lc_full_child_name.equals( "vuze:seeds" )){
								
								got_seeds_peers = true;
								
								result.setNbSeedsFromHTML( value );
								
							}else if ( lc_full_child_name.equals( "vuze:superseeds" )){
								
								got_seeds_peers = true;
								
								result.setNbSuperSeedsFromHTML( value );
								
							}else if ( lc_full_child_name.equals( "vuze:peers" )){
								
								got_seeds_peers = true;
								
								result.setNbPeersFromHTML( value );
								
							}else if ( lc_full_child_name.equals( "vuze:rank" )){
								
								result.setRankFromHTML( value );
								
							}else if ( lc_full_child_name.equals( "vuze:contenttype" )){
								
								String	type = value.toLowerCase();
								
								if ( type.startsWith( "video" )){
									
									type = Engine.CT_VIDEO;
									
								}else if ( type.startsWith( "audio" )){
									
									type = Engine.CT_AUDIO;
									
								}else if ( type.startsWith( "games" )){
									
									type = Engine.CT_GAME;
								}
								
								result.setContentType( type );
								
							}else if ( lc_full_child_name.equals( "vuze:downloadurl" )){

								result.setTorrentLink( value);
								
							}else if ( lc_full_child_name.equals( "vuze:playurl" )){

								result.setPlayLink( value);
								
							}else if ( lc_full_child_name.equals( "vuze:drmkey" )){

								result.setDrmKey( value);
								
							}else if ( lc_full_child_name.equals( "vuze:assethash" )){

								result.setHash( value);
							}
						}
					}
					
					if ( !got_seeds_peers ){
						
						try{
							SimpleXMLParserDocumentNode desc_node = node.getChild( "description" );
							
							if ( desc_node != null ){
								
								String desc = desc_node.getValue().trim();
								
									// see if we can pull from description
								
								Matcher m = seed_leecher_pat.matcher( desc );
							
								while( m.find()){
									
									String	num = m.group(1);
									
									String	type = m.group(2);
									
									if ( type.toLowerCase().charAt(0) == 's' ){
										
										result.setNbSeedsFromHTML( num );
										
									}else{
										
										result.setNbPeersFromHTML( num );
									}
								}
							}
							
						}catch( Throwable e ){
							
						}
					}
					
						// override existing values with explicit <torrent> entry if present
					
					try{
						SimpleXMLParserDocumentNode torrent_node = node.getChild( "torrent" );
						
						if ( torrent_node != null ){
						
							if ( result.getSize() <= 0 ){
								
								SimpleXMLParserDocumentNode n = torrent_node.getChild( "contentLength" );
								
								if ( n != null ){
									
									try{
										long l = Long.parseLong( n.getValue().trim());
										
										result.setSizeFromHTML( l + " B" );
										
									}catch( Throwable e ){
										
									}
								}
							}
							
							String dlink = result.getDownloadLink();
							
							if ( dlink == null || dlink.length() == 0 ){
								
								SimpleXMLParserDocumentNode n = torrent_node.getChild( "magnetURI" );
								
								if ( n != null ){
									
									dlink = n.getValue().trim();
									
									result.setTorrentLink( dlink );
								}
							}
							
							String hash = result.getHash();
							
							if ( hash == null || hash.length() == 0 ){
								
								SimpleXMLParserDocumentNode n = torrent_node.getChild( "infoHash" );
								
								if ( n != null ){
									
									String h = n.getValue().trim();
									
									result.setHash( h );
									
									if ( dlink == null || dlink.length() == 0 ){
										
										String uri = UrlUtils.normaliseMagnetURI( h );
										
										if ( uri != null ){
											
											result.setTorrentLink( uri );
										}
									}
								}
							}
							
							SimpleXMLParserDocumentNode trackers_node = torrent_node.getChild( "trackers" );

							if ( trackers_node != null && !got_seeds_peers ){
								
								SimpleXMLParserDocumentNode[] groups = trackers_node.getChildren();
								
								int	max_total = -1;
								
								int	best_seeds		= 0;
								int	best_leechers	= 0;
								
								for ( SimpleXMLParserDocumentNode group: groups ){
									
									SimpleXMLParserDocumentNode[] g_kids = group.getChildren();
									
									for ( SimpleXMLParserDocumentNode t: g_kids ){
										
										if ( t.getName().equalsIgnoreCase( "tracker" )){
											
											SimpleXMLParserDocumentAttribute a_seeds 	= t.getAttribute( "seeds" );
											SimpleXMLParserDocumentAttribute a_leechers = t.getAttribute( "peers" );
											
											int	seeds 		= a_seeds==null?-1:Integer.parseInt( a_seeds.getValue().trim());
											int	leechers 	= a_leechers==null?-1:Integer.parseInt( a_leechers.getValue().trim());
											
											int	total = seeds + leechers;
											
											if ( total > max_total ){
											
												max_total = total;
												
												best_seeds 		= seeds;
												best_leechers	= leechers;
											}
										}									
									}
								}
								
								if ( max_total >= 0 ){
									
									result.setNbSeedsFromHTML( String.valueOf( Math.max( 0, best_seeds )));
									result.setNbPeersFromHTML( String.valueOf( Math.max( 0, best_leechers )));
								}
							}
						}
					}catch( Throwable e ){
						
						e.printStackTrace();
					}
					
						// if we still have no download link see if the magnet is in the title
					
					String dlink = result.getDownloadLink();
					
					if ( dlink == null || dlink.length() == 0 ){
						
						String name = result.getName();
						
						if ( name != null ){
							
							String magnet = UrlUtils.parseTextForMagnets( name );
							
							if ( magnet != null ){
								
								result.setTorrentLink( magnet );
							}
						}
					}

					results.add(result);
					
					if ( absolute_max_matches >= 0 && results.size() == absolute_max_matches ){
						
						break;
					}
				}
			}
			
			Result[] res = (Result[]) results.toArray(new Result[results.size()]);

			debugLog( "success: found " + res.length + " results" );
			
			return( res );
			
			
		}catch ( Throwable e ){
			
			debugLog( "failed: " + Debug.getNestedExceptionMessageAndStack( e ));
			
			if ( e instanceof SearchException ){
				
				throw((SearchException)e );
			}
			
			throw( new SearchException( "RSS matching failed", e ));
		}
	}
	
	protected boolean
	linkIsToTorrent(
		URL		url )
	{
		try{
			HttpURLConnection con = (HttpURLConnection)url.openConnection();
			
			con.setRequestMethod( "HEAD" );
			
			con.setConnectTimeout( 10*1000 );
			
			con.setReadTimeout( 10*1000 );
			
			String content_type = con.getContentType();

			log( "Testing link " + url + " to see if torrent link -> content type=" + content_type );
			
			if ( content_type.equalsIgnoreCase( "application/x-bittorrent" )){
				
				return( true );
			}
			
			return( false );
			
		}catch( Throwable e ){
			
			return( false );
		}
	}
}
