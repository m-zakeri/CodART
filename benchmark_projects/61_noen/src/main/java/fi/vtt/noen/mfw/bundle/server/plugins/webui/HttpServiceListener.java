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

package fi.vtt.noen.mfw.bundle.server.plugins.webui;

import fi.vtt.noen.mfw.bundle.common.Logger;
import org.apache.felix.http.api.ExtHttpService;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceEvent;
import org.osgi.framework.ServiceListener;
import org.osgi.framework.ServiceReference;

/**
 * OSGI listener to capture the HTTP service when available.
 *
 * @author Teemu Kanstren
 */
public class HttpServiceListener implements ServiceListener {
  private final static Logger log = new Logger(HttpServiceListener.class);
  //OSGI container access
  private final BundleContext bc;
  //the main web ui class
  private final WebUIPlugin ui;

  public HttpServiceListener(BundleContext bc, WebUIPlugin ui) {
    this.bc = bc;
    this.ui = ui;
  }

  public void serviceChanged(ServiceEvent se) {
    if (se.getType() == ServiceEvent.REGISTERED) {
      ServiceReference ref = se.getServiceReference();
      log.debug("registration:"+ref);
      Object service = bc.getService(ref);
      if (service instanceof ExtHttpService) {
        ui.init();
        log.debug("Listener initialized webui");
      }
    }
    if (se.getType() == ServiceEvent.UNREGISTERING) {
      //for some reason Felix seems to register, unregister, and register again this service
      ui.terminate();
      log.debug("Listener terminating webui");
    }

  }
}
