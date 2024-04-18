package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.OutputType;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

public class TextProbe extends BaseProbe {
  public TextProbe(PFTest test, byte typeId, String name) {
    super(test, OutputType.TEXT, typeId, name);
  }

  public void data(String data) {
    byte[] msg = dataBuilder.output1Msg(nextMsgId(), typeId, data);
    send(msg);
  }
}
