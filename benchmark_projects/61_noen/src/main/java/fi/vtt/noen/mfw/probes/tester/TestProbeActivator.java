/*
 * Copyright (C) 2010-2011 VTT Technical Research Centre of Finland.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation;
 * version 2.1 of the License.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

package fi.vtt.noen.mfw.probes.tester;

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgentActivator;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEventBus;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import org.osgi.framework.BundleContext;

import java.util.Properties;

/**
 * OSGI activator for all the test probes.
 *
 * @author Teemu Kanstren
 */
public class TestProbeActivator extends BaseProbeAgentActivator {
  private final static Logger log = new Logger(TestProbeActivator.class);
  private TestProbe testProbe1 = null;
  private TestProbe testProbe1v2 = null;
  private TestProbe testProbe2 = null;
  private TestProbe testProbe3 = null;
  private TestProbe testProbe4 = null;
  private TestProbeWithCompareMode testProbeWithCompareMode = null;

  public TestProbeActivator() {
    super(log, Const.TEST_PROBE_AGENT_CONFIG_PREFIX);
  }

  //for testing
  public TestProbeActivator(Properties config) {
    super(log, config, Const.TEST_PROBE_AGENT_CONFIG_PREFIX);
  }

  public void start(BundleContext bc) throws Exception {
    ProbeEventBus eventBus = new ProbeEventBus(bc);
    testProbe1 = (TestProbe1) register(eventBus, bc, TestProbe1.class, 1);
    testProbe2 = (TestProbe2) register(eventBus, bc, TestProbe2.class, 2);
    //testprobewitherrors will throw an exception in the constructor, placing it here enables testing for successful registration of further probes
    TestProbeWithErrors error = (TestProbeWithErrors) register(eventBus, bc, TestProbeWithErrors.class, 6);
    testProbe3 = (TestProbe3) register(eventBus, bc, TestProbe3.class, 3);
    testProbe4 = (TestProbe4) register(eventBus, bc, TestProbe4.class, 4);
    testProbe1v2 = (TestProbe1v2) register(eventBus, bc, TestProbe1v2.class, 5);
    testProbeWithCompareMode = (TestProbeWithCompareMode) register(eventBus, bc, TestProbeWithCompareMode.class, 7);

    new ProbeEventBus(bc).event(testProbe1.getInformation(), "hello");
  }

  public void stop(BundleContext bundleContext) throws Exception {

  }


  public TestProbe getTestProbe1() {
    return testProbe1;
  }

  public TestProbe getTestProbe1v2() {
    return testProbe1v2;
  }

  public TestProbe getTestProbe2() {
    return testProbe2;
  }

  public TestProbe getTestProbe3() {
    return testProbe3;
  }

  public TestProbe getTestProbe4() {
    return testProbe4;
  }

  public TestProbeWithCompareMode getTestProbeWithCompareMode() {
    return testProbeWithCompareMode;
  }

}
