/*
 * Created on Sep 22, 2008
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


package com.aelitis.azureus.core.subs;

import java.util.ArrayList;
import java.util.List;

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.torrent.TOTorrent;

import com.aelitis.azureus.core.AzureusCore;

public class 
SubscriptionUtils 
{
	public static SubscriptionDownloadDetails[]
	getAllCachedDownloadDetails(AzureusCore core)
	{
		List<DownloadManager> 	dms 	= core.getGlobalManager().getDownloadManagers();
		
		List<SubscriptionDownloadDetails>	result 	= new ArrayList<SubscriptionDownloadDetails>();
		
		SubscriptionManager sub_man = SubscriptionManagerFactory.getSingleton();
		
		for (int i=0;i<dms.size();i++){
			
			DownloadManager	dm = dms.get(i);
			
			TOTorrent torrent = dm.getTorrent();
			
			if ( torrent != null ){
				
				try{
					Subscription[] subs = sub_man.getKnownSubscriptions( torrent.getHash());
					
					if ( subs != null && subs.length > 0 ){
						
						if ( sub_man.hideSearchTemplates()){
							
							List<Subscription>	filtered = new ArrayList<Subscription>();
							
							for ( Subscription s: subs ){
								
								if ( !s.isSearchTemplate()){
									
									filtered.add( s );
								}
							}
							
							if ( filtered.size() > 0 ){
							
								result.add( new SubscriptionDownloadDetails( dm, filtered.toArray( new Subscription[filtered.size()] )));
							}
						}else{
							
							result.add( new SubscriptionDownloadDetails( dm, subs ));
						}
					}
				}catch( Throwable e ){
				}
			}
		}
		
		return(result.toArray( new SubscriptionDownloadDetails[result.size()]));
	}
	

	
	public static class
	SubscriptionDownloadDetails
	{
		private DownloadManager		download;
		private Subscription[]		subscriptions;
		
		protected
		SubscriptionDownloadDetails(
			DownloadManager		dm,
			Subscription[]		subs )
		{
			download 		= dm;
			subscriptions	= subs;
		}
		
		public DownloadManager
		getDownload()
		{
			return( download );
		}
		
		public Subscription[]
		getSubscriptions()
		{
			return( subscriptions );
		}
	}
}
