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

import fi.vtt.noen.mfw.bundle.common.Logger;

import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.Availability;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.BM;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.Device;
//import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.OperationResult;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.Probe;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

//import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
//import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;


public class AvailabilityProvider implements Runnable {
  private final static Logger log = new Logger(AvailabilityProvider.class);
  private ScheduledExecutorService executor;
  //private SACPlugin sacPlugin;
  //private boolean availabilityChanged;
  private Availability availability;
  private Map<Long, SAC> sacs = new HashMap<Long, SAC>();
  private long mfwId = 1;
  
  public AvailabilityProvider(SACPlugin sacPlugin, int availabilityInterval, long mfwId) {
    //this.sacPlugin = sacPlugin;
    executor = new ScheduledThreadPoolExecutor(1, new AvailabilityThreadFactory());
    executor.scheduleWithFixedDelay(this, 5000, availabilityInterval, TimeUnit.MILLISECONDS);
    log.debug("Started availability provider with interval "+availabilityInterval+"ms");
    availability = new Availability();
    this.mfwId = mfwId;
  }
  
/*  
  public synchronized void setAvailabilityChanged() {
    this.availabilityChanged = true;
  }
*/  
  
  public synchronized void probeRegistered(ProbeRegistered pr) {
    ProbeDescription probe = pr.getProbeDescription();
    if (pr.isNewTarget()) {
      createAndAddDevice(probe.getTarget(), availability.getDevice(), false);
    }    
    if(pr.isNewBM()) {
      createAndAddBM(probe.getBm(), availability.getBM(), false);
    }
    createAndAddProbe(probe, availability.getProbe(), false);
  }
  
  public synchronized void probeDisabled(ProbeDisabled pd) {
    ProbeDescription probe = pd.getProbeDescription();    
    if (pd.isTargetDisabled()) {
      createAndAddDevice(probe.getTarget(), availability.getDevice(), true);
    }    
    if(pd.isBmDisabled()) {
      createAndAddBM(probe.getBm(), availability.getBM(), true);
    }
    createAndAddProbe(probe, availability.getProbe(), true);
   
  }
  
  private void createAndAddDevice(TargetDescription target, Collection<Device> devices, boolean disabled) {
    //create and add device only if it does not exist. if device exists with different disable value it is removed (no need to report availability true and false in the same message). 
    Iterator<Device> iterator = devices.iterator();
    while (iterator.hasNext()) {
      Device device = iterator.next(); 
      if (device.getId() == target.getTargetId()) {
        if (device.isDisabled() != disabled) {
          iterator.remove();
        }
        return;
      } 
    } 
    Device device = new Device();
    device.setId(target.getTargetId());
    device.setName(target.getTargetName());
    device.setType(target.getTargetType());
    device.setDisabled(disabled);
    devices.add(device);
  }

  private void createAndAddBM(BMDescription bmDescription, Collection<BM> bms, boolean disabled) {
    //create and add bm only if it does not exist. if bm exists with different disable value it is removed (no need to report availability true and false in the same message). 
    Iterator<BM> iterator = bms.iterator();
    while (iterator.hasNext()) {
      BM bm = iterator.next(); 
      if (bm.getId() == bmDescription.getBmId()) {
        if (bm.isDisabled() != disabled) {
          iterator.remove();
        } 
        return;
      }
    }
    BM bm = new BM();
    bm.setClazz(bmDescription.getBmClass());
    bm.setDescription(bmDescription.getBmDescription());
    bm.setId(bmDescription.getBmId());
    bm.setName(bmDescription.getBmName());
    bm.setDisabled(disabled);
    bm.getDeviceId().add(bmDescription.getTarget().getTargetId());
    bms.add(bm);
  }

  private void createAndAddProbe(ProbeDescription pd, Collection<Probe> probes, boolean disabled) {
    //create and add probe only if it does not exist. if probe exists with different disable value it is removed (no need to report availability true and false in the same message).
    Iterator<Probe> iterator = probes.iterator();
    while (iterator.hasNext()) {
      Probe probe = iterator.next(); 
      if (probe.getId() == pd.getProbeId()) {
        if (probe.isDisabled() != disabled) {
          iterator.remove();
        }
        return;
      } 
    }
    Probe probe = new Probe();
    probe.setId(pd.getProbeId());
    probe.setName(pd.getProbeName());
    probe.setDisabled(disabled);
    probe.getBmId().add(pd.getBm().getBmId());
    probes.add(probe);
  }
  
/*  
  private Availability getAvailability() {
    Availability availability = new Availability();
    availability.setMfwId(1);          
    Collection<TargetDescription> devices = sacPlugin.getTargetList();
    if (devices != null) {
      Iterator<TargetDescription> iterator = devices.iterator();
      while (iterator.hasNext()) {
        TargetDescription target = iterator.next();
        Device device = new Device();
        device.setDisabled(false);
        device.setId(target.getTargetId());
        device.setName(target.getTargetName());
        device.setType(target.getTargetType());
        availability.getDevice().add(device);
      }
    }          
    List<BMDescription> availableBMs = sacPlugin.getAvailableBMList();
    if(availableBMs != null) {
      Iterator<BMDescription> iterator = availableBMs.iterator();
      while (iterator.hasNext()) {
        BMDescription bmDesc = iterator.next(); 
        BM bm = new BM();
        bm.setDisabled(false);
        bm.setDescription(bmDesc.getBmDescription());             
        bm.setName(bmDesc.getBmName());
        bm.setClazz(bmDesc.getBmClass());
        bm.setId(bmDesc.getBmId());
        TargetDescription target = bmDesc.getTarget();
        long deviceId = target.getTargetId();
        if (deviceId > 0) {
          bm.getDeviceId().add(deviceId); 
        }
        availability.getBM().add(bm);
      } 
    }
    List<ProbeDescription> probes = sacPlugin.getProbeList();
    if(probes != null) {
      Iterator<ProbeDescription> iterator = probes.iterator();
      while (iterator.hasNext()) {
        ProbeDescription probeDesc = iterator.next();
        Probe probe = new Probe();
        probe.setDisabled(false);
        probe.setName(probeDesc.getProbeName());
        probe.setId(probeDesc.getProbeId());
        long bmId = probeDesc.getBm().getBmId();
        if (bmId > 0) {
          probe.getBmId().add(bmId);
        }
        availability.getProbe().add(probe);
      }
    }
    return availability;
  }
*/
  
  private void setAvailability(Availability availability) {
    if (sacs.isEmpty()) {      
      log.error("No SAC registered, not reporting availability change");
      return;
    }
    for (SAC sac : sacs.values()) {
      sac.setAvailability(availability);
    }
  }
  
  public synchronized void registerSAC(long sacId, SAC sac) {
    //log.debug("Registering SAC (ID:" +sacId+ ")");
    sacs.put(sacId, sac);
  }
  
  public void run() {
    //log.debug("Availability provider running");
    
    synchronized(this) {
      //if (availabilityChanged) {
      if (!(availability.getProbe().isEmpty() && availability.getBM().isEmpty() && availability.getDevice().isEmpty())) {
        log.debug("Availability changed");
        
        //sacPlugin.setAvailability(getAvailability());
        availability.setMfwId(mfwId);
        //sacPlugin.setAvailability(availability);
        setAvailability(availability);
        
        //availabilityChanged = false;
        availability = new Availability();
      }
    }
  }

  public void stop() {
    executor.shutdown();    
  }
}
