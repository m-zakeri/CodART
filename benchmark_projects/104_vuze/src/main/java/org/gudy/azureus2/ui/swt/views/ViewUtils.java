/*
 * File    : ViewUtils.java
 * Created : 24-Oct-2003
 * By      : parg
 * 
 * Copyright (C) 2004, 2005, 2006 Aelitis SAS, All rights Reserved
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details ( see the LICENSE file ).
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * AELITIS, SAS au capital de 46,603.30 euros,
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 */
 
package org.gudy.azureus2.ui.swt.views;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Map;

import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.widgets.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.config.ParameterListener;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.util.Constants;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.DisplayFormatters;
import org.gudy.azureus2.core3.util.SystemTime;
import org.gudy.azureus2.plugins.ui.UIInputReceiver;
import org.gudy.azureus2.plugins.ui.UIInputReceiverListener;
import org.gudy.azureus2.plugins.ui.menus.MenuItemListener;
import org.gudy.azureus2.plugins.ui.tables.TableContextMenuItem;
import org.gudy.azureus2.plugins.ui.toolbar.UIToolBarItem;
import org.gudy.azureus2.ui.swt.Messages;
import org.gudy.azureus2.ui.swt.SimpleTextEntryWindow;
import org.gudy.azureus2.ui.swt.TorrentUtil;
import org.gudy.azureus2.ui.swt.Utils;
import org.gudy.azureus2.ui.swt.views.table.utils.CoreTableColumn;
import org.gudy.azureus2.ui.swt.views.utils.ManagerUtils;

import com.aelitis.azureus.ui.common.ToolBarItem;
import com.aelitis.azureus.ui.swt.UIFunctionsManagerSWT;

/**
 * @author parg
 */

public class 
ViewUtils 
{
	private static SimpleDateFormat formatOverride = null;
	
	static{
		COConfigurationManager.addAndFireParameterListener(
			"Table.column.dateformat", new ParameterListener() {
				public void parameterChanged(String parameterName) {
					String temp = COConfigurationManager.getStringParameter(
										"Table.column.dateformat", "");
					
					if ( temp == null || temp.trim().length() == 0 ){
						
						formatOverride = null;
						
					}else{
						
						try{
							SimpleDateFormat format = new SimpleDateFormat( temp.trim());
							
							format.format(new Date());
							
							formatOverride = format;
							
						}catch( Throwable e ){
							
							formatOverride = null;
						}
					}
				}
			});
	}
	
	public static String
	formatETA(
		long				value,
		boolean				absolute,
		SimpleDateFormat	override )
	{
		SimpleDateFormat df = override!=null?override:formatOverride;
		
		if (	absolute && 
				df != null && 
				value > 0 && 
				!(value == Constants.CRAPPY_INFINITY_AS_INT || value >= Constants.CRAPPY_INFINITE_AS_LONG )){
			
			try{
				return( df.format( new Date( SystemTime.getCurrentTime() + 1000*value )));
				
			}catch( Throwable e ){
			}
		}
		
		return( DisplayFormatters.formatETA( value, absolute ));
	}
	

	public static class
	CustomDateFormat
	{
		private CoreTableColumn			column;
		private TableContextMenuItem	custom_date_menu;
		private SimpleDateFormat		custom_date_format;

		private
		CustomDateFormat(
			CoreTableColumn	_column )
		{
			column	= _column;
			
			custom_date_menu = column.addContextMenuItem(
					"label.date.format", CoreTableColumn.MENU_STYLE_HEADER );
			custom_date_menu.setStyle(TableContextMenuItem.STYLE_PUSH);
			
			custom_date_menu.addListener(new MenuItemListener() {
				public void selected(org.gudy.azureus2.plugins.ui.menus.MenuItem menu, Object target){
					
					Object existing_o = column.getUserData( "CustomDate" );
					
					String existing_text = "";
					
					if ( existing_o instanceof String ){
						existing_text = (String)existing_o;
					}else if ( existing_o instanceof byte[] ){
						try{
							existing_text = new String((byte[])existing_o, "UTF-8" );
						}catch( Throwable e ){
						}
					}
					SimpleTextEntryWindow entryWindow = new SimpleTextEntryWindow(
							"ConfigView.section.style.customDateFormat",
							"label.date.format");
					
					entryWindow.setPreenteredText( existing_text, false );
					
					entryWindow.prompt(new UIInputReceiverListener() {
						public void UIInputReceiverClosed(UIInputReceiver entryWindow) {
							if (!entryWindow.hasSubmittedInput()) {
								return;
							}
							String date_format = entryWindow.getSubmittedInput();
							
							if ( date_format == null ){
								return;
							}
							
							date_format = date_format.trim();
							
							column.setUserData( "CustomDate", date_format );
							
							column.invalidateCells();
							
							update();
						}
					});
				}
			});
		}
			
		public void
		update()
		{
			Object cd = column.getUserData( "CustomDate" );
			
			String	format = null;
			
			if ( cd instanceof byte[]){
				
				try{
					cd = new String((byte[])cd, "UTF-8");
					
				}catch( Throwable e ){
					
				}
			}
			
			if ( cd instanceof String ){
				
				String	str = (String)cd;
				
				str = str.trim();
				
				if ( str.length() > 0 ){
					
					format = str;
				}
			}
			
			if ( format == null ){
				
				format = MessageText.getString( "label.table.default" );
				
				custom_date_format = null;
				
			}else{
				
				try{
					custom_date_format = new SimpleDateFormat( format );
					
				}catch( Throwable e ){
					
					Debug.out( e );
				}
			}
			
			custom_date_menu.setText( MessageText.getString( "label.date.format" )  + " <" + format + "> ..." );
		}
		
		public SimpleDateFormat
		getDateFormat()
		{
			return( custom_date_format );
		}
	}
	
	public static CustomDateFormat
	addCustomDateFormat(
		CoreTableColumn	column )
	{
		return( new CustomDateFormat( column ));
	}
	public static void
	addSpeedMenu(
		final Shell 		shell,
		Menu				menuAdvanced,
		boolean				isTorrentContext,
		boolean				hasSelection,
		boolean				downSpeedDisabled,
		boolean				downSpeedUnlimited,
		long				totalDownSpeed,
		long				downSpeedSetMax,
		long				maxDownload,
		boolean				upSpeedDisabled,
		boolean				upSpeedUnlimited,
		long				totalUpSpeed,
		long				upSpeedSetMax,
		long				maxUpload,
		final int			num_entries,
		final SpeedAdapter	adapter )
	{
		// advanced > Download Speed Menu //
		final MenuItem itemDownSpeed = new MenuItem(menuAdvanced, SWT.CASCADE);
		Messages.setLanguageText(itemDownSpeed, "MyTorrentsView.menu.setDownSpeed"); //$NON-NLS-1$
		Utils.setMenuItemImage(itemDownSpeed, "speed");

		final Menu menuDownSpeed = new Menu(shell, SWT.DROP_DOWN);
		itemDownSpeed.setMenu(menuDownSpeed);

		final MenuItem itemCurrentDownSpeed = new MenuItem(menuDownSpeed, SWT.PUSH);
		itemCurrentDownSpeed.setEnabled(false);
		StringBuffer speedText = new StringBuffer();
		String separator = "";
		//itemDownSpeed.                   
		if (downSpeedDisabled) {
			speedText.append(MessageText
					.getString("MyTorrentsView.menu.setSpeed.disabled"));
			separator = " / ";
		}
		if (downSpeedUnlimited) {
			speedText.append(separator);
			speedText.append(MessageText
					.getString("MyTorrentsView.menu.setSpeed.unlimited"));
			separator = " / ";
		}
		if (totalDownSpeed > 0) {
			speedText.append(separator);
			speedText.append(DisplayFormatters
					.formatByteCountToKiBEtcPerSec(totalDownSpeed));
		}
		itemCurrentDownSpeed.setText(speedText.toString());

		new MenuItem(menuDownSpeed, SWT.SEPARATOR);

		final MenuItem itemsDownSpeed[] = new MenuItem[12];
		Listener itemsDownSpeedListener = new Listener() {
			public void handleEvent(Event e) {
				if (e.widget != null && e.widget instanceof MenuItem) {
					MenuItem item = (MenuItem) e.widget;
					int speed = item.getData("maxdl") == null ? 0 : ((Integer) item
							.getData("maxdl")).intValue();
					adapter.setDownSpeed(speed);
				}
			}
		};

		itemsDownSpeed[1] = new MenuItem(menuDownSpeed, SWT.PUSH);
		Messages.setLanguageText(itemsDownSpeed[1],
				"MyTorrentsView.menu.setSpeed.unlimit");
		itemsDownSpeed[1].setData("maxdl", new Integer(0));
		itemsDownSpeed[1].addListener(SWT.Selection, itemsDownSpeedListener);

		if (hasSelection) {

			//using 200KiB/s as the default limit when no limit set.
			if (maxDownload == 0){		
				if ( downSpeedSetMax == 0 ){
					maxDownload = 200 * 1024;
				}else{
					maxDownload	= 4 * ( downSpeedSetMax/1024 ) * 1024;
				}
			}

			for (int i = 2; i < 12; i++) {
				itemsDownSpeed[i] = new MenuItem(menuDownSpeed, SWT.PUSH);
				itemsDownSpeed[i].addListener(SWT.Selection, itemsDownSpeedListener);
	
				// dms.length has to be > 0 when hasSelection
				int limit = (int)(maxDownload / (10 * num_entries) * (12 - i));
				StringBuffer speed = new StringBuffer();
				speed.append(DisplayFormatters.formatByteCountToKiBEtcPerSec(limit
						* num_entries));
				if (num_entries > 1) {
					speed.append(" ");
					speed.append(MessageText
							.getString("MyTorrentsView.menu.setSpeed.in"));
					speed.append(" ");
					speed.append(num_entries);
					speed.append(" ");
					speed.append(MessageText
							.getString("MyTorrentsView.menu.setSpeed.slots"));
					speed.append(" ");
					speed
							.append(DisplayFormatters.formatByteCountToKiBEtcPerSec(limit));
				}
				itemsDownSpeed[i].setText(speed.toString());
				itemsDownSpeed[i].setData("maxdl", new Integer(limit));
			}
		}

		// ---
		new MenuItem(menuDownSpeed, SWT.SEPARATOR);
		
		String menu_key = "MyTorrentsView.menu.manual";
		if (num_entries > 1) {menu_key += (isTorrentContext?".per_torrent":".per_peer" );}

		final MenuItem itemDownSpeedManualSingle = new MenuItem(menuDownSpeed, SWT.PUSH);
		Messages.setLanguageText(itemDownSpeedManualSingle, menu_key);
		itemDownSpeedManualSingle.addSelectionListener(new SelectionAdapter() {
			public void widgetSelected(SelectionEvent e) {
				int speed_value = getManualSpeedValue(shell, true);
				if (speed_value > 0) {adapter.setDownSpeed(speed_value);}
			}
		});
		
		if (num_entries > 1) {
			final MenuItem itemDownSpeedManualShared = new MenuItem(menuDownSpeed, SWT.PUSH);
			Messages.setLanguageText(itemDownSpeedManualShared, isTorrentContext?"MyTorrentsView.menu.manual.shared_torrents":"MyTorrentsView.menu.manual.shared_peers");
			itemDownSpeedManualShared.addSelectionListener(new SelectionAdapter() {
				public void widgetSelected(SelectionEvent e) {
					int speed_value = getManualSharedSpeedValue(shell, true, num_entries);
					if (speed_value > 0) {adapter.setDownSpeed(speed_value);}
				}
			});
		}
		
		// advanced >Upload Speed Menu //
		final MenuItem itemUpSpeed = new MenuItem(menuAdvanced, SWT.CASCADE);
		Messages.setLanguageText(itemUpSpeed, "MyTorrentsView.menu.setUpSpeed"); //$NON-NLS-1$
		Utils.setMenuItemImage(itemUpSpeed, "speed");

		final Menu menuUpSpeed = new Menu(shell, SWT.DROP_DOWN);
		itemUpSpeed.setMenu(menuUpSpeed);

		final MenuItem itemCurrentUpSpeed = new MenuItem(menuUpSpeed, SWT.PUSH);
		itemCurrentUpSpeed.setEnabled(false);
		separator = "";
		speedText = new StringBuffer();
		//itemUpSpeed.                   
		if (upSpeedDisabled) {
			speedText.append(MessageText
					.getString("MyTorrentsView.menu.setSpeed.disabled"));
			separator = " / ";
		}
		if (upSpeedUnlimited) {
			speedText.append(separator);
			speedText.append(MessageText
					.getString("MyTorrentsView.menu.setSpeed.unlimited"));
			separator = " / ";
		}
		if (totalUpSpeed > 0) {
			speedText.append(separator);
			speedText.append(DisplayFormatters
					.formatByteCountToKiBEtcPerSec(totalUpSpeed));
		}
		itemCurrentUpSpeed.setText(speedText.toString());

		// ---
		new MenuItem(menuUpSpeed, SWT.SEPARATOR);

		final MenuItem itemsUpSpeed[] = new MenuItem[12];
		Listener itemsUpSpeedListener = new Listener() {
			public void handleEvent(Event e) {
				if (e.widget != null && e.widget instanceof MenuItem) {
					MenuItem item = (MenuItem) e.widget;
					int speed = item.getData("maxul") == null ? 0 : ((Integer) item
							.getData("maxul")).intValue();
					adapter.setUpSpeed(speed);
				}
			}
		};

		itemsUpSpeed[1] = new MenuItem(menuUpSpeed, SWT.PUSH);
		Messages.setLanguageText(itemsUpSpeed[1],
				"MyTorrentsView.menu.setSpeed.unlimit");
		itemsUpSpeed[1].setData("maxul", new Integer(0));
		itemsUpSpeed[1].addListener(SWT.Selection, itemsUpSpeedListener);

		if (hasSelection) {
			//using 75KiB/s as the default limit when no limit set.
			if (maxUpload == 0){
				maxUpload = 75 * 1024;
			}else{
				if ( upSpeedSetMax == 0 ){
					maxUpload = 200 * 1024;
				}else{
					maxUpload = 4 * ( upSpeedSetMax/1024 ) * 1024;
				}
			}
			for (int i = 2; i < 12; i++) {
				itemsUpSpeed[i] = new MenuItem(menuUpSpeed, SWT.PUSH);
				itemsUpSpeed[i].addListener(SWT.Selection, itemsUpSpeedListener);

				int limit = (int)( maxUpload / (10 * num_entries) * (12 - i));
				StringBuffer speed = new StringBuffer();
				speed.append(DisplayFormatters.formatByteCountToKiBEtcPerSec(limit
						* num_entries));
				if (num_entries > 1) {
					speed.append(" ");
					speed.append(MessageText
							.getString("MyTorrentsView.menu.setSpeed.in"));
					speed.append(" ");
					speed.append(num_entries);
					speed.append(" ");
					speed.append(MessageText
							.getString("MyTorrentsView.menu.setSpeed.slots"));
					speed.append(" ");
					speed
							.append(DisplayFormatters.formatByteCountToKiBEtcPerSec(limit));
				}

				itemsUpSpeed[i].setText(speed.toString());
				itemsUpSpeed[i].setData("maxul", new Integer(limit));
			}
		}

		new MenuItem(menuUpSpeed, SWT.SEPARATOR);

		final MenuItem itemUpSpeedManualSingle = new MenuItem(menuUpSpeed, SWT.PUSH);
		Messages.setLanguageText(itemUpSpeedManualSingle, menu_key);
		itemUpSpeedManualSingle.addSelectionListener(new SelectionAdapter() {
			public void widgetSelected(SelectionEvent e) {
				int speed_value = getManualSpeedValue(shell, false);
				if (speed_value > 0) {adapter.setUpSpeed(speed_value);}
			}
		});
		
		if (num_entries > 1) {
			final MenuItem itemUpSpeedManualShared = new MenuItem(menuUpSpeed, SWT.PUSH);
			Messages.setLanguageText(itemUpSpeedManualShared, isTorrentContext?"MyTorrentsView.menu.manual.shared_torrents":"MyTorrentsView.menu.manual.shared_peers" );
			itemUpSpeedManualShared.addSelectionListener(new SelectionAdapter() {
				public void widgetSelected(SelectionEvent e) {
					int speed_value = getManualSharedSpeedValue(shell, false, num_entries);
					if (speed_value > 0) {adapter.setUpSpeed(speed_value);}
				}
			});
		}
		
	}
	
	public static int getManualSpeedValue(Shell shell, boolean for_download) {
		String kbps_str = MessageText.getString("MyTorrentsView.dialog.setNumber.inKbps",
				new String[]{ DisplayFormatters.getRateUnit(DisplayFormatters.UNIT_KB ) });
		
		String set_num_str = MessageText.getString("MyTorrentsView.dialog.setNumber." +
				((for_download) ? "download" : "upload"));

		SimpleTextEntryWindow entryWindow = new SimpleTextEntryWindow();
		entryWindow.initTexts(
				"MyTorrentsView.dialog.setSpeed.title",
				new String[] {set_num_str},
				"MyTorrentsView.dialog.setNumber.text",
				new String[] {
						kbps_str,
						set_num_str
				});

		entryWindow.prompt();
		if (!entryWindow.hasSubmittedInput()) {
			return -1;
		}
		String sReturn = entryWindow.getSubmittedInput();
		
		if (sReturn == null)
			return -1;

		try {
			int result = (int) (Double.valueOf(sReturn).doubleValue() * 1024);
			
			if ( DisplayFormatters.isRateUsingBits()){
				
				result /= 8;
			}
			
			if (result <= 0) {throw new NumberFormatException("non-positive number entered");}
			return result;
		} catch (NumberFormatException er) {
			MessageBox mb = new MessageBox(shell, SWT.ICON_ERROR | SWT.OK);
			mb.setText(MessageText
					.getString("MyTorrentsView.dialog.NumberError.title"));
			mb.setMessage(MessageText
					.getString("MyTorrentsView.dialog.NumberError.text"));

			mb.open();
			return -1;
		}
	}
	
	public static int getManualSharedSpeedValue(Shell shell, boolean for_download, int num_entries) {
		int result = getManualSpeedValue(shell, for_download);
		if (result == -1) {return -1;}
		result = result / num_entries;
		if (result == 0) {result = 1;}
		return result;
	}
	
	public static boolean toolBarItemActivated( DownloadManager manager, ToolBarItem item, long activationType,
			Object datasource) {
		String itemKey = item.getID();

		if (itemKey.equals("run")) {
			ManagerUtils.run(manager);
			return true;
		}
		
		if (itemKey.equals("start")) {
			ManagerUtils.queue(manager, null);
			UIFunctionsManagerSWT.getUIFunctionsSWT().refreshIconBar();
			return true;
		}
		
		if (itemKey.equals("stop")) {
			ManagerUtils.stop(manager, null);
			UIFunctionsManagerSWT.getUIFunctionsSWT().refreshIconBar();
			return true;
		}
		
		if (itemKey.equals("remove")) {
			TorrentUtil.removeDownloads(new DownloadManager[] {
				manager
			}, null);
			return true;
		}
		
		return false;
	}

	public static void refreshToolBarItems( DownloadManager manager, Map<String, Long> list) {
		list.put("run", UIToolBarItem.STATE_ENABLED);
		list.put("start", ManagerUtils.isStartable(manager) ? UIToolBarItem.STATE_ENABLED : 0);
		list.put("startstop", UIToolBarItem.STATE_ENABLED);
		list.put("stop", ManagerUtils.isStopable(manager) ? UIToolBarItem.STATE_ENABLED : 0);
		list.put("remove", UIToolBarItem.STATE_ENABLED);
	}	
	
	public interface
	SpeedAdapter
	{
		public void
		setUpSpeed(
			int		val );
		
		public void
		setDownSpeed(
			int		val );
	}
	
	public interface
	ViewTitleExtraInfo
	{
		public void
		update(
			Composite	composite,
			boolean		seeding_view,
			int			count,
			int			active );
			
		public void
		setEnabled(
			Composite	composite,
			boolean		seeding_view,
			boolean		enabled );
			
	}
}
