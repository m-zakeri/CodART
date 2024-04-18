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

package com.aelitis.azureus.activities;

import java.util.*;

import org.gudy.azureus2.core3.util.*;

import com.aelitis.azureus.core.AzureusCore;
import com.aelitis.azureus.core.AzureusCoreLifecycleAdapter;
import com.aelitis.azureus.core.cnetwork.*;
import com.aelitis.azureus.core.messenger.config.PlatformVuzeActivitiesMessenger;
import com.aelitis.azureus.util.ConstantsVuze;
import com.aelitis.azureus.util.MapUtils;

/**
 * Manage Vuze News Entries.  Loads, Saves, and expires them
 * 
 * @author TuxPaper
 * @created Jan 28, 2008
 *
 */
public class VuzeActivitiesManager
{
	public static final long MAX_LIFE_MS = 1000L * 60 * 60 * 24 * 365 * 2;

	private static final long DEFAULT_PLATFORM_REFRESH = 60 * 60 * 1000L * 24;

	private static final String SAVE_FILENAME = "VuzeActivities.config";

	private static ArrayList<VuzeActivitiesListener> listeners = new ArrayList<VuzeActivitiesListener>();

	private static ArrayList<VuzeActivitiesLoadedListener> listenersLoaded = new ArrayList<VuzeActivitiesLoadedListener>();

	private static ArrayList<VuzeActivitiesEntry> allEntries = new ArrayList<VuzeActivitiesEntry>();

	private static AEMonitor allEntries_mon = new AEMonitor("VuzeActivityMan");

	private static List<VuzeActivitiesEntry> removedEntries = new ArrayList<VuzeActivitiesEntry>();

	private static PlatformVuzeActivitiesMessenger.GetEntriesReplyListener replyListener;

	private static AEDiagnosticsLogger diag_logger;

	/** Key: NetworkID, Value: last time we pulled news **/ 
	private static Map<String, Long> lastNewsAt = new HashMap<String, Long>();

	private static boolean skipAutoSave = true;

	private static AEMonitor config_mon = new AEMonitor("ConfigMon");

	private static boolean saveEventsOnClose = false;

	static {
		if (System.getProperty("debug.vuzenews", "0").equals("1")) {
			diag_logger = AEDiagnostics.getLogger("v3.vuzenews");
			diag_logger.log("\n\nVuze News Logging Starts");
		} else {
			diag_logger = null;
		}
	}

	public static void initialize(final AzureusCore core) {
		new AEThread2("lazy init", true) {
			public void run() {
				_initialize(core);
			}
		}.start();
	}

	private static void _initialize(AzureusCore core) {
		if (diag_logger != null) {
			diag_logger.log("Initialize Called");
		}
		
		core.addLifecycleListener(new AzureusCoreLifecycleAdapter() {
			public void stopping(AzureusCore core) {
				if (saveEventsOnClose) {
					saveEventsNow();
				}
			}
		});

		loadEvents();

		ContentNetworkManager cnm = ContentNetworkManagerFactory.getSingleton();
		if (cnm != null) {
			ContentNetwork[] contentNetworks = cnm.getContentNetworks();
			cnm.addListener(new ContentNetworkListener() {

				public void networkRemoved(ContentNetwork network) {
				}

				public void networkChanged(ContentNetwork network) {
				}

				public void networkAdded(ContentNetwork cn) {
					setupContentNetwork(cn);
				}

				public void networkAddFailed(long network_id, Throwable error) {
				}
			});
			
			for (ContentNetwork cn : contentNetworks) {
				setupContentNetwork(cn);
			}
		}
		
		replyListener = new PlatformVuzeActivitiesMessenger.GetEntriesReplyListener() {
			public void gotVuzeNewsEntries(VuzeActivitiesEntry[] entries,
					long refreshInMS) {
				if (diag_logger != null) {
					diag_logger.log("Received Reply from platform with " + entries.length
							+ " entries.  Refresh in " + refreshInMS);
				}

				addEntries(entries);

				if (refreshInMS <= 0) {
					refreshInMS = DEFAULT_PLATFORM_REFRESH;
				}

				SimpleTimer.addEvent("GetVuzeNews",
						SystemTime.getOffsetTime(refreshInMS), new TimerEventPerformer() {
							public void perform(TimerEvent event) {
								pullActivitiesNow(5000, "timer", false);
							}
						});
			}
		};

		pullActivitiesNow(5000, "initial", false);
	}

	/**
	 * @param cn
	 *
	 * @since 4.0.0.5
	 */
	private static void setupContentNetwork(final ContentNetwork cn) {
		cn.addPersistentPropertyChangeListener(new ContentNetworkPropertyChangeListener() {
			// @see com.aelitis.azureus.core.cnetwork.ContentNetworkPropertyChangeListener#propertyChanged(java.lang.String)
			public void propertyChanged(String name) {
				if (!ContentNetwork.PP_ACTIVE.equals(name)) {
					return;
				}
				Object oIsActive = cn.getPersistentProperty(ContentNetwork.PP_ACTIVE);
				boolean isActive = (oIsActive instanceof Boolean)
						? ((Boolean) oIsActive).booleanValue() : false;
				if (isActive) {
					pullActivitiesNow(2000, "CN:PropChange", false);
				}
			}
		});
		
		/*
		final String id_str = cn.getServiceURL( ContentNetwork.SERVICE_IDENTIFY );
		
		if ( id_str != null && id_str.length() > 0 ){
			
			try{
				SimpleTimer.addPeriodicEvent(
					"act:id",
					23*60*60*1000,
					new TimerEventPerformer()
					{
						public void 
						perform(
							TimerEvent event ) 
						{
							identify( cn, id_str );
						}
					});
				
				identify( cn, id_str );
				
			}catch( Throwable e ){
				
				Debug.out( e );
			}
		}
		*/
	}
	
	/**
	 * Pull entries from webapp
	 * 
	 * @param delay max time to wait before running request
	 *
	 * @since 3.0.4.3
	 */
	public static void pullActivitiesNow(long delay, String reason,
			boolean alwaysPull) {
		/*
		ContentNetworkManager cnm = ContentNetworkManagerFactory.getSingleton();
		if (cnm == null) {
			return;
		}
		
		ContentNetwork[] contentNetworks = cnm.getContentNetworks();
		for (ContentNetwork cn : contentNetworks) {
		*/
		{
			// short circuit.. only get vuzenews from default network
			ContentNetwork cn = ConstantsVuze.getDefaultContentNetwork();
			if (cn == null) {
				return; //continue;
			}
			
			String id = "" + cn.getID();
			Long oLastPullTime = lastNewsAt.get(id);
			long lastPullTime = oLastPullTime != null ? oLastPullTime.longValue() : 0;
			long now = SystemTime.getCurrentTime();
			long diff = now - lastPullTime;
			if (!alwaysPull && diff < 5000) {
				return;
			}
			if (diff > MAX_LIFE_MS) {
				diff = MAX_LIFE_MS;
			}
			PlatformVuzeActivitiesMessenger.getEntries(diff, delay,
					reason, replyListener);
			// broken..
			//lastNewsAt.put(id, new Long(now));
		}
	}
	
	public static void clearLastPullTimes() {
		lastNewsAt = new HashMap<String, Long>();
	}

	/**
	 * Clear the removed entries list so that an entry that was once deleted will
	 * will be able to be added again
	 * 
	 *
	 * @since 3.0.4.3
	 */
	public static void resetRemovedEntries() {
		removedEntries.clear();
		saveEvents();
	}

	/**
	 * 
	 *
	 * @since 3.1.1.1
	 */
	private static void saveEvents() {
		saveEventsOnClose  = true;
	}

	/**
	 * 
	 *
	 * @since 3.0.4.3
	 */
	@SuppressWarnings({
		"rawtypes",
		"unchecked"
	})
	private static void loadEvents() {
		skipAutoSave = true;

		try {
			Map<?,?> map = FileUtil.readResilientConfigFile(SAVE_FILENAME);

			// Clear all entries if we aren't on v2
			if (map != null && map.size() > 0
					&& MapUtils.getMapLong(map, "version", 0) < 2) {
				clearLastPullTimes();
				skipAutoSave = false;
				saveEventsNow();
				return;
			}
			
			long cutoffTime = getCutoffTime();

			try {
				lastNewsAt = MapUtils.getMapMap(map, "LastChecks", new HashMap());
			} catch (Exception e) {
				Debug.out(e);
			}

			// "LastCheck" backward compat
			if (lastNewsAt.size() == 0) {
  			long lastVuzeNewsAt = MapUtils.getMapLong(map, "LastCheck", 0);
  			if (lastVuzeNewsAt > 0) {
    			if (lastVuzeNewsAt < cutoffTime) {
    				lastVuzeNewsAt = cutoffTime;
    			}
  				lastNewsAt.put("" + ContentNetwork.CONTENT_NETWORK_VUZE, new Long(
  						lastVuzeNewsAt));
  			}
			}
			
			Object value;

			List newRemovedEntries = (List) MapUtils.getMapObject(map,
					"removed-entries", null, List.class);
			if (newRemovedEntries != null) {
				for (Iterator iter = newRemovedEntries.iterator(); iter.hasNext();) {
					value = iter.next();
					if (!(value instanceof Map)) {
						continue;
					}
					VuzeActivitiesEntry entry = createEntryFromMap((Map) value, true);

					if (entry != null && entry.getTimestamp() > cutoffTime) {
						removedEntries.add(entry);
					}
				}
			}

			value = map.get("entries");
			if (!(value instanceof List)) {
				return;
			}

			List entries = (List) value;
			List<VuzeActivitiesEntry> entriesToAdd = new ArrayList<VuzeActivitiesEntry>(entries.size());
			for (Iterator iter = entries.iterator(); iter.hasNext();) {
				value = iter.next();
				if (!(value instanceof Map)) {
					continue;
				}

				VuzeActivitiesEntry entry = createEntryFromMap((Map) value, true);

				if (entry != null) {
					if (entry.getTimestamp() > cutoffTime) {
						entriesToAdd.add(entry);
					}
				}
			}

			int num = entriesToAdd.size();
			if (num > 0) {
				addEntries((VuzeActivitiesEntry[]) entriesToAdd.toArray(new VuzeActivitiesEntry[num]));
			}
		} finally {
			skipAutoSave = false;
			
			synchronized (SAVE_FILENAME) {
				if (listenersLoaded != null) {
					for (VuzeActivitiesLoadedListener l : listenersLoaded) {
						try {
							l.vuzeActivitiesLoaded();
						} catch (Exception e) {
							Debug.out(e);
						}
					}
					listenersLoaded = null;
				}
			}

		}
	}

	private static void saveEventsNow() {
		if (skipAutoSave) {
			return;
		}

		try {
			config_mon.enter();

			Map<String, Object> mapSave = new HashMap<String, Object>();
			mapSave.put("LastChecks", lastNewsAt);
			mapSave.put("version", new Long(2));

			List<Object> entriesList = new ArrayList<Object>();

			VuzeActivitiesEntry[] allEntriesArray = getAllEntries();
			for (int i = 0; i < allEntriesArray.length; i++) {
				VuzeActivitiesEntry entry = allEntriesArray[i];
				if (entry == null) {
					continue;
				}

				boolean isHeader = VuzeActivitiesConstants.TYPEID_HEADER.equals(entry.getTypeID());
				if (!isHeader) {
					entriesList.add(entry.toMap());
				}
			}
			mapSave.put("entries", entriesList);

			List<Object> removedEntriesList = new ArrayList<Object>();
			for (Iterator<VuzeActivitiesEntry> iter = removedEntries.iterator(); iter.hasNext();) {
				VuzeActivitiesEntry entry = iter.next();
				removedEntriesList.add(entry.toDeletedMap());
			}
			mapSave.put("removed-entries", removedEntriesList);

			FileUtil.writeResilientConfigFile(SAVE_FILENAME, mapSave);

		} catch (Throwable t) {
			Debug.out(t);
		} finally {
			config_mon.exit();
		}
	}

	public static long getCutoffTime() {
		return SystemTime.getOffsetTime(-MAX_LIFE_MS);
	}

	public static void addListener(VuzeActivitiesListener l) {
		listeners.add(l);
	}

	public static void removeListener(VuzeActivitiesListener l) {
		listeners.remove(l);
	}

	public static void addListener(VuzeActivitiesLoadedListener l) {
		synchronized (SAVE_FILENAME) {
			if (listenersLoaded != null) {
				listenersLoaded.add(l);
			} else {
				try {
					l.vuzeActivitiesLoaded();
				} catch (Exception e) {
					Debug.out(e);
				}
			}
		}
	}

	public static void removeListener(VuzeActivitiesLoadedListener l) {
		synchronized (SAVE_FILENAME) {
			if (listenersLoaded != null) {
				listenersLoaded.remove(l);
			}
		}
	}

	/**
	 * 
	 * @param entries
	 * @return list of entries actually added (no dups)
	 *
	 * @since 3.0.4.3
	 */
	public static VuzeActivitiesEntry[] addEntries(VuzeActivitiesEntry[] entries) {
		long cutoffTime = getCutoffTime();

		ArrayList<VuzeActivitiesEntry> newEntries = new ArrayList<VuzeActivitiesEntry>(entries.length);
		ArrayList<VuzeActivitiesEntry> existingEntries = new ArrayList<VuzeActivitiesEntry>(0);

		try {
			allEntries_mon.enter();

			for (int i = 0; i < entries.length; i++) {
				VuzeActivitiesEntry entry = entries[i];
				boolean isHeader = VuzeActivitiesConstants.TYPEID_HEADER.equals(entry.getTypeID());
				if ((entry.getTimestamp() >= cutoffTime || isHeader)
						&& !removedEntries.contains(entry)) {
					if (allEntries.contains(entry)) {
						existingEntries.add(entry);
					} else {
						newEntries.add(entry);
						allEntries.add(entry);
					}
				}
			}
		} finally {
			allEntries_mon.exit();
		}

		VuzeActivitiesEntry[] newEntriesArray = (VuzeActivitiesEntry[]) newEntries.toArray(new VuzeActivitiesEntry[newEntries.size()]);

		if (newEntriesArray.length > 0) {
			saveEventsNow();

			Object[] listenersArray = listeners.toArray();
			for (int i = 0; i < listenersArray.length; i++) {
				VuzeActivitiesListener l = (VuzeActivitiesListener) listenersArray[i];
				l.vuzeNewsEntriesAdded(newEntriesArray);
			}
		}

		if (existingEntries.size() > 0) {
			if (newEntriesArray.length == 0) {
				saveEvents();
			}

  		for (Iterator<VuzeActivitiesEntry> iter = existingEntries.iterator(); iter.hasNext();) {
  			VuzeActivitiesEntry entry = iter.next();
  			triggerEntryChanged(entry);
  		}
		}

		return newEntriesArray;
	}

	public static void removeEntries(VuzeActivitiesEntry[] entries) {
		removeEntries(entries, false);
	}
	
	public static void removeEntries(VuzeActivitiesEntry[] entries, boolean allowReAdd) {
		long cutoffTime = getCutoffTime();

		try {
			allEntries_mon.enter();

			for (int i = 0; i < entries.length; i++) {
				VuzeActivitiesEntry entry = entries[i];
				if (entry == null) {
					continue;
				}
				allEntries.remove(entry);
				boolean isHeader = VuzeActivitiesConstants.TYPEID_HEADER.equals(entry.getTypeID());
				if (!allowReAdd && entry.getTimestamp() > cutoffTime && !isHeader) {
					removedEntries.add(entry);
				}
			}
		} finally {
			allEntries_mon.exit();
		}

		Object[] listenersArray = listeners.toArray();
		for (int i = 0; i < listenersArray.length; i++) {
			VuzeActivitiesListener l = (VuzeActivitiesListener) listenersArray[i];
			l.vuzeNewsEntriesRemoved(entries);
		}
		saveEventsNow();
	}

	public static VuzeActivitiesEntry getEntryByID(String id) {
		try {
			allEntries_mon.enter();

			for (Iterator<VuzeActivitiesEntry> iter = allEntries.iterator(); iter.hasNext();) {
				VuzeActivitiesEntry entry = iter.next();
				if (entry == null) {
					continue;
				}
				String entryID = entry.getID();
				if (entryID != null && entryID.equals(id)) {
					return entry;
				}
			}
		} finally {
			allEntries_mon.exit();
		}

		return null;
	}
	
	public static boolean isEntryIdRemoved(String id) {
		for (VuzeActivitiesEntry entry : removedEntries) {
			if (entry.getID().equals(id)) {
				return true;
			}
		}
		return false;
	}

	public static VuzeActivitiesEntry[] getAllEntries() {
		return allEntries.toArray(new VuzeActivitiesEntry[allEntries.size()]);
	}
	
	public static int getNumEntries() {
		return allEntries.size();
	}

	public static void log(String s) {
		if (diag_logger != null) {
			diag_logger.log(s);
		}
	}

	/**
	 * @param vuzeActivitiesEntry
	 *
	 * @since 3.0.4.3
	 */
	public static void triggerEntryChanged(VuzeActivitiesEntry entry) {
		Object[] listenersArray = listeners.toArray();
		for (int i = 0; i < listenersArray.length; i++) {
			VuzeActivitiesListener l = (VuzeActivitiesListener) listenersArray[i];
			l.vuzeNewsEntryChanged(entry);
		}
		saveEvents();
	}

	/**
	 * @param map
	 * @return
	 *
	 * @since 3.0.5.3
	 */
	public static VuzeActivitiesEntry createEntryFromMap(Map<?, ?> map,
			boolean internalMap) {
		VuzeActivitiesEntry entry;
		entry = new VuzeActivitiesEntry();
		if (internalMap) {
			entry.loadFromInternalMap(map);
		} else {
			entry.loadFromExternalMap(map);
		}
		return entry;
	}
}
