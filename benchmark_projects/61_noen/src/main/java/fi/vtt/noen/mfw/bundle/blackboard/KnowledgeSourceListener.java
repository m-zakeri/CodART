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

package fi.vtt.noen.mfw.bundle.blackboard;

import fi.vtt.noen.mfw.bundle.common.KnowledgeSource;
import fi.vtt.noen.mfw.bundle.common.Logger;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;

/**
 * Listens for new OSGI services and registers any found knowledge sources (plugins) to the blackboard.
 *
 * @author Teemu Kanstrén
 */
public class KnowledgeSourceListener implements ServiceListener {
  private final static Logger log = new Logger(KnowledgeSourceListener.class);
  private final Blackboard blackboard;
  private final BundleContext bc;

  public KnowledgeSourceListener(Blackboard blackboard, BundleContext bc) {
    this.blackboard = blackboard;
    this.bc = bc;
  }

  public void serviceChanged(ServiceEvent se) {
    if (se.getType() == ServiceEvent.REGISTERED) {
      ServiceReference ref = se.getServiceReference();
      Object service = bc.getService(ref);
      if (service instanceof KnowledgeSource) {
        log.debug("New service found in listener..");
        blackboard.register((KnowledgeSource)service);
      }
    }
    //TODO UNREGISTERED (switch)
  }
}
