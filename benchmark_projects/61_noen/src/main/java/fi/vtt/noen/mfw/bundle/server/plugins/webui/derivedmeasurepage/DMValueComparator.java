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

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMValue;

import java.util.Comparator;

/**
 * @author Teemu Kanstr�n
 */
public class DMValueComparator implements Comparator<DMValue> {
  private final String sortKey;
  private final boolean ascending;

  public DMValueComparator(String sortKey, boolean ascending) {
    this.sortKey = sortKey;
    this.ascending = ascending;
  }

  public int compare(DMValue a1, DMValue a2) {
    int result = 0;
    if (sortKey.equals("id")) {
      result = a1.getId() - a2.getId();
    }
    if (sortKey.equals("name")) {
      result = a1.getName().compareTo(a2.getName());
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
