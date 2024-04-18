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

public class BMComparator implements Comparator<BMDesc> {
  private final String sortKey;
  private final boolean ascending;

  public BMComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(BMDesc a1, BMDesc a2) {
    int result = 0;
    if (sortKey.equals("bmId")) {
      result = (int)(a1.getBmId()-a2.getBmId());
    }
    if (sortKey.equals("deviceId")) {
      result = (int)(a1.getDeviceId()-a2.getDeviceId());
    }
    if (sortKey.equals("clazz")) {
      result = a1.getClazz().compareTo(a2.getClazz());
    }
    if (sortKey.equals("name")) {
      result = a1.getName().compareTo(a2.getName());
    }
    if (sortKey.equals("description")) {
      result = a1.getDescription().compareTo(a2.getDescription());
    }
    if (!ascending) {
      result = 0 - result;
    }
    return result;
  }
}
