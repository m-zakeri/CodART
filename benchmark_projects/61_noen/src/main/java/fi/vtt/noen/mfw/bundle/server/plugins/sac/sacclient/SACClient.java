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

package fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.SAC;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.SACPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.BMResults.PerDevice;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

import javax.xml.datatype.DatatypeFactory;
import javax.xml.datatype.XMLGregorianCalendar;
import javax.xml.namespace.QName;
import java.net.URL;
import java.util.Collection;
import java.util.GregorianCalendar;
import java.util.Iterator;
import java.util.List;

public class SACClient implements SAC {
  private final static Logger log = new Logger(SACClient.class);
  private static final QName SERVICE_NAME = new QName("http://www.bugyobeyond.org/MFW_SAC/", "MFW_SAC_service");
  private URL wsdlURL;
  private MFWSACService ss;
  private MFWSAC port;
  private long SACId;
  private SACPlugin sacPlugin;
  private String sacURL;
  private long mfwId = 1;

  public SACClient(SACPlugin sacPlugin, String sacURL, long sacId, long mfwId) {
    wsdlURL = MFWSACService.WSDL_LOCATION;
    ss = new MFWSACService(wsdlURL, SERVICE_NAME);
    this.sacURL = sacURL;
    port = ss.getMFWSAC(sacURL);
    this.SACId = sacId;
    this.sacPlugin = sacPlugin;
    this.mfwId = mfwId;
  }

  public void event(String message) {
    // its not possible to send events to sac anymore...

  }

  public void bmResult(Value value) {
    try {
      log.info("Invoking setBMResults on the SAC (ID:"+SACId+")");
      BMResults bmResults = new BMResults();
      bmResults.setMfwId(mfwId);
      BMResult bmResult = new BMResult();
      bmResult.setId(value.getBm().getBmId());
      bmResult.setValue(value.getString());
      bmResult.setError(value.isError());

      GregorianCalendar calendar = new GregorianCalendar();
      calendar.setTime(value.getTime());
      DatatypeFactory factory = DatatypeFactory.newInstance();
      XMLGregorianCalendar XMLCalendar = factory.newXMLGregorianCalendar(calendar);
      bmResult.setTimeStamp(XMLCalendar);

      PerDevice perDevice = new PerDevice();
      perDevice.getBMResult().add(bmResult);
      perDevice.setDeviceId(value.getBm().getTarget().getTargetId());
      bmResults.getPerDevice().add(perDevice);

      OperationResult result = port.setBMResults(bmResults);
      if (result.isError()) {
        log.debug("Error invoking setBMResults on the SAC (ID:"+SACId+")");
      }

    } catch (Exception e) {
      log.error("Error invoking setBMResults on the SAC (ID:"+SACId+")", e);
      return;
    }
  }

  public void probeRegistered(ProbeRegistered pr) {
    log.info("Probe Registered: Invoking setAvailability on the SAC (ID:"+SACId+")");
    Availability availability = new Availability();
    availability.setMfwId(mfwId);
/*    
    //this is "fixed" to send complete availability information every time something has changed
    Collection<TargetDescription> devices = sacPlugin.getTargetList();
    if (devices != null) {
      for (TargetDescription target : devices) {
        createAndAddDevice(target, availability.getDevice(), false);
      }
    }
    List<BMDescription> availableBMs = sacPlugin.getAvailableBMList();
    if (availableBMs != null) {
      for (BMDescription bmDesc : availableBMs) {
        createAndAddBM(bmDesc, availability.getBM(), false);
      }
    }
    List<ProbeDescription> probes = sacPlugin.getProbeList();
    if (probes != null) {
      for (ProbeDescription probeDesc : probes) {
        createAndAddProbe(probeDesc, availability.getProbe(), false);
      }
    }
*/
    //todo: one probe becoming disabled does not mean all bm and targets related should be disabled. add tests for this
    
    ProbeDescription probe = pr.getProbeDescription();
    if (pr.isNewTarget()) {
      createAndAddDevice(probe.getTarget(), availability.getDevice(), false);
    }    
    if(pr.isNewBM()) {
      createAndAddBM(probe.getBm(), availability.getBM(), false);
    }
    createAndAddProbe(probe, availability.getProbe(), false);

    OperationResult result = null;
    try {
      result = port.setAvailability(availability);
    } catch (Exception e) {
      //ignore until better mechanism in place
      log.error("Error invoking setAvailability on the SAC (ID:"+SACId+")", e);
      //return is needed to avoid nullpointer after this try-catch
      return;
    }
    if (result.isError()) {
      //todo: create event
      log.debug("Error invoking setAvailability on the SAC (ID:"+SACId+")");
    }
  }
  
  public void probeDisabled(ProbeDisabled pd) {
    log.info("Probe Disabled: Invoking setAvailability on the SAC (ID:"+SACId+")");
    Availability availability = new Availability();
    availability.setMfwId(mfwId);
/*    
    //this is "fixed" to send complete availability information every time something has changed
    Collection<TargetDescription> devices = sacPlugin.getTargetList();
    if (devices != null) {
      for (TargetDescription target : devices) {
        createAndAddDevice(target, availability.getDevice(), false);
      }
    }
    List<BMDescription> availableBMs = sacPlugin.getAvailableBMList();
    if (availableBMs != null) {
      for (BMDescription bmDesc : availableBMs) {
        createAndAddBM(bmDesc, availability.getBM(), false);
      }
    }
    List<ProbeDescription> probes = sacPlugin.getProbeList();
    if (probes != null) {
      for (ProbeDescription probeDesc : probes) {
        createAndAddProbe(probeDesc, availability.getProbe(), false);
      }
    }
*/
    //todo: one probe becoming disabled does not mean all bm and targets related should be disabled. add tests for this
    
    ProbeDescription probe = pd.getProbeDescription();
    if (pd.isTargetDisabled()) {
      createAndAddDevice(probe.getTarget(), availability.getDevice(), true);
    }    
    if(pd.isBmDisabled()) {
      createAndAddBM(probe.getBm(), availability.getBM(), true);
    }
    createAndAddProbe(probe, availability.getProbe(), true);

    OperationResult result = null;
    try {
      result = port.setAvailability(availability);
    } catch (Exception e) {
      //todo:fix the class to create some sensible connection mechanism
      log.error("Error invoking setAvailability on the SAC (ID:"+SACId+")", e);
      //return is needed to avoid nullpointer after this try-catch
      return;
    }
    if (result.isError()) {
      //todo: create event
      log.debug("Error invoking setAvailability on the SAC (ID:"+SACId+")");
    }
  }

  private void createAndAddDevice(TargetDescription target, Collection<Device> devices, boolean disabled) {
    Device device = new Device();
    device.setId(target.getTargetId());
    device.setName(target.getTargetName());
    device.setType(target.getTargetType());
    device.setDisabled(disabled);
    devices.add(device);
  }

  private void createAndAddBM(BMDescription bmDescription, Collection<BM> bms, boolean disabled) {
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
    Probe probe = new Probe();
    probe.setId(pd.getProbeId());
    probe.setName(pd.getProbeName());
    probe.setDisabled(disabled);
    probe.getBmId().add(pd.getBm().getBmId());
    probes.add(probe);
  }

  public long getSAC(long MFWId) {
    GetSAC getSAC = new GetSAC();
    getSAC.setMfwId(MFWId);
    fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.SAC SACInfo = null;
    try {
      SACInfo = port.getSAC(getSAC);
    } catch (Exception e) {
      log.error("Error invoking getSAC on the SAC (ID:"+SACId+")", e);
      e.printStackTrace();
      return -1;
    }
    if (SACInfo != null) {
      return SACInfo.getId();
    } else {
      log.debug("Error invoking getSAC on the SAC. SACInfo null");
      return -1;
    }
  }
  
  public void setAvailability(Availability availability) {
    log.info("Invoking setAvailability on the SAC (ID:"+SACId+")");
    OperationResult result = null;
    try {
      result = port.setAvailability(availability);
    } catch (Exception e) {
      log.error("Error invoking setAvailability on the SAC (ID:"+SACId+")", e);
      return;
    }
    if (!result.isError()) {
    } else {
      log.debug("Error invoking setAvailability on the SAC (ID:"+SACId+")");
    }
  }

  public boolean initAvailability() {
    log.info("Initializing and invoking setAvailability on the SAC (ID:"+SACId+")");
    Availability availability = new Availability();
    availability.setMfwId(mfwId);
    Collection<TargetDescription> devices = sacPlugin.getTargetList();
    if (devices != null) {
      for (TargetDescription target : devices) {
        createAndAddDevice(target, availability.getDevice(), false);
      }
    }
    List<BMDescription> availableBMs = sacPlugin.getAvailableBMList();
    if (availableBMs != null) {
      for (BMDescription bmDesc : availableBMs) {
        createAndAddBM(bmDesc, availability.getBM(), false);
      }
    }
    List<ProbeDescription> probes = sacPlugin.getProbeList();
    if (probes != null) {
      for (ProbeDescription probeDesc : probes) {
        createAndAddProbe(probeDesc, availability.getProbe(), false);
      }
    }
    OperationResult result = null;
    try {
      result = port.setAvailability(availability);
    } catch (Exception e) {
      //log.error("Error invoking setAvailability on the SAC", e);
      return false;
    }
    if (!result.isError()) {
      return true;
    } else {
      log.debug("Error invoking setAvailability on the SAC");
      return false;
    }
  }
}
