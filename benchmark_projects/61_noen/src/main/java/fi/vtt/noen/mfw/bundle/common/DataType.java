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

package fi.vtt.noen.mfw.bundle.common;

/**
 * Types of information (events, commands, measurement data, ...) that the MFW handles.
 *
 * @author Teemu Kanstren
 */
public enum DataType {
  STRINGVALUE,
  SERVER_EVENT,
  PROBE_EVENT,
  DM_DEFINITION,
  DM_VALUE,
  UPDATE,
  BM_REPORT,
  //used by probe-adapter
  MEASUREMENT_REQUEST,
  MEASUREMENT_RESPONSE,
  PROBE_REGISTERED,
  PROBE_DISABLED,
  UNSUBSCRIPTION_REQUEST,
  MEASUREMENT_REPORT
}
