/*
 * Created on Jul 9, 2009
 * Created by Paul Gardner
 * 
 * Copyright 2009 Vuze, Inc.  All rights reserved.
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


package com.aelitis.azureus.core.content;

import org.gudy.azureus2.core3.util.Base32;
import org.gudy.azureus2.plugins.download.Download;

import com.aelitis.azureus.core.cnetwork.ContentNetwork;

public abstract class 
RelatedContent 
{
	final private String 		title;
	final private byte[]		hash;
	final private String		tracker;
	final private long			size;
	private int					date;
	private int					seeds_leechers;
	private byte				content_network;
	
	private byte[]		related_to_hash;

	public
	RelatedContent(
		byte[]		_related_to_hash,
		String		_title,
		byte[]		_hash,
		String		_tracker,
		long		_size,
		int			_date,
		int			_seeds_leechers,
		byte		_cnet )
	{
		related_to_hash		= _related_to_hash;
		title				= _title;
		hash				= _hash;
		tracker				= _tracker;
		size				= _size;
		date				= _date;
		seeds_leechers		= _seeds_leechers;
		content_network		= _cnet;
	}
	
	public
	RelatedContent(
		String		_title,
		byte[]		_hash,
		String		_tracker,
		long		_size,
		int			_date,
		int			_seeds_leechers,
		byte		_cnet )
	{
		title				= _title;
		hash				= _hash;
		tracker				= _tracker;
		size				= _size;
		date				= _date;
		seeds_leechers		= _seeds_leechers;
		content_network		= _cnet;
	}
	
	protected void
	setRelatedToHash(
		byte[]		h )
	{
		related_to_hash = h;
	}
	
	public byte[]
	getRelatedToHash()
	{
		return( related_to_hash );
	}
	
	public abstract Download
	getRelatedToDownload();
	
	public String
	getTitle()
	{
		return( title );
	}
	
	public abstract int
	getRank();
	
	public byte[]
	getHash()
	{
		return( hash );
	}
	
	public abstract int
	getLevel();
	
	public abstract boolean
	isUnread();
	
	public abstract void
	setUnread(
		boolean	unread );
	
	public abstract int
	getLastSeenSecs();
	
	public String
	getTracker()
	{
		return( tracker );
	}
	
	public long
	getSize()
	{
		return( size );
	}
	
	public long
	getPublishDate()
	{
		return( date*60*60*1000L );
	}
	
	protected int
	getDateHours()
	{
		return( date );
	}
	
	protected void
	setDateHours(
		int		_date )
	{
		date = _date;
	}
	
	public int
	getLeechers()
	{
		if ( seeds_leechers == -1 ){
			
			return( -1 );
		}
		
		return( seeds_leechers&0xffff );
	}
	
	public int
	getSeeds()
	{
		if ( seeds_leechers == -1 ){
			
			return( -1 );
		}
		
		return( (seeds_leechers>>16) & 0xffff );
	}
	
	protected int
	getSeedsLeechers()
	{
		return( seeds_leechers );
	}
	
	protected void
	setSeedsLeechers(
		int		_sl )
	{
		seeds_leechers = _sl;
	}
	
	public long
	getContentNetwork()
	{
		return((content_network&0xff)==0xff?ContentNetwork.CONTENT_NETWORK_UNKNOWN:(content_network&0xff));
	}
	
	protected void
	setContentNetwork(
		long		cnet )
	{
		content_network = (byte)cnet;
	}
	
	public abstract void
	delete();
	
	public String
	getString()
	{
		return( "title=" + title + ", hash=" + (hash==null?"null":Base32.encode( hash )) + ", tracker=" + tracker +", date=" + date + ", sl=" + seeds_leechers + ", cnet=" + content_network );
	}
}
