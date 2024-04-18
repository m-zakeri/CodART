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

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;

/**
 * A thread that keeps trying to register probes that have not yet been registered but should be.
 * This is separate in order not to block the OSGI container methods that notify about new services, which
 * basically gives us the probes to register.
 *
 * @author Teemu Kanstren
 */
public class RegistrationThread implements Runnable {
  private final static Logger log = new Logger(RegistrationThread.class);
  //when set to false, the thread should terminate
  private boolean shouldRun = true;
  //contains the set of probes that needs to be registered
  private Collection<Probe> toBeRegistered = new HashSet<Probe>();
  //the set of threads sending keep-alive messages to the server-agent
  private Collection<KeepAliveThread> keepAliveThreads = new ArrayList<KeepAliveThread>();
  //configuration for this probe-agent
  private ProbeAgentConfig config;
  private Map<Long, Probe> probes;
  private Map<String, Probe> measureURItoProbeMap;
  //the server-agent that we are communicating with
//  private ServerAgent destination;

  public RegistrationThread(ProbeAgentConfig config, Map<Long, Probe> probes, Map<String, Probe> measureURItoProbeMap) {
    this.config = config;
    this.probes = probes;
    this.measureURItoProbeMap = measureURItoProbeMap;
  }

  public void start() {
    Thread t = new Thread(this);
    t.setDaemon(true);
    t.start();
    log.info("started registration thread");
  }

  public synchronized void stop() {
    shouldRun = false;
    notifyAll();
    for (KeepAliveThread thread : keepAliveThreads) {
      thread.stop();
    }
    log.info("stopped registration thread");
  }

  public void run() {
    while (shouldRun) {
      //we have to copy the contents of toBeRegistered or we risk concurrent modification from addToBeRegistered() method
      Collection<Probe> copy = new ArrayList<Probe>();
      copy.addAll(toBeRegistered);
//      log.debug("registering:"+toBeRegistered.size());
      for (Probe probe : copy) {
        registerProbeInformation(probe);
        toBeRegistered.remove(probe);
      }
//      log.debug("all probes registered");
      synchronized (this) {
        try {
          wait(config.getRetryDelay());
        } catch (InterruptedException e) {
          log.error("Wait interrupted?", e);
        }
      }
    }
  }

  /**
   * Reads the relevant probe configuration information from the given probe and registers this information
   * to the server-agent as a new probe. Store the probe reference with the probe id value given back from
   * the server-agent.
   *
   * @param probe The probe implementation to be registered.
   */
  private synchronized void registerProbeInformation(Probe probe) {
    log.debug("registering information for probe:" + probe);
    ProbeInformation pi = probe.getInformation();
    Map<String, String> registrationInfo = new HashMap<String, String>();
    registrationInfo.put(Const.PROBE_BM_CLASS, pi.getBmClass());
    registrationInfo.put(Const.PROBE_BM_NAME, pi.getBmName());
    registrationInfo.put(Const.PROBE_BM_DESCRIPTION, pi.getBmDescription());
    registrationInfo.put(Const.PROBE_TARGET_TYPE, pi.getTargetType());
    registrationInfo.put(Const.PROBE_TARGET_NAME, pi.getTargetName());
    registrationInfo.put(Const.PROBE_PRECISION, "" + pi.getPrecision());
    registrationInfo.put(Const.PROBE_NAME, "" + pi.getProbeName());
    registrationInfo.put(Const.XMLRPC_PORT, ""+config.getProbeAgentServerPort());
    String ownUrl = pi.getXmlRpcUrl();
    if (config.isLocalInUse()) {
      ownUrl = Const.LOCAL_LINK_ENDPOINT_URL;
    }
    registrationInfo.put(Const.XMLRPC_URL, ownUrl);
    log.debug("now registering probe:" + registrationInfo);
    //this must be here since registration can invoke subscriptions, which need the map
    measureURItoProbeMap.put(pi.getMeasureURI(), probe);
    while (shouldRun) {
      try {
        //we redo get here every time in order to get any updates. updates can happen when local connection is used.
        ServerAgent destination = config.getDestination();
        log.debug("Trying to register to:"+destination);
        long probeId = destination.register(registrationInfo);
        if (probeId < 1) {
          String errorMsg = "(unspecified code)";
          if (probeId == Const.ERROR_CODE_ILLEGAL_ARGUMENTS_FOR_PROBE) {
            errorMsg = "Missing one of the required arguments for probe: target type, target name, bm class, bm name, bm description (got " +
                    pi.getTargetType()+", "+pi.getTargetName()+", "+pi.getBmClass()+", "+pi.getBmName()+", "+pi.getBmDescription()+").";
          }
          log.error("Failed to register probe. Error code:"+probeId+" = "+errorMsg);
          measureURItoProbeMap.remove(pi.getMeasureURI());
          break;
        }
        probes.put(probeId, probe);
        log.debug("registered probe:" + registrationInfo);
        //then we create a thread that keeps sending keepalive messages to the server for this probe..
        KeepAliveThread thread = new KeepAliveThread(destination, probeId, config.getKeepAliveInterval(), this);
        thread.start();
        keepAliveThreads.add(thread);
        break;
      } catch (Exception e) {
        //clear the probe from the map since registration failed
        measureURItoProbeMap.put(pi.getMeasureURI(), null);
        log.error("Failed to register with server. Waiting "+config.getRetryDelay()+" milliseconds to retry.");
        log.debug("Error:",e );
        try {
          wait(config.getRetryDelay());
        } catch (InterruptedException e1) {
          //ignorance is bliss
        }
      }
    }
    log.info("Registration thread registration loop terminated");
  }

  public synchronized void addToBeRegistered(Probe probe) {
    log.debug("Adding probe for registration:"+probe);
    toBeRegistered.add(probe);
    notifyAll();
  }

  //same as above but with integer probeid for a probe that was already previously registered (from keepalive thread)
  public synchronized void addToBeRegistered(long probeId) {
    log.debug("Adding probe for registration:"+probeId);
    addToBeRegistered(probes.get(probeId));
  }
}
