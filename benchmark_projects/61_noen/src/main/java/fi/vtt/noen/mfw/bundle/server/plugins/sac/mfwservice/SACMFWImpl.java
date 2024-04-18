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

package fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.SACPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

import javax.xml.datatype.DatatypeFactory;
import javax.xml.datatype.XMLGregorianCalendar;
import java.util.Collection;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;


@javax.jws.WebService(
                      serviceName = "SAC_MFW_service",
                      portName = "SAC_MFW",
                      targetNamespace = "http://www.bugyobeyond.org/SAC_MFW/",
                      wsdlLocation = "SAC_MFW_proposal_v2.4.wsdl",
                      endpointInterface = "fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW")
                      
public class SACMFWImpl implements SACMFW {
  private final static Logger log = new Logger(SACMFWImpl.class);
  private SACPlugin sac;
  private long mfwId = 1;
  
  public SACMFWImpl(SACPlugin sac, long mfwId) {
    this.sac = sac;
    this.mfwId = mfwId;
  }

  /* (non-Javadoc)
   * @see fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW#getProbeParameters(fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.ProbeParametersRequest  parameters )*
   */
  public ProbeParameters getProbeParameters(ProbeParametersRequest parameters) { 
    ProbeParameters probeParams = new ProbeParameters();
//    try {          
    long sacId = parameters.getSacId();
    log.info("Executing operation getProbeParameters (SACId:"+sacId+")");
    if (sac.sacRegistered(sacId)) {
      try {
        long probeId = parameters.getProbeId();
        log.debug("ProbeId: " +probeId);            
        Collection<ProbeConfiguration> configuration = sac.getProbeConfigurationParameters(probeId);
        if (configuration != null) {
          Iterator<ProbeConfiguration> iterator = configuration.iterator();
          while (iterator.hasNext()) {
            ProbeConfiguration configParams = (ProbeConfiguration) iterator.next();
            ProbeParameter param = new ProbeParameter(); 
            if (configParams.getName() != null) {
              param.setName(configParams.getName());
            } else {
              param.setName("");
            }
            if (configParams.getDescription() != null) {
              param.setDescription(configParams.getDescription());
            } else {
              param.setDescription("");
            }
            if (configParams.getValue() != null) {
              param.setValue(configParams.getValue());
            } else {
              param.setValue("");
            }
            param.setMandatory(configParams.isMandatory());
            probeParams.getProbeParameter().add(param);
          }
        }
      } catch (Exception ex) {
        log.error("Failed to get probe parameters", ex);
        throw new RuntimeException("Failed to get probe parameters");
      }
/*
        else {
          // fixed values for testing
          ProbeParameter param = new ProbeParameter();
          param.setName("name");
          param.setValue("value"); 
          param.setDescription("description");
          param.setMandatory(false);
          probeParams.getProbeParameter().add(param);
        }
*/
      } else {
        log.debug("Failed to get probe parameters, SAC (ID:" +sacId+ ") not registered");
        throw new RuntimeException("Failed to get probe parameters, SAC not registered");
      }
      return probeParams;
        
/*    } catch (Exception ex) {
      log.error("Failed to get probe parameters", ex);
      //return probeParams;
      throw new RuntimeException("Failed to get probe parameters");
    }*/
  }

  /* (non-Javadoc)
   * @see fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW#setProbeParameters(fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.ProbeParameterValues  parameters )*
   */
  public OperationResult setProbeParameters(ProbeParameterValues parameters) {  
    OperationResult result = new OperationResult();
    try {
      long sacId = parameters.getSacId();
      log.info("Executing operation setProbeParameters (SACId:"+sacId+")");
      if (sac.sacRegistered(sacId)) {
        long probeId = parameters.getProbeId();
        log.debug("ProbeId: " +probeId);
        ProbeParameterValue probeParam;
        boolean configSuccess;         
        Map<String, String> map = new HashMap<String, String>();
        Iterator<ProbeParameterValue> iterator = parameters.getProbeParameterValue().iterator();
        while (iterator.hasNext()) {
          probeParam = iterator.next();
          map.put(probeParam.getName(), probeParam.getValue());
          configSuccess = sac.setProbeConfiguration(probeId, map);
          if (configSuccess) {
            result.setError(false);
          } else {
            result.setError(true);
          }
        }
      } else {
        log.debug("Failed to set probe parameters, SAC (ID:" +sacId+ ") not registered");
        result.setError(true);
      }
      return result;
        
    } catch (Exception ex) {
      log.error("Failed to set probe parameters", ex);
      result.setError(true);
      return result;
      //throw new RuntimeException(ex);
    }
  }

  /* (non-Javadoc)
   * @see fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW#getAvailability(fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.GetAvailability  parameters )*
   */
  public Availability getAvailability(GetAvailability parameters) {  
    Availability availability = new Availability();
//    try {
    long sacId = parameters.getSacId();
    log.info("Executing operation getAvailability (SACId:"+sacId+")");
    boolean sacRegistered = sac.register(sacId);
    if (sacRegistered) {
      try {
        availability.setMfwId(mfwId);
        Collection<TargetDescription> devices = sac.getTargetList();
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
        List<BMDescription> availableBMs = sac.getAvailableBMList();
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
        List<ProbeDescription> probes = sac.getProbeList();
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
      } 
      catch (Exception ex) {
        log.error("Failed to get availability information", ex);
        throw new RuntimeException("Failed to get availability information");
      }
    } else {
      log.debug("Failed to get availability information, SAC (ID:" +sacId+ ") not registered");
      throw new RuntimeException("Failed to get availability information, SAC not registered");      
    }
    return availability;
        
/*    } catch (Exception ex) {
      log.error("Failed to get availability information", ex);
      throw new RuntimeException("Failed to get availability information");
    }*/
  }

  /* (non-Javadoc)
   * @see fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW#getBMResults(fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.BMResultsRequest  parameters )*
   */
  public OperationResult getBMResults(BMResultsRequest parameters) { 
    OperationResult result = new OperationResult();
    try {
      long sacId = parameters.getSacId();
      log.info("Executing operation getBMResults (SACId:"+sacId+")");
      if (sac.sacRegistered(sacId)) {
        List<BMResultRequest> bmResultRequests = parameters.getBMResultRequest();
        if(bmResultRequests != null) {
          Iterator<BMResultRequest> requestIterator = bmResultRequests.iterator();
          while (requestIterator.hasNext()) {
            BMResultRequest bmRequest = requestIterator.next();
            long bmId = bmRequest.getId();
            long frequency = bmRequest.getFrequency();
            if (frequency > 0) { 
              // request continuous measurements
              // bmId is unique so there is no need for deviceId
              sac.subscribeToBM(sacId, bmId, frequency);
              result.setError(false);
              
            } else if (frequency == 0){ 
              // request bm once                   
              // bmId is unique so there is no need for deviceId
              boolean ok = sac.requestBM(sacId, bmId);
              if (ok) {
                result.setError(false);
              } else {
                result.setError(true);
              }                            
            } 
            else {
              // stop measurement 
              sac.unSubscribeToBM(sacId, bmId);
              result.setError(false);
            }               
          }
        }               
      } else {
        log.debug("Failed to get BM results, SAC (ID:" +sacId+ ") not registered");
        result.setError(true);
      }
      return result;
      
    } catch (Exception ex) {
      log.error("Failed to get BM results", ex);
      result.setError(true);
      return result;
      //throw new RuntimeException(ex);
    }
  }

  /* (non-Javadoc)
   * @see fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFW#getMFW(fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.GetMFW  parameters )*
   */
  public MFW getMFW(GetMFW parameters) { 
    MFW mfw = new MFW();
    try { 
      long sacId = parameters.getSacId();
      log.info("Executing operation getMFW (SACId:"+sacId+")");
      boolean sacRegistered = sac.register(sacId);
//      if (sacRegistered) { 
        // some values for testing
        mfw.setId(1);
        mfw.setVersion("version");
        mfw.setIfs("ifs");
        mfw.setCompany("company");
        
        // this should give current time
        GregorianCalendar calendar = new GregorianCalendar();
        DatatypeFactory factory = DatatypeFactory.newInstance();
        XMLGregorianCalendar XMLCalendar = factory.newXMLGregorianCalendar(calendar);
        mfw.setTime(XMLCalendar);
/*      } else {
        log.debug("SAC (ID:" +sacId+ ") not registered");
      }*/
      return mfw;
        
    } catch (Exception ex) {
      log.error("Failed to get MFW information", ex);
      throw new RuntimeException("Failed to get MFW information");
    }
  }

}
