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

import fi.vtt.noen.mfw.bundle.blackboard.Blackboard;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMValue;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import java.util.Collection;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * A component that takes care of actual processing of derived measures according to received requests.
 *
 * @author Teemu Kanstren
 */
public class DMProcessor {
  private final static Logger log = new Logger(DMProcessor.class);
  private final Collection<BMDescription> requiredValues;
  //this is a set to keep only the latest value available
  protected final Map<BMDescription, Value> values = new TreeMap<BMDescription, Value>();
  private final String name;
  private final DMDefinition dmDefinition;
  protected final Blackboard bb;
//  private final DMPlugin plugin;

  public DMProcessor(Blackboard bb, DMDefinition dmDefinition) {
    this.dmDefinition = dmDefinition;
    this.requiredValues = dmDefinition.getRequiredBM();
    this.name = dmDefinition.getName();
    this.bb = bb;
//    this.plugin = plugin;
  }

  public String name() {
    return name;
  }

  public void process(Value toProcess) throws DMProcessingException {
    checkAndSaveValue(toProcess);

    Collection<BMDescription> missingValues = getMissingValues();
    log.debug("Missing values:" + missingValues);
    DMValue dmValue = null;
    if (missingValues.size() > 0) {
      dmValue = new DMValue(dmDefinition, System.currentTimeMillis(), missingValues);
    } else if (dmDefinition.getScript() == null) {
      //todo: create an event here..
//      dmValue = new DMValue("No script defined");
    } else {
      dmValue = executeScript();
    }
    log.debug("publishing DM value:" + dmValue);
    bb.process(dmValue);
  }

  public void checkAndSaveValue(Value value) {
    log.debug("processing value:" + value);
    for (BMDescription bm : requiredValues) {
      if (bm.matches(value)) {
        Value old = values.get(bm);
        //todo: timeout for when do we take the new measure into use if higher precision is old?
        if (old == null || value.getPrecision() >= old.getPrecision()) {
          values.put(bm, value);
        }
        break;
      }
    }
  }

  private Collection<BMDescription> getMissingValues() {
    Set<BMDescription> missing = new HashSet<BMDescription>();
    log.debug("required values:"+requiredValues);
    for (BMDescription bm : requiredValues) {
      if (values.get(bm) == null) {
        missing.add(bm);
      }
    }
    return missing;
  }

  private DMValue executeScript() throws DMProcessingException {
    ScriptEngineManager mgr = new ScriptEngineManager();
    ScriptEngine jsEngine = mgr.getEngineByName("JavaScript");
    String script = createFullScript();
    log.debug("Trying to execute script:" + script);
    Object result = null;
    try {
      result = jsEngine.eval(script);
    } catch (ScriptException e) {
      throw new DMProcessingException("Error in processing derived measure " + name, e);
    }
    long time = System.currentTimeMillis();
    if (result instanceof Number) {
      Number n = (Number) result;
      double d = n.doubleValue();
      return new DMValue(dmDefinition, d, time);
    }
    if (result instanceof Boolean) {
      Boolean b = (Boolean) result;
      return new DMValue(dmDefinition, b, time);
    }
    if (result instanceof String) {
      String str = (String) result;
      return new DMValue(dmDefinition, str, time);
    }
    throw new DMProcessingException("Unable to map script return type to value type (not one of Number, Boolean or String) for DM " + name);
  }

  public String createFullScript() throws DMProcessingException {
    Collection<BMDescription> missingValues = getMissingValues();
    if (missingValues.size() > 0) {
      throw new DMProcessingException("Cannot create script for derived measure:" + name + " - missing values: " + missingValues);
    }
    String script = "";
    int i = 1;
    for (Value value : values.values()) {
      script += "bm" + (i++) + " = " + value.valueString() + ";\n";
    }
    script += dmDefinition.getScript();
    return script;
  }
}
