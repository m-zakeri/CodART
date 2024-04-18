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

package fi.vtt.noen.mfw.probes.configurabletester;

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgent;

import java.util.Collection;
import java.util.Map;
import java.util.Properties;

/**
 * @author Teemu Kanstren
 */
public class ConfigurableTestProbeAgent extends BaseProbeAgent {
  private String name = null;
  private int count = 0;

  @Override
  public void init(Properties properties) {
    super.init(properties);
    name = properties.getProperty("name");
  }

  public BaseMeasure measure() {
    count++;
    return new BaseMeasure(name+" measure "+count);
  }

  public void startProbe() {
  }

  public void stopProbe() {
  }

  public void setConfiguration(Map<String, String> configuration) {
  }

  public Collection<ProbeConfiguration> getConfigurationParameters() {
    return null;
  }
}

