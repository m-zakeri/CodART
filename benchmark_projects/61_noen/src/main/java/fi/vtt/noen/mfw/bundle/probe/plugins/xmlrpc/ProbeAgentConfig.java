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

package fi.vtt.noen.mfw.bundle.probe.plugins.xmlrpc;

import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Properties;

/**
 * Defines a configuration for a probe-bundle.
 *
 * @author Teemu Kanstren
 */
public class ProbeAgentConfig {
  private final static Logger log = new Logger(ProbeAgentConfig.class);
  //only initialize it once
  private boolean initialized = false;
  //port where the xmlrpc server will listen to the incoming messages
  private int port = -1;
  //default interval between sending the keep-alive messages
  private static final int DEFAULT_KEEPALIVE_INTERVAL = 1000;
  //default interval between trying to reconnect to server
  private static final int DEFAULT_RETRY_DELAY = 5000;
  //actual keep alive interval for this thread
  private int keepAliveInterval;
  //the server-agent where the keep-alive messages are sent
  private ServerAgent destination = null;
  //time to wait between retrying a failed connection to a server-agent
  private int retryDelay;
  //is this a local connection or distributed
  private boolean localInUse = false;
  //default subscription check interval
  private static final int DEFAULT_SUBSCRIPTION_CHECK_INTERVAL = 20000;
  //subscription checking interval
  private int subscriptionCheckInterval;

  public ProbeAgentConfig(int port, String destinationUrl, int keepAliveInterval, int retryDelay, int subscriptionCheckInterval) {
    init(port, destinationUrl, keepAliveInterval, retryDelay, subscriptionCheckInterval);
  }

  public ProbeAgentConfig(int port, ServerAgent server, int keepAliveInterval, int retryDelay, int subscriptionCheckInterval) {
    init(port, server, keepAliveInterval, retryDelay, subscriptionCheckInterval);
  }

  public ProbeAgentConfig(InputStream in) {
    init(in);
  }

  public ProbeAgentConfig() {
  }

  private void init(int port, String destinationUrl, int keepAliveInterval, int retryDelay, int subscriptionCheckInterval) {
    if (port < 0) {
      //this means we need to use a local connection
      init(port, (ServerAgent)null, keepAliveInterval, retryDelay, subscriptionCheckInterval);
      return;
    }
    URL url = null;
    try {
      log.debug("Creating connection to server agent at:"+destinationUrl);
      url = new URL(destinationUrl);
    } catch (MalformedURLException e) {
      log.error("Unable to create connection with URL:" + destinationUrl, e);
    }
    //create the component to send XMLRPC requests to the server-agent
    XmlRpcServerClient server = new XmlRpcServerClient(url);
    init(port, server, keepAliveInterval, retryDelay, subscriptionCheckInterval);
  }

  private void init(int port, ServerAgent server, int keepAliveInterval, int retryDelay, int subscriptionCheckInterval) {
    if (initialized) {
      throw new IllegalStateException("Trying to initialize configuration twice");
    }
    log.debug("initializing: XMLRPC server port = " + port);
    this.port = port;
    if (port < 0) {
      localInUse = true;
    }
    this.keepAliveInterval = keepAliveInterval;
    this.destination = server;
    this.retryDelay = retryDelay;
    this.subscriptionCheckInterval = subscriptionCheckInterval;
    initialized = true;
  }

  public boolean isLocalInUse() {
    return localInUse;
  }

  public ServerAgent getDestination() {
    return destination;
  }

  public void setDestination(ServerAgent destination) {
    this.destination = destination;
  }

  public int getProbeAgentServerPort() {
    return port;
  }

  public int getKeepAliveInterval() {
    return keepAliveInterval;
  }

  public int getRetryDelay() {
    return retryDelay;
  }
  
  public int getSubscriptionCheckInterval() {
    return subscriptionCheckInterval;
  }

  /**
   * Reads the initial configuration from the properties file given as the input stream.
   *
   * @param in The data for the properties file.
   */
  private void init(InputStream in) {
    if (initialized) {
      throw new IllegalStateException("Trying to initialize configuration twice");
    }
    Properties properties = new Properties();
    try {
      properties.load(in);
    } catch (IOException e) {
      throw new RuntimeException("Failed to load properties from given inputstream", e);
    }
    log.debug("Loaded properties:" + properties);
    String destinationUrl = properties.getProperty(Const.MFW_SERVER_URL_KEY);
    String portValue = properties.getProperty(Const.PROBE_AGENT_PORT_KEY);
    int port = -1;
    if (portValue != null) {
      //we leave it at -1 as undefined if nothing found in configuration. this defaults to local node connection.
      port = Integer.parseInt(portValue);
    }
    String reportIntervalValue = properties.getProperty(Const.KEEP_ALIVE_INTERVAL);
    int reportInterval = DEFAULT_KEEPALIVE_INTERVAL;
    if (reportIntervalValue != null) {
      try {
        reportInterval = Integer.parseInt(reportIntervalValue);
      } catch (NumberFormatException e) {
        log.error("Failed to read report interval from config, gof:" + reportIntervalValue + ". Using defaults.");
      }
    }
    String retryDelayValue = properties.getProperty(Const.RETRY_DELAY);
    int retryDelay = DEFAULT_RETRY_DELAY;
    if (retryDelayValue != null) {
      try {
        retryDelay = Integer.parseInt(retryDelayValue);
      } catch (NumberFormatException e) {
        log.error("Failed to read retry delay from config, gof:"+retryDelayValue+". Using defaults.");
      }
    }
    String checkIntervalValue = properties.getProperty(Const.SUBSCRIPTION_CHECK_INTERVAL);
    int checkInterval = DEFAULT_SUBSCRIPTION_CHECK_INTERVAL;
    if (checkIntervalValue != null) {
      try {
        checkInterval = Integer.parseInt(checkIntervalValue);
      } catch (NumberFormatException e) {
        log.error("Failed to read subscription check interval from config, gof:" + checkIntervalValue + ". Using defaults.");
      }
    }
    if (destinationUrl == null) {
      init (-1, (ServerAgent)null, reportInterval, retryDelay, checkInterval);
    } else {
      init(port, destinationUrl, reportInterval, retryDelay, checkInterval);
    }
  }
}
