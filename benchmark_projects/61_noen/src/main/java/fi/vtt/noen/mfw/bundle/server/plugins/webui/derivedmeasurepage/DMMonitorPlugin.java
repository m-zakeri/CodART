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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMValue;
import org.osgi.framework.BundleContext;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Monitors for posted values for derived measures, stores these values and provides access to them.
 * TODO: if DM are to be properly supported, this needs to be persisted etc.
 *
 * @author Teemu Kanstren
 */
public class DMMonitorPlugin extends BasePlugin {
  private final static Logger log = new Logger(DMMonitorPlugin.class);
  //key=dm id, value=dm value
  private Map<Integer, DMValue> values = new HashMap<Integer, DMValue>();

  public DMMonitorPlugin(BundleContext bc) {
    super(bc, log);
  }

  public Set getCommands() {
    return createCommandSet(DMValue.class);
  }

  public void process(DataObject data) {
    DMValue dm = (DMValue) data;
    values.put(dm.getId(), dm);
  }

  //gives access to the value of a specific dm
  public DMValue getValueFor(Integer dmId) {
    return values.get(dmId);
  }
}
