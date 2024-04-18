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

package fi.vtt.noen.mfw.bundle.probe.plugins.measurement;

import fi.vtt.noen.mfw.bundle.blackboard.Blackboard;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.MeasurementReport;
import fi.vtt.noen.mfw.bundle.probe.shared.MeasurementRequest;
import fi.vtt.noen.mfw.bundle.probe.shared.MeasurementResponse;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEvent;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

import java.util.Map;

/**
 * @author Teemu Kanstren
 */
public class MeasurementTask implements Runnable {
  private final static Logger log = new Logger(MeasurementProvider.class);
  private final Probe probe;
  private final ServerAgent server;
  private final Long subscriptionId;
  private final Blackboard bb;
  private long startTime;
  private boolean running = false;
  private boolean compareMode = false;
  private String reference;

  public MeasurementTask(MeasurementRequest req, Blackboard bb) {
    //actual probe instance is saved with the request when it is created when an xmlrpc request was received
    this.probe = req.getProbe();
    this.server = req.getServer();
    this.subscriptionId = req.getSubscriptionId();
    this.bb = bb;
    this.compareMode = isCompareMode();
  }

  public void run() {
    log.debug("Calling measure on:" + probe);
    startTime = System.currentTimeMillis();
    running = true;
    BaseMeasure measure = null;
    try {
      measure = probe.measure();
    } catch (Exception e) {
      log.error("Error while performing measurement on probe "+probe.getInformation().getMeasureURI(), e);
    }
    running = false;
    log.debug("Received measure:" + measure + " from:"+probe);
    int precision = probe.getInformation().getPrecision();
    
    if (measure == null || measure.getMeasure() == null) {
      ProbeEvent event = new ProbeEvent(server, EventType.NO_VALUE_FOR_BM, probe.getInformation().getMeasureURI(), "No valid measurement value available.", subscriptionId);
      bb.process(event);
      return;
    }
    
    //if compare mode is used current measure value needs to be compared with reference  
    if (compareMode) {
      log.debug("probe in compare mode");
      //log.debug("mode:"+probe.getConfigurationParameters().iterator().next().getValue());
      boolean matchReference = false;
      if (reference == null) {
        this.reference = measure.getMeasure();
      } 
      if (reference.equals(measure.getMeasure())) {
        matchReference = true;
      }
      MeasurementReport report = new MeasurementReport(measure, server, probe.getInformation(), subscriptionId, matchReference, reference);
      bb.process(report);
      MeasurementResponse resp = new MeasurementResponse(new BaseMeasure(""+matchReference), server, probe.getInformation(), precision, subscriptionId);
      bb.process(resp);    } 
    else {
      MeasurementResponse resp = new MeasurementResponse(measure, server, probe.getInformation(), precision, subscriptionId);
      bb.process(resp);
    }
    
  }

  public ProbeInformation getProbeInfo() {
    return probe.getInformation();
  }

  public Long getSubscriptionId() {
    return subscriptionId;
  }

  public long getRunningTime() {
    log.debug("Running:"+running);
    if (!running) {
      return 0;
    }
    long now = System.currentTimeMillis();
    return now-startTime;
  }

  public long getStartTime() {
    return startTime;
  }

  public boolean isRunning() {
    return running;
  }
  
  public Probe getProbe() {
    return probe;
  }
  
  public synchronized void setReference(String reference) {
    log.debug("setReference");
    this.reference = reference;
  }
  
  public synchronized void setCompare(boolean compare) {
    log.debug("setCompare");
    this.compareMode = compare;
  }
  
  private boolean isCompareMode() {
    if (probe.getConfigurationParameters() != null) {
      for (ProbeConfiguration param: probe.getConfigurationParameters()) {
        if (param.getName().equals("mode") && param.getValue().equals("compare")) {
          return true;
        }
      }
    }
    return false;
  }
}
