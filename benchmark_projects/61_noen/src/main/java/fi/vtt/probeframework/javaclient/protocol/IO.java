package fi.vtt.probeframework.javaclient.protocol;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class IO {
  protected static OutputStream file = new NullStream();
  protected static OutputStream tcp = new NullStream();
  private static boolean configured = false;

  public static void reset() {
    file = new NullStream();
    tcp = new NullStream();
    configured = false;
  }

  public static synchronized void send(byte[] data) {
    try {
      file.write(data);
      tcp.write(data);
    } catch (IOException e) {
      // TODO Auto-generated catch block
      e.printStackTrace();
    }
  }
  
  private static class NullStream extends OutputStream {
    @Override
    public void write(int arg0) throws IOException {
    }
  }

  public static void config(String fileName, String ip, int port) {
    if (configured) {
      throw new IllegalStateException("IO already configured - runtime config not support");
    }
    configured = true;
    if (fileName != null) {
      try {
        file = new FileOutputStream(fileName);
      } catch (FileNotFoundException e) {
        // TODO Auto-generated catch block
        e.printStackTrace();
      }
    }
    if (tcp != null && ip != null && port > 0) {
      try {
        tcp = new Socket(ip, port).getOutputStream();
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
  }
}
