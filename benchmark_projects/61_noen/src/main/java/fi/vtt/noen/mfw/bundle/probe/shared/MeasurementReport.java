package fi.vtt.noen.mfw.bundle.probe.shared;

import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.DataType;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

public class MeasurementReport extends DataObject {
  //the actual value that was measured
  private final BaseMeasure measure;
  //the server-agent where the measure should be delivered
  private final ServerAgent server;
  //the probe information for the provided measure
  private final ProbeInformation probeInfo;
  //unique identifier for measurement request/response subscription
  private final long subscriptionId;
  //does current measurement value match with reference value
  private final boolean matchReference;
  //the reference value probe uses in compare mode
  private final String reference;

  public MeasurementReport(BaseMeasure measure, ServerAgent server, ProbeInformation probeInfo, long subscriptionId, boolean matchReference, String reference) {
    super(DataType.MEASUREMENT_REPORT);
    this.measure = measure;
    this.server = server;
    this.probeInfo = probeInfo;
    this.subscriptionId = subscriptionId;
    this.matchReference = matchReference;
    this.reference = reference;
  }

  public BaseMeasure getMeasure() {
    return measure;
  }

  public ServerAgent getServer() {
    return server;
  }

  public ProbeInformation getProbeInfo() {
    return probeInfo;
  }

  public long getSubscriptionId() {
    return subscriptionId;
  }

  public boolean isMatchReference() {
    return matchReference;
  }

  public String getReference() {
    return reference;
  }
  
}