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
 * Describes a base measure value as a result of a measurement performed by a probe (in response to measurementrequest).
 *
 * @author Teemu Kanstren
 */
public class MeasurementResponse extends DataObject {
  //the actual value that was measured
  private final BaseMeasure measure;
  //the server-agent where the measure should be delivered
  private final ServerAgent server;
  //the probe information for the provided measure
  private final ProbeInformation probeInfo;
  //the precision of the measurement
  private final int precision;
  //unique identifier for measurement request/response subscription
  private final long subscriptionId;

  public MeasurementResponse(BaseMeasure measure, ServerAgent server, ProbeInformation probeInfo, int precision, long subscriptionId) {
    super(DataType.MEASUREMENT_RESPONSE);
    this.measure = measure;
    this.server = server;
    this.probeInfo = probeInfo;
    this.precision = precision;
    this.subscriptionId = subscriptionId;
  }
  
  public long getSubscriptionId() {
    return subscriptionId;
  }

  public BaseMeasure value() {
    return measure;
  }

  public int precision() {
    return precision;
  }

  public ServerAgent server() {
    return server;
  }

  public String getMeasureURI() {
    return probeInfo.getMeasureURI();
  }

  public ProbeInformation getProbeInfo() {
    return probeInfo;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    MeasurementResponse that = (MeasurementResponse) o;

    if (precision != that.precision) return false;
    if (subscriptionId != that.subscriptionId) return false;
    if (measure != null ? !measure.equals(that.measure) : that.measure != null) return false;
    if (probeInfo != null ? !probeInfo.equals(that.probeInfo) : that.probeInfo != null) return false;
    if (server != null ? !server.equals(that.server) : that.server != null) return false;

    return true;
  }

  @Override
  public int hashCode() {
    int result = measure != null ? measure.hashCode() : 0;
    result = 31 * result + (server != null ? server.hashCode() : 0);
    result = 31 * result + (probeInfo != null ? probeInfo.hashCode() : 0);
    result = 31 * result + precision;
    result = 31 * result + (int) (subscriptionId ^ (subscriptionId >>> 32));
    return result;
  }

  @Override
  public String toString() {
    return "MeasurementResponse{" +
            "measure=" + measure +
            ", server=" + server +
            ", probeInfo=" + probeInfo +
            ", precision=" + precision +
            ", subscriptionId=" + subscriptionId +
            '}';
  }
}
