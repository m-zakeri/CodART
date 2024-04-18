package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.IO;
import fi.vtt.probeframework.javaclient.protocol.messages.OutputBuilder;
import fi.vtt.probeframework.javaclient.protocol.messages.OutputType;
import fi.vtt.probeframework.javaclient.protocol.messages.OutputTypeBuilder;
import fi.vtt.probeframework.javaclient.protocol.messages.BaseBuilder;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

/**
 * Base class from which actual probes inherit. Provides some basic functionality, such as
 * tracking all probe and message id's to make sure different probes keep their id values in
 * sequence, writing data to specified output stream and initializing overall framework state
 * when needed.
 * 
 * @author Teemu Kanstrén
 */
public abstract class BaseProbe {
  /** Builds data type messages to register probes. */
  protected OutputTypeBuilder typeBuilder;
  /** Builds different types of output messages. */
  protected OutputBuilder dataBuilder;
  /** Internally keeps track of probe id's to make sure they are unique and in sequence. */
  //TODO: onko tällä jotain käyttöä? on aina 1
  private static int nextProbeId = 1;
  /** Internally keeps track of message id's to make sure they are unique and in sequence. */
  private static int nextMsgId = 1;
  /** Synchronization lock for passing out message id values. */
  private static Object lock = new Object();
  /** Stores the type id of the created probe, as in user defined type (user name, sensor value, ...) */
  protected byte typeId = 0;
  /** Test to which this probe is tied to. */
  private final PFTest test;
  /**
   * The test for which data has been previously passed over the binary protocol.
   * Used to differentiate if a new test id msg needs to be sent in binary protocol when sending data
   * for a (new) test case.
   */
  private static PFTest currentTest = null;

  /** Reset static values for testing */
  //TODO: is this also needed for new test case ?
  public static void reset() {
    nextProbeId = 1;
    nextMsgId = 1;
    currentTest = null;
  }

  /**
   * Initializes PF, registers probe with output type msg.
   *
   * @param type    Type as allowed by the PF (int, long, float, string, ...)
   * @param typeId  Type as anything created by user (sensor reading, user name, ...)
   * @param name    Name of user defined type, associated with typeId.
   */
  public BaseProbe(PFTest test, OutputType type, byte typeId, String name) {
    this.test = test;
    this.typeId = typeId;
    dataBuilder = new OutputBuilder(test);
    typeBuilder = new OutputTypeBuilder(test);
    if (currentTest == null) {
      currentTest = test;
    }
    send(typeBuilder.outputTypeMsg(type, typeId, name));
  }

  /**
   * Provides synchronized message id handling.
   *
   * @return  Id for the next message to be written to the output stream(s).
   */
  protected static int nextMsgId() {
    //TODO: is lock required or can we synchronize the method?
    synchronized (lock) {
      return nextMsgId++;
    }
  }
//TODO: pitääkö uuden startmsg:n jälkeen lähettää testid jos eri testille dataa kuin mille startmsg? eli onko startmsg sama vaikutus kuin testid (tunniste) msg?
  /**
   * Send data to configured output stream(s).
   *
   * @param data  Data to be sent.
   */
  protected synchronized void send(byte[] data) {
    if (test.equals(currentTest) == false) {
//      System.out.println("test change:"+currentTest.getTestId()+" -> "+test.getTestId());
      currentTest = test;
      byte[] testIdData = new byte[4];
      testIdData[0] = 0;
      BaseBuilder.longToBytes(test.getTestId(), testIdData, 1, 3);
      IO.send(testIdData);
    }
    IO.send(data);
  }
}
