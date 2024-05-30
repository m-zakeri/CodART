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

import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;

/**
 * Test probe to provide test data to the server-agent.
 *
* @author Teemu Kanstren
 */
public class TestProbe2 extends TestProbe {
  private int counter = 0;
  public static final String PROBE_DESCRIPTION = "Test Probe 2";
  public static final String TARGET_NAME = "Bob2";
  public static final String TARGET_TYPE = "Spam Filter";
  public static final String BM_CLASS = "configuration file";
  public static final String BM_NAME = "Bobby";
  public static final String BM_DESCRIPTION = "Provides the configuration file";

  public TestProbe2() {
    super(TARGET_NAME, TARGET_TYPE, BM_CLASS, BM_NAME, BM_DESCRIPTION, PROBE_DESCRIPTION, 1);
  }

  public BaseMeasure measure() {
//    String result = "test probe2 measure " + counter;
    String result = Integer.toString( counter % 100 );
    counter++;
    return new BaseMeasure(result);
  }
}