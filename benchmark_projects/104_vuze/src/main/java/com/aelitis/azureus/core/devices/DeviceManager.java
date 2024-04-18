/*
 * Created on Jan 27, 2009
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


package com.aelitis.azureus.core.devices;

import java.io.File;
import java.net.InetAddress;

public interface 
DeviceManager 
{
	public DeviceTemplate[]
	getDeviceTemplates(
		int		device_type );
	
	public DeviceManufacturer[]
	getDeviceManufacturers(
		int		device_type );
	
	public Device[]
	getDevices();
	
	public Device
	addVirtualDevice(
		int					type,
		String				uid,
		String				classification,
		String				name )
	
		throws DeviceManagerException;
	
	Device addInetDevice(
		int					type, 
		String					uid, 
		String					classification,
		String					name,
		InetAddress					address )

		throws DeviceManagerException;

	public void
	search(
		int						max_millis,
		DeviceSearchListener	listener );
	
	public boolean
	getAutoSearch();
	
	public void
	setAutoSearch(
		boolean	auto );
	
	public boolean
	isRSSPublishEnabled();
	
	public void
	setRSSPublishEnabled(
		boolean		enabled );

	public String
	getRSSLink();
	
	public UnassociatedDevice[]
	getUnassociatedDevices();
	
	public TranscodeManager
	getTranscodeManager();
	
	public File
	getDefaultWorkingDirectory();
	
	public void
	setDefaultWorkingDirectory(
		File		dir );
	
	public boolean
	isBusy(
		int	device_type );
	
	public DeviceOfflineDownloaderManager
	getOfflineDownlaoderManager();
	
	public boolean
	isTiVoEnabled();
	
	public void
	setTiVoEnabled(
		boolean	enabled );
	
	public boolean
	getDisableSleep();
	
	public void
	setDisableSleep(
		boolean		b );
	
	public void
	addDiscoveryListener(
		DeviceManagerDiscoveryListener	listener );
	
	public void
	removeDiscoveryListener(
		DeviceManagerDiscoveryListener	listener );
	
	public void
	addListener(
		DeviceManagerListener		listener );
	
	public void
	removeListener(
		DeviceManagerListener		listener );
	
	public interface 
	UnassociatedDevice
	{
		public InetAddress
		getAddress();
		
		public String
		getDescription();
	}
	
	public interface
	DeviceManufacturer
	{
		public String
		getName();
		
		public DeviceTemplate[]
		getDeviceTemplates();
	}
}
