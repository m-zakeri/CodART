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

package fi.vtt.noen.mfw.bundle.probe.plugins.xmlrpc;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.plugins.measurement.MeasurementProvider;
import fi.vtt.noen.mfw.bundle.probe.plugins.measurement.MeasurementTask;
import fi.vtt.noen.mfw.bundle.probe.plugins.measurement.MeasurementThreadFactory;
import fi.vtt.noen.mfw.bundle.probe.plugins.measurement.WatchedTask;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeAgent;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;


public class SubscriptionChecker implements Runnable {
  private final static Logger log = new Logger(SubscriptionChecker.class);
  private ProbeAgent probeAgent;
  private ServerAgent serverAgent;
  private MeasurementProvider measurementProvider;
  private ScheduledExecutorService executor;  
  
  public SubscriptionChecker(ProbeAgent probeAgent, int subscriptionCheckInterval) {
    this.probeAgent = probeAgent;
    executor = new ScheduledThreadPoolExecutor(1, new MeasurementThreadFactory());
    executor.scheduleWithFixedDelay(this, 5000, subscriptionCheckInterval, TimeUnit.MILLISECONDS);
    log.debug("Started subscription checker with interval "+subscriptionCheckInterval+"ms");
  }

  public void run() {
    if (measurementProvider == null) {
      log.debug("measurementProvider is null, subscriptionChecker not running");
      return;
    } 
    if (serverAgent == null) {
      log.debug("ServerAgent is null, subscriptionChecker not running");
      return;
    }
    log.debug("Subscription checker running");
    Map<Long, Probe> probes = probeAgent.getProbes();
    for (Map.Entry<Long, Probe> probeEntry : probes.entrySet()) {
      Probe probe = probeEntry.getValue();  
      Long probeId = probeEntry.getKey();
      //log.debug("ProbeId:"+probeId);
      Map<Long, WatchedTask> subscriptions = measurementProvider.getSubscriptions();
      List<Long> subscriptionIds = new ArrayList<Long>();
      for (Map.Entry<Long, WatchedTask> subscriptionEntry : subscriptions.entrySet()) {      
        WatchedTask watchedTask = subscriptionEntry.getValue();
        MeasurementTask task = watchedTask.getMeasurementTask();
        if (probe == task.getProbe()) {
          long subscriptionId = subscriptionEntry.getKey();
          if (subscriptionId >= 0) {
            subscriptionIds.add(subscriptionId);
            //log.debug("SubscriptionId:"+subscriptionId);
          }
        }
      }      
      log.debug("Checking subscriptions for probe (ID:"+probeId+")");      
      serverAgent.checkSubscriptions(probeId, subscriptionIds);
/*
      List<Long> subscriptionIds = measurementProvider.getSubscriptionIdsForProbe(probe);
      Long probeId = entry.getKey();
      log.debug("ProbeId:"+probeId);
      for (Long subscriptionId : subscriptionIds) {
        log.debug("SubscriptionId:"+subscriptionId);
      }
      log.debug("Checking subscriptions");
      serverAgent.checkSubscriptions(probeId, subscriptionIds);
*/
    }
  }
  
  public void setServerAgent(ServerAgent serverAgent) {
    log.debug("Server interface received");
    this.serverAgent = serverAgent;
  }
  
  public void setMeasurementProvider(MeasurementProvider measurementProvider) {
    log.debug("Measurement provider interface received");
    this.measurementProvider = measurementProvider;
  }

  public void stop() {
    executor.shutdown();    
  }
}
