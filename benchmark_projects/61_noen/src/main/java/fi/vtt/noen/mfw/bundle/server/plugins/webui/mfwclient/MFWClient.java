
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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient;


import fi.vtt.noen.mfw.bundle.common.Logger;

import javax.xml.namespace.QName;
import java.net.URL;


public final class MFWClient {
    private final static Logger log = new Logger(MFWClient.class);
    private static final QName SERVICE_NAME = new QName("http://www.bugyobeyond.org/SAC_MFW/", "SAC_MFW_service");
    private URL wsdlURL;
    private SACMFWService ss;
    private SACMFW port;
    private final long sacId;
    
    public MFWClient(String mfwURL, long sacId) {
      wsdlURL = SACMFWService.WSDL_LOCATION;
      ss = new SACMFWService(wsdlURL, SERVICE_NAME);
      port = ss.getSACMFW(mfwURL);
      this.sacId = sacId;
    }
        
    public MFW getMFW() {
      try {
        log.debug("Invoking getMFW web service");
        GetMFW getMFW = new GetMFW();
        getMFW.setSacId(sacId);
        MFW mfwInfo = port.getMFW(getMFW);
        return mfwInfo;
        
      }catch (Exception e) {
        e.printStackTrace();
        return null;
      }
    }
    
    public boolean requestBM(long bmId, long deviceId) {
      try {
        log.debug("Invoking getBMResults web service");
        BMResultsRequest request = new BMResultsRequest();
        request.setSacId(sacId);
        BMResultRequest req = new BMResultRequest();
        req.setFrequency(0);
        req.setId(bmId);
        req.getDeviceId().add(deviceId);
        request.getBMResultRequest().add(req);
        OperationResult result = port.getBMResults(request);
        if (result.isError()) {
          return false;
        }else {
          return true;
        }
      }catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }
    
    public boolean subscribeToBM(long bmId, long deviceId, long frequency) {
      try {
        log.debug("Invoking getBMResults web service");
        BMResultsRequest request = new BMResultsRequest();
        request.setSacId(sacId);
        BMResultRequest req = new BMResultRequest();
        req.setFrequency(frequency);
        req.setId(bmId);
        req.getDeviceId().add(deviceId);
        request.getBMResultRequest().add(req);
        OperationResult result = port.getBMResults(request);
        if (result.isError()) {
          return false;
        }else {
          return true;
        }
      }catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }
    
    public boolean unsubscribeToBM(long bmId, long deviceId) {
      try {
        log.debug("Invoking getBMResults web service");
        BMResultsRequest request = new BMResultsRequest();
        request.setSacId(sacId);
        BMResultRequest req = new BMResultRequest();
        req.setFrequency(-1);
        req.setId(bmId);
        req.getDeviceId().add(deviceId);
        request.getBMResultRequest().add(req);
        OperationResult result = port.getBMResults(request);
        if (result.isError()) {
          return false;
        }else {
          return true;
        }
      }catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }
    
    public ProbeParameters getProbeParamaters(long probeId) {
      log.debug("Invoking getProbeParameters web service");
      try {
        ProbeParametersRequest request = new ProbeParametersRequest();
        request.setSacId(sacId);
        request.setProbeId(probeId);
        ProbeParameters result = port.getProbeParameters(request);
        return result;
        
      }catch (Exception e) {
        e.printStackTrace();
        return null;
      }
    }

    public boolean setProbeParamaters(long probeId, String name, String value) {
      log.debug("Invoking setProbeParameters web service");
      try {       
        ProbeParameterValues request = new ProbeParameterValues();        
        request.setSacId(sacId);
        request.setProbeId(probeId);
        ProbeParameterValue paramValue = new ProbeParameterValue();
        paramValue.setName(name);
        paramValue.setValue(value);
        request.getProbeParameterValue().add(paramValue);
        OperationResult result = port.setProbeParameters(request);
        if (result.isError()) {
          return false;
        }else {
          return true;
        }
      }catch (Exception e) {
        e.printStackTrace();
        return false;
      }
    }
    
    public Availability getAvailability() {      
      try {
        log.debug("Invoking getAvailability web service");
        GetAvailability request = new GetAvailability();
        request.setSacId(sacId);
        Availability availability = null;
        try {
          availability = port.getAvailability(request);
        } catch (Exception e) { 
          log.debug("Failed to invoke getAvailability web service. Exception occured");
          e.printStackTrace();
        }  
        return availability;
        
      }catch (Exception e) {
        e.printStackTrace();
        return null;
      }
    }
    
}

