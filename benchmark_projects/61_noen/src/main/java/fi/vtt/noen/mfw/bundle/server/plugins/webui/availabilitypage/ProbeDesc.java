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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.availabilitypage;

public class ProbeDesc {
  private final long probeId;
  private final long bmId;
  private final String name;
  private final boolean disabled;
  
  public ProbeDesc(long probeId, long bmId, String name, boolean disabled) {
    super();
    this.probeId = probeId;
    this.bmId = bmId;
    this.name = name;
    this.disabled = disabled;
  }

  public long getProbeId() {
    return probeId;
  }

  public long getBmId() {
    return bmId;
  }

  public String getName() {
    return name;
  }

  public boolean isDisabled() {
    return disabled;
  }
}
