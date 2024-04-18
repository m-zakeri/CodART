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

package fi.vtt.noen.mfw.bundle.server.plugins.derivedmeasure;

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Logger;
import org.osgi.framework.BundleContext;

import java.util.Properties;

/**
 * @author Teemu Kanstren
 */
public class DMPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(DMPluginActivator.class);

  public DMPluginActivator() {
    super(log);
  }

  public void start(BundleContext bc) throws Exception {
    log.debug("DM plugin starting");
    Properties props = new Properties();
    props.put("version", "1.0");
    DMPlugin dm = new DMPlugin(bc);
    registerPlugin(bc, dm, props, DMPlugin.class.getName());
    log.debug("start done");
  }

  public void stop(BundleContext bc) throws Exception {

  }
}
