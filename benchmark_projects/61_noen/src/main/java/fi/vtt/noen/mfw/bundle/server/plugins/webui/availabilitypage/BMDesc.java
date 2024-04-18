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

public class BMDesc {
  private final long bmId;
  private final long deviceId;
  private final String clazz;
  private final String name;
  private final String description;
  private final boolean disabled;
  
  public BMDesc(long bmId, long deviceId, String clazz, String name,
      String description, boolean disabled) {
    super();
    this.bmId = bmId;
    this.deviceId = deviceId;
    this.clazz = clazz;
    this.name = name;
    this.description = description;
    this.disabled = disabled;
  }
  
  public long getBmId() {
    return bmId;
  }
  public long getDeviceId() {
    return deviceId;
  }
  public String getClazz() {
    return clazz;
  }
  public String getName() {
    return name;
  }
  public String getDescription() {
    return description;
  }
  public boolean isDisabled() {
    return disabled;
  }
}
