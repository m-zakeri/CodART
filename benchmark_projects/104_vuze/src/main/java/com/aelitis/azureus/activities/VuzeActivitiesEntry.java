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

import java.util.HashMap;
import java.util.Map;

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.core3.torrent.TOTorrent;
import org.gudy.azureus2.core3.torrent.TOTorrentException;
import org.gudy.azureus2.core3.torrent.TOTorrentFactory;
import org.gudy.azureus2.core3.util.*;

import com.aelitis.azureus.core.AzureusCoreFactory;
import com.aelitis.azureus.core.torrent.PlatformTorrentUtils;
import com.aelitis.azureus.ui.common.table.TableColumnCore;
import com.aelitis.azureus.ui.common.table.TableColumnSortObject;
import com.aelitis.azureus.ui.selectedcontent.SelectedContentV3;
import com.aelitis.azureus.ui.utils.ImageBytesDownloader;
import com.aelitis.azureus.ui.utils.ImageBytesDownloader.ImageDownloaderListener;
import com.aelitis.azureus.util.DataSourceUtils;
import com.aelitis.azureus.util.MapUtils;
import com.aelitis.azureus.util.PlayUtils;

/**
 * 
 * Comparable implementation sorts on timestamp.<P>
 * equals() implementation compares IDs
 * 
 * @author TuxPaper
 * @created Jan 28, 2008
 *
 */
public class VuzeActivitiesEntry
	implements TableColumnSortObject
{
	private String text;

	private String iconID;

	private String id;

	private long timestamp;

	private String typeID;

	private String assetHash;

	private String assetImageURL;

	private DownloadManager dm;

	public Object urlInfo;

	public TableColumnCore tableColumn;

	private byte[] imageBytes;

	private boolean showThumb = true;

	private String torrentName;

	private TOTorrent torrent;

	private boolean playable;
	
	private long readOn;

	private GlobalManager gm = null;
	
	public VuzeActivitiesEntry(long timestamp, String text, String typeID) {
		this.setText(text);
		this.timestamp = timestamp;
		this.setTypeID(typeID, true);
	}

	public VuzeActivitiesEntry(long timestamp, String text, String icon,
			String id, String typeID, String assetHash) {
		this.timestamp = timestamp;
		this.setText(text);
		this.setIconID(icon);
		this.setID(id);
		this.setTypeID(typeID, true);
		this.setAssetHash(assetHash);
	}

	/**
	 * 
	 */
	public VuzeActivitiesEntry() {
		this.timestamp = SystemTime.getCurrentTime();
	}

	/**
	 * @param platformEntry
	 */
	public void loadFromExternalMap(Map<?, ?> platformEntry) {
		timestamp = SystemTime.getCurrentTime()
				- MapUtils.getMapLong(platformEntry, "age-ms", 0);
		setIconID(MapUtils.getMapString(platformEntry, "icon-url",
				MapUtils.getMapString(platformEntry, "icon-id", null)));
		setTypeID(MapUtils.getMapString(platformEntry, "type-id", null), true);
		setAssetHash(MapUtils.getMapString(platformEntry, "related-asset-hash",
				null));
		setAssetImageURL(MapUtils.getMapString(platformEntry, "related-image-url",
				null));
		setTorrentName(MapUtils.getMapString(platformEntry, "related-asset-name",
				null));
		setReadOn(MapUtils.getMapLong(platformEntry, "readOn", 0));
		loadCommonFromMap(platformEntry);
	}

	public void loadFromInternalMap(Map<?, ?> map) {
		timestamp = MapUtils.getMapLong(map, "timestamp", 0);
		if (timestamp == 0) {
			timestamp = SystemTime.getCurrentTime();
		}
		setAssetHash(MapUtils.getMapString(map, "assetHash", null));
		setIconID(MapUtils.getMapString(map, "icon", null));
		setTypeID(MapUtils.getMapString(map, "typeID", null), true);
		setShowThumb(MapUtils.getMapLong(map, "showThumb", 1) == 1);
		setAssetImageURL(MapUtils.getMapString(map, "assetImageURL", null));
		setImageBytes(MapUtils.getMapByteArray(map, "imageBytes", null));
		setReadOn(MapUtils.getMapLong(map, "readOn", SystemTime.getCurrentTime()));
		loadCommonFromMap(map);
	}

	public void loadCommonFromMap(Map<?, ?> map) {
		if (!playable) {
			setPlayable(MapUtils.getMapBoolean(map, "playable", false));
		}
		setID(MapUtils.getMapString(map, "id", null));
		setText(MapUtils.getMapString(map, "text", null));
		Map<?, ?> torrentMap = MapUtils.getMapMap(map, "torrent", null);
		if (torrentMap != null) {
			TOTorrent torrent = null;
			try {
				torrent = TOTorrentFactory.deserialiseFromMap(torrentMap);
				setTorrent(torrent);
			} catch (TOTorrentException e) {
			}
		}
		if (dm == null && torrentName == null) {
			setTorrentName(MapUtils.getMapString(map, "torrent-name", null));
		}
	}

	// @see java.lang.Object#equals(java.lang.Object)
	public boolean equals(Object obj) {
		if ((obj instanceof VuzeActivitiesEntry) && id != null) {
			return id.equals(((VuzeActivitiesEntry) obj).id);
		}
		return super.equals(obj);
	}

	// @see java.lang.Comparable#compareTo(java.lang.Object)
	public int compareTo(Object obj) {
		if (obj instanceof VuzeActivitiesEntry) {
			VuzeActivitiesEntry otherEntry = (VuzeActivitiesEntry) obj;

			long x = (timestamp - otherEntry.timestamp);
			return x == 0 ? 0 : x > 0 ? 1 : -1;
		}
		// we are bigger
		return 1;
	}

	public void setAssetImageURL(final String url) {
		if (url == null && assetImageURL == null) {
			return;
		}
		if (url == null || url.length() == 0) {
			assetImageURL = null;
			VuzeActivitiesManager.triggerEntryChanged(VuzeActivitiesEntry.this);
			return;
		}
		if (url.equals(assetImageURL)) {
			return;
		}

		assetImageURL = url;
		ImageBytesDownloader.loadImage(url, new ImageDownloaderListener() {
			public void imageDownloaded(byte[] image) {
				setImageBytes(image);
				VuzeActivitiesManager.triggerEntryChanged(VuzeActivitiesEntry.this);
			}
		});
	}

	public String getAssetImageURL() {
		return assetImageURL;
	}

	public Map<String, Object> toDeletedMap() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("timestamp", new Long(timestamp));
		map.put("id", id);
		return map;
	}

	@SuppressWarnings({
		"unchecked",
		"rawtypes"
	})
	public Map<String, Object> toMap() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("timestamp", new Long(timestamp));
		if (assetHash != null) {
			map.put("assetHash", assetHash);
		}
		map.put("icon", getIconID());
		map.put("id", id);
		map.put("text", getText());
		map.put("typeID", getTypeID());
		map.put("assetImageURL", assetImageURL);
		map.put("showThumb", new Long(getShowThumb() ? 1 : 0));
		if (imageBytes != null) {
			map.put("imageBytes", imageBytes);
		} else if (dm != null) {
			byte[] thumbnail = PlatformTorrentUtils.getContentThumbnail(dm.getTorrent());
			if (thumbnail != null) {
				map.put("imageBytes", thumbnail);
			}
		}

		if (torrent != null && (dm == null || assetHash == null)) {
			try {
				// make a copy of the torrent

				Map torrent_map = torrent.serialiseToMap();
				
				TOTorrent torrent_to_send = TOTorrentFactory.deserialiseFromMap( torrent_map );

				Map<?, ?>	vuze_map = (Map<?, ?>)torrent_map.get( "vuze" );
				
				// remove any non-standard stuff (e.g. resume data)

				torrent_to_send.removeAdditionalProperties();

				torrent_map = torrent_to_send.serialiseToMap();
				
				if ( vuze_map != null ){
					
					torrent_map.put( "vuze", vuze_map );
				}
				
				map.put("torrent", torrent_map );
			} catch (TOTorrentException e) {
				Debug.outNoStack("VuzeActivityEntry.toMap: " + e.toString());
			}
		}
		if (torrentName != null) {
			map.put("torrent-name", torrentName);
		}
		
		if (playable) {
			map.put("playable", new Long(playable ? 1 : 0));
		}
		
		map.put("readOn", new Long(readOn));
		
		return map;
	}

	public long getTimestamp() {
		return timestamp;
	}

	public void setTimestamp(long timestamp) {
		if (this.timestamp == timestamp) {
			return;
		}
		this.timestamp = timestamp;
		if (tableColumn != null) {
			tableColumn.setLastSortValueChange(SystemTime.getCurrentTime());
		}
	}

	/**
	 * @param typeID the typeID to set
	 */
	public void setTypeID(String typeID, boolean autoSetIcon) {
		this.typeID = typeID;
		if (getIconID() == null && typeID != null) {
			setIconID("image.vuze-entry." + typeID.toLowerCase());
		}
	}

	/**
	 * @return the typeID
	 */
	public String getTypeID() {
		return typeID;
	}

	/**
	 * @param iconID the iconID to set
	 */
	public void setIconID(String iconID) {
		if (iconID != null && iconID.indexOf("image.") < 0
				&& !iconID.startsWith("http")) {
			iconID = "image.vuze-entry." + iconID;
		}
		this.iconID = iconID;
	}

	/**
	 * @return the iconID
	 */
	public String getIconID() {
		return iconID;
	}

	/**
	 * @param text the text to set
	 */
	public void setText(String text) {
		this.text = text;
	}

	/**
	 * @return the text
	 */
	public String getText() {
		return text;
	}

	/**
	 * @param id the id to set
	 */
	public void setID(String id) {
		this.id = id;
	}

	/**
	 * @return the id
	 */
	public String getID() {
		return id;
	}

	/**
	 * @param assetHash the assetHash to set
	 */
	public void setAssetHash(String assetHash) {
		this.assetHash = assetHash;
		if (assetHash != null) {
			try {
  			if (gm == null) {
  				gm = AzureusCoreFactory.getSingleton().getGlobalManager();
  			}
  			setDownloadManager(gm.getDownloadManager(new HashWrapper(
  					Base32.decode(assetHash))));
			} catch (Exception e) {
				setDownloadManager(null);
				Debug.out("Core not ready", e);
			}
		} else {
			setDownloadManager(null);
		}
	}

	/**
	 * @return the assetHash
	 */
	public String getAssetHash() {
		return assetHash;
	}

	/**
	 * @param dm the dm to set
	 */
	public void setDownloadManager(DownloadManager dm) {
		if (this.dm == dm) {
			return;
		}
		if (gm == null) {
			try {
				gm = AzureusCoreFactory.getSingleton().getGlobalManager();
			} catch (Exception e) {
				// ignore
			}
		}
		
		this.dm = dm;
		if (dm != null) {
			setTorrent(dm.getTorrent());
		}
	}

	/**
	 * @return the dm
	 */
	public DownloadManager getDownloadManger() {
		if (gm != null && !gm.contains(dm)) {
			setDownloadManager(null);
			return null;
		}
		return dm;
	}

	/**
	 * @param imageBytes the imageBytes to set
	 */
	public void setImageBytes(byte[] imageBytes) {
		this.imageBytes = imageBytes;
	}

	/**
	 * @return the imageBytes
	 */
	public byte[] getImageBytes() {
		return imageBytes;
	}

	/**
	 * @param showThumb the showThumb to set
	 */
	public void setShowThumb(boolean showThumb) {
		this.showThumb = showThumb;
	}

	/**
	 * @return the showThumb
	 */
	public boolean getShowThumb() {
		return showThumb;
	}

	/**
	 * Independant for {@link #getDownloadManger()}.  This will be written to
	 * the map.
	 * 
	 * @return Only returns TOTorrent set via {@link #setTorrent(TOTorrent)}
	 *
	 * @since 3.0.5.3
	 */
	public TOTorrent getTorrent() {
		return torrent;
	}

	/**
	 * Not needed if you {@link #setDownloadManager(DownloadManager)}. This will
	 * be written the map.
	 * 
	 * @param torrent
	 *
	 * @since 3.0.5.3
	 */
	public void setTorrent(TOTorrent torrent) {
		this.torrent = torrent;

		try {
			assetHash = torrent.getHashWrapper().toBase32String();
		} catch (Exception e) {
		}
	}

	public String getTorrentName() {
		if (torrentName == null) {
			if (dm != null) {
				return PlatformTorrentUtils.getContentTitle2(dm);
			}
			if (torrent != null) {
				return TorrentUtils.getLocalisedName(torrent);
			}
		}
		return torrentName;
	}

	public void setTorrentName(String torrentName) {
		this.torrentName = torrentName;
	}

	public SelectedContentV3 createSelectedContentObject()
			throws Exception {

		boolean ourContent = DataSourceUtils.isPlatformContent(this);
		
		SelectedContentV3 sc = new SelectedContentV3();
		if (assetHash == null) {
			// Contains no content
			return sc;
		}

		dm = getDownloadManger();
		if (dm != null) {
			sc.setDisplayName(PlatformTorrentUtils.getContentTitle2(dm));
			sc.setDownloadManager(dm);
			return sc;
		}else{
			if ( torrent != null ){
				sc.setTorrent( torrent );
			}
		}

		sc.setDisplayName(getTorrentName());
		if (sc.getDisplayName() == null) {
			TOTorrent torrent = getTorrent();
			if (torrent != null) {
				sc.setDisplayName(TorrentUtils.getLocalisedName(torrent));
				sc.setHash(torrent.getHashWrapper().toBase32String(), ourContent);
			}
		}
		
		if (sc.getHash() == null ){
			
			if ( assetHash != null ){

				sc.setHash(assetHash, true);
			}
		}

		sc.setThumbURL(assetImageURL);
		sc.setImageBytes(imageBytes);

		return sc;

	}

	public boolean isPlayable() {
		// our variable is an override
		if (playable)  {
			return true;
		}
		// use torrent so we don't recurse
		return PlayUtils.canPlayDS(DataSourceUtils.getTorrent(this), -1);
	}

	public void setPlayable(boolean playable) {
		this.playable = playable;
	}

	public long getReadOn() {
		return readOn;
	}

	public void setReadOn(long readOn) {
		if (this.readOn == readOn) {
			return;
		}
		this.readOn = readOn;
		VuzeActivitiesManager.triggerEntryChanged(VuzeActivitiesEntry.this);		
	}
	
	public void setRead(boolean read) {
		long now = SystemTime.getCurrentTime();
		if (read) {
			setReadOn(now);
		} else {
			setReadOn(now * -1);
		}
	}
	
	public boolean isRead() {
		return readOn > 0;
	}
	
	public boolean canFlipRead() {
		long ofs = SystemTime.getOffsetTime(-300);
		if (readOn > 0) {
			return ofs > readOn;
		} else {
			return ofs > (-1 * readOn);
		}
	}
}
