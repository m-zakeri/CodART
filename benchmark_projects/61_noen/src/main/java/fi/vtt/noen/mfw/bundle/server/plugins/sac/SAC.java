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

package fi.vtt.noen.mfw.bundle.server.plugins.sac;

import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.Availability;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

/**
 * An interface to link the MFW server to the BUGYO Beyond cockpit.
 *
 * @author Teemu Kanstren
 */
public interface SAC {
  public void event(String message);

  public void bmResult(Value value);

  //public void probeRegistered(ProbeDescription probe);
  public void probeRegistered(ProbeRegistered pr);
  
  //public void probeDisabled(ProbeDescription probe);
  public void probeDisabled(ProbeDisabled pd);

  public boolean initAvailability();
  
  public void setAvailability(Availability availability);
}
