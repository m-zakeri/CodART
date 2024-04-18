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

import java.util.Collection;
import java.util.Collections;

/**
 * A resulting value from a derived measure calculation.
 *
 * @author Teemu Kanstren
 */
public class DMValue extends DataObject {
  //the definition of this DM.
  private final DMDefinition dmDefinition;
  //any BM that are still missing, preventing the DM from being calculated.
  private final Collection<BMDescription> missingBM;
  //the value of the DM when successfully calculated
  private final Object value;
  //time of calculation
  private final long time;

  public DMValue(DMDefinition dmDefinition, boolean value, long time) {
    super(DataType.DM_VALUE);
    this.dmDefinition = dmDefinition;
    this.value = value;
    this.time = time;
    this.missingBM = Collections.emptyList();
  }

  public DMValue(DMDefinition dmDefinition, long time, Collection<BMDescription> missingBM) {
    super(DataType.DM_VALUE);
    this.dmDefinition = dmDefinition;
    this.value = null;
    this.time = time;
    this.missingBM = missingBM;
  }

  public DMValue(DMDefinition dmDefinition, String value, long time) {
    super(DataType.DM_VALUE);
    this.dmDefinition = dmDefinition;
    this.value = value;
    this.time = time;
    this.missingBM = Collections.emptyList();
  }

  public DMValue(DMDefinition dmDefinition, double value, long time) {
    super(DataType.DM_VALUE);
    this.dmDefinition = dmDefinition;
    this.value = value;
    this.time = time;
    this.missingBM = Collections.emptyList();
  }

  public String getValue() {
    if (missingBM.size() > 0) {
      return "Unknown";
    }
    return ""+value;
  }

  public int getId() {
    return dmDefinition.getId();
  }

  public String getName() {
    return dmDefinition.getName();
  }

  public long getTime() {
    return time;
  }

  public Collection<BMDescription> getMissingBM() {
    return missingBM;
  }

  @Override
  public String toString() {
    return "DMValue{" +
            "missingBM=" + missingBM +
            ", value=" + value +
            ", time=" + time +
            '}';
  }

  
}
