package fi.vtt.probeframework.javaclient.protocol.messages;

public class Precision {
  //public static final Precision NANOS = new Precision(0);
  //public static final Precision MICROS = new Precision(1);
  public static final Precision MILLIS = new Precision(2);
  public static final Precision SECOND = new Precision(3);
  public static final Precision MINUTE = new Precision(4);

  public final byte id;

  public Precision(int id) {
    this.id = (byte)id;
  }
}
