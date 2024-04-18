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

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeAgent;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.osgi.framework.BundleContext;

/**
 * OSGI activator for probe-agent XMLRPC communication interface.
 *
 * @author Teemu Kanstren
 */
public class PAXmlRpcPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(PAXmlRpcPluginActivator.class);
  //the probe-agent XMLRPC communication implementation
  private ProbeAgentImpl probe;
  private ProbeAgentConfig config = null;

  public PAXmlRpcPluginActivator() {
    super(log);
  }

  //for testing
  public PAXmlRpcPluginActivator(ProbeAgentConfig config) {
    super(log);
    this.config = config;
  }

  public void start(BundleContext bc) throws Exception {
    probe = new ProbeAgentImpl(bc, config);
    probe.startAgent();
    //re-get it in case it was only initialized in the probe-agent
    config = probe.getConfig();
    registerPlugin(bc, probe, null, ProbeAgent.class.getName());
    if (!config.isLocalInUse()) {
      ServerAgent serverAgent = probe.getConfig().getDestination();
      bc.registerService(ServerAgent.class.getName(), serverAgent, null);
    }
  }

  public void stop(BundleContext bc) throws Exception {
    probe.stopAgent();
  }

  public ProbeAgentImpl getProbeAgent() {
    return probe;
  }
}
