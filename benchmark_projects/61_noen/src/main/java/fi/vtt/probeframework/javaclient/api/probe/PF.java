package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.StartBuilder;
import fi.vtt.probeframework.javaclient.protocol.IO;
import fi.vtt.probeframework.javaclient.protocol.Configuration;
import fi.vtt.probeframework.javaclient.api.probe.PFTest;

/**
 * Used to control the high-level functionality of the PF.
 *
 * @author Teemu Kanstrén
 */
public class PF {
  private static boolean configured = false;

  public static void reset() {
    PFTest.reset();
  }

  private static synchronized void configure() {
    if (!configured) {
      Configuration.configure();
      configured = true;
    }
  }

  /**
   * Call this when a test case is starting. Sets up the basic identification information such as
   * project name, version, test name. Creates the protocol start message for test information.
   * If this is not called, the use of any probes will fail.
   *
   * @param test  Name of the test case that is starting.
   */
  public static void startTest(PFTest test) {
    configure();
    byte[] startMsg = new StartBuilder(test).startMsg();
    try {
      IO.send(startMsg);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }
}
