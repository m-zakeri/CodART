package fi.vtt.probeframework.javaclient.protocol.messages;

import fi.vtt.probeframework.javaclient.api.probe.PFTest;

//TODO this is not fully implemented, missing ID values from beginning
public class InputBuilder extends BaseBuilder {
  //id(1)+inputn(2)+datatype(1)+time(4)
  public static final int INPUT1BASELENGTH = 1+2+1+4;

  public InputBuilder(PFTest test) {
    super(test);
  }

  public int startInput1(byte[] msg, int inputN, byte dataType) {
    int i = 0;
    msg[i++] = 0x0a;
    longToBytes(inputN, msg, i, 2);
    i += 2;
    msg[i++] = dataType;
    return i;
  }
    
  public byte[] input1Msg(int n, boolean value) {
    byte[] msg = new byte[INPUT1BASELENGTH+1];
    int i = startInput1(msg, n, (byte)0x01);

    if (value) {
      msg[i++] = 0x01;
    } else {
      msg[i++] = 0x00;
    }

    setTime(msg, i);
    return msg;
  }

  public byte[] input1Msg(int n, long value) {
    byte[] msg = new byte[INPUT1BASELENGTH+8];
    int i = startInput1(msg, n, (byte)0x6);

    longToBytes(value, msg, i, 8);
    i += 8;

    setTime(msg, i);
    return msg;
  }

  public byte[] input1Msg(int n, String text) {
    byte[] msg = new byte[INPUT1BASELENGTH+text.length()+2];
    int i = startInput1(msg, n, (byte)0x8);

    stringToBytes(text, msg, i, 2);
    i += text.length()+2;

    setTime(msg, i);
    return msg;
  }

  public byte[] input1Msg(int n, byte[] data) {
    byte[] msg = new byte[INPUT1BASELENGTH+data.length+2];
    int i = startInput1(msg, n, (byte)0x9);
 
    longToBytes(data.length, msg, i, 2);
    i += 2;
    for (int d = 0 ; d < data.length ; d++) {
      msg[i++] = data[d];
    }

    setTime(msg, i);
    return msg;
  }
}
