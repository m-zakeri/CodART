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

package fi.vtt.noen.mfw.bundle.server.plugins.update;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.updater.UpdateRequest;
import org.osgi.framework.BundleContext;

import java.util.Set;
/**
 * Handles updates of components with the help of the OSGI features. Should work for all
 * agents in the MFW.
 *
 * @author Teemu Kanstren
 */
public class UpdatePlugin extends BasePlugin {
  private final static Logger log = new Logger(UpdatePlugin.class);

  public UpdatePlugin(BundleContext bc) {
    super(bc, log);
  }

  public void process(DataObject data) {
  }

  public Set getCommands() {
    return createCommandSet(UpdateRequest.class);
  }

}
