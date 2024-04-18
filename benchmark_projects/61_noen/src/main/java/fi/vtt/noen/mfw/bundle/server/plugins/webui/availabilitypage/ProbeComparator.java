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

public class ProbeComparator implements Comparator<ProbeDesc> {
  private final String sortKey;
  private final boolean ascending;

  public ProbeComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(ProbeDesc a1, ProbeDesc a2) {
    int result = 0;
    if (sortKey.equals("probeId")) {
      result = (int)(a1.getProbeId()-a2.getProbeId());
    }
    if (sortKey.equals("bmId")) {
      result = (int)(a1.getBmId()-a2.getBmId());
    }
    if (sortKey.equals("name")) {
      result = a1.getName().compareTo(a2.getName());
    }    
    if (!ascending) {
      result = 0 - result;
    }
    return result;
  }
}
