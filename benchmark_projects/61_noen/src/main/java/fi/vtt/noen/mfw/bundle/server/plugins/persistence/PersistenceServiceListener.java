/*
 * Copyright (C) 2010-2011 VTT Technical Research Centre of Finland.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

package fi.vtt.noen.mfw.bundle.server.plugins.persistence;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.NewServiceListener;
import org.osgi.framework.BundleContext;

/**
 * Listens to the OSGI bundlecontext for the appearance of the PersistencePlugin.
 * Used by PersistencePlugin "clients" to gain access to the service.
 *
 * @author Teemu Kanstren
 */
public class PersistenceServiceListener extends NewServiceListener {
  private final PersistenceUser user;

  public PersistenceServiceListener(BundleContext bc, Logger log, PersistenceUser user) {
    super(bc, PersistencePlugin.class, log);
    this.user = user;
  }

  @Override
  public void registered(Object service) {
    user.setPersistence((PersistencePlugin) service);
  }

  @Override
  public void unregistered(Object service) {
    user.setPersistence(null);
  }
}
