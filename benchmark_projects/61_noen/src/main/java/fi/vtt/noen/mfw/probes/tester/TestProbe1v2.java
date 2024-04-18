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

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;

/**
 * Test probe to provide test data to the server-agent.
 * The same as TestProbe1 but with a higher precision.
 *
 * @author Teemu Kanstren
 */
public class TestProbe1v2 extends TestProbe {
  private final static Logger log = new Logger(TestProbe1v2.class);
  private int counter = 0;

  public static final String PROBE_DESCRIPTION = "Test Probe 1v2";
  public static final String TARGET_NAME = "Bob1";
  public static final String TARGET_TYPE = "Firewall";
  public static final String BM_CLASS = "Configuration file";
  public static final String BM_NAME = "Bobby1";
  public static final String BM_DESCRIPTION = "Reads the configuration, but only better";

  public TestProbe1v2() {
    super(TARGET_NAME, TARGET_TYPE, BM_CLASS, BM_NAME, BM_DESCRIPTION, PROBE_DESCRIPTION, 2);
    addConfig("x", "x coord", true, "0px");
    addConfig("y", "y coord", true, "0px");
  }

  private void addConfig(String name, String description, boolean mandatory, String value) {
    ProbeConfiguration pc = new ProbeConfiguration(name, description, mandatory, value);
    addConfigurationParameter(pc);
  }

  public BaseMeasure measure() {
    String result = "test probe1v2 measure " + counter;
    counter++;
    log.debug("Performed measure:" + result);
    return new BaseMeasure(result);
  }

}
