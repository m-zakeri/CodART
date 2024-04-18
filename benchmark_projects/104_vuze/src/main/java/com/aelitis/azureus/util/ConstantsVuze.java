/**
 * Created on Feb 10, 2009
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

import org.gudy.azureus2.core3.util.Base32;

import com.aelitis.azureus.core.cnetwork.ContentNetwork;
import com.aelitis.azureus.core.cnetwork.ContentNetworkManagerFactory;
import com.aelitis.azureus.core.crypto.VuzeCryptoManager;

/**
 * @author TuxPaper
 * @created Feb 10, 2009
 *
 */
public class ConstantsVuze
{

	public static final String AZID = Base32.encode(VuzeCryptoManager.getSingleton().getPlatformAZID());

	public static final long DEFAULT_CONTENT_NETWORK_ID = ContentNetwork.CONTENT_NETWORK_VUZE;

	public static final boolean DIAG_TO_STDOUT = System.getProperty(
			"DIAG_TO_STDOUT", "0").equals("1");

	/**
	 * @return the dEFAULT_CONTENT_NETWORK
	 */
	public static ContentNetwork getDefaultContentNetwork() {
		return ContentNetworkManagerFactory.getSingleton().getContentNetwork(
				DEFAULT_CONTENT_NETWORK_ID);
	}

}
