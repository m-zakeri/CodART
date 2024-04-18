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

package fi.vtt.noen.mfw.probes.http;

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgentActivator;
import org.osgi.framework.BundleContext;

/**
 * OSGI activagtor for HTTP probe-agent.
 *
 * @author Teemu Kanstren
 */
public class HttpProbeAgentActivator extends BaseProbeAgentActivator {
  private final static Logger log = new Logger(HttpProbeAgentActivator.class);

  public HttpProbeAgentActivator() {
    super(log, Const.HTTP_CONFIG_PREFIX);
  }

  public void start(BundleContext bc) throws Exception {
    registerMany(bc, HTTPProbeAgent.class);
    HttpServiceTracker tracker = new HttpServiceTracker(bc);
    tracker.open();
    log.debug("HTTP agent started with information:" + getProbeProperties());
  }

  public void stop(BundleContext bc) throws Exception {
  }
}