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

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.KnowledgeSource;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Set;

/**
 * Processes derived measure values from received measurement data according to received
 * derived measure definitions.
 *
 * @author Teemu Kanstren
 * @see KnowledgeSource
 */
public class DMPlugin extends BasePlugin {
  private final static Logger log = new Logger(DMPlugin.class);
  private Collection<DMProcessor> dmprocessors = new ArrayList<DMProcessor>();

  public DMPlugin(BundleContext bc) {
    super(bc, log);
  }

  public void process(DataObject data) throws DMProcessingException {
    log.debug("Processing data " + data);
    if (data instanceof DMDefinition) {
      processDMDefinition((DMDefinition) data);
      return;
    }
    if (data instanceof Value) {
      processValue((Value) data);
      return;
    }
    throw new IllegalStateException("DMPlugin does not support data type:" + data.getClass());
  }

  private void processValue(Value value) throws DMProcessingException {
    for (DMProcessor dm : dmprocessors) {
      log.debug("DM invocation:" + dm);
      dm.process(value);
    }
  }

  private void processDMDefinition(DMDefinition definition) {
    log.debug("Adding derived measure definition:" + definition);
    DMProcessor processor = new DMProcessor(bb, definition);
    dmprocessors.add(processor);
  }

  public Set getCommands() {
    return createCommandSet(DMDefinition.class, Value.class);
  }
}
