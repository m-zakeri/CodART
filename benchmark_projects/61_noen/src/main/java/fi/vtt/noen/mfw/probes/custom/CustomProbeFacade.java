
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

import ch.ethz.ssh2.Connection;
import ch.ethz.ssh2.Session;
import ch.ethz.ssh2.StreamGobbler;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.Probe;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEventBus;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import org.osgi.framework.BundleContext;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Map;
import java.util.Properties;

/**
 * This class includes the functionality of custom probes as added from the SAC interface.
 *
 * @author Teemu Kanstren
 */
public class CustomProbeFacade implements Probe {
  private final static Logger log = new Logger(CustomProbeActivator.class);
  //these KEY_XXX values are the configuration values for each probe
  private static final String KEY_SCRIPT = "script";
  private static final String KEY_PASSWORD = "password";
  private static final String KEY_LOGIN = "login";
  private static final String KEY_TARGET = "target";
  private static final String KEY_BMDESCRIPTION = "bmdescription";
  //this allows us to provide events to the web-ui
  private final ProbeEventBus eventBus;
  //access to shared state/resources
  private final CustomCore core;
  //the 5 variables below are the ones given in the "add" parameter
  private final String targetName;
  private final String targetType;
  private final String bmClass;
  private final String bmName;
  private final String name;
  //the 5 variables below are the ones that can be set one at a time from the SAC interface
  private String target;
  private String login;
  private String password;
  private String script;
  private String bmDescription;

  public CustomProbeFacade(CustomCore core, BundleContext bc, String url) {
    this.core = core;
    //here the "url" is the "add" parameter value from CoreConfigurationHandler
    //it is expected to have the form "targettype/targetname/bmclass/bmname/probename"
    String[] items = url.split("/");
    targetType = items[0];
    targetName = items[1];
    bmClass = items[2];
    bmName = items[3];
    name = items[4];
    this.eventBus = new ProbeEventBus(bc);
    log.debug("Created probe with target type="+targetType+", target name="+targetName+" bmclass="+bmClass+" bmname="+bmName+" name="+name);
  }

  public ProbeInformation getInformation() {
    //this is how the generic probe-agent knows what this can measure
    return new ProbeInformation(targetName, targetType, bmClass, bmName, bmDescription, name, 1, null);
  }

  //here is the actual measurement done
  //give it a string value and return it, and the result will be delivered to the SAC
  public BaseMeasure measure() {
    //we can only run the SSH script if we have all required items: address, login, password, script
    String error = checkParameter(target, KEY_TARGET, "");
    error = checkParameter(login, KEY_LOGIN, error);
    error = checkParameter(password, KEY_PASSWORD, error);
    error = checkParameter(script, KEY_SCRIPT, error);
    if (error.length() > 0) {
      eventBus.event(getInformation(), "Unable to measure:"+error);
      return null;
    }

    try {
      String result = executeScript();
      log.debug("measurement result:" + result);
      return new BaseMeasure(result);
    } catch (Exception e) {
      throw new RuntimeException("Failed to perform measure for " + target + ", " + bmClass + ", ", e);
    }
  }

  private String checkParameter(String value, String name, String error) {
    if (value != null) {
      return error;
    }
    if (error.length() > 0) {
      error += ", ";
    }
    error += name;
    return error;
  }

  public void startProbe() {
  }

  public void stopProbe() {
  }

  //here we handle the setting of the parameters from the SAC
  public void setConfiguration(Map<String, String> configuration) {
    String target = configuration.get(KEY_TARGET);
    String login = configuration.get(KEY_LOGIN);
    String password = configuration.get(KEY_PASSWORD);
    String script = configuration.get(KEY_SCRIPT);
    String bmDescription = configuration.get(KEY_BMDESCRIPTION);
    if (target != null) {
      this.target = target;
    }
    if (login != null) {
      this.login = login;
    }
    if (password != null) {
      this.password = password;
    }
    if (script != null) {
      this.script = script;
    }
    if (bmDescription != null) {
      this.bmDescription = bmDescription;
    }
  }

  //return the current configuration parameters to the SAC when requested
  public Collection<ProbeConfiguration> getConfigurationParameters() {
    Collection<ProbeConfiguration> config = new ArrayList<ProbeConfiguration>();
    config.add(new ProbeConfiguration(KEY_TARGET, "Target address", true, target));
    config.add(new ProbeConfiguration(KEY_LOGIN, "Username for login", true, login));
    config.add(new ProbeConfiguration(KEY_PASSWORD, "Password for login", true, password));
    config.add(new ProbeConfiguration(KEY_BMDESCRIPTION, "BM Description", true, bmDescription));
    config.add(new ProbeConfiguration(KEY_SCRIPT, "SSH Script to collect the measure", true, script));
    return config;
  }

  public void init(Properties properties) {
  }

  //execute the script over SSH
  private String executeScript() throws Exception {
    //get the shared connection resource
    Connection connection = core.getConnection(target, login, password);
    log.debug("executing script on target:" + target);

    Session session = connection.openSession();
    session.execCommand(script);

    InputStream stdout = new StreamGobbler(session.getStdout());
    InputStream stderr = new StreamGobbler(session.getStderr());

    String output = readOutput(stdout);
    String errors = readOutput(stderr);

    log.debug("done reading, errors:"+errors);

    /* Close this session */
    session.close();
    return output;
  }

  private String readOutput(InputStream in) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(in));
    StringBuffer result = new StringBuffer();
    while (true) {
      String line = br.readLine();
      if (line == null)
        break;
      result.append(line);
      result.append("\n");
    }
    return result.toString();
  }
}
