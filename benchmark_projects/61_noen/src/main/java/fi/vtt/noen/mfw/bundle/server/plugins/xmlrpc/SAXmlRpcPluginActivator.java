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

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.osgi.framework.BundleContext;

/**
 * OSGI activator for the server-agent XMLRPC communication service.
 *
 * @author Teemu Kanstren
 */
public class SAXmlRpcPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(SAXmlRpcPluginActivator.class);
  //the server-agent implementation
  private ServerAgentImpl serverAgent;
  //the port where the XMLRPC implementation is listening to for messages
  private int port = -1;
  private Boolean localInUse = null;
  private ServerPluginImpl serverPlugin;

  public SAXmlRpcPluginActivator() {
    super(log);
  }

  //for testing
  public SAXmlRpcPluginActivator(Boolean localInUse) {
    super(log);
    this.localInUse = localInUse;
  }

  //for testing
  public SAXmlRpcPluginActivator(int port) {
    super(log);
    this.port = port;
    this.localInUse = false;
  }

  public void start(BundleContext bc) throws Exception {
    serverAgent = new ServerAgentImpl(bc, port, localInUse);
    serverAgent.startAgent();
    registerPlugin(bc, serverAgent, null, ServerAgent.class.getName());

    serverPlugin = new ServerPluginImpl(bc, localInUse);
    serverPlugin.start();
    registerPlugin(bc, serverPlugin, null, ServerPlugin.class.getName());
  }

  public void stop(BundleContext bc) throws Exception {
    serverAgent.stopAgent();
  }

  public ServerAgentImpl getServerAgent() {
    return serverAgent;
  }

  public ServerPluginImpl getServerPlugin() {
    return serverPlugin;
  }
}
