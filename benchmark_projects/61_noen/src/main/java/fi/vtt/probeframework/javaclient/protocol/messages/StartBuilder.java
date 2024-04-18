package fi.vtt.probeframework.javaclient.protocol.messages;

import java.util.Calendar;

import fi.vtt.probeframework.javaclient.api.probe.PFTest;

public class StartBuilder extends BaseBuilder {

  public StartBuilder(PFTest test) {
    super(test);
  }

  public byte[] startMsg() {
    //+1 for id + 1 for byte-order + 1 for protocol version
    //+ project name size (1+number of characters)
    //+ test description size (1+number of characters)
    //+1 for empty versionname
    //+1 for empty targetname
    //+ description size (1+number of characters)
    //+1 for time accuracy + 4 for starttime + 3 for packet id
    int projLen = strlen(test.getProject()) + 1; //this is project name
    int testLen = strlen(test.getName()) + 1;  //test name
    int descLen = strlen(test.getSuite()) + 1; //suite is description is spec
    int versionLen = strlen(test.getProjectVersion()) + 1; //project version
    int targetLen = strlen(test.getTestTarget()) + 1; //test target
    //+1 for empty projectname + 1 for empty testcase number
    byte[] msg = new byte[1 + 1 + 1 + projLen + versionLen + testLen + targetLen + descLen + 1 + 4 + 3];

    int i = 0;
    //ID for start binary message
    msg[i++] = (byte) 0xFF;
    //big-endian byte order = FF
    msg[i++] = (byte) 0xFF;
    //protocol version
    msg[i++] = 2;
    //project name
    stringToBytes(test.getProject(), msg, i, 1);
    i += projLen;
    //project version
    stringToBytes(test.getProjectVersion(), msg, i, 1);
    i += versionLen;
    //test case identifier
    stringToBytes(test.getName(), msg, i, 1);
    i += testLen;
    //test target
    stringToBytes(test.getTestTarget(), msg, i, 1);
    i += targetLen;
    //suite name (test description)
    stringToBytes(test.getSuite(), msg, i, 1);
    i += descLen;
    msg[i++] = test.getAccuracy().id;
    
    Calendar cal = Calendar.getInstance();
    cal.set(2007, Calendar.JANUARY, 1, 0, 0, 0);
    long baseTime = cal.getTime().getTime();
    long millis = test.startTime();
    millis -= baseTime;
    millis /= 1000;
    longToBytes(millis, msg, i, 4);
    i+=4;
    //TODO for now only one connection from a VM is supported
    longToBytes(test.getTestId(), msg, i, 3);
    return msg;
  }

  private int strlen(String testDescription) {
    if (testDescription == null) {
      return 0;
    }
    int descLen = testDescription.length();
    if (descLen > 255) {
      descLen = 255;
    }
    return descLen;
  }

}
