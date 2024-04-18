package fi.vtt.probeframework.javaclient.protocol;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import fi.vtt.probeframework.javaclient.protocol.messages.Precision;

public class Configuration {
  public static String fileName = null;
  public static String ip = null;
  public static int port = -1;
  public static Precision precision = Precision.MILLIS;
  public static boolean testMode = false;
  
  public static void configure() {
    try {
      configure(Configuration.class.getResourceAsStream("/pf.properties"));
    } catch (Exception e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }
  
  public static void configure(InputStream in) throws IOException {
    if (testMode) {
      return;
    }
    Properties config = new Properties();
    config.load(in);
    fileName = config.getProperty("filename");
    ip = config.getProperty("ip");
    try {
      port = Integer.parseInt(config.getProperty("port"));
    } catch (NumberFormatException e) {
      port = -1;
      //TODO:error log
    }
    IO.config(fileName, ip, port);
    String precision = config.getProperty("time-precision");
    if (precision != null) {
      if ("millis".equalsIgnoreCase(precision)) {
        Configuration.precision = Precision.MILLIS;
      } else if ("seconds".equalsIgnoreCase(precision)) {
        Configuration.precision = Precision.SECOND;
      } else if ("minute".equalsIgnoreCase(precision)) {
        Configuration.precision = Precision.MINUTE;
      }
    }
  }

}
