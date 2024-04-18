/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

package net.sourceforge.ganttproject.util;

import java.util.*;
import java.io.*;
/**
 *  Reads the (Linux) systems BROWSER environment variable
 *
 *@author     Roger Andresen
 *@created    November 23, 2004
 */
public class GetEnv {

	/**
	 *  Description of the Method
	 *
	 *@param  newUrl         The URL to invoke
	 *@return                Array of commands
	 */
	public static String[] GetEnv(String newUrl) {
		//Deprecated but requires a lot less "magic" than the alternative
		String browser = System.getenv("BROWSER");
		String myBrowser = "/usr/bin/" + browser + " " + newUrl;
		return myBrowser.split(" ");
	}
}

