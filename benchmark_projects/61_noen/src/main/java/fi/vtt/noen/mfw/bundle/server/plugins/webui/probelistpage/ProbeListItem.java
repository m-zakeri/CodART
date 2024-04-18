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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage;

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

/**
 * @author Teemu Kanstren
 */
public class ProbeListItem {
  private final ProbeDescription probe;

  public ProbeListItem(ProbeDescription probe) {
    this.probe = probe;
  }

  public long getProbeId() {
    return probe.getProbeId();
  }

  public TargetDescription getTarget() {
    return probe.getTarget();
  }

  public String getEndpoint() {
    return probe.getEndpoint();
  }

  public void setEndpoint(String probeUrl) {
    probe.setEndpoint(probeUrl);
  }

  public String getMeasureURI() {
    return probe.getMeasureURI();
  }

  public int getPrecision() {
    return probe.getPrecision();
  }

  public int getDelay() {
    return probe.getDelay();
  }

  public String getProbeName() {
    return probe.getProbeName();
  }

  public String getBmName() {
    return probe.getBm().getBmName();
  }
}
