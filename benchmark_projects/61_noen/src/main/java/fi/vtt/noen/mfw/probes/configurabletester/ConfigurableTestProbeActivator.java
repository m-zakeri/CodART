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

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgentActivator;
import org.osgi.framework.BundleContext;

import java.util.Properties;

/**
 * This is a test probe to allow deploying any number of test probes for performance testing,
 * with the probe information being configured in a properties file.
 *
 * @author Teemu Kanstren
 */
public class ConfigurableTestProbeActivator extends BaseProbeAgentActivator {
  private final static Logger log = new Logger(ConfigurableTestProbeActivator.class);

  public ConfigurableTestProbeActivator() {
    super(log, Const.TEST_PROBE_AGENT_CONFIG_PREFIX);
  }

  //for testing
  public ConfigurableTestProbeActivator(Properties config) {
    super(log, config, Const.TEST_PROBE_AGENT_CONFIG_PREFIX);
  }

  public void start(BundleContext bc) throws Exception {
    registerMany(bc, ConfigurableTestProbeAgent.class);
  }

  public void stop(BundleContext bundleContext) throws Exception {

  }
}
