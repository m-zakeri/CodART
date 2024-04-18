package fi.vtt.probeframework.javaclient.protocol.messages;

import fi.vtt.probeframework.javaclient.api.probe.PFTest;

public class OutputBuilder extends BaseBuilder {
  //outputid(1)+outputn(2)+datatype(1)+time(4)
  public static final int OUTPUT1BASELENGTH = 1+2+1+4;

  public OutputBuilder(PFTest test) {
    super(test);
  }

  public int startOutput1(byte[] msg, int outputN, byte typeId) {
    int i = 0;
    msg[i++] = 0x11;
    longToBytes(outputN, msg, i, 2);
    i += 2;
    msg[i++] = typeId;
    return i;
  }
    
  public byte[] output1Msg(int n, byte typeId, boolean value) {
    byte[] msg = new byte[OUTPUT1BASELENGTH+1];
    int i = startOutput1(msg, n, typeId);

    if (value) {
      msg[i++] = 0x01;
    } else {
      msg[i++] = 0x00;
    }

    setTime(msg, i);
    return msg;
  }

  public byte[] output1Msg(int n, byte typeId, long value) {
    byte[] msg = new byte[OUTPUT1BASELENGTH+8];
    int i = startOutput1(msg, n, typeId);

    longToBytes(value, msg, i, 8);
    i += 8;

    setTime(msg, i);
    return msg;
  }

  public byte[] output1Msg(int n, byte typeId, String text) {
    byte[] msg = new byte[OUTPUT1BASELENGTH+strlen(text, 2)+2];
    int i = startOutput1(msg, n, typeId);

    stringToBytes(text, msg, i, 2);
    i += text.length()+2;

    setTime(msg, i);
    return msg;
  }

  public byte[] output1Msg(int n, byte typeId, byte[] data) {
    byte[] msg = new byte[OUTPUT1BASELENGTH+data.length+2];
    int i = startOutput1(msg, n, typeId);
 
    longToBytes(data.length, msg, i, 2);
    i += 2;
    for (int d = 0 ; d < data.length ; d++) {
      msg[i++] = data[d];
    }

    setTime(msg, i);
    return msg;
  }
}
