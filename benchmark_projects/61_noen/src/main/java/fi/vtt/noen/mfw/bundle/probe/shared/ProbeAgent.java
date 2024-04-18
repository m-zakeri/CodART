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

package fi.vtt.noen.mfw.bundle.probe.shared;

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;

import java.util.Collection;
import java.util.Map;

/**
 * Interface to control a probe-agent.
 * <p/>
 * TODO: security is not considered, authentication, etc.
 *
 * @author Teemu Kanstren
 */
public interface ProbeAgent {
  public void startProbe(long probeId);
  public void stopProbe(long probeId);
  public void requestMeasure(String measureURI, long subscriptionId);
  public void subscribe(String measureURI, long interval, long subscriptionId);
  public void unSubscribe(String measureURI, long subscriptionId);
  public void setConfiguration(long probeId, Map<String, String> configuration);  
  public Collection<ProbeConfiguration> getConfigurationParameters(long probeId);  
  public Map<Long, Probe> getProbes();  
  public void setReference(long subscriptionId, String reference);
}
