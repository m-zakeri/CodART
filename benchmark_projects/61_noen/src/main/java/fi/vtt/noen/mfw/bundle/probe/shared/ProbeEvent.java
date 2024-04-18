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

import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.DataType;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

/**
 * @author Teemu Kanstren
 */
public class ProbeEvent extends DataObject {
  private final long time;
  private final EventType type;
  private final String source;
  private final String msg;
  private final ServerAgent serverAgent;
  private final long subscriptionId;

  public ProbeEvent(ServerAgent serverAgent, EventType type, String source, String msg, long subscriptionId) {
    super(DataType.PROBE_EVENT);
    this.serverAgent = serverAgent;
    this.type = type;
    this.source = source;
    this.msg = msg;
    this.time = System.currentTimeMillis();
    this.subscriptionId = subscriptionId;
  }

  public ServerAgent getServerAgent() {
    return serverAgent;
  }

  public long getTime() {
    return time;
  }

  public EventType getEventType() {
    return type;
  }

  public String getSource() {
    return source;
  }

  public String getMessage() {
    return msg;
  }

  public long getSubscriptionId() {
    return subscriptionId;
  }
}
