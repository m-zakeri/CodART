package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.OutputType;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

/**
 * A probe for boolean values.
 * 
 * @author Teemu Kanstrén
 */
public class BooleanProbe extends BaseProbe {

  /**
   * Initialize with user defined type id and type name (PF type is always boolean).
   *
   * @param test    Test to which this probe is linked to.
   * @param typeId  The user defined type (such as sensor data, user name, ...)
   * @param name    User defined name of probe.
   */
  public BooleanProbe (PFTest test, byte typeId, String name) {
    super(test, OutputType.BOOLEAN, typeId, name);
  }

  /**
   * Write out the given value.
   *
   * @param data  The boolean value to store.
   */
  public void data(boolean data) {
    byte[] msg = dataBuilder.output1Msg(nextMsgId(), typeId, data);
    send(msg);
  }
}
