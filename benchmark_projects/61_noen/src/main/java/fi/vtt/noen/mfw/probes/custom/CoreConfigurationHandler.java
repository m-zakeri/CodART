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

package fi.vtt.noen.mfw.probes.custom;

import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import org.osgi.framework.BundleContext;

import java.util.Collection;
import java.util.Map;
import java.util.Properties;

/**
 * @author Teemu Kanstren
 */
public class CoreConfigurationHandler implements Probe {
  private final CustomCore core;
  //this is the OSGI reference that allows all the plugins to find each other
  private final BundleContext bc;

  public CoreConfigurationHandler(CustomCore core, BundleContext bc) {
    this.core = core;
    this.bc = bc;
  }

  public ProbeInformation getInformation() {
    //you should in practice replace the values here with something of your own.
    //as this probe is there just to let new probes be installed on the fly, there is no valid measurement
    return new ProbeInformation("CustomTarget1", "ProbeConfigurationHandler", "None", "None", "None", "This probe is only a facade to add other probes", 0, null);
  }

  public BaseMeasure measure() {
    //always returns null, causing endless errors in the MFW "events" page when activated
    return null;
  }

  public void startProbe() {
  }

  public void stopProbe() {
  }

  public void setConfiguration(Map<String, String> configuration) {
    String url = configuration.get("add");
    //if there is a parameter named "add" present, we create a new probe from the information embedded in it
    //check the CustomProbeFacade constructor for the parsing of the data.
    //NOTE: There is no real error handling here, you should check your parameters for real
    if (url != null) {
      CustomProbeFacade facade = new CustomProbeFacade(core, bc, url);
      bc.registerService(Probe.class.getName(), facade, null);
    }
  }

  public Collection<ProbeConfiguration> getConfigurationParameters() {
    return null;
  }

  public void init(Properties properties) {
  }
}
