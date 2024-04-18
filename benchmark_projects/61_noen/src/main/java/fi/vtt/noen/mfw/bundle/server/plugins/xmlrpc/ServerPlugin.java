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

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;

import java.util.Collection;
import java.util.Map;

/**
 * @author Teemu Kanstren
 */
public interface ServerPlugin {
  public void requestBM(long bmId, long subscriptionId);
  public void subscribeToBM(long bmId, long interval, long subscriptionId);
  public void unSubscribeToBM(long bmId, long subscriptionId);
  public boolean setProbeConfiguration(long probeId, Map<String, String> configuration);
  public Collection<ProbeConfiguration> requestProbeConfigurationParameters(long probeId);
  //public void requestBMResults(long bmId, int interval);
  public void unSubscribeToBM(ProbeDescription probeDescription, Long subscriptionId);
  public void setReference(long subscriptionId, String reference);
}
