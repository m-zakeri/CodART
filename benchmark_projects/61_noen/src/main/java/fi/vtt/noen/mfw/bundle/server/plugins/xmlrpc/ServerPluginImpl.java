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

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeAgent;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import org.osgi.framework.BundleContext;

import java.io.FileInputStream;
import java.io.InputStream;
import java.net.URL;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/**
 * A facade to forward requests to the client. Whereas the ServerAgentImpl is the server-agent that the
 * probe-agent communicates with, this would be the part that the client (e.g. SAC) interacts with.
 *
 * @author Teemu Kanstren
 */
public class ServerPluginImpl extends BasePlugin implements ServerPlugin, RegistryUser {
  private final static Logger log = new Logger(ServerPluginImpl.class);
  private RegistryPlugin registry;
  private final Map<String, ProbeAgent> probeEndpoints = new HashMap<String, ProbeAgent>();
  private ProbeAgent localLink = null;
  private Boolean localInUse = false;

  public ServerPluginImpl(BundleContext bc, Boolean localInUse) {
    super(bc, log);
    this.localInUse = localInUse;
  }

  public void start() {
    RegistryServiceListener rl = new RegistryServiceListener(bc, log, this);
    rl.init();

    ProbeAgentListener pl = new ProbeAgentListener(bc, this);
    pl.init();

    if (localInUse != null) {
      return;
    }

    try {
      InputStream in = new FileInputStream(Const.CONFIGURATION_FILENAME);
      Properties props = new Properties();
      props.load(in);
      if (props.getProperty(Const.LOCAL_LINK_IN_USE) != null) {
        this.localInUse = true;
      }
    } catch (Exception e) {
      throw new RuntimeException("Failed to read configuration file '" + Const.CONFIGURATION_FILENAME + "'", e);
    }
  }

  public void setLocalLink(ProbeAgent localLink) {
    this.localLink = localLink;
  }

  public synchronized void requestBM(long bmId, long subscriptionId) {
    ProbeDescription desc = registry.getProbeForBM(bmId);
    if (desc == null) {
      throw new IllegalArgumentException("No probe available for bmid:" + bmId);
    }
    ProbeAgent probe = getProbeFor(desc);

    log.debug("Requesting bm:" + bmId);
    
    probe.requestMeasure(desc.getMeasureURI(), subscriptionId);
    
  }

  public synchronized void subscribeToBM(long bmId, long frequency, long subscriptionId) {
    ProbeDescription desc = registry.getProbeForBM(bmId);
    if (desc == null) {
      throw new IllegalArgumentException("No probe available for bmid:" + bmId);
    }
    ProbeAgent probe = getProbeFor(desc);

    log.debug("Requesting bm:" + bmId);
    
    probe.subscribe(desc.getMeasureURI(), frequency, subscriptionId);
    
  }

  public synchronized void unSubscribeToBM(long bmId, long subscriptionId) {
    ProbeDescription desc = registry.getProbeForBM(bmId);
    if (desc == null) {
      throw new IllegalArgumentException("No probe available for bmid:" + bmId);
    }
    ProbeAgent probe = getProbeFor(desc);

    log.debug("Requesting bm:" + bmId);
    
    probe.unSubscribe(desc.getMeasureURI(), subscriptionId);
    
  }
  
  public synchronized void unSubscribeToBM(ProbeDescription probeDescription, Long subscriptionId) {
    ProbeAgent probe = getProbeFor(probeDescription);

    log.debug("unSubscribeToBM");
    
    probe.unSubscribe(probeDescription.getMeasureURI(), subscriptionId);
    
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  public boolean setProbeConfiguration(long probeId, Map<String, String> configuration) {
    ProbeDescription desc = registry.getProbeFor(probeId);
    ProbeAgent probe = getProbeFor(desc);
    probe.setConfiguration(probeId, configuration);
    return true;
  }

  private ProbeAgent getProbeFor(ProbeDescription desc) {
    String endpoint = desc.getEndpoint();

    if (endpoint.equals(Const.LOCAL_LINK_ENDPOINT_URL)) {
//    if (localInUse) {
      return localLink;
    }

    ProbeAgent probe = probeEndpoints.get(endpoint);
    if (probe == null) {
      try {
        probe = new XmlRpcProbeClient(new URL(endpoint));
      } catch (Exception e) {
        throw new RuntimeException("Unable to create XMLRPC connection to probe for URL:" + endpoint, e);
      }
      probeEndpoints.put(endpoint, probe);
    }
    return probe;
  }

  
  public Collection<ProbeConfiguration> requestProbeConfigurationParameters(long probeId) {
    ProbeDescription desc = registry.getProbeFor(probeId);
    ProbeAgent probe = getProbeFor(desc);
    log.debug("probe:"+probe);
    return probe.getConfigurationParameters(probeId);
  }

  public void setReference(long subscriptionId, String reference) {
    ProbeDescription desc = registry.getProbeForSubscription(subscriptionId);
    ProbeAgent probe = getProbeFor(desc);
    log.debug("probe:"+probe);
    probe.setReference(subscriptionId, reference);
  }

}
