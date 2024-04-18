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

/**
 * When a probe is disabled (does not provide keep-alive), an event is created on the blackboard.
 * //TODO: check if this would be better of as an Event class extension.
 */
public class ProbeDisabled extends DataObject {
  private final ProbeDescription probeDescription;
  private final boolean bmDisabled;
  private final boolean targetDisabled;

  public ProbeDisabled(ProbeDescription probe, boolean bmDisabled, boolean targetDisabled) {
    super(DataType.PROBE_DISABLED);
    this.probeDescription = probe;
    this.bmDisabled= bmDisabled;
    this.targetDisabled= targetDisabled;
  }

  public ProbeDescription getProbeDescription() {
    return probeDescription;
  }
  
  public boolean isBmDisabled() {
    return bmDisabled;
  }

  public boolean isTargetDisabled() {
    return targetDisabled;
  }
}
