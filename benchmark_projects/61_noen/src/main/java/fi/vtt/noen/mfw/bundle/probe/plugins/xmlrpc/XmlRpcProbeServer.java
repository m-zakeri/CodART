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

package fi.vtt.noen.mfw.bundle.probe.plugins.xmlrpc;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.MFWRequestProcessFactoryFactory;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeAgent;
import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServer;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.WebServer;

/**
 * An XML-RPC server for receiving calls for a probe-agent.
 *
 * @author Teemu Kanstren
 */
public class XmlRpcProbeServer {
  private final static Logger log = new Logger(XmlRpcProbeServer.class);
  //the probe-agent for which the requests are to be forwarded.
  private final ProbeAgent agent;
  //the XMLRPC (HTTP) web-server
  private WebServer webServer;
  //the port where the XMLRPC server will listen to for connections
  private final int port;

  public XmlRpcProbeServer(ProbeAgent agent, int port) {
    this.agent = agent;
    this.port = port;
  }

  //starts and configures the webserver
  public void start() {
    try {
      webServer = new WebServer(port);
      XmlRpcServer xmlRpcServer = webServer.getXmlRpcServer();
      //magic tricks to make the Apache XMLRPC framework use the given "agent" to handle all requests instead of always creating a new one
      //this allows the calls to share runtime state, such as accessing the specific probe implementations
      PropertyHandlerMapping phm = new PropertyHandlerMapping();
      phm.setRequestProcessorFactoryFactory(new MFWRequestProcessFactoryFactory(agent));
      phm.setVoidMethodEnabled(true);
      String name = ProbeAgent.class.getName();
      phm.addHandler(name, ProbeAgent.class);
      xmlRpcServer.setHandlerMapping(phm);

      XmlRpcServerConfigImpl serverConfig = (XmlRpcServerConfigImpl) xmlRpcServer.getConfig();
      serverConfig.setEnabledForExtensions(true);
      serverConfig.setContentLengthOptional(false);
      webServer.start();
      log.debug("web server started on port " + port);
    } catch (Exception e) {
      log.error("Failed to start XmlRpcProbeServer", e);
    }
  }

  public void stop() {
    webServer.shutdown();
  }
}
