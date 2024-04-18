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
import java.util.Properties;

/**
 * The interface for requesting the actual measurements from actual probes.
 * Called by the probe-agent to satisfy the measurement requests.
 * Sampling is expected to be done by the probe-agent through this interface.
 * The implementation of this interface itself can and needs to implement any functionality
 * to address specific needs set by a probe, such as handling any sampling done by the probe
 * itself, or custom protocols for the probe control.
 *
 * @author Teemu Kanstren
 */
public interface Probe {
  /** Return the descriptions for the probe. */
  public ProbeInformation getInformation();
  /** Called by the MFW components when a measurement is needed. */
  public BaseMeasure measure();
  /** start and stop a probe if supported */
  public void startProbe();
  public void stopProbe();
  /** Same as getConfiguration but used to set the values from the SAC. */
  public void setConfiguration(Map<String, String> configuration);
  public Collection<ProbeConfiguration> getConfigurationParameters();
  public void init(Properties properties);
}
