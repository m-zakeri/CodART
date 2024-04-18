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

/**
 * Represents a request to provide a measurement from a probe, either once or at a given sampling interval.
 *
 * @author Teemu Kanstren
 */
public class MeasurementRequest extends DataObject {
  //the probe that provides the measure. currently assumed to give only the one exact measure.
  private final String measureURI;
  //sampling interval for continuously providing the values
  private final long interval;
  //the last time when a measurement was done
  private long lastMeasureTime = -1;
  //the server-agent where the measurement should be delivered
  private final ServerAgent server;
  //the probe that should perform the measure
  private final Probe probe;
  //unique identifier for measurement request/response subscription
  private final long subscriptionId;

  public MeasurementRequest(ServerAgent server, String measureURI, Probe probe) {
    this(server, measureURI, probe, -1, -1);
  }

  public MeasurementRequest(ServerAgent server, String measureURI, Probe probe, long interval) {
    this(server, measureURI, probe, interval, -1);
  }
  
  public MeasurementRequest(ServerAgent server, String measureURI, Probe probe, long interval, long subscriptionId) {
    super(DataType.MEASUREMENT_REQUEST);
    this.measureURI = measureURI;
    this.interval = interval;
    this.server = server;
    this.probe = probe;
    this.subscriptionId = subscriptionId;
  }
  
  public long getSubscriptionId() {
    return subscriptionId;
  }

  public Probe getProbe() {
    return probe;
  }

  public String getMeasureURI() {
    return measureURI;
  }

  public long getInterval() {
    return interval;
  }

  public long getLastMeasureTime() {
    return lastMeasureTime;
  }

  public void setLastMeasureTime(long lastMeasureTime) {
    this.lastMeasureTime = lastMeasureTime;
  }

  public ServerAgent getServer() {
    return server;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    MeasurementRequest that = (MeasurementRequest) o;

    if (interval != that.interval) return false;
    if (measureURI != null ? !measureURI.equals(that.measureURI) : that.measureURI != null) return false;
    if (server != null ? !server.equals(that.server) : that.server != null) return false;
    if (subscriptionId != that.subscriptionId) return false;

    return true;
  }

  @Override
  public int hashCode() {
    int result = measureURI != null ? measureURI.hashCode() : 0;
    result = 31 * result + (int)interval;
    result = 31 * result + (server != null ? server.hashCode() : 0);
    result = 31 * result + (int)subscriptionId;
    
    return result;
  }

  @Override
  public String toString() {
    return "MeasurementRequest{" +
            "measureURI='" + measureURI + '\'' +
            ", interval=" + interval +
            ", server=" + server +
            ", subscriptionId=" + subscriptionId +
            '}';
  }
}
