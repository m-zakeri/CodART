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

//import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class AvailabilityStorage {
  
  private final Vector<DeviceDesc> devices = new Vector<DeviceDesc>();
  private final Vector<BMDesc> bms = new Vector<BMDesc>();
  private final Vector<ProbeDesc> probes = new Vector<ProbeDesc>();
  
  public synchronized void addDevice(DeviceDesc device) {
    devices.add(device);
  }
  
  public synchronized void addBM(BMDesc bm) {
    bms.add(bm);
  }
  
  public synchronized void addProbe(ProbeDesc probe) {
    probes.add(probe);
  }

  public synchronized List<DeviceDesc> getDevices() {
    return devices;
  }

  public synchronized List<BMDesc> getBms() {
    return bms;
  }

  public synchronized List<ProbeDesc> getProbes() {
    return probes;
  }
  
}
