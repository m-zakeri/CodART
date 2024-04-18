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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage;

import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage.BMListItem;

import java.util.Comparator;

/**
 * @author Teemu Kanstren
 */
public class BMComparator implements Comparator<BMListItem> {
  private final String sortKey;
  private final boolean ascending;

  public BMComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(BMListItem a1, BMListItem a2) {
    int result = 0;
    if (sortKey.equals("bmId")) {
      result = (int)(a1.getBmId() - a2.getBmId());
    }
    if (sortKey.equals("measureURI")) {
      result = a1.getMeasureURI().compareTo(a2.getMeasureURI());
    }
    if (sortKey.equals("bmDescription")) {
      result = a1.getBmDescription().compareTo(a2.getBmDescription());
    }
    if (sortKey.equals("value")) {
      result = a1.getValue().compareTo(a2.getValue());
    }
    if (!ascending) {
      result = 0 - result;
    }
    return result;
  }
}
