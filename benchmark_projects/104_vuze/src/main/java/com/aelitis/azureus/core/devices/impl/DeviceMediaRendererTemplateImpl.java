/*
 * Created on Jul 10, 2009
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


package com.aelitis.azureus.core.devices.impl;

import java.util.*;

import com.aelitis.azureus.core.devices.Device;
import com.aelitis.azureus.core.devices.DeviceManagerException;
import com.aelitis.azureus.core.devices.DeviceMediaRenderer;
import com.aelitis.azureus.core.devices.DeviceMediaRendererTemplate;
import com.aelitis.azureus.core.devices.TranscodeProfile;

public class 
DeviceMediaRendererTemplateImpl
	implements DeviceMediaRendererTemplate
{
	private List<TranscodeProfile>		profiles = new ArrayList<TranscodeProfile>();
	
	private final DeviceManagerImpl		manager;
	private final String				classification;
	private final String				name;
	private final String				manufacturer;
	private final boolean				auto;
	
	protected
	DeviceMediaRendererTemplateImpl(
		DeviceManagerImpl	_manager,
		String				_classification,
		boolean				_auto )
	{
		manager			= _manager;
		classification 	= _classification;
		auto			= _auto;
		
		int	pos = classification.indexOf( '.' );
		
		if ( pos == -1 ){
			
			manufacturer = classification;
			
		}else{
			
			manufacturer = classification.substring( 0, pos );
		}
		
		pos = classification.lastIndexOf( '.' );
		
		if ( pos == -1 ){
			
			name = classification;
			
		}else{
			
			name = classification.substring( pos+1 );
		}
	}
	
	protected void
	addProfile(
		TranscodeProfile	profile )
	{
		profiles.add( profile );
	}
	
	public TranscodeProfile[]
	getProfiles()
	{
		return( profiles.toArray(new TranscodeProfile[profiles.size()]));
	}
	
	public int
	getType()
	{
		return( Device.DT_MEDIA_RENDERER );
	}
	
	public String
	getName()
	{
		return( name );
	}
	
	public String
	getManufacturer()
	{
		return( manufacturer );
	}
	
	public String
	getClassification()
	{
		return( classification );
	}
	
	public String
	getShortDescription()
	{
		return( null );
	}
	
	public int
	getRendererSpecies()
	{
		return( DeviceMediaRenderer.RS_OTHER );
	}
	
	public boolean
	isAuto()
	{
		return( auto );
	}
	
	public Device
	createInstance(
		String		name )
	
		throws DeviceManagerException
	{
		return( createInstance( name, null, true ));
	}
	
	public Device
	createInstance(
		String		name,
		String		uid,
		boolean		manual )
	
		throws DeviceManagerException
	{
		if ( auto ){
			
			throw( new DeviceManagerException( "Device can't be added manually" ));
		}
		
		Device res = manager.createDevice( Device.DT_MEDIA_RENDERER, uid, classification, name, manual );
		
		return( res );
	}
}