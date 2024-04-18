/*
 * Created on 26/01/2005
 * Created by Paul Duran
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
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 * AELITIS, SARL au capital de 30,000 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */

package org.gudy.azureus2.ui.console.multiuser;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

import junit.framework.TestCase;

import org.gudy.azureus2.ui.console.UserProfile;

/**
 * test class for the UserManager object
 * @author pauld
 */
public class TestUserManager extends TestCase {

	private InMemoryUserManager manager;
	private UserProfile profile1;
	private UserProfile profile2;

	/*
	 * @see TestCase#setUp()
	 */
	protected void setUp() throws Exception {
		super.setUp();
		
		manager = new InMemoryUserManager(null);
		profile1 = new UserProfile();
		profile1.setUsername("myuser1");
		profile1.setPassword("mypassword");
		manager.addUser(profile1);
		profile2 = new UserProfile();
		profile2.setUsername("myuser2");
		profile2.setPassword("zigzag");
		profile2.setUserType(UserProfile.USER);
		manager.addUser(profile2);		
	}

	/*
	 * @see TestCase#tearDown()
	 */
	protected void tearDown() throws Exception {
		super.tearDown();
	}

	public void testLoadSave()
	{
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		manager.save(out);
		System.out.println("Saved to: " + new String(out.toByteArray()));
		ByteArrayInputStream in = new ByteArrayInputStream(out.toByteArray());
		InMemoryUserManager newManager = new InMemoryUserManager(null);
		newManager.load(in);
		UserProfile profile3 = new UserProfile();
		profile3.setUserType(UserProfile.GUEST);
		profile3.setUsername("user3");
		profile3.setPassword("whatever");
		assertTrue( manager.getUsers().contains(profile1 ) );
		assertTrue( manager.getUsers().contains(profile2 ) );
		assertFalse( manager.getUsers().contains(profile3 ) );
		assertTrue( newManager.getUsers().contains(profile1 ) );
		assertTrue( newManager.getUsers().contains(profile2 ) );
		assertFalse( newManager.getUsers().contains(profile3 ) );
	}
	public void testAuthenticate()
	{
		assertEquals( "verify authentication succeeds", profile1, manager.authenticate("myuser1", "mypassword"));
		assertNull( "verify authentication fails", manager.authenticate("myuser1", "mypassword_shouldfail"));
	}
	
	private static final class InMemoryUserManager extends UserManager
	{
		public InMemoryUserManager(String fileName) {
			super(fileName);
		}

		public void save(OutputStream out)
		{
			doSave( out );
		}
		public void load(InputStream in)
		{
			doLoad( in );
		}
	}
}
