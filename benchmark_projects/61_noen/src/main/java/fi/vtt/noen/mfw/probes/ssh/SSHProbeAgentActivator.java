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

package fi.vtt.noen.mfw.probes.ssh;

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgentActivator;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEventBus;
import org.osgi.framework.BundleContext;

import java.util.Collection;
import java.util.Properties;

/**
 * OSGi activator
 *
 * @author Teemu Kanstren
 */
public class SSHProbeAgentActivator extends BaseProbeAgentActivator {
  private final static Logger log = new Logger(SSHProbeAgentActivator.class);

  public SSHProbeAgentActivator() {
    super(log, Const.SSH_CONFIG_PREFIX);
  }

  //for testing
  public SSHProbeAgentActivator(Properties config) {
    super(log, config, Const.SSH_CONFIG_PREFIX);
  }

  public void start(BundleContext bc) throws Exception {
    registerMany(bc, SSHProbeAgent.class);
    ProbeEventBus eb = new ProbeEventBus(bc);
    eb.event("SSH ProbeAgent Activator", "Started");
    log.debug("SSH agent started with information:" + getProbeProperties());
  }

  public void stop(BundleContext bc) throws Exception {
    Collection<Probe> probes = getProbes().values();
    for (Probe probe : probes) {
      probe.stopProbe();
    }
    //call stop on all agents
  }
}
