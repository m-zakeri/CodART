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

package fi.vtt.noen.mfw.bundle.common;

import fi.vtt.noen.mfw.bundle.blackboard.Blackboard;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;

/**
 * OSGI service listeners that waits for a blackboard service to become available and when found, sets it
 * as the blackboard instance for the provided baseplugin. The plugin to set it for is given on listener creation.
 *
 * @author Teemu Kanstren
 */
public class BlackboardListener implements ServiceListener {
  private final static Logger log = new Logger(BlackboardListener.class);
  //OSGI bundlecontext
  private final BundleContext bc;
  //the plugin for which the blackboard should be set
  private final BasePlugin plugin;
  //this is used to guard against multiple initializations if OSGI provides several registration events for the blackboard
  private boolean initialized = false;

  public BlackboardListener(BundleContext bc, BasePlugin plugin) {
    this.bc = bc;
    this.plugin = plugin;
  }

  /**
   * Called by OSGI when the subscribed service type (blackboard) becomes available.
   *
   * @param se The registration event.
   */
  public void serviceChanged(ServiceEvent se) {
    if (initialized) {
      return;
    }
    if (se.getType() == ServiceEvent.REGISTERED) {
      ServiceReference ref = se.getServiceReference();
      Object service = bc.getService(ref);
      if (service instanceof Blackboard) {
        Blackboard bb = (Blackboard) service;
        plugin.setBlackboard(bb);
        initialized = true;
      }
    }
    if (se.getType() == ServiceEvent.UNREGISTERING) {
      //TODO: fix this to work with updates of blackboard that would case unregister+new register
      log.debug("Blackboard is unregistering(??)");
      initialized = false;
    }
  }
}
