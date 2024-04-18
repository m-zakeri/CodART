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

package fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.MFWRequestProcessFactoryFactory;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServer;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.ServletWebServer;

/**
 * An XML-RPC server for receiving calls for the MFW server.
 *
 * @author Teemu Kanstren
 */
public class XmlRpcServerServer {
  private final static Logger log = new Logger(XmlRpcServerServer.class);
  //the port where to listen to for messages
  private final int port;
  //the HTTP server for receiving the XMLRPC messages
  private ServletWebServer webServer;
  //the implementation class
  private final ServerAgent agent;

  public XmlRpcServerServer(int port, ServerAgent agent) {
    this.port = port;
    this.agent = agent;
  }

  public void start() {
    try {
      PropertyHandlerMapping phm = new PropertyHandlerMapping();
      //we need to set this to get around how XMLRPC wants to create a new object each time a request is received, in order to share some state
      phm.setRequestProcessorFactoryFactory(new MFWRequestProcessFactoryFactory(agent));
      //enables void types in XMLRPC calls
      phm.setVoidMethodEnabled(true);
      String name = ServerAgent.class.getName();
      phm.addHandler(name, ServerAgent.class);
      //xmlRpcServer.setHandlerMapping(phm);

      webServer = new ServletWebServer(new MfwXmlRpcServlet(phm), port);
      XmlRpcServer xmlRpcServer = webServer.getXmlRpcServer();

      XmlRpcServerConfigImpl serverConfig = new XmlRpcServerConfigImpl();
      serverConfig.setEnabledForExtensions(true);
      serverConfig.setContentLengthOptional(false);
      xmlRpcServer.setConfig(serverConfig);
      webServer.start();
    } catch (Exception e) {
      log.error("Failed to start XmlRpcServerServer", e);
    }
  }

  public void stop() {
    webServer.shutdown();
  }
}
