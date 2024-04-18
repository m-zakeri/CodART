package fi.vtt.probeframework.javaclient.api.probe;

import fi.vtt.probeframework.javaclient.protocol.messages.Precision;

/**
 * Describes a test case as linked to all the probes created for the Probe Framework.
 *
 * @author Teemu Kanstrén
 */
public class PFTest {
  /** All tests need an ID, this is used to give them a unique id value. */
  private static int globalTestId = 1;

  /** ID of the test case that this object represents. */
  private int testId = 0;
  /** When was the test started? Full time value as milliseconds. */
  private long startTime = 0;
  /** Project name to which the test is linked. */
  private String project = "PF-analysis";
  /** Accuracy of timing used to represent the time for probe data. */
  private Precision accuracy = Precision.SECOND;
  /** Name of the test suite to which this test belongs. */
  private String suite = "PF-suite";
  /** Name of this test case. */
  private String name = "PF-test";
  private String projectVersion = "1";
  private String testTarget = "SUT";

  /**
   * Used to create next id value for tests.
   *
   * @return  Id for next test case.
   */
  private static synchronized int nextId() {
    return globalTestId++;
  }

  /**
   * Resets id values (for testing).
   */
  protected static synchronized void reset() {
    globalTestId = 1;
  }

  /**
   * Initializes the test object and also sets start time from system clock.
   *
   * @param project   Project name.
   * @param accuracy  Time accuracy.
   * @param name      Name of test case.
   * @param suite     Name of test suite.
   */
  public PFTest(String project, String projectVersion, String testTarget, Precision accuracy, String name, String suite) {
    this.project = project;
    this.projectVersion = projectVersion;
    this.testTarget = testTarget;
    this.accuracy = accuracy;
    this.suite = suite;
    this.name = name;
    testId = nextId();
    startTime = System.currentTimeMillis();
  }

  public int getTestId() {
    return testId;
  }

  public String getProject() {
    return project;
  }

  public Precision getAccuracy() {
    return accuracy;
  }

  public String getSuite() {
    return suite;
  }

  public String getName() {
    return name;
  }

  public String getProjectVersion() {
    return projectVersion;
  }

  public String getTestTarget() {
    return testTarget;
  }

  /**
   * Gives the difference of time using the chosen precision.
   *
   * @return  Time diff from test start to now, in millis, seconds, minutes, ...
   */
  public long timeDelta() {
    long divider = 1;
    if (accuracy == Precision.SECOND) {
      divider = 1000;
    } else if (accuracy == Precision.MINUTE) {
      divider = 1000*60;
    }
    return (System.currentTimeMillis()-startTime)/divider;
  }

  public long startTime() {
    return startTime;
  }

  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    PFTest pfTest = (PFTest) o;

    if (startTime != pfTest.startTime) return false;
    if (testId != pfTest.testId) return false;
    if (accuracy != null ? !accuracy.equals(pfTest.accuracy) : pfTest.accuracy != null) return false;
    if (name != null ? !name.equals(pfTest.name) : pfTest.name != null) return false;
    if (project != null ? !project.equals(pfTest.project) : pfTest.project != null) return false;
    if (suite != null ? !suite.equals(pfTest.suite) : pfTest.suite != null) return false;

    return true;
  }

  public int hashCode() {
    int result;
    result = testId;
    result = 31 * result + (int) (startTime ^ (startTime >>> 32));
    result = 31 * result + (project != null ? project.hashCode() : 0);
    result = 31 * result + (accuracy != null ? accuracy.hashCode() : 0);
    result = 31 * result + (suite != null ? suite.hashCode() : 0);
    result = 31 * result + (name != null ? name.hashCode() : 0);
    return result;
  }
}
