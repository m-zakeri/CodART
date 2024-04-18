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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage;

import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

/**
 * @author Teemu Kanstren
 */
public class BMListItem {
  private final BMDescription bm;
  private final String value;

  public BMListItem(BMDescription bm, String value) {
    this.bm = bm;
    if (value != null && value.length() > 102) {
      value = value.substring(0, 100);
    }
    this.value = value;
  }

  public long getBmId() {
    return bm.getBmId();
  }

  public TargetDescription getTarget() {
    return bm.getTarget();
  }

  public String getBmClass() {
    return bm.getBmClass();
  }

  public String getBmName() {
    return bm.getBmName();
  }

  public String getBmDescription() {
    return bm.getBmDescription();
  }

  public String getMeasureURI() {
    return bm.getMeasureURI();
  }

  public String getValue() {
    return value;
  }
}
