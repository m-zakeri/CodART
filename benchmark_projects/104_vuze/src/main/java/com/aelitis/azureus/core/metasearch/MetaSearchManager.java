/*
 * Created on May 6, 2008
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


package com.aelitis.azureus.core.metasearch;

import java.util.Map;

import com.aelitis.azureus.core.vuzefile.VuzeFile;

public interface 
MetaSearchManager 
{
	public MetaSearch
	getMetaSearch();
	
	public boolean
	isAutoMode();
			
	public void
	setSelectedEngines(
		long[]		ids,
		boolean		auto )
	
		throws MetaSearchException;
	
	public Engine
	addEngine(
		long		id,
		int			type,
		String		name,
		String		json_value )
	
		throws MetaSearchException;
	
	public boolean
	isImportable(
		VuzeFile		vf );
	
	public Engine
	importEngine(
		Map			map,
		boolean		warn_user )
	
		throws MetaSearchException;
	
	public void
	addListener(
		MetaSearchManagerListener		listener );
	
	public void
	removeListener(
		MetaSearchManagerListener		listener );
	
	public void
	log(
		String		str );
}
