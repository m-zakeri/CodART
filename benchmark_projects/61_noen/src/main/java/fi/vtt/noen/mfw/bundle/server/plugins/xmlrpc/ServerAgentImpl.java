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

package fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.EventType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.BaseMeasure;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeInformation;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMReport;
import org.osgi.framework.BundleContext;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;
import java.util.Map;
import java.util.Properties;

/**
 * Implements the basic server-bundle functionality for probe-agents to connect to. The ServerPluginImpl provides
 * the interface for the client (e.g. SAC) to connect to.
 *
 * @author Teemu Kanstren
 */
public class ServerAgentImpl extends BasePlugin implements ServerAgent, RegistryUser {
  private final static Logger log = new Logger(ServerAgentImpl.class);
  //is this started? to avoid several starts if we get several calls from OSGI
  private boolean started = false;
  //http server to listen to for xmlrpc messages
  private XmlRpcServerServer server;
  //access to overall runtime state
  private RegistryPlugin registry;
  //where we listen to for xmlrpc messages
  private final int port;
  private boolean localInUse = false;

  public ServerAgentImpl(BundleContext bc, int port, Boolean localInUse) {
    super(bc, log);
    if (localInUse != null) {
      this.localInUse = localInUse;
    }
    //localinuse is non-null in testing
    if (port <= 0 && localInUse == null) {
      try {
        InputStream in = new FileInputStream(Const.CONFIGURATION_FILENAME);
        Properties props = new Properties();
        props.load(in);
        port = Integer.parseInt(props.getProperty(Const.SERVER_AGENT_PORT_KEY));
        if (props.getProperty(Const.LOCAL_LINK_IN_USE) != null) {
          this.localInUse = true;
        }
      } catch (IOException e) {
        throw new RuntimeException("Failed to read configuration file '" + Const.CONFIGURATION_FILENAME + "'", e);
      } catch (NumberFormatException ne) {
        log.error("Unable to parse port number from configuration. Assuming local connection.", ne);
        this.localInUse = true;
      }
    }
    this.port = port;
  }

  //called from OSGI bundle.start()
  public void startAgent() {
    if (started) {
      throw new IllegalStateException("Trying to start the server while already started - cannot be started more than once.");
    }
    started = true;
    if (port > 0) {
      server = new XmlRpcServerServer(port, this);
      server.start();
    }
    log.debug("Started XMLRPC server on port " + port);
    RegistryServiceListener listener = new RegistryServiceListener(bc, log, this);
    listener.init();
  }

  public void setRegistry(RegistryPlugin registry) {
    log.debug("Setting registry:"+registry);
    this.registry = registry;
  }

  //called from OSGI bundle.stop()
  public void stopAgent() {
    started = false;
    if (port > 0) {
      server.stop();
    }
  }

  /**
   * A measurement value from the probe-agent.
   *
   * @param time Measurement time.
   * @param measureURI BM Identifier.
   * @param precision Prevision of measurement.
   * @param data The value itself. Only strings are currently supported, others can be added as needed.
   */
  public boolean measurement(long time, String measureURI, int precision, String data, long subscriptionId) {
    try {
      log.debug("received String measure for:"+measureURI);
      BMDescription bm = registry.descriptionFor(measureURI);
      if (bm == null) {
        return false;
      }
      Value value = new Value(bm, precision, data, time, subscriptionId);
      bb.process(value);
    } catch (Exception e) {
      handleException(e, measureURI, precision, data);
    }
    return true;
  }

  /**
   * For probe-agents to report errors. These are basically turned into events noting that it is an error
   * reported from the probe-agent.
   *
   * @param time Time when the event was observed.
   * @param msg The message describing the error/event.
   */
  public void event(long time, String type, String source, String msg, long subscriptionId) {
    ServerEvent event = new ServerEvent(time, EventType.valueOf(type), source, msg, subscriptionId);
    bb.process(event);
  }


  //a probe-agent noting that it is still alive
  public boolean keepAlive(long probeId) {
    try {
      return registry.processKeepAlive(probeId);
    } catch (Exception e) {
      handleException(e, probeId);
      return false;
    }
  }

  //a probe-agent registering itself
  public synchronized long register(Map<String, String> properties) {
    log.info("Probe is registering:"+properties);
    try {
      String url = properties.get(Const.XMLRPC_URL);
      //local link means we are making local connect,
      //"http" means that the user manually defined the URL in probe-agent configuration
      if (url == null || (!url.equals(Const.LOCAL_LINK_ENDPOINT_URL) && !url.startsWith("http://"))) {
        String port = properties.get(Const.XMLRPC_PORT);
        String ip = MfwXmlRpcServlet.getClientIp();
        String newURL = "http://" + ip + ":" + port + "/xmlrpc";
        properties.put(Const.XMLRPC_URL, newURL);
        log.debug("set new XMLRPC URL:"+newURL);
      }
      log.debug("Registering with URL:"+properties.get(Const.XMLRPC_URL));
      long probeId = registry.registerProbe(properties);
      log.debug("Registration done:"+probeId);
      return probeId;
    } catch (Exception e) {
      handleException(e, properties);
      throw new RuntimeException("Error in registering probe information", e);
    }
  }

  //a probe-agent unregistering itself.. currently not clear what it should do, or if it is needed, so nothing is done
  public void unregister(long probeId) {

  }
 
  public void checkSubscriptions(long probeId, List<Long> subscriptionIds) {
    registry.checkSubscriptions(probeId, subscriptionIds);
    
  }

  //log the exception..
  private void handleException(Exception e, Object... data) {
    String parameters = "::";
    for (Object param : data) {
      parameters += param;
      parameters += ",";
    }
    log.error("Error processing a message from client:" + parameters, e);
  }

  public boolean BMReport(long time, String measureURI, String value,
      long subscriptionId, boolean matchReference, String reference) {
    try {
      log.debug("received BM report for:"+measureURI);
      log.debug("subscriptionId:"+subscriptionId);
/*      BMDescription bm = registry.descriptionFor(measureURI);
      if (bm == null) {
        return false;
      }*/
      BMReport bmReport = new BMReport(measureURI, value, time, subscriptionId, matchReference, reference);
      bb.process(bmReport);
    } catch (Exception e) {
      handleException (e, measureURI, value);
    }
    return true;
  }

  
}
