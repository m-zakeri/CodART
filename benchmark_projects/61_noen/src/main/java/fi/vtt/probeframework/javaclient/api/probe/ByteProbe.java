package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.OutputType;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

/**
 * A probe for byte values (binary in spec). Basically equals sending byte array data.
 * 
 * @author Teemu Kanstrén
 */
public class ByteProbe extends BaseProbe {

  /**
   * Init with given values, creating output type msg.
   *
   * @param test    Test to which this probe is linked to.
   * @param typeId  The user defined type (such as sensor data, user name, ...)
   * @param name    User defined name of probe.
   */
  public ByteProbe (PFTest test, byte typeId, String name) {
    super(test, OutputType.BINARY, typeId, name);
  }

  /**
   *
   * @param data  The data to be sent.
   */
  public void data(byte[] data) {
    byte[] msg = dataBuilder.output1Msg(nextMsgId(), typeId, data);
    send(msg);
  }

}
