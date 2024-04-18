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

package fi.vtt.noen.mfw.bundle.server.shared.datamodel;

import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.DataType;

import java.util.ArrayList;
import java.util.List;

/**
 * Defines a derived measure. A DM has a name and a script (Javascript) that is used to evaluate it. It also has
 * a set of base measures that the script gets as input for calculation.
 *
 * @author Teemu Kanstren
 */
public class DMDefinition extends DataObject {
  private final int id;
  private final String name;
  private String script;
  private final List<BMDescription> requiredBM = new ArrayList<BMDescription>();

  public DMDefinition(int id, String name, String script) {
    super(DataType.DM_DEFINITION);
    this.id = id;
    this.name = name;
    this.script = script;
  }

  public int getId() {
    return id;
  }

  public String getName() {
    return name;
  }

  public String getScript() {
    return script;
  }

  public void setScript(String script) {
    this.script = script;
  }

  public List<BMDescription> getRequiredBM() {
    return requiredBM;
  }
}
