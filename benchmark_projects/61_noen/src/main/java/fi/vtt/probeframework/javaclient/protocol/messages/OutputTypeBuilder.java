package fi.vtt.probeframework.javaclient.protocol.messages;

import fi.vtt.probeframework.javaclient.api.probe.PFTest;

public class OutputTypeBuilder extends BaseBuilder {

  public OutputTypeBuilder(PFTest test) {
    super(test);
  }

  public byte[] outputTypeMsg(OutputType type, int id, String name) {
    //+1 for the byte to store name size
    int namelen = 1+strlen(name, 1);
    int len = 1 + 1 + namelen + 1;
    byte[] msg = new byte[len];
    int i = 0;
    msg[i++] = 0x10;
    longToBytes(id, msg, i, 1);
    i++;
    stringToBytes(name, msg, i, 1);
    i += namelen;
    msg[i] = type.id;
    return msg;
  }
}
