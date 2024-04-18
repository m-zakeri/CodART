/*
 * Created on Sep 13, 2012
 * Created by Paul Gardner
 * 
 * Copyright 2012 Vuze, Inc.  All rights reserved.
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


package org.gudy.azureus2.ui.swt.mainwindow;

import org.gudy.azureus2.ui.swt.mainwindow.MainStatusBar.CLabelPadding;
import org.gudy.azureus2.ui.swt.update.UpdateWindow;

import com.aelitis.azureus.ui.UIStatusTextClickListener;


public interface 
IMainStatusBar 
{
	public void
	createStatusEntry(
		CLabelUpdater 	updater );
	
	public boolean
	isMouseOver();
	
	public void
	setUpdateNeeded(
		UpdateWindow	update_window );
	
	public void
	setStatusText(
		String			text );
	
	public void 
	setStatusText(
		int 						statustype, 
		String 						string,
		UIStatusTextClickListener 	l );
	
	public void
	setDebugInfo(
		String			text );
	
	public interface 
	CLabelUpdater
	{
		public void 
		created(
			CLabelPadding label );
		
		public boolean 
		update(
			CLabelPadding label );
	}
}
