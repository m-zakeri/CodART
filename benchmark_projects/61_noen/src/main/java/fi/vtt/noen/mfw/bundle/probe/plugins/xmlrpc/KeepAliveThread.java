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
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

/**
 * Sends keep-alive messages to the server-agent for the associated probe-agent.
 *
 * @author Teemu Kanstren
 */
public class KeepAliveThread implements Runnable {
  private final static Logger log = new Logger(KeepAliveThread.class);
  //the server-agent where the keep-alive messages should be sent
  private final ServerAgent server;
  //the identifier for the probe for which keep-alive messages should be sent
  private final long probeId;
  //interval between sending keep-alive messages. milliseconds.
  private final int reportInterval;
  //should the thread stop running?
  private boolean shouldRun = true;
  private final RegistrationThread registrationThread;
  //lock for Thread.wait
  private final Object lock = new Object();

  public KeepAliveThread(ServerAgent server, long probeId, int reportInterval, RegistrationThread registrationThread) {
    this.server = server;
    this.probeId = probeId;
    this.reportInterval = reportInterval;
    this.registrationThread = registrationThread;
  }

  /**
   * Separate start method for bundleactivator.start()
   */
  public void start() {
    Thread t = new Thread(this);
    t.setDaemon(true);
    t.start();
  }

  /**
   * Separate stop method for bundleactivator.stop()
   */
  public void stop() {
    shouldRun = false;
    synchronized (lock) {
      lock.notifyAll();
    }
  }

  public void run() {
    log.debug("started keepalive thread with interval " + reportInterval);
    while (shouldRun) {
//      log.debug("Reneving registration for probe:"+probeId);
      try {
        boolean ok = server.keepAlive(probeId);
//        log.debug("keepalive sent: result="+ok+" probe="+probeId);
        if (!ok) {
          log.debug("Failed to send keepalive for probe " + probeId);
          registrationThread.addToBeRegistered(probeId);
        }
      } catch (Exception e) {
        log.error("Failed to connect to server to send keepalive message", e);
      }
      try {
        synchronized (lock) {
          lock.wait(reportInterval);
        }
      } catch (InterruptedException e) {
        //ignored, whee
      }
    }
    log.debug("KeepAliveThread stopped..");
  }
}
