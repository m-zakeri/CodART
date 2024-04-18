/*
 * Created on May 14, 2007
 * Created by Paul Gardner
 * Copyright (C) 2007 Aelitis, All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 * 
 * AELITIS, SAS au capital de 63.529,40 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */


package com.aelitis.azureus.util;

import org.gudy.azureus2.plugins.download.Download;
import org.gudy.azureus2.plugins.torrent.TorrentAttribute;
import org.gudy.azureus2.plugins.torrent.TorrentManager;
import org.gudy.azureus2.pluginsimpl.local.PluginInitializer;

public class 
DownloadUtils 
{
	private static TorrentAttribute	ta_tracker_extensions;
	
	public static synchronized void
	initialise()
	{
		if ( ta_tracker_extensions == null ){
			
			TorrentManager tm = PluginInitializer.getDefaultInterface().getTorrentManager();
	
			ta_tracker_extensions = tm.getAttribute( TorrentAttribute.TA_TRACKER_CLIENT_EXTENSIONS );
		}
	}
	
	public static synchronized void
	addTrackerExtension(
		Download	download,
		String		extension_prefix,
		String		extension_value )
	{
		String	extension = "&" + extension_prefix + "=" + extension_value;
		
		String value = download.getAttribute( ta_tracker_extensions );

		if ( value != null ){

				// if already exists then bail
			
			if ( value.indexOf( extension ) != -1 ){

				return;
			}

				// if prefix exists then remove existing value
			
			if ( value.indexOf( extension_prefix ) != -1 ){

				String[] bits = value.split("&");

				value = "";

				for ( int i=0; i<bits.length; i++ ){

					String bit = bits[i].trim();

					if ( bit.length() == 0 ){

						continue;
					}

					if ( !bit.startsWith( extension_prefix+"=" )){

						value += "&" + bit;
					}
				}
			}

			value += extension;

		}else{

			value = extension;
		}
		
		download.setAttribute( ta_tracker_extensions, value );
	}
	
	public static synchronized String
	getTrackerExtensions(
		Download	download )
	{
		return( download.getAttribute( ta_tracker_extensions ));
	}
	
	public static synchronized void
	removeTrackerExtension(
		Download	download,
		String		extension_prefix )
	{
		String value = download.getAttribute( ta_tracker_extensions );

		if ( value != null ){

			int	pos = value.indexOf( extension_prefix );
			
			if ( pos == -1 ){

				return;
			}

			String[] bits = value.split("&");

			value = "";

			for ( int i=0; i<bits.length; i++ ){

				String bit = bits[i].trim();

				if ( bit.length() == 0 ){

					continue;
				}

				if ( !bit.startsWith(extension_prefix+"=")){

					value += "&" + bit;
				}
			}

			if ( value.length() == 0 ){
				
				value = null;
			}
			
			download.setAttribute( ta_tracker_extensions, value );
		}
	}
}
