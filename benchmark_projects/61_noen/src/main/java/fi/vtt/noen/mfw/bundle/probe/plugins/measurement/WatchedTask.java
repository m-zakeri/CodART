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

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

import java.util.Map;
import java.util.concurrent.Future;

/**
 * @author Teemu Kanstren
 */
public class WatchedTask {
  private final static Logger log = new Logger(WatchedTask.class);
  private final Future future;
  private final MeasurementTask task;
  private final Map<Long, WatchedTask> subscriptions;
  private final boolean oneTime;
  private final ServerAgent serverAgent;

  public WatchedTask(Future future, MeasurementTask task, Map<Long, WatchedTask> subscriptions, boolean oneTime, ServerAgent serverAgent) {
    this.future = future;
    this.task = task;
    this.subscriptions = subscriptions;
    this.oneTime = oneTime;
    this.serverAgent = serverAgent;
  }

  public long getRunningTime() {
    return task.getRunningTime();
  }

  public void cancel() {
    future.cancel(true);
    subscriptions.remove(task.getSubscriptionId());
  }

  public ProbeInformation getProbeInfo() {
    return task.getProbeInfo();
  }

  public void checkState() {
    if (!oneTime) {
      return;
    }
    if (!task.isRunning() && task.getStartTime() > 0) {
      //this means it has finished
      subscriptions.remove(task.getSubscriptionId());
    }
  }

  public ServerAgent getServerAgent() {
    return serverAgent;
  }
  
  public MeasurementTask getMeasurementTask() {
    return task;
  }
}
