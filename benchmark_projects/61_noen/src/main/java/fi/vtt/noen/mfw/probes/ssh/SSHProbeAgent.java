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

package fi.vtt.noen.mfw.probes.ssh;

import ch.ethz.ssh2.Connection;
import ch.ethz.ssh2.SCPClient;
import ch.ethz.ssh2.Session;
import ch.ethz.ssh2.StreamGobbler;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseProbeAgent;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;

/**
 * A probe-agent for performing measurements over the SSH protocol. Connects to the configured IP address,
 * sends a (configured) script file over with SCP to the host, does a login over SSH using the given credentials,
 * and uses the configured shell command to execute the script in question. Provides the system.out output of the
 * script as a base measure.
 *
 * @author Teemu Kanstren
 */
public class SSHProbeAgent extends BaseProbeAgent {
  private final static Logger log = new Logger(SSHProbeAgent.class);
  private final static Map<String, Connection> connections = new HashMap<String, Connection>();
  //filename of the script. should be relative to the "working directory"
  private String filename = null;
  private String username = null;
  private String password = null;
  //shell command to execute the script
  private String command = null;
  private String errors = null;

  public void init(Properties properties) {
    super.init(properties);
    filename = properties.getProperty((Const.SSH_SCRIPT_FILENAME));
    username = properties.getProperty((Const.SSH_USERNAME));
    password = properties.getProperty((Const.SSH_PASSWORD));
    command = properties.getProperty((Const.SSH_SCRIPT_COMMAND));
  }

  public BaseMeasure measure() {
    try {
      String result = executeScript();
      log.debug("measurement result:" + result);
      return new BaseMeasure(result);
    } catch (Exception e) {
      throw new RuntimeException("Failed to perform measure for " + pi.getTargetName()+ ", " + pi.getBmClass() + ", ", e);
    }
  }

  public void startProbe() {

  }

  public void stopProbe() {
    for (Connection connection : connections.values()) {
      connection.close();
    }
  }

  public Collection<ProbeConfiguration> getConfigurationParameters() {
    Collection<ProbeConfiguration> config = getBaseConfigurationParameters();
    try {
      FileInputStream file = new FileInputStream(filename);
      String commands = readOutput(file);
      config.add(new ProbeConfiguration(Const.SSH_SCRIPT_FILE_CONTENTS, "Script to collect the BM", true, commands));
    } catch (IOException e) {
      log.error("Error while reading file:" + filename, e);
      throw new RuntimeException("Error reading file:" + filename, e);
    }
    //with hashset this replaces the original
    config.add(new ProbeConfiguration(Const.PROBE_TARGET_NAME, "Target IP address", true, pi.getTargetName()));
    config.add(new ProbeConfiguration(Const.SSH_SCRIPT_FILENAME, "Script file name", true, filename));
    config.add(new ProbeConfiguration(Const.SSH_USERNAME, "User name for login", true, username));
    config.add(new ProbeConfiguration(Const.SSH_PASSWORD, "Password for login", true, password));
    config.add(new ProbeConfiguration(Const.SSH_SCRIPT_COMMAND, "Command to execute script", true, command));
    return config;
  }

  public void setConfiguration(Map<String, String> config) {
    setBaseConfigurationParameters(config);
    try {
      String commands = config.get(Const.SSH_SCRIPT_FILE_CONTENTS);
      FileOutputStream file = new FileOutputStream(filename);
      file.write(commands.getBytes());
      file.close();
    } catch (IOException e) {
      throw new RuntimeException("Failed to write to file:" + filename, e);
    }
  }

  //executes the configured shell script on the configured target
  private String executeScript() throws Exception {
    String targetName = pi.getTargetName();
    Connection conn = connections.get(targetName);
    if (conn == null) {
      conn = new Connection(targetName);
      log.debug("connecting now to:"+targetName);
      /* Now connect */
      conn.connect();
      log.debug("connected ok");
      boolean authenticated = conn.authenticateWithPassword(username, password);

      if (!authenticated)
        throw new IOException("Authentication failed.");

      log.debug("authenticated ok");
      connections.put(targetName, conn);
    }
    log.debug("executing script on target:"+targetName);


    SCPClient client = conn.createSCPClient();
    client.put(filename, ".");

    log.debug("script file moved to server");
    Session sess = conn.openSession();
    sess.execCommand(command + " " + filename);

    InputStream stdout = new StreamGobbler(sess.getStdout());
    InputStream stderr = new StreamGobbler(sess.getStderr());

    String output = readOutput(stdout);
    errors = readOutput(stderr);

    System.out.println("done reading, errors:"+errors);

    /* Show exit status, if available (otherwise "null") */
//    System.out.println("ExitCode: " + sess.getExitStatus());
    /* Close this session */
    sess.close();
    /* Close the connection */
    //conn.close();
    return output;
  }

  /**
   * This is just for testing.
   *
   * @return Error messages from remote host.
   */
  public String getErrors() {
    return errors;
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

  //for testing
  public static void main(String[] args) throws Exception {
    /* Create a connection instance */
    Connection conn = new Connection("192.168.60.128");

    /* Now connect */
    conn.connect();

    /* Authenticate.
     * If you get an IOException saying something like
     * "Authentication method password not supported by the server at this stage."
     * then please check the FAQ.
     */
    String username = "hii";
    String password = "haa";
    String filename = "java\\distro\\distro.zip";
    boolean authenticated = conn.authenticateWithPassword(username, password);

    if (authenticated == false)
      throw new IOException("Authentication failed.");

    SCPClient client = conn.createSCPClient();
    client.put(filename, ".");
    conn.close();
  }
}
