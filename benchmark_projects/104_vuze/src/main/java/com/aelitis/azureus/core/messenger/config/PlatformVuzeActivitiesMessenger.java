/**
 * Created on Jan 28, 2008 
 *
 * Copyright 2008 Vuze, Inc.  All rights reserved.
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
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA 
 */

package com.aelitis.azureus.core.messenger.config;

import java.util.Iterator;
import java.util.List;
import java.util.Map;

import com.aelitis.azureus.activities.VuzeActivitiesEntry;
import com.aelitis.azureus.activities.VuzeActivitiesManager;
import com.aelitis.azureus.core.messenger.PlatformMessage;
import com.aelitis.azureus.core.messenger.PlatformMessenger;
import com.aelitis.azureus.core.messenger.PlatformMessengerListener;
import com.aelitis.azureus.util.MapUtils;

/**
 * @author TuxPaper
 * @created Jan 28, 2008
 *
 */
public class PlatformVuzeActivitiesMessenger
{
	public static final String LISTENER_ID = "vuzenews";

	public static final String OP_GET = "get-entries";

	public static final long DEFAULT_RETRY_MS = 1000L * 60 * 60 * 24;

	public static void getEntries(final long agoMS,
			long maxDelayMS, String reason, final GetEntriesReplyListener replyListener) {
		PlatformMessage message = new PlatformMessage("AZMSG",
				reason.equals("shown") ? "vznews" : LISTENER_ID, OP_GET, new Object[] {
					"ago-ms",
					new Long(agoMS),
					"reason",
					reason,
				}, maxDelayMS);

		PlatformMessengerListener listener = null;
		if (replyListener != null) {
			listener = new PlatformMessengerListener() {
				public void messageSent(PlatformMessage message) {
				}

				public void replyReceived(PlatformMessage message, String replyType,
						Map reply) {
					VuzeActivitiesEntry[] entries = new VuzeActivitiesEntry[0];
					List entriesList = (List) MapUtils.getMapObject(reply, "entries",
							null, List.class);
					if (entriesList != null && entriesList.size() > 0) {
						entries = new VuzeActivitiesEntry[entriesList.size()];
						int i = 0;
						for (Iterator iter = entriesList.iterator(); iter.hasNext();) {
							Map platformEntry = (Map) iter.next();
							if (platformEntry == null) {
								continue;
							}
							
							entries[i] = VuzeActivitiesManager.createEntryFromMap(
									platformEntry, false);
							if (entries[i] != null) {
								i++;
							}
						}
					}
					long refreshInMS = MapUtils.getMapLong(reply, "refresh-in-ms",
							DEFAULT_RETRY_MS);
					replyListener.gotVuzeNewsEntries(entries, refreshInMS);
				}
			};
		}

		PlatformMessenger.queueMessage(message, listener);
	}

	public static interface GetEntriesReplyListener
	{
		public void gotVuzeNewsEntries(VuzeActivitiesEntry[] entries, long refreshInMS);
	}
}
