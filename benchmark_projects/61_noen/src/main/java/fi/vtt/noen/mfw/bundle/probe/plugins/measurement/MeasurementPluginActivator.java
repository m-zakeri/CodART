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

package fi.vtt.noen.mfw.bundle.probe.plugins.measurement;

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.plugins.xmlrpc.ProbeAgentConfig;
import org.osgi.framework.BundleContext;

/**
 * OSGI activator for MeasurementPlugin.
 *
 * @author Teemu Kanstren
 */
public class MeasurementPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(MeasurementPluginActivator.class);
  private MeasurementProvider provider;
  private int threadPoolSize = -1;
  private int timeout = -1;

  public MeasurementPluginActivator() {
    super(log);
  }

  public MeasurementPluginActivator(int threadPoolSize, int timeout) {
    super(log);
    this.threadPoolSize = threadPoolSize;
    this.timeout = timeout;
  }

  public void start(BundleContext bc) throws Exception {
    init(bc);
  }

  public void init(BundleContext bc) throws Exception {
    provider = new MeasurementProvider(bc, threadPoolSize, timeout);
    provider.start();
    registerPlugin(bc, provider, null, MeasurementProvider.class.getName());
  }

  public void stop(BundleContext bc) throws Exception {
    provider.stop();
  }
}
