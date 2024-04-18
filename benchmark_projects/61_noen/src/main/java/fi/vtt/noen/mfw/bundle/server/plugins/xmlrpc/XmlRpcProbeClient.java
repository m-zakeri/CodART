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
import fi.vtt.noen.mfw.bundle.common.MFWXmlRpcFactoryFactory;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeAgent;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.client.util.ClientFactory;

import java.net.URL;
import java.util.Collection;
import java.util.Map;

/**
 * An XML-RPC client for calling a probeagent.
 *
 * @author Teemu Kanstren
 */
public class XmlRpcProbeClient implements ProbeAgent {
  private final static Logger log = new Logger(XmlRpcProbeClient.class);
  private ProbeAgent probe;

  public XmlRpcProbeClient(ProbeAgent probe) {
    this.probe = probe;
  }

  public XmlRpcProbeClient(URL url) throws XmlRpcException {
    ClientFactory factory = MFWXmlRpcFactoryFactory.createFactory(url);
    //we create the proxy that forwards all received calls over XMLRPC to the given endpoint (URL)
    probe = (ProbeAgent) factory.newInstance(getClass().getClassLoader(), ProbeAgent.class);
  }

  public void startProbe(long probeId) {
    log.debug("pre-startprobe:" + probeId);
    probe.startProbe(probeId);
    log.debug("post-startprobe:" + probeId);
  }

  public void stopProbe(long probeId) {
    probe.stopProbe(probeId);
  }

  public void subscribe(String measureURI, long interval, long subscriptionId) {
    probe.subscribe(measureURI, interval, subscriptionId);
  }

  public void unSubscribe(String measureURI, long subscriptionId) {
    probe.unSubscribe(measureURI, subscriptionId);
  }

  public void requestMeasure(String measureURI, long subscriptionId) {
    probe.requestMeasure(measureURI, subscriptionId);
  }

  public void setConfiguration(long probeId, Map<String, String> configuration) {
    probe.setConfiguration(probeId, configuration);
  }
  
  public Collection<ProbeConfiguration> getConfigurationParameters(long probeId) {
    return probe.getConfigurationParameters(probeId);
  }

  public Map<Long, Probe> getProbes() {
    return probe.getProbes();
  }

  public void setReference(long subscriptionId, String reference) {
    probe.setReference(subscriptionId, reference);
  }
}
