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
 * When a new probe is created, this Event is created. TODO: check if it would be better to extend the Event class.
 */
public class ProbeRegistered extends DataObject {
  private final ProbeDescription probeDescription;
  private final boolean newBM;
  private final boolean newTarget;

  public ProbeRegistered(ProbeDescription probeDescription, boolean newBM, boolean newTarget) {
    super(DataType.PROBE_REGISTERED);
    this.probeDescription = probeDescription;
    this.newBM= newBM;
    this.newTarget= newTarget;
  }

  public ProbeDescription getProbeDescription() {
    return probeDescription;
  }
  
  public boolean isNewBM() {
    return newBM;
  }

  public boolean isNewTarget() {
    return newTarget;
  }

  @Override
  public String toString() {
    return "ProbeRegistered{" +
            "probeDescription=" + probeDescription +
            '}';
  }
}
