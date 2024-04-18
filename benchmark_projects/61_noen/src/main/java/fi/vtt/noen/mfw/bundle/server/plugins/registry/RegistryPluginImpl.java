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

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistencePlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceUser;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerUser;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.MeasurementSubscription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import org.osgi.framework.BundleContext;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * @author Teemu Kanstren
 */
public class RegistryPluginImpl extends BasePlugin implements RegistryPlugin, PersistenceUser, ServerUser, Runnable {
  private final static Logger log = new Logger(RegistryPluginImpl.class);
  //key = measureURI
  private final Map<String, BMDescription> availableBM = new HashMap<String, BMDescription>();
  //key = long bmid provided by sac
  private final Map<Long, BMDescription> bmIds = new HashMap<Long, BMDescription>();
  //key = targetType+targetName
  private final Map<String, TargetDescription> targets = new HashMap<String, TargetDescription>();
  //key = probeId, value = ProbeDescription
  private final Map<Long, ProbeDescription> probes = new HashMap<Long, ProbeDescription>();
  //all DM definitions created
  private final Collection<DMDefinition> dms = new HashSet<DMDefinition>();
  private int nextDmId = 1;
  //maximum delay for receiving keep-alive messages before a probe-agent is reported as lost
  private int maxDelay = DEFAULT_DELAY;
  //how much time to wait between checking the keep-alive status of probe-agents
  private int delayIncrement = DEFAULT_INCREMENT;
  //default keep-alive threshold if nothing is configured
  private static final int DEFAULT_DELAY = 10 * 1000; //10 seconds
  //default keep-alive wait time if nothing is configured
  private static final int DEFAULT_INCREMENT = 1000; //1 second
  //should the registry keep running its threads or shut down?
  private boolean shouldRun = true;
  //access to the persistent state
  private PersistencePlugin persistence = null;
  private ServerPlugin server = null;
  private SubscriptionRegistry subscriptionRegistry;

  public RegistryPluginImpl(BundleContext bc, int maxDelay, int delayIncrement) {
    super(bc, log);
    if (maxDelay > 0) {
      //assume that if one is set, both are set
      this.maxDelay = maxDelay;
      this.delayIncrement = delayIncrement;
    } else {
      try {
        Properties props = readConfiguration();
        this.maxDelay = Integer.parseInt(props.getProperty(Const.MAX_KEEPALIVE_DELAY));
      } catch (IOException e) {
        log.error("Error in reading configuration file. Using defaults.", e);
      }
    }
    //start a thread to monitor keep-alive messages
    Thread t = new Thread(this);
    t.setDaemon(true);
    t.start();

    //register a listener to capture the persistenceplugin when available
    PersistenceServiceListener pl = new PersistenceServiceListener(bc, log, this);
    pl.init();

    //register a listener to capture the server-agent when available
    ServerServiceListener serverListener = new ServerServiceListener(bc, log, this);
    serverListener.init();

    subscriptionRegistry = new SubscriptionRegistry(bc);
  }

  public void stop() {
    shouldRun = false;
  }

  public void setPersistence(PersistencePlugin persistence) {
    this.persistence = persistence;
  }

  public void setServer(ServerPlugin server) {
    this.server = server;
  }

  //get the BMDescription for the given measureURI (measure identifier)
  public BMDescription descriptionFor(String measureURI) {
    return availableBM.get(measureURI);
  }

  //provides a list of all registered probes
  public List<ProbeDescription> getProbes() {
    //create copy of current state to avoid breaking on concurrent access etc.
    List<ProbeDescription> result = new ArrayList<ProbeDescription>(probes.size());
    result.addAll(probes.values());
    return result;
  }

  //get current list of registered probes
  public synchronized List<BMDescription> getAvailableBM() {
    Collection<BMDescription> values = availableBM.values();
    //create copy of current state to avoid breaking on concurrent access etc.
    List<BMDescription> result = new ArrayList<BMDescription>(values.size());
    result.addAll(values);
    return result;
  }

  //list of all currently defined DM
  public synchronized List<DMDefinition> getDerivedMeasures() {
    //create copy of current state to avoid breaking on concurrent access etc.
    List<DMDefinition> result = new ArrayList<DMDefinition>(dms.size());
    result.addAll(dms);
    return result;
  }

  //list of all active targets (with probes registered for them)
  public Collection<TargetDescription> getTargets() {
    //create copy of current state to avoid breaking on concurrent access etc.
    List<TargetDescription> targets = new ArrayList<TargetDescription>();
    targets.addAll(this.targets.values());
    return targets;
  }

  //create a derived measure. currently not a core feature, not persisted, etc.
  public void createDM(String name, String script) {
    DMDefinition newDm = new DMDefinition(nextDmId++, name, script);
    dms.add(newDm);
    bb.process(newDm);
    log.debug("Registered DM:" + name);
  }

  //gives probe description for given probeid
  public ProbeDescription getProbeFor(long probeId) {
    return probes.get(probeId);
  }

  //give the best available probe for given BM (with highest precision)
  public ProbeDescription getProbeForBM(long bmId) {
    BMDescription bm = bmIds.get(bmId);
    String measureURI = bm.getMeasureURI();
    ProbeDescription result = null;
    for (ProbeDescription probe : probes.values()) {
      if (!probe.getMeasureURI().equals(measureURI)) {
        continue;
      }
      if (result != null) {
        if (result.getPrecision() < probe.getPrecision()) {
          result = probe;
        }
      } else {
        result = probe;
      }
    }
    return result;
  }

  //find the target id for the given measureURI
  public long targetIdFor(String measureURI) {
    //parse type from uri
    String targetType = parseTargetType(measureURI);
    //parse name from uri
    String targetName = parseTargetName(measureURI);
    //get the name from the target map
    TargetDescription target = targets.get(targetType + targetName);
    if (target == null) {
      throw new IllegalArgumentException("No target found for measureURI:" + measureURI);
    }
    return target.getTargetId();
  }

  //parse target type from a measureURI
  public String parseTargetType(String measureURI) {
    int[] bounds = getTargetTypeBounds(measureURI);
    return measureURI.substring(bounds[0], bounds[1]);
  }

  //get start and end index of target type inside given measureURI
  private int[] getTargetTypeBounds(String measureURI) {
    int si = measureURI.indexOf("//");
    if (si <= 0) {
      throw new IllegalArgumentException("Invalid measure URI:" + measureURI);
    }
    si += 2;
    int ei = measureURI.indexOf("/", si);
    if (si <= 0) {
      throw new IllegalArgumentException("Invalid measure URI:" + measureURI);
    }
    return new int[]{si, ei};
  }

  //parse target name from given measureURI
  public String parseTargetName(String measureURI) {
    int[] bounds = getTargetTypeBounds(measureURI);
    //end of type + "/"
    int si = bounds[1] + 1;
    int ei = measureURI.indexOf("/", si);
    if (si <= 0) {
      throw new IllegalArgumentException("Invalid measure URI:" + measureURI);
    }
    return measureURI.substring(si, ei);
  }

  //when a probe sends a keep-alive message, this is invoked
  public boolean processKeepAlive(long probeId) {
    ProbeDescription probe = probes.get(probeId);
    if (probe != null) {
      probe.resetDelay();
      return true;
    }
    return false;
  }

  /**
   * Called when a registration is received from a probe-agent.
   *
   * @param properties A set of key-value pairs describing the probe. For key and their description see.. what? :)
   * @return The probe identifier for the registered probe.
   */
  public synchronized long registerProbe(Map<String, String> properties) {
    log.debug("registering probe");
    BMDescription bm = null;
    boolean newTarget = false;
    boolean newBM = false;
    try {
      log.debug("creating target description");
      TargetDescription target = persistence.createTargetDescription(properties);
      if (!targets.containsValue(target)) {
        newTarget = true;
      }
      targets.put(target.getTargetType() + target.getTargetName(), target);
      log.debug("creating bm description");
      bm = persistence.createBMDescription(properties);
    } catch (Exception e) {
      log.error("Failed to create target/bm for probe description.", e);
      return Const.ERROR_CODE_ILLEGAL_ARGUMENTS_FOR_PROBE;
    }
    if (!bmIds.containsKey(bm.getBmId())) {
      newBM = true;
    }
    availableBM.put(bm.getMeasureURI(), bm);
    bmIds.put(bm.getBmId(), bm);

    //we use the database to manage the probe information
    log.debug("creating probe description");
    ProbeDescription desc = persistence.createProbeDescription(properties);
    //we keep a mapping from id to desc to ease access in other functions
    probes.put(desc.getProbeId(), desc);

    // send probe registered data object to blackboard 
    ProbeRegistered pr = new ProbeRegistered(desc, newBM, newTarget);
    bb.process(pr);

    return desc.getProbeId();
  }

  //this is the thread that runs checking when a keep-alive message is received and if the delay for a probe has
  //surpassed the given threshold. if one gets lots, the set of available BM is updated accordingly.
  public void run() {
    while (shouldRun) {
      try {
        Thread.sleep(delayIncrement);
      } catch (InterruptedException e) {
        log.error("sleep interrupted", e);
      }
      synchronized (this) {
        for (Iterator<Map.Entry<Long, ProbeDescription>> i = probes.entrySet().iterator(); i.hasNext(); ) {
          Map.Entry<Long, ProbeDescription> entry = i.next();
          ProbeDescription probe = entry.getValue();
          probe.increaseDelay(delayIncrement);
//          log.debug("Increasing delay for "+probe+" by "+delayIncrement);
          if (probe.getDelay() >= maxDelay) {
            //TODO: also check all BM if we need to remove one, etc.
            log.info("Lease terminated for:" + probe);
            i.remove();

            //check if there are any BM for the target (device)            
            boolean found = false;
            boolean targetDisabled = false;
            TargetDescription target = probe.getBm().getTarget();
            for (Map.Entry<Long, BMDescription> bmEntry : bmIds.entrySet()) {
              TargetDescription targetDesc = bmEntry.getValue().getTarget();
              if (target == targetDesc) {
                found = true;
                break;
              }
            }
            if (!found) {
              //there are no BM for the target so it can be removed
              log.debug("removing Target:" + target);
              String key = target.getTargetType() + target.getTargetName();
              targets.remove(key);
              targetDisabled = true;
            }

            // here can be several probes for the same BM so we can only remove the BM if no other probe is present
            //note that above we removed this probe from the list of probes so it is no longer found by getForBM()
            boolean bmDisabled = false;
            if (getProbeForBM(probe.getBm().getBmId()) == null) {
              String measureURI = probe.getMeasureURI();
              BMDescription bmDesc = availableBM.remove(measureURI);
              log.debug("removind BM:" + bmDesc);
              bmIds.remove(bmDesc.getBmId());
              bmDisabled = true;
            }
            // send probe disabled data object to blackboard
            ProbeDisabled pd = new ProbeDisabled(probe, bmDisabled, targetDisabled);
            bb.process(pd);
          }
        }
      }
    }
  }

  public void setProbeDisabled(ProbeDescription probe) {
    log.info("Disabling Probe:" + probe);
    probes.remove(probe.getProbeId());

    //check if there are any BM for the target (device)            
    boolean found = false;
    boolean targetDisabled = false;
    TargetDescription target = probe.getBm().getTarget();
    for (Map.Entry<Long, BMDescription> bmEntry : bmIds.entrySet()) {
      TargetDescription targetDesc = bmEntry.getValue().getTarget();
      if (target == targetDesc) {
        found = true;
        break;
      }
    }
    if (!found) {
      //there are no BM for the target so it can be removed
      log.debug("removing Target:" + target);
      String key = target.getTargetType() + target.getTargetName();
      targets.remove(key);
      targetDisabled = true;
    }

    // here can be several probes for the same BM so we can only remove the BM if no other probe is present
    //note that above we removed this probe from the list of probes so it is no longer found by getForBM()
    boolean bmDisabled = false;
    if (getProbeForBM(probe.getBm().getBmId()) == null) {
      String measureURI = probe.getMeasureURI();
      BMDescription bmDesc = availableBM.remove(measureURI);
      log.debug("removind BM:" + bmDesc);
      bmIds.remove(bmDesc.getBmId());
      bmDisabled = true;
    }
    // send probe disabled data object to blackboard
    ProbeDisabled pd = new ProbeDisabled(probe, bmDisabled, targetDisabled);
    bb.process(pd);
  }

  public ProbeDescription getProbeForSubscription(long subscriptionId) {
    try {
      long probeId = subscriptionRegistry.getSubscription(subscriptionId).getProbeId();
      return getProbeFor(probeId);
    } catch (Exception e) {
      log.error("Failed to get probe for subscription", e);
      return null;
    }
  }

  public long addSubscription(long sacId, BMDescription bm, long frequency, long probeId) {
    String msg = "New measurement subscription URI:" + bm.getMeasureURI() + " F:" + frequency + " PID:" + probeId;
    bb.process(new ServerEvent(System.currentTimeMillis(), EventType.NEW_SUBSCRIPTION, "SAC " + sacId, msg));
    return subscriptionRegistry.addSubscription(sacId, bm, frequency, probeId);
  }

  public long getSacIdForSubscription(long subscriptionId) {
    return subscriptionRegistry.getSacIdForSubscriptionId(subscriptionId);
  }

  public long getFrequencyForSubscription(long subscriptionId) {
    return subscriptionRegistry.getFrequencyForSubscriptionId(subscriptionId);
  }

  public void removeSubscription(long sacId, long subscriptionId) {
    String msg = "Removed measurement subscription id:" + subscriptionId;
    bb.process(new ServerEvent(System.currentTimeMillis(), EventType.DELETE_SUBSCRIPTION, "SAC " + sacId, msg));
    subscriptionRegistry.removeSubscription(subscriptionId);
  }

  public long getIdForSubscription(long sacId, long bmId) {
    return subscriptionRegistry.getIdForSubscription(sacId, bmId);
  }

  public long addMeasurementRequest(long sacId, BMDescription bm, long probeId) {
    String msg = "New measurement request URI:" + bm.getMeasureURI() + " PID:" + probeId;
    bb.process(new ServerEvent(System.currentTimeMillis(), EventType.NEW_MEASUREMENT_REQUEST, "SAC " + sacId, msg));
    return subscriptionRegistry.addSubscription(sacId, bm, 0, probeId);
  }

  public void checkSubscriptions(long probeId, List<Long> subscriptionIds) {
    log.debug("checkSubscriptions (probeId:" + probeId + ") - subscriptions:" + subscriptionIds);
    //check if some other probe is better for the bm 
    //should be done only once after probe registration?
    //get the best available probe for bm
    long bmId = probes.get(probeId).getBm().getBmId();
    ProbeDescription probe = getProbeForBM(bmId);
    List<MeasurementSubscription> subscriptions = subscriptionRegistry.getSubscriptionsForBM(bmId);
    log.debug("Probe BM subscriptions:" + subscriptions);
    for (MeasurementSubscription subscription : subscriptions) {
      if (subscription.getProbeId() != probe.getProbeId()) {
        log.debug("Probe with higher precision found");
        subscriptionRegistry.setProbeForSubscription(subscription.getSubscriptionId(), probe.getProbeId());
      }
    }
    subscriptions = subscriptionRegistry.getSubscriptionsForProbe(probeId);
    log.debug("Subscriptions for probe:" + subscriptions);
    for (MeasurementSubscription ms : subscriptions) {
      //log.debug("Subscription on server (ID:"+ms.getSubscriptionId()+")");
      //if there is a new subscription
      if (!subscriptionIds.contains(ms.getSubscriptionId())) {
        log.info("New subscription found (bmId:" + ms.getBmId() + ") while checking existing ones");
        //send subscription request to probe
        if (server != null) {
          server.subscribeToBM(ms.getBmId(), ms.getFrequency(), ms.getSubscriptionId());
        } else {
          log.error("Could not request bm, server null");
        }
      }
    }
    //if probes current subscription is not found on the server it should be removed from the probe    
    for (Long subscriptionId : subscriptionIds) {
      //log.debug("Probes current subscription (ID:"+subscriptionId+")");
      boolean found = false;
      for (MeasurementSubscription ms : subscriptions) {
        if (ms.getSubscriptionId() == subscriptionId) {
          found = true;
          break;
        }
      }
      if (!found) {
        log.debug("Probes (ID:" + probeId + ") current subscription (ID:" + subscriptionId + ") not found on server, sending unsubscription request to probe");
        server.unSubscribeToBM(getProbeFor(probeId), subscriptionId);
      }
    }
  }

}
