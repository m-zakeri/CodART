/*
 * Created on Jul 11, 2008
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

import java.net.URL;
import java.util.Map;

import org.gudy.azureus2.pluginsimpl.local.utils.UtilitiesImpl;

public interface 
SubscriptionManager
	extends UtilitiesImpl.PluginSubscriptionManager
{
	public Subscription
	create(
		String		name,
		boolean		is_public,
		String		json )
		
		throws SubscriptionException;
	
	public Subscription
	createRSS(
		String		name,
		URL			url,
		int			check_interval_mins,
		Map			user_data )
		
		throws SubscriptionException;
	
		// creates a subscription that will always have the same identity for the given parameters
		// and can't be updated
	
	public Subscription
	createSingletonRSS(
		String		name,
		URL			url,
		int			check_interval_mins )
	
		throws SubscriptionException;
	
	public int
	getKnownSubscriptionCount();
	
	public int
	getSubscriptionCount(
		boolean	subscribed_only );
	
	public Subscription[]
	getSubscriptions();
	
	public Subscription[]
   	getSubscriptions(
   		boolean	subscribed_only );

	public Subscription
	getSubscriptionByID(
		String			id );
	
		/**
		 * Full lookup
		 * @param hash
		 * @param listener
		 * @return
		 * @throws SubscriptionException
		 */
	
	public SubscriptionAssociationLookup
	lookupAssociations(
		byte[]						hash,
		SubscriptionLookupListener	listener )
	
		throws SubscriptionException;
	
		/**
		 * Cached view of hash's subs
		 * @param hash
		 * @return
		 */
	
	public Subscription[]
	getKnownSubscriptions(
		byte[]						hash );
	
	public Subscription[]
	getLinkedSubscriptions(
		byte[]						hash );
	
	public SubscriptionScheduler
	getScheduler();
	
	public int
	getMaxNonDeletedResults();
	
	public void
	setMaxNonDeletedResults(
		int			max );
	
	public boolean
	getAutoStartDownloads();
	
	public void
	setAutoStartDownloads(
		boolean		auto_start );

	public int
	getAutoStartMinMB();
	
	public void
	setAutoStartMinMB(
		int			mb );

	public int
	getAutoStartMaxMB();
	
	public void
	setAutoStartMaxMB(
		int			mb );

	public boolean
	isRSSPublishEnabled();
	
	public void
	setRSSPublishEnabled(
		boolean		enabled );
	
	public boolean
	isSearchEnabled();
	
	public void
	setSearchEnabled(
		boolean		enabled );
	
	public boolean
	isSubsDownloadEnabled();
	
	public void
	setSubsDownloadEnabled(
		boolean		enabled );
	
	public boolean
	hideSearchTemplates();
	
	public String
	getRSSLink();
	
	public void
	addListener(
		SubscriptionManagerListener	listener );
	
	public void
	removeListener(
		SubscriptionManagerListener	listener );
}
