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

package fi.vtt.noen.mfw.bundle.probe.shared;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/**
 * @author Teemu Kanstren
 */
public class ProbeEventBus extends BasePlugin implements ServerAgentUser, Runnable {
  private final static Logger log = new Logger(ProbeEventBus.class);
  private static final String KEY_SOURCE = "source";
  private static final String KEY_MSG = "msg";
  private final Collection<Map<String, String>> queue = Collections.synchronizedCollection(new ArrayList<Map<String, String>>());
  private ScheduledExecutorService executor;
  private ServerAgent serverAgent;

  public ProbeEventBus(BundleContext bc) {
    super(bc, log);
    ServerAgentListener serverAgentListener = new ServerAgentListener(bc, this);
    serverAgentListener.init();
    executor = new ScheduledThreadPoolExecutor(1);
    executor.scheduleWithFixedDelay(this, 1, 1, TimeUnit.SECONDS);
  }

  public void event(ProbeInformation probeInfo, String msg) {
    event(probeInfo.getMeasureURI(), msg);
  }

  public void event(String source, String msg) {
    log.debug("Sending event:"+msg);
    if (serverAgent == null || bb == null) {
      log.debug("No interface to server-agent available. Unable to send event:"+msg);
      log.debug("Event is queued for later delivery if possible");
      Map<String, String> map = new HashMap<String, String>();
      map.put(KEY_SOURCE, source);
      map.put(KEY_MSG, msg);
      queue.add(map);
      return;
    }
    ProbeEvent event = new ProbeEvent(serverAgent, EventType.PROBE_CUSTOM, source, msg, -1);
    bb.process(event);
  }

  public void setServerAgent(ServerAgent serverAgent) {
    log.debug("Server interface received");
    this.serverAgent = serverAgent;
  }

  public void run() {
    if (bb == null || serverAgent == null) {
      return;
    }
    synchronized (queue) {
      for (Map<String, String> map : queue) {
        String source = map.get(KEY_SOURCE);
        String msg = map.get(KEY_MSG);

        ProbeEvent event = new ProbeEvent(serverAgent, EventType.PROBE_CUSTOM, source, msg, -1);
        bb.process(event);
      }
      queue.clear();
    }
    //since the eventbus is now operational, we can stop this scheduled service
    executor.shutdown();
    log.debug("Queue poll executor shutdown.");
  }
}
