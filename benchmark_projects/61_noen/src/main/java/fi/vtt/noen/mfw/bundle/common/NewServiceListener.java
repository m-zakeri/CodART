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

import org.osgi.framework.BundleContext;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;

import java.util.Collection;

/**
 * A base class for OSGI services to listen to new services of given type appearing and to keep track of them in a list.
 *
 * @author Teemu Kanstren
 */
public abstract class NewServiceListener implements ServiceListener {
  //OSGI stuff
  private final BundleContext bc;
  //type of service this is listening to
  private final Class serviceType;
  //the services of the given type that have been found. can be null in which case only the registered() method is called.
  private final Collection items;
  private final Logger log;

  public NewServiceListener(BundleContext bc, Class serviceType, Logger log) {
    this(bc, serviceType, null, log);
  }

  public NewServiceListener(BundleContext bc, Class serviceType, Collection items, Logger log) {
    this.bc = bc;
    this.serviceType = serviceType;
    this.items = items;
    this.log = log;
  }

  /**
   * Called by OSGI when the monitored registration is done.
   *
   * @param se The registration event.
   */
  public void serviceChanged(ServiceEvent se) {
    ServiceReference ref = se.getServiceReference();
    Object service = bc.getService(ref);
    if (!serviceType.isInstance(service)) {
      return;
    }
    if (se.getType() == ServiceEvent.REGISTERED) {
      if (items != null) {
        items.add(service);
      }
      registered(service);
    }
    if (se.getType() == ServiceEvent.UNREGISTERING) {
      if (items != null) {
        items.remove(service);
      }
      unregistered(service);
    }
  }

  /**
   * This is here to allow subclasses to specify specific actions when a service is made available.
   * For example, a new probe is installed and the client wishes to register it to the server..
   *
   * @param service The discovered object.
   */
  public abstract void registered(Object service);

  public abstract void unregistered(Object service);

  /**
   * Starts by reading all registered services of the given type from the current OSGI bundlecontext.
   * After this list is done, new registrations/unregistrations are captured with the help of the listener.
   */
  public void init() {
    bc.addServiceListener(this);
    //if a new communication layer is added between these two calls, a duplicate is added and thus
    //the comms collection needs to be a HashSet which removes duplicates
    String serviceName = serviceType.getName();
    log.debug("Getting all "+serviceName+" services while starting a MFW bundle");
    ServiceReference[] serviceRefs = null;
    try {
      serviceRefs = bc.getServiceReferences(serviceType.getName(), null);
    } catch (InvalidSyntaxException e) {
      log.error("Failed to get servicese of type:"+serviceName, e);
      return;
    }
    if (serviceRefs == null) {
      log.debug("No "+ serviceName +" service found");
      return;
    }
    for (ServiceReference sr : serviceRefs) {
      log.debug("Attaching to "+serviceName+" service:"+sr);
      Object service = bc.getService(sr);
      if (items != null) {
        items.add(service);
      }
      registered(service);
    }
  }

  public void stop() {
    bc.removeServiceListener(this);
    if (items != null) {
      items.clear();
    }
  }
}
