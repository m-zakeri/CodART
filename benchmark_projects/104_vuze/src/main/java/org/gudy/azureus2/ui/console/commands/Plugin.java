/*
 * Created on 22 Aug 2008
 * Created by Allan Crooks
 * Copyright (C) 2008 Vuze Inc., All Rights Reserved.
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
 */
package org.gudy.azureus2.ui.console.commands;

import java.io.File;
import java.io.PrintStream;
import java.util.List;
import java.util.TreeSet;

import org.gudy.azureus2.core3.util.FileUtil;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.ui.console.ConsoleInput;
import org.gudy.azureus2.ui.console.util.TextWrap;

public class Plugin extends IConsoleCommand {

	public Plugin()
	{
		super("plugin");
	}
	
	public String getCommandDescriptions()
	{
		return("plugin [various options]\t\tRun with no parameter for more help.");
	}
	
	public void printHelpExtra(PrintStream out, List args) {
		out.println("> -----");
		out.println("Subcommands:");
		out.println("location\t\tLists where plugins are being loaded from");
		out.println("list\t\tList all running plugins");
		out.println("listall\t\tList all plugins - running or not");
		out.println("status pluginid\tPrints the status of a given plugin");
		out.println("startup pluginid on|off\tEnables or disables the plugin running at startup");
		out.println("> -----");
	}
	
	public void execute(String commandName, ConsoleInput ci, List args) {
		if (args.isEmpty()) {
			printHelpExtra(ci.out, args);
			return;
		}

		String subcmd = (String)args.get(0);
		if (!java.util.Arrays.asList(new String[] {
				"location", "list", "listall", "status", "startup"
			}).contains(subcmd)) {
			ci.out.println("Invalid subcommand: " + subcmd);
			ci.out.println();
			return;
		}
		
		if (subcmd.equals("list") || subcmd.equals("listall")) {
			boolean all_plugins = subcmd.equals("listall");
			ci.out.println("> -----");
			PluginInterface[] plugins = ci.getCore().getPluginManager().getPluginInterfaces();
			TreeSet plugin_ids = new TreeSet(String.CASE_INSENSITIVE_ORDER);
			for (int i=0; i<plugins.length; i++) {
				if (!all_plugins && !plugins[i].getPluginState().isOperational()) {continue;}
				String plugin_id = plugins[i].getPluginID();
				plugin_ids.add(plugin_id);
			}
			TextWrap.printList(plugin_ids.iterator(), ci.out, "   ");
			ci.out.println("> -----");
			return;
		}
		
		if (subcmd.equals("location")) {
			// Taken from ConfigSectionPlugins.
			File fUserPluginDir = FileUtil.getUserFile("plugins");
			String sep = File.separator;
			
			String sUserPluginDir;
			
			try{
				sUserPluginDir = fUserPluginDir.getCanonicalPath();
			}catch( Throwable e ){
				sUserPluginDir = fUserPluginDir.toString();
			}
			
			if (!sUserPluginDir.endsWith(sep)) {
				sUserPluginDir += sep;
			}

			File fAppPluginDir = FileUtil.getApplicationFile("plugins");
			
			String sAppPluginDir;
			
			try{
				sAppPluginDir = fAppPluginDir.getCanonicalPath();
			}catch( Throwable e ){
				sAppPluginDir = fAppPluginDir.toString();
			}

			if (!sAppPluginDir.endsWith(sep)) {
				sAppPluginDir += sep;
			}
			
			ci.out.println("Shared plugin location:");
			ci.out.println("  " + sAppPluginDir);
			ci.out.println("User plugin location:");
			ci.out.println("  " + sUserPluginDir);
			ci.out.println();
			return;
		}
		
		// Commands from this point require a plugin ID.
		if (args.size() == 1) {
			ci.out.println("No plugin ID given.");
			ci.out.println();
			return;
		}
		
		String plugin_id = (String)args.get(1);
		PluginInterface plugin = ci.getCore().getPluginManager().getPluginInterfaceByID(plugin_id, false);
		if (plugin == null) {
			ci.out.println("Invalid plugin ID: " + plugin_id);
			ci.out.println();
			return;
		}
		
		if (subcmd.equals("status")) {
			ci.out.println("ID     : " + plugin.getPluginID());
			ci.out.println("Name   : " + plugin.getPluginName());
			ci.out.println("Version: " + plugin.getPluginVersion());
			ci.out.println("Running: " + plugin.getPluginState().isOperational());
			ci.out.println("Runs at startup: " + plugin.getPluginState().isLoadedAtStartup());
			if (!plugin.getPluginState().isBuiltIn()) {
				ci.out.println("Location: " + plugin.getPluginDirectoryName());
			}
			ci.out.println();
			return;
		}
		
		if (subcmd.equals("startup")) {
			if (args.size() == 2) {
				ci.out.println("Need to pass either \"on\" or \"off\"");
				ci.out.println();
				return;
			}
			String enabled_mode = (String)args.get(2);
			if (enabled_mode.equals("on")) {
				plugin.getPluginState().setLoadedAtStartup(true);
			}
			else if (enabled_mode.equals("off")) {
				plugin.getPluginState().setLoadedAtStartup(false);
			}
			else {
				ci.out.println("Need to pass either \"on\" or \"off\"");
				ci.out.println();
				return;
			}
			ci.out.println("Done.");
			ci.out.println();
			return;
		}
	}
}
