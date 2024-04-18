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

package fi.vtt.noen.mfw.bundle.server.plugins.registry;

//import java.util.Iterator;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.MeasurementSubscription;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

//import java.util.Collection;
//import java.util.Vector;

public class SubscriptionRegistry {
  private final static Logger log = new Logger(SubscriptionRegistry.class);
  private Map<Long, MeasurementSubscription> subscriptions = new HashMap<Long, MeasurementSubscription>();
  private long nextId = 1;

  public SubscriptionRegistry(BundleContext bc) {    
  }
  
  public synchronized long addSubscription(long sacId, BMDescription bm, long frequency, long probeId) {
    if (frequency > 0) {
      for (MeasurementSubscription subscription : subscriptions.values()) {
        if ((subscription.getSacId() == sacId) && (subscription.getBmId() == bm.getBmId())) {
          //if measurement subscription exists for sacId/bmId change new frequency for the subscription
          subscription.setFrequency(frequency);
          return subscription.getSubscriptionId();
        }
      }
    }
    //create and add new subscription
    long subscriptionId = nextId++;
    MeasurementSubscription subscription = new MeasurementSubscription(subscriptionId, bm, sacId, frequency, probeId);
    subscriptions.put(subscriptionId, subscription);
    return subscriptionId;
  }
    
  
  public synchronized long getSacIdForSubscriptionId(long subscriptionId) {
    MeasurementSubscription subscription = subscriptions.get(subscriptionId);
    if (subscription != null) {
      return subscription.getSacId();
    }
    return 0;
  }
  
  public synchronized long getFrequencyForSubscriptionId(long subscriptionId) { 
    MeasurementSubscription subscription = subscriptions.get(subscriptionId);
    if (subscription != null) {
      return subscription.getFrequency();
    }
    return -1;
  }

  public synchronized void removeSubscription(long subscriptionId) {
    log.debug("removing");
    subscriptions.remove(subscriptionId);
    log.debug("removing done");
  }
  
  public synchronized MeasurementSubscription getSubscription(long subscriptionId) {
    return subscriptions.get(subscriptionId);
  }
  
  public synchronized long getIdForSubscription(long sacId, long bmId) {
    long result = 0;
    //search existing subscription for sacId/bmId
    for (MeasurementSubscription ms : subscriptions.values()) {
      if ((ms.getSacId() == sacId) && (ms.getBmId() == bmId)) {
        //ignore one time requests
        if (ms.getFrequency() > 0) {
          result = ms.getSubscriptionId();
        }
      }
    }
    return result;
  }
  
  public synchronized List<MeasurementSubscription> getSubscriptionsForBM(long bmId) {
    List <MeasurementSubscription> result = new ArrayList <MeasurementSubscription>();
    for (MeasurementSubscription ms : subscriptions.values()) {
      if (ms.getBmId() == bmId) {
        result.add(ms);
      } 
    }
    return result;
  }

  public synchronized List<MeasurementSubscription> getSubscriptionsForProbe(long probeId) {
    List <MeasurementSubscription> result = new ArrayList <MeasurementSubscription>();
    for (MeasurementSubscription ms : subscriptions.values()) {
      if (ms.getProbeId() == probeId) {
        result.add(ms);
      } 
    }
    return result;
  }
  
  public synchronized void setProbeForSubscription(long subscriptionId, long probeId) {    
    subscriptions.get(subscriptionId).setProbeId(probeId);
  }

}
