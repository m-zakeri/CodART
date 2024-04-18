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

import java.util.Comparator;

public class DeviceComparator implements Comparator<DeviceDesc> {
  private final String sortKey;
  private final boolean ascending;

  public DeviceComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(DeviceDesc a1, DeviceDesc a2) {
    int result = 0;
    if (sortKey.equals("deviceId")) {
      result = (int)(a1.getDeviceId()-a2.getDeviceId());
    }    
    if (sortKey.equals("name")) {
      result = a1.getName().compareTo(a2.getName());
    }
    if (sortKey.equals("type")) {
      result = a1.getType().compareTo(a2.getType());
    }
    if (!ascending) {
      result = 0 - result;
    }
    return result;
  }
}