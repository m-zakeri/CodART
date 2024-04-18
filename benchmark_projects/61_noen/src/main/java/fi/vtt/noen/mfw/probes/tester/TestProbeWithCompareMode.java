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

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;

/**
 * Test probe to provide test data to the server-agent.
 *
* @author Teemu Kanstren
 */
public class TestProbeWithCompareMode extends TestProbe {
  private int counter = 0;
  private int value = 0;
  public static final String PROBE_DESCRIPTION = "Test Probe with compare mode";
  public static final String TARGET_NAME = "Bob5";
  public static final String TARGET_TYPE = "Bob";
  public static final String BM_CLASS = "compare tester";
  public static final String BM_NAME = "Bobby5";
  public static final String BM_DESCRIPTION = "Provides compare mode testing values";
  private final long DELAY = 30000;
  private long oldTime = 0;
  private long currentTime = 0;

  public TestProbeWithCompareMode() {
    super(TARGET_NAME, TARGET_TYPE, BM_CLASS, BM_NAME, BM_DESCRIPTION, PROBE_DESCRIPTION, 1);
    addConfig("mode", "to use compare or normal mode", true, "compare");
  }
  
  private void addConfig(String name, String description, boolean mandatory, String value) {
    ProbeConfiguration pc = new ProbeConfiguration(name, description, mandatory, value);
    addConfigurationParameter(pc);
  }

  public BaseMeasure measure() {
//    if (counter % 10 == 0) {
//      value = counter;
//    }
    currentTime = System.currentTimeMillis();
    if (currentTime > (oldTime + DELAY)) {
      oldTime = currentTime;
      value = counter;
    }    
    String result = "compare mode test probe value " + value;    
    counter++;
    return new BaseMeasure(result);
  }
}
