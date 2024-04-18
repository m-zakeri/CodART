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

package fi.vtt.noen.mfw.bundle.server.plugins.rest;

import com.sun.jersey.spi.container.servlet.ServletContainer;
import fi.vtt.noen.mfw.bundle.common.Logger;
import org.apache.felix.http.api.ExtHttpService;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceReference;
import org.osgi.service.http.HttpService;
import org.osgi.util.tracker.ServiceTracker;

import java.util.Dictionary;
import java.util.Hashtable;

/**
 * Looks for the OSGI HTTP service and registers the Jersey services as a filter to this service when available.
 *
 * @author Teemu Kanstren
 */
public class HttpServiceTracker extends ServiceTracker {
  private final static Logger log = new Logger(HttpServiceTracker.class);
  private ExtHttpService httpService = null;

  public HttpServiceTracker(BundleContext bc) {
    super(bc, HttpService.class.getName(), null);
  }

  @Override
  public Object addingService(ServiceReference sr) {
    httpService = (ExtHttpService) super.addingService(sr);

    try {
      Dictionary<String, String> config = new Hashtable<String, String>();
      config.put("javax.ws.rs.Application", JerseyApplication.class.getName());
//      config.put("com.sun.jersey.config.property.packages", "fi.vtt.noen.mfw.bundle.server.plugins.rest");
//      config.put("filterMappingUrlPattern", "/mfw/rest/*");
      httpService.registerServlet("/rest", new ServletContainer(), config, null);
//      httpService.registerFilter(new ServletContainer(), "/mfw/rest/*", config, 0, null);
//      httpService.registerServlet("/test/*", new BaseMeasureServlet(), null, null);

    } catch (Exception e) {
      log.error("Failed to register servlet", e);
    }
    /*
    Dictionary<String, String> jerseyParameters = new Hashtable<String, String>();
    jerseyParameters.put("javax.ws.rs.Application", JerseyApplication.class.getName());
    try {
      httpService.registerServlet("/jersey", new ServletContainer(), jerseyParameters, null);
    } catch (Exception e) {
      log.error("Failed to register Jersey servlet", e);
    }*/

    return httpService;
  }

  @Override
  public void removedService(ServiceReference reference, Object service) {
    super.removedService(reference, service);
  }
}