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

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.Availability;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.SACClient;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerUser;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import org.osgi.framework.BundleContext;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
//import java.util.Vector;

/**
 * The actual component that links the MFW server to the BUGYO Beyond cockpit.
 *
 * @author Teemu Kanstren
 */
public class SACPlugin extends BasePlugin implements RegistryUser, ServerUser {
  private final static Logger log = new Logger(SACPlugin.class);
  //for the server-agent to communicate with the probe-agents
  private ServerPlugin server;
  //for accessing runtime state
  private RegistryPlugin registry;
  
  private Map<Long, String> sacsUrls;
  private Map<Long, SAC> sacs = new HashMap<Long, SAC>();
  private AvailabilityProvider availabilityProvider;
  private long mfwId = 1;

  public SACPlugin(BundleContext bc, Map<Long, String> sacsUrls, int availabilityInterval, long mfwId) {
    super(bc, log);

    //set up listeners to capture server-agent and registry services
    ServerServiceListener serverListener = new ServerServiceListener(bc, log, this);
    serverListener.init();

    RegistryServiceListener listener = new RegistryServiceListener(bc, log, this);
    listener.init();
    this.sacsUrls = sacsUrls;
    
    availabilityProvider = new AvailabilityProvider(this, availabilityInterval, mfwId);
    this.mfwId = mfwId;
  }

  public void setServer(ServerPlugin server) {
    this.server = server;
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  //Gives a list of available BM.
  public List<BMDescription> getAvailableBMList() {
    return registry.getAvailableBM();
  }
  
  //Requests for a given measurement to be provided.
  public boolean requestBM(long sacId, long bmId) {
    //TODO: failure handling, if invalid SAC ID or BM ID is given, this should fail as well as all the other calls in this class
    boolean result = false;
    log.info("SAC Requesting BM - SAC ID:"+sacId+" BM ID:"+bmId);
    try {
      ProbeDescription probe = registry.getProbeForBM(bmId);
      long subscriptionId = registry.addMeasurementRequest(sacId, probe.getBm(), probe.getProbeId());
      server.requestBM(bmId, subscriptionId);
      result = true;
    } catch (Exception e) {
      log.error("Failed to fetch requested BM: " + bmId, e);
      event(new ServerEvent(System.currentTimeMillis(), EventType.GENERAL_ERROR, "SACPlugin", e.getMessage()));
    }
    return result;
  }

  /**
   * Requests for a given measurement to be provided.
   *
   * @param sacId identifies the SAC
   * @param bmId identifies the BM
   * @param interval How often should we sample? In milliseconds.
   */
  public void subscribeToBM(long sacId, long bmId, long interval) {
    log.info("SAC subscribing to BM - SAC ID:"+sacId+" BM ID:"+bmId+" interval:"+interval);
    ProbeDescription probe = registry.getProbeForBM(bmId);
    long subscriptionId = registry.addSubscription(sacId, probe.getBm(), interval, probe.getProbeId());
    server.subscribeToBM(bmId, interval, subscriptionId);
  }

  //removes an existing subscription
  public void unSubscribeToBM(long sacId, long bmId) {
    log.info("SAC unsubscribing to BM - SAC ID:"+sacId+" BM ID:"+bmId);
    long subscriptionId = registry.getIdForSubscription(sacId, bmId);
    server.unSubscribeToBM(bmId, subscriptionId);
    registry.removeSubscription(sacId, subscriptionId);
  }

   //This should return a list of probes connected to the MFW.
  public List<ProbeDescription> getProbeList() {
    return registry.getProbes();
  }

  //list of targets of measurement (some call them devices)
  public Collection<TargetDescription> getTargetList() {
    return registry.getTargets();
  }

  public Collection<ProbeConfiguration> getProbeConfigurationParameters(long probeId) {
    Collection<ProbeConfiguration> configuration = server.requestProbeConfigurationParameters(probeId);
    return configuration;
  }

   //This should set the configuration for a given probe.
  public boolean setProbeConfiguration(long probeId, Map<String, String> configuration) {
    boolean ok = server.setProbeConfiguration(probeId, configuration);
    return ok;
  }

   //This gives some information about the MFW.
  public String getMFWInformation() {
    return "Your favourite MFW is here";
    //TODO: need to return id, version, IFs???, company, time
  }

  /**
   * Sends an event to the SAC. Since the SAC interface currently supports no events, this is left here for
   * the time when people again realize it should.
   *
   * @param event The event to be passed.
   */
  public void event(ServerEvent event) {
    if (sacs.isEmpty()) {      
      log.debug("No SAC defined, ignoring event");
      return;
    }
    for (SAC sac : sacs.values()) {
      String msg = event.getMessage();
      log.debug("passing event:" + event);
      sac.event(msg);
    }
  }
  
  public boolean sacRegistered(long sacId) {
    return register(sacId);
  }
  
  public boolean register(long sacId) {
    //if sac not registered
    if (!sacs.containsKey(sacId)) {
      String sacUrl = sacsUrls.get(sacId);
      //if sacId/sacUrl found (read from property file on startup)
      if (sacUrl != null) {
        SACClient sacClient = new SACClient(this, sacUrl, sacId, mfwId);
        //log.debug("Registering SAC (ID:" +sacId+ ")");
        //sacs.put(sacId, sacClient);
        register(sacId, sacClient);
        bb.process(new ServerEvent(System.currentTimeMillis(), EventType.SAC_REGISTERED, "SAC:"+sacId, "New SAC registered URL:"+sacUrl));
      } else {
        bb.process(new ServerEvent(System.currentTimeMillis(), EventType.SAC_REGISTERED, "SAC:"+sacId, "Attempt to register a SAC with unknown ID failed."));
        return false;
      }
    }
    return true;
  }
  
  public void register(long sacId, SAC sac) {
    log.info("Registering SAC (ID:" +sacId+ ")");
    sacs.put(sacId, sac);
    availabilityProvider.registerSAC(sacId, sac);
  }
  
  //called by the server-agent to provide a BM value to the SAC as it has requested
  public void bmValue(Value value) {
    log.info("Received BM value:"+value);
    
    //get sacId for subscriptionId
    long sid = value.getSubscriptionId();
    long sacId = registry.getSacIdForSubscription(sid);
    log.debug("subscriptionId: " + sid + ", sacId: " +sacId);
        
    if (sacId == 0) {
      //received measurement value for subscription that was not found (removed)
      //(re)send unsubscription
      //server.unSubscribeToBM(value.getBm().getBmId(), value.getSubscriptionId());
    }
    //get sac for sacId
    SAC sac = sacs.get(sacId);
    log.debug("SAC:"+sac);

    if (sac == null) {
      log.error("No SAC registered for measurement, not sending BM Value");
      return;
    }

    //if one time measurement, remove subscription from registry
    if (registry.getFrequencyForSubscription(sid) == 0) {
      log.debug("remove call");
      registry.removeSubscription(sacId, sid);
      log.debug("remove call done");
    }

    log.debug("providing value to:" + sac);
    sac.bmResult(value);
  }
/*  
  public void setAvailability(Availability availability) {
    if (sacs.isEmpty()) {      
      log.error("No SAC registered, not reporting availability change");
      return;
    }
    for (SAC sac : sacs.values()) {
      sac.setAvailability(availability);
    }
  }
*/
  //list of information to be received from the blackboard
  public Set getCommands() {
    return createCommandSet(Value.class, ServerEvent.class, ProbeRegistered.class, ProbeDisabled.class);
  }

  public void process(DataObject data) {
    if (data instanceof Value) {
      Value value = (Value) data;
      log.debug("received value:" + value);
      bmValue(value);
    } else if (data instanceof ServerEvent) {
      ServerEvent event = (ServerEvent) data;
      log.debug("received event:" + event);
      event(event);
/*      if (event.type.equals(EventType.PROBE_HUNG)) {
        ProbeDescription probe = registry.getProbeForSubscription(event.getSubscriptionId());
        registry.setProbeDisabled(probe);
      }*/
    } else if (data instanceof ProbeRegistered) {      
/*
      ProbeRegistered pr = (ProbeRegistered) data;
      log.debug("received probe registered:" + pr);
      
      if (sacs.isEmpty()) {      
        log.error("No SAC registered, not reporting Probe registration");
        return;
      }
      //ProbeDescription pd = pr.getProbeDescription();
      for (SAC sac : sacs.values()) {
        sac.probeRegistered(pr);
      }
      //todo: create event     
*/
      //availabilityProvider.setAvailabilityChanged();
      
      ProbeRegistered pr = (ProbeRegistered) data;
      log.debug("received probe registered:" + pr);
      availabilityProvider.probeRegistered(pr);

    } else if (data instanceof ProbeDisabled) {
/*
      ProbeDisabled msg = (ProbeDisabled) data;
      log.debug("received probe disabled:" + msg);
      
      if (sacs.isEmpty()) {      
        log.error("No SAC registered, not reporting Probe disabled");
        return;
      }
      //ProbeDescription pd = msg.getProbeDescription();
      for (SAC sac : sacs.values()) {
        sac.probeDisabled(msg);
      }
*/
      //availabilityProvider.setAvailabilityChanged();
      
      ProbeDisabled msg = (ProbeDisabled) data;
      log.debug("received probe disabled:" + msg);
      availabilityProvider.probeDisabled(msg);
    }
  }
}
