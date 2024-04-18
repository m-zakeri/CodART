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

package fi.vtt.noen.mfw.probes.custom;

import ch.ethz.ssh2.Connection;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEventBus;
import org.osgi.framework.BundleContext;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * This class is here to show how you might wish to share resources between your probes if you think they are
 * costly or if you can not have more than one etc.
 *
 * @author Teemu Kanstren
 */
public class CustomCore {
  private final static Logger log = new Logger(CustomCore.class);
  //keeps track of SSH connections, only creating one for one address
  private final static Map<String, Connection> connections = new HashMap<String, Connection>();
  private final BundleContext bc;

  public CustomCore(BundleContext bc) {
    this.bc = bc;
  }

  public void init() {
    //register the CoreConfigurationHandler probe
    //it is the one that creates new probes when "add" parameter is given
    bc.registerService(Probe.class.getName(), new CoreConfigurationHandler(this, bc), null);
  }

  //Provides access to the shared resources, SSH connections, as requested from CustomProbeFacade
  public Connection getConnection(String target, String username, String password) throws Exception {
    Connection connection = connections.get(target);
    if (connection == null) {
      connection = new Connection(target);
      log.debug("connecting now to:"+target);
      /* Now connect */
      connection.connect();
      log.debug("connected ok");
      boolean authenticated = connection.authenticateWithPassword(username, password);

      if (!authenticated)
        throw new IOException("Authentication failed.");

      log.debug("authenticated ok");
      connections.put(target, connection);
    }
    return connection;
  }
}
