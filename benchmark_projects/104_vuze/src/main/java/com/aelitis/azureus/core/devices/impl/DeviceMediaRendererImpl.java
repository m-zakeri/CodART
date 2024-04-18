/*
 * Created on Jan 28, 2009
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

import java.io.File;
import java.io.IOException;
import java.net.InetAddress;
import java.util.List;
import java.util.Map;

import org.gudy.azureus2.core3.util.Constants;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.IndentWriter;

import com.aelitis.azureus.core.devices.*;
import com.aelitis.net.upnp.UPnPDevice;
import com.aelitis.net.upnp.impl.device.UPnPDeviceImpl;

public class 
DeviceMediaRendererImpl
	extends DeviceUPnPImpl
	implements DeviceMediaRenderer
{
	public
	DeviceMediaRendererImpl(
		DeviceManagerImpl	_manager,
		UPnPDevice			_device )
	{
		super( _manager, _device, Device.DT_MEDIA_RENDERER );
	}
	
	public
	DeviceMediaRendererImpl(
		DeviceManagerImpl	_manager,
		String				_classification )
	{
		super( _manager, Device.DT_MEDIA_RENDERER, _classification );
	}
	
	public
	DeviceMediaRendererImpl(
		DeviceManagerImpl	_manager,
		String				_uuid,
		String				_classification,
		boolean				_manual,
		String				_name )
	{
		super( _manager, Device.DT_MEDIA_RENDERER, _uuid, _classification, _manual, _name );
	}
	
	public
	DeviceMediaRendererImpl(
		DeviceManagerImpl	_manager,
		String				_uuid,
		String				_classification,
		boolean				_manual )
	{
		super( _manager, Device.DT_MEDIA_RENDERER, _uuid, _classification, _manual );
	}
	
	protected
	DeviceMediaRendererImpl(
		DeviceManagerImpl	_manager,
		Map					_map )
	
		throws IOException
	{
		super(_manager, _map );
	}
	
	public void setAddress(InetAddress address) {
		super.setAddress(address);
		
		if (address != null && getType() == DT_MEDIA_RENDERER) {
			//System.out.println("Set Address " + address.getHostAddress() + "; " + getName() + "/" + getClassification());

			boolean hasUPnPDevice = getUPnPDevice() != null;
			DeviceImpl[] devices = getManager().getDevices();
			for (DeviceImpl device : devices) {
				if (device == this || device.getID().equals(getID())
						|| !((device instanceof DeviceUPnPImpl))) {
					continue;
				}
				DeviceUPnPImpl deviceUPnP = ((DeviceUPnPImpl) device);
				if (!address.equals(device.getAddress()) || !device.isAlive()) {
					continue;
				}

				if (hasUPnPDevice) {
					if (device.getType() == DT_MEDIA_RENDERER) {
						// prefer UPnP Device over Manual one added by a Browse event
						if (deviceUPnP.getUPnPDevice() != null) {
							int fileCount = deviceUPnP.getFileCount();
							if (fileCount == 0 && !device.isHidden()) {
								log("Hiding " + device.getName() + "/"
										+ device.getClassification() + "/" + device.getID()
										+ " due to " + getName() + "/" + getClassification() + "/"
										+ getID());
  							device.setHidden(true);
							}
						}
					}
				} else {
					if (device.getType() == DT_MEDIA_RENDERER) {
						int fileCount = getFileCount();
						// prefer UPnP Device over Manual one added by a Browse event
						if (fileCount == 0 && !isHidden()) {
							log("hiding " + getName() + "/" + getClassification() + "/"
									+ getID() + " due to " + device.getName() + "/"
									+ device.getClassification() + "/" + device.getID());
							setHidden(true);
						} else if (fileCount > 0 && Constants.IS_CVS_VERSION && isHidden()) {
							// Fix beta bug where we hid devices that had files.  Remove after 4605
							setHidden(false);
						}
					} else {
						// Device has UPnP stuff, but did not register itself as
						// renderer.
  					UPnPDevice upnpDevice = deviceUPnP.getUPnPDevice();
  					if (upnpDevice != null) {
    					String manufacturer = upnpDevice.getManufacturer();
    					if (manufacturer == null || !manufacturer.startsWith("Vuze")) {
    						log("Linked " + getName() + " to UPnP Device " + device.getName());
      					setUPnPDevice(upnpDevice);
      					setDirty();
    					}
  					}
					}
				}
				break;
			}
		}
	}
	
	@Override
	protected boolean
	updateFrom(
		DeviceImpl		_other,
		boolean			_is_alive )
	{
		if ( !super.updateFrom( _other, _is_alive )){
			
			return( false );
		}
		
		if ( !( _other instanceof DeviceMediaRendererImpl )){
			
			Debug.out( "Inconsistent" );
			
			return( false );
		}
		
		DeviceMediaRendererImpl other = (DeviceMediaRendererImpl)_other;
		
		return( true );
	}
	
	@Override
	protected void
	initialise()
	{
		super.initialise();
	}
	
	@Override
	protected void
	destroy()
	{
		super.destroy();
	}
	
	public boolean
	canCopyToDevice()
	{
		return( false );
	}
	
	public int
	getCopyToDevicePending()
	{
		return( 0 );
	}
	
	public boolean
	canAutoStartDevice()
	{
		return( false );
	}
	
	public boolean
	getAutoStartDevice()
	{
		return( false );
	}
	
	public void
	setAutoStartDevice(
		boolean		auto )
	{
	}
	
	public boolean
	canCopyToFolder()
	{
		return( false );
	}
	
	public void
	setCanCopyToFolder(
		boolean		can )
	{
		// nothing to do
	}
	
	public File
	getCopyToFolder()
	{
		return( null );
	}
	
	public void
	setCopyToFolder(
		File		file )
	{
	}
	
	public int
	getCopyToFolderPending()
	{
		return( 0 );
	}
	
	public boolean
	getAutoCopyToFolder()
	{
		return( false );
	}
		
	public void
	setAutoCopyToFolder(
		boolean		auto )
	{
	}
	
	public void 
	manualCopy() 
	
		throws DeviceManagerException 
	{
		throw( new DeviceManagerException( "Unsupported" ));
	}
	
	public boolean
	canShowCategories()
	{
		return( false );
	}
	
	public void
	setShowCategories(
		boolean	b )
	{
		setPersistentBooleanProperty( PP_REND_SHOW_CAT, b );
	}
	
	public boolean
	getShowCategories()
	{
		return( getPersistentBooleanProperty( PP_REND_SHOW_CAT, getShowCategoriesDefault()));
	}
	
	protected boolean
	getShowCategoriesDefault()
	{
		return( false );
	}
	
	@Override
	protected void
	getDisplayProperties(
		List<String[]>	dp )
	{
		super.getDisplayProperties( dp );

		if ( canCopyToFolder()){
			
			addDP( dp, "devices.copy.folder.auto", getAutoCopyToFolder());
			addDP( dp, "devices.copy.folder.dest", getCopyToFolder());
		}
		
		if ( canShowCategories()){
			
			addDP( dp, "devices.cat.show", getShowCategories());

		}
		super.getTTDisplayProperties( dp );
	}	
	
	@Override
	public void
	generate(
		IndentWriter		writer )
	{
		super.generate( writer );
		
		try{
			writer.indent();
	
			generateTT( writer );
			
		}finally{
			
			writer.exdent();
		}
	}
}
