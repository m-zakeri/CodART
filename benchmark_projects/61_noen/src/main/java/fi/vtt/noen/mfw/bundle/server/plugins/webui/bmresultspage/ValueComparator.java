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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmresultspage;

//import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

import java.util.Comparator;

/**
 * @author Teemu Kanstr�n
 */
public class ValueComparator implements Comparator<BMResult> {
  private final String sortKey;
  private final boolean ascending;

  public ValueComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(BMResult result1, BMResult result2) {
    int result = 0;
    if (sortKey.equals("bm_id")) {
      result = (int) (result1.getBm_id()- result2.getBm_id());
    }
    if (sortKey.equals("device_id")) {
      result = (int) (result1.getDevice_id() - result2.getDevice_id());
    }
    if (sortKey.equals("value")) {
      result = result1.getValue().compareTo(result2.getValue());
    }
    if (sortKey.equals("time")) {
      result = result1.getTime().compare(result2.getTime());
    }
    if (!ascending) {
      result = 0 - result;
    }
    return result;
  }

}