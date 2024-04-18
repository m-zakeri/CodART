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

package fi.vtt.noen.mfw.bundle.probe.plugins.communication;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.MeasurementReport;
import fi.vtt.noen.mfw.bundle.probe.shared.MeasurementResponse;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEvent;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.osgi.framework.BundleContext;

import java.util.Set;

/**
 * This plugin listens to measurements provided by the MeasurementProvider and sends them to the server-agent.
 *
 * @author Teemu Kanstren
 */
public class CommunicationPlugin extends BasePlugin {
  private final static Logger log = new Logger(CommunicationPlugin.class);

  public CommunicationPlugin(BundleContext bc) {
    super(bc, log);
  }

  public Set getCommands() {
    return createCommandSet(ProbeEvent.class, MeasurementResponse.class, MeasurementReport.class);
  }

  public void process(DataObject data) {
    if (data instanceof MeasurementResponse) {
      MeasurementResponse mr = (MeasurementResponse) data;
      processMeasurementResponse(mr);
      return;
    }
    if (data instanceof ProbeEvent) {
      ProbeEvent event = (ProbeEvent) data;
      processEvent(event);
      return;
    }
    if (data instanceof MeasurementReport) {
      MeasurementReport mr = (MeasurementReport) data;
      processMeasurementReport(mr);
      return;
    }
    throw new IllegalArgumentException("Not supporting data type:"+data.getClass());
  }

  private void processEvent(ProbeEvent event) {
    ServerAgent server = event.getServerAgent();
    log.debug("Sending event to:"+server);
    server.event(event.getTime(), event.getEventType().name(), event.getSource(), event.getMessage(), event.getSubscriptionId());
  }

  private void processMeasurementResponse(MeasurementResponse mr) {
    ServerAgent server = mr.server();
    BaseMeasure bm = mr.value();
    if (bm == null) {
      ProbeEvent event = new ProbeEvent(server, EventType.NO_VALUE_FOR_BM, mr.getProbeInfo().getMeasureURI(), "No valid measurement value available.", mr.getSubscriptionId());
      bb.process(event);
      return;
    }
    String value = bm.getMeasure();
    log.debug("measure:"+ value);
    boolean ok = server.measurement(bm.getTime(), mr.getMeasureURI(), mr.precision(), value, mr.getSubscriptionId());
    if (!ok) {
      log.error("Failed to send measurement");
    }
  }
  
  private void processMeasurementReport(MeasurementReport mr) {
    try {
      ServerAgent server = mr.getServer();
      //log.debug("server: "+server);
      BaseMeasure bm = mr.getMeasure();
      String value = bm.getMeasure();
      //log.debug("value: "+value);
      boolean matchReference = mr.isMatchReference();
      boolean ok;
      log.debug("measure match reference:"+ matchReference);
      if (matchReference) {
        ok = server.BMReport(bm.getTime(), mr.getProbeInfo().getMeasureURI(), null , mr.getSubscriptionId(), mr.isMatchReference(), null);
      }
      else {
        ok = server.BMReport(bm.getTime(), mr.getProbeInfo().getMeasureURI(), value, mr.getSubscriptionId(), mr.isMatchReference(), mr.getReference());
      }
      if (!ok) {
      log.error("Failed to send BM report");
      }
    } catch (Exception e) {
      log.error("Failed to send BM report", e);
    }
  }
/*
  public static void main(String[] args) {
    System.out.println("name:"+EventType.PROBE_HUNG.name());
  }
*/
}
