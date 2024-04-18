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

import javax.xml.datatype.XMLGregorianCalendar;

public class BMResult {
  private final long bm_id;
  private final long device_id;
  private final String value;
  private final XMLGregorianCalendar time;
  private final boolean error;
  
  public BMResult(long bmId, long deviceId, String value,
      XMLGregorianCalendar time, boolean error) {
    super();
    this.bm_id = bmId;
    this.device_id = deviceId;
    this.value = value;
    this.time = time;
    this.error = error;
  }

  public long getBm_id() {
    return bm_id;
  }

  public long getDevice_id() {
    return device_id;
  }

  public String getValue() {
    return value;
  }

  public XMLGregorianCalendar getTime() {
    return time;
  }

  public boolean isError() {
    return error;
  }
}
