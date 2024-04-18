/*
 * Created on Nov 24, 2008
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


package com.aelitis.azureus.core.cnetwork.impl;


import com.aelitis.azureus.core.cnetwork.ContentNetwork;
// import com.aelitis.azureus.core.util.FeatureAvailability;

public class 
ContentNetworkVuze 
	extends ContentNetworkVuzeGeneric
{
	private static final String DEFAULT_ADDRESS = "client.vuze.com"; //DO NOT TOUCH !!!!  use the -Dplatform_address=ip override instead

	private static final String DEFAULT_PORT = "80";

	private static final String DEFAULT_RELAY_ADDRESS = "www.vuze.com"; //DO NOT TOUCH !!!!  use the -Drelay_address=ip override instead

	private static final String DEFAULT_RELAY_PORT = "80";

	private static final String DEFAULT_EXT_ADDRESS = "www.vuze.com"; //DO NOT TOUCH !!!!  

	/*
	static{
		if ( FeatureAvailability.ENABLE_PLUS()){
			
			if ( System.getProperty( "platform_address", "" ).length() == 0 ){
			
				System.setProperty( "platform_address", "www2.vuze.com" );
			}
		}
	}
	*/
	
	private static final String URL_ADDRESS = System.getProperty( "platform_address", DEFAULT_ADDRESS );

	private static final String URL_PORT 	= System.getProperty( "platform_port", DEFAULT_PORT );

	private static final String URL_PREFIX = "http://" + URL_ADDRESS + ":" + URL_PORT + "/";

	private static final String URL_EXT_PREFIX = "http://" 
		+ System.getProperty( "platform_address_ext", DEFAULT_EXT_ADDRESS ) + ":"
		+ System.getProperty( "platform_port_ext", DEFAULT_PORT ) + "/";

	private static final String DEFAULT_AUTHORIZED_RPC = "https://" + URL_ADDRESS + ":443/rpc";

	private static String URL_RELAY_RPC = System.getProperty("relay_url",
			"http://" + System.getProperty("relay_address", DEFAULT_RELAY_ADDRESS)
					+ ":" + System.getProperty("relay_port", DEFAULT_RELAY_PORT)
					+ "/msgrelay/rpc");

	private static final String URL_AUTHORIZED_RPC = System.getProperty(
			"authorized_rpc", "1").equals("1") ? DEFAULT_AUTHORIZED_RPC : URL_PREFIX
			+ "app";
	
	private static final String URL_FAQ = "http://wiki.vuze.com/";

	private static final String URL_BLOG = "http://blog.vuze.com/";
	
	private static final String URL_FORUMS = "http://forum.vuze.com/";
	
	private static final String URL_WIKI = "http://wiki.vuze.com/";

	protected
	ContentNetworkVuze(
		ContentNetworkManagerImpl	manager )
	{
		super( 	manager,
				ContentNetwork.CONTENT_NETWORK_VUZE,
				1,
				"Vuze HD Network",
				null,
				null,
				URL_ADDRESS,
				URL_PREFIX,
				null,			// no icon
				URL_RELAY_RPC,
				URL_AUTHORIZED_RPC,
				URL_FAQ,
				URL_BLOG,
				URL_FORUMS,
				URL_WIKI,
				URL_EXT_PREFIX );
	}
}
