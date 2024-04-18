/*
 * Created on 23-Nov-2004
 * Created by Paul Gardner
 * Copyright (C) 2004 Aelitis, All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 * 
 * AELITIS, SARL au capital de 30,000 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */

package org.gudy.azureus2.ui.telnet;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.HashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.apache.log4j.Logger;
import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.torrentdownloader.TorrentDownloaderFactory;
import org.gudy.azureus2.core3.util.FileUtil;
import org.gudy.azureus2.core3.util.TorrentUtils;
import org.gudy.azureus2.ui.common.IUserInterface;
import org.gudy.azureus2.ui.common.UIConst;
import org.gudy.azureus2.ui.console.ConsoleInput;
import org.gudy.azureus2.ui.console.UserProfile;
import org.gudy.azureus2.ui.console.multiuser.MultiUserConsoleInput;
import org.gudy.azureus2.ui.console.multiuser.UserManager;
import org.gudy.azureus2.ui.console.multiuser.commands.UserCommand;

import com.aelitis.azureus.core.AzureusCore;

/**
 * this is a telnet UI that starts up a server socket that listens for new connections 
 * on a (configurable) port. when an incoming connection is recieved, we check the host 
 * against our list of allowed hosts and if this host is permitted, we start a new 
 * command line interface for that connection.
 * @author fatal
 */
public class UI extends org.gudy.azureus2.ui.common.UITemplateHeadless implements IUserInterface 
{
	public String[] processArgs(String[] args) {
		return args;
	}
	
	private UserManager userManager;
	
	/**
	 * start up a server socket thread on an appropriate port as obtained from the configuration manager.
	 */
	public void startUI() {
		if( ! isStarted() )
		{
			try {
				int telnetPort = COConfigurationManager.getIntParameter("Telnet_iPort", 57006);
				String allowedHostsStr = COConfigurationManager.getStringParameter("Telnet_sAllowedHosts", "127.0.0.1,titan");				
				StringTokenizer st = new StringTokenizer(allowedHostsStr, ",");
				Set allowedHosts = new HashSet();
				while( st.hasMoreTokens() )
					allowedHosts.add(st.nextToken().toLowerCase());
				int maxLoginAttempts = COConfigurationManager.getIntParameter("Telnet_iMaxLoginAttempts", 3);
				userManager = initUserManager();
				Thread thread = new Thread(new SocketServer(this, telnetPort, allowedHosts, userManager, maxLoginAttempts), "Telnet Socket Server Thread");
				thread.setDaemon(true);
				thread.start();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		super.startUI();
	}
	
	/**
	 * @return user manager instance if multi user is enabled, otherwise null 
	 */
	private UserManager initUserManager()
	{
		if( System.getProperty("azureus.console.multiuser") != null )
			return UserManager.getInstance(UIConst.getAzureusCore().getPluginManager().getDefaultPluginInterface());
		else
			return null;
	}
	
	/**
	 * shamelessly copied from the console ui. could this be extracted into a static utility method?
	 */
	public void openTorrent(String fileName) {
	   if( fileName.toUpperCase().startsWith( "HTTP://" ) ) {
	      System.out.println( "Downloading torrent from url: " + fileName );
	      TorrentDownloaderFactory.downloadManaged( fileName );
	      return;
	    }
	    
	    try {
	      if (!TorrentUtils.isTorrentFile(fileName)) {//$NON-NLS-1$
	        Logger.getLogger("azureus2.ui.telnet").error(fileName+" doesn't seem to be a torrent file. Not added.");
	        return;
	      }
	    } catch (Exception e) {
	      Logger.getLogger("azureus2.ui.telnet").error("Something is wrong with "+fileName+". Not added. (Reason: "+e.getMessage()+")");
	      return;
	    }
	    if (UIConst.getGlobalManager()!=null) {
	      try {
	        UIConst.getGlobalManager().addDownloadManager(fileName, COConfigurationManager.getDirectoryParameter("Default save path"));
	      } catch (Exception e) {
	        Logger.getLogger("azureus2.ui.telnet").error("The torrent "+fileName+" could not be added.", e);
	      }
	    }
	}
	/**
	 * creates a new console input using the specified input/output streams.
	 * we create the new input in non-controlling mode because we don't want the 'quit'
	 * command to shut down the whole interface - simply this clients connection.
	 * @param consoleName
	 * @param inputStream
	 * @param outputStream
	 * @param profile
	 */
	public void createNewConsoleInput(String consoleName, InputStream inputStream, PrintStream outputStream, UserProfile profile)
	{
		ConsoleInput console; 
		if( userManager != null )
		{
			MultiUserConsoleInput muc = new MultiUserConsoleInput(consoleName, UIConst.getAzureusCore(), new InputStreamReader(inputStream), outputStream, Boolean.FALSE, profile);
			muc.registerCommand( new UserCommand(userManager) );
			console = muc;
		}
		else
		{
			console = new ConsoleInput(consoleName, UIConst.getAzureusCore(), new InputStreamReader(inputStream), outputStream, Boolean.FALSE, profile);
			
			System.out.println( "TelnetUI: console input instantiated" );
		}	
		console.printwelcome();
		console.printconsolehelp();
	}
}