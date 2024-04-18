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

package fi.vtt.noen.mfw.bundle.server.plugins.registry;

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

import java.util.Collection;
import java.util.List;
import java.util.Map;

/**
 * @author Teemu Kanstren
 */
public interface RegistryPlugin {
  public List<ProbeDescription> getProbes();
  public List<BMDescription> getAvailableBM();
  public List<DMDefinition> getDerivedMeasures();
  public long registerProbe(Map<String, String> properties);
  public ProbeDescription getProbeForBM(long bmId);
  public ProbeDescription getProbeFor(long probeId);
  public boolean processKeepAlive(long probeId);
  public void createDM(String name, String script);
  public BMDescription descriptionFor(String measureURI);
  public long targetIdFor(String measureURI);
  public Collection<TargetDescription> getTargets();
  public long addSubscription(long sacId, BMDescription bm, long frequency, long probeId);
  public long getSacIdForSubscription(long subscriptionId);
  public long getFrequencyForSubscription(long subscriptionId);
  public void removeSubscription(long sacId, long subscriptionId);
  public long addMeasurementRequest(long sacId, BMDescription bm, long probeId);
  public long getIdForSubscription(long sacId, long bmId);
  public void checkSubscriptions(long probeId, List<Long> currentSubscriptions);
  public ProbeDescription getProbeForSubscription(long subscriptionId);
  public void setProbeDisabled(ProbeDescription probe);
}
