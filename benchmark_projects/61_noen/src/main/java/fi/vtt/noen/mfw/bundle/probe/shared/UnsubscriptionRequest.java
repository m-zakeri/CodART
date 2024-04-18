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
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;


public class UnsubscriptionRequest extends DataObject {
  //the probe that provides the measure
  private final String measureURI;
  //the server-agent where the measurement should be delivered
  private final ServerAgent server;
  //unique identifier for measurement request/response subscription
  private final long subscriptionId;

 
  public UnsubscriptionRequest(ServerAgent server, String measureURI, long subscriptionId) {
    super(DataType.MEASUREMENT_REQUEST);
    this.measureURI = measureURI;
    this.server = server;
    this.subscriptionId = subscriptionId;
  }
  
  public long getSubscriptionId() {
    return subscriptionId;
  }

  public String getMeasureURI() {
    return measureURI;
  }

  public ServerAgent getServer() {
    return server;
  }

}
