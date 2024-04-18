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

package fi.vtt.noen.mfw.bundle.server.plugins.tester;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerUser;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Set;

/**
 * Emulates a SAC by subscribing to all the base measures from all the registered probes.
 *
 * @author Teemu Kanstren
 */
public class SACEmulatorPlugin extends BasePlugin implements Runnable, ServerUser, RegistryUser {
  private final static Logger log = new Logger(SACEmulatorPlugin.class);
  //server-agent interface
  private ServerPlugin server;
  //server-agent runtime state access
  private RegistryPlugin registry;
  //should this thread run or stop?
  private boolean shouldRun = true;
  //list of base measures that this has subscribed to
  private Collection<Long> subscriptions = new ArrayList<Long>();

  public SACEmulatorPlugin(BundleContext bc) {
    super(bc, log);

    ServerServiceListener serverListener = new ServerServiceListener(bc, log, this);
    serverListener.init();

    RegistryServiceListener registryListener = new RegistryServiceListener(bc, log, this);
    registryListener.init();
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  public void setServer(ServerPlugin server) {
    this.server = server;
  }

  public void start() {
    subscribeToRegistered();
//    Thread t = new Thread(this);
//    t.setDaemon(true);
//    t.start();
  }

  public synchronized void stop() {
    shouldRun = false;
    notifyAll();
  }

  @Override
  public Set getCommands() {
    return createCommandSet(ProbeRegistered.class);
  }

  //we use the proberegistered notification to subscribe to all available measurements

  @Override
  public void process(DataObject data) {
    ProbeRegistered pr = (ProbeRegistered) data;
    log.debug("Processing probe registration:"+pr);
    //server.subscribeToBM(pr.getProbeDescription().getBm().getBmId(), 5000, -1);
    
    BMDescription bm = pr.getProbeDescription().getBm();
    if (!subscriptions.contains(bm.getBmId())) {
      ProbeDescription probe = registry.getProbeForBM(bm.getBmId());
      long subscriptionId = registry.addSubscription(-1, bm, 5000, probe.getProbeId());
      server.subscribeToBM(bm.getBmId(), 5000, subscriptionId);
      log.debug("requested measure for " + bm);
      subscriptions.add(bm.getBmId());
    }
  }

  public void run() {
    while (shouldRun) {
      try {
        wait(5000);
      } catch (InterruptedException e) {
        //ignored, whheeee
      }
      subscribeToRegistered();
    }
  }

  private void subscribeToRegistered() {
    Collection<BMDescription> bms = registry.getAvailableBM();

    for (BMDescription bm : bms) {
      if (subscriptions.contains(bm.getBmId())) {
        continue;
      }
      //subscribe to get the measure value once every second
      //todo: put this into configuration file
      
      ProbeDescription probe = registry.getProbeForBM(bm.getBmId());
      long subscriptionId = registry.addSubscription(-1, bm, 5000, probe.getProbeId());
      server.subscribeToBM(bm.getBmId(), 5000, subscriptionId);

      //server.subscribeToBM(bm.getBmId(), 5000, -1);
      log.debug("requested measure for " + bm);
      subscriptions.add(bm.getBmId());
    }
  }
}
