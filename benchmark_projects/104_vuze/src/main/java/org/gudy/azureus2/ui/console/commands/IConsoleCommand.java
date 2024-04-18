/*
 * Written and copyright 2001-2004 Tobias Minich. Distributed under the GNU
 * General Public License; see the README file. This code comes with NO
 * WARRANTY.
 * 
 */

package org.gudy.azureus2.ui.console.commands;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import org.gudy.azureus2.ui.console.ConsoleInput;

/**
 * base interface for all console commands
 * @author Tobias Minich
 */
public abstract class IConsoleCommand {
	private String main_name;
	private String short_name;
	private HashSet commands;

	public IConsoleCommand(String main_name) {
		this(main_name, null);
	}
	
	public IConsoleCommand(String main_name, String short_name) {
		this.commands = new HashSet();
		this.main_name = main_name;
		this.short_name = short_name;
		
		if (main_name != null)  {commands.add(main_name);}
		if (short_name != null) {commands.add(short_name);}
	}
	
	/**
	 * execute the command with the specified name using the specified arguments 
	 * @param commandName
	 * @param console
	 * @param arguments
	 */
	public abstract void execute(String commandName, ConsoleInput console, List arguments);
	
	/**
	 * return high-level help about the commands supported by this object.
	 * @return
	 */
	public abstract String getCommandDescriptions();
	
	/**
	 * do nothing by default
	 * @param out
	 * @param args
	 */
	public final void printHelp(PrintStream out, List args)
	{
		out.println(getCommandDescriptions());
		printHelpExtra(out, args);
	}
	
	public void printHelpExtra(PrintStream out, List args) {
		// Do nothing by default.
	}
	
	/**
	 * helper method if subclasses want to print out help for a particular subcommand
	 * @param out
	 * @param arg
	 */
	protected final void printHelp(PrintStream out, String arg)
	{
		List args;
		if( arg != null )
		{
			args = new ArrayList();
			args.add(arg);
		}
		else
			args = Collections.EMPTY_LIST;
		
		printHelp(out, args);
	}
	
	/**
	 * returns the set of command names that this command understands.
	 * eg: the 'quit' command might understand 'quit', 'q', 'bye'
	 * other commands might actually have several command names and
	 * execute different code depending upon the command name
	 * @return
	 */
	public Set getCommandNames()
	{
		return Collections.unmodifiableSet(commands);
	}
	
	public final String getCommandName() {return this.main_name;}
	public final String getShortCommandName() {return this.short_name;}

}
