package fi.vtt.probeframework.javaclient.protocol.messages;

import fi.vtt.probeframework.javaclient.api.probe.PFTest;

import java.io.UnsupportedEncodingException;

public class BaseBuilder {
  private static final String CHARSET = "US-ASCII";
  protected final PFTest test;

  public BaseBuilder(PFTest test) {
    this.test = test;
  }

  /**
   * Calculate length of a given string. Takes into consideration the
   * number of bytes used to store the string length and gives this
   * max value if string is longer. Length is calculated from the byte
   * array with US-ASCII encoding, in case unicode chars would be used
   * that would make the array length different from string length.
   * 
   * @param str     String to process
   * @param bytes   Number of bytes used to hold the length, defining max length of bytearray
   * @return        Length of string as bytes, within given constraints
   */
  public int strlen(String str, int bytes) {
    if (str == null) {
      return 0;
    }
    int len = 0;
    try {
      len = str.getBytes(CHARSET).length;
    } catch (UnsupportedEncodingException e) {
      // TODO exception handling
      e.printStackTrace();
    }
    int maxlen = (int)Math.pow(2, bytes*8)-1;
    if (len > maxlen) {
      len = maxlen;
    }
    return len;
  }

  /**
   * Convert a string into an array of bytes and copy the result into the given
   * bytearray starting at the given location. Respects the given maximum size
   * by leaving out any data that does not fit into given size. Size is given as
   * the number of bytes that is used to hold the length. Thus 1 equals max of
   * 2^8-1=255 characters and 2 equals 2^16-1=65535 characters and so on.
   *
   * @param str   String to convert
   * @param msg   The bytearray into which the converted bytes are stored
   * @param start Start index for storing in bytearray
   * @param bytes Number of bytes to hold size (1=255, 2=65535)
   */
  public void stringToBytes(String str, byte[] msg, int start, int bytes) {
    int len = strlen(str, bytes);
//    System.out.println("strlen:"+len);
    longToBytes(len, msg, start, bytes);
    if (len == 0) {
      //no need to copy anything, avoid possible NPE
      return;
    }
    start += bytes;
    byte[] strBytes = null;
    try {
      strBytes = str.getBytes(CHARSET);
    } catch (UnsupportedEncodingException e) {
      // TODO exception handling
      e.printStackTrace();
    }
    System.arraycopy(strBytes, 0, msg, start, len);
  }

  public static void longToBytes(long value, byte[] msg, int start, int bytes) {
    for (int i = bytes-1 ; i >= 0 ; i--) {
      msg[start+i] = (byte)value;
      value >>>= 8;
    }
  }

  public void setTime(byte[] msg, int index) {
    longToBytes(test.timeDelta(), msg, index, 4);
  }
  
}
