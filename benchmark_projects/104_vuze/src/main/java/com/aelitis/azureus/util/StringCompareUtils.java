/**
 * Created on Jun 1, 2008
 *
 * Copyright 2008 Vuze, Inc.  All rights reserved.
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
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA 
 */
 
package com.aelitis.azureus.util;

/**
 * @author TuxPaper
 * @created Jun 1, 2008
 *
 */
public class StringCompareUtils
{
	public static boolean equals(String s0, String s1) {
		boolean s0Null = s0 == null;
		boolean s1Null = s1 == null;
		if (s0Null || s1Null) {
			return  s0Null == s1Null;
		}
		return s0.equals(s1);
	}
}
