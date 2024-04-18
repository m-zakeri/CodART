package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.OutputType;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

/**
 * Probe for integer values. Defaults to 8 byte integers, spec supports also different types
 * but this is for now only limited to the largest one of 8 bytes.
 * 
 * @author Teemu Kanstrén
 */
public class IntProbe extends BaseProbe {

  /**
  * @param test    Test to which this probe is linked to.
  * @param typeId  The user defined type (such as sensor data, user name, ...)
  * @param name    User defined name of probe.
   */
  public IntProbe(PFTest test, byte typeId, String name) {
    super(test, OutputType.INTEGER, typeId, name);
  }

  public void data(int data) {
    byte[] msg = dataBuilder.output1Msg(nextMsgId(), typeId, data);
    send(msg);
  }
}
