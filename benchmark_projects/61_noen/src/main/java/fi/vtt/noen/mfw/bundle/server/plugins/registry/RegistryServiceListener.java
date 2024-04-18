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

package fi.vtt.noen.mfw.bundle.server.plugins.registry;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.NewServiceListener;
import org.osgi.framework.BundleContext;

/**
 * OSGI listener for capturing the registry service.
 *
 * @author Teemu Kanstren
 */
public class RegistryServiceListener extends NewServiceListener {
  private final RegistryUser user;

  public RegistryServiceListener(BundleContext bc, Logger log, RegistryUser user) {
    super(bc, RegistryPlugin.class, log);
    this.user = user;
  }

  @Override
  public void registered(Object service) {
    user.setRegistry((RegistryPlugin) service);
  }

  @Override
  public void unregistered(Object service) {
    user.setRegistry(null);
  }
}
