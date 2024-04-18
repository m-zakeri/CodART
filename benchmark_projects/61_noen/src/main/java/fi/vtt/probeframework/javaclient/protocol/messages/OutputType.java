package fi.vtt.probeframework.javaclient.protocol.messages;

public class OutputType {
  public static final OutputType BOOLEAN = new OutputType(1);
  public static final OutputType INTEGER = new OutputType(6);
  public static final OutputType TEXT = new OutputType(8);
  public static final OutputType BINARY = new OutputType(9);

  public final byte id;

  public OutputType(int id) {
    this.id = (byte) id;
  }
}
