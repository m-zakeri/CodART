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

package fi.vtt.noen.mfw.bundle.probe.shared;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.NewServiceListener;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.osgi.framework.BundleContext;

/**
 * @author Teemu Kanstren
 */
public class ServerAgentListener extends NewServiceListener {
  private final static Logger log = new Logger(ServerAgentListener.class);
  private ServerAgentUser user;

  public ServerAgentListener(BundleContext bc, ServerAgentUser user) {
    super(bc, ServerAgent.class, log);
    this.user = user;
  }

  @Override
  public void registered(Object service) {
    user.setServerAgent((ServerAgent) service);
  }

  @Override
  public void unregistered(Object service) {
    //TODO: what do we do here?
  }
}
