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

package fi.vtt.noen.mfw.bundle.server.plugins.sac;

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.mfwservice.SACMFWImpl;
import fi.vtt.noen.mfw.bundle.server.plugins.sac.sacclient.SACClient;
import org.osgi.framework.BundleContext;

import javax.xml.ws.Endpoint;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;


/**
 * OSGI activator for the SAC plugin.
 *
 * @author Teemu Kanstren
 */
public class SACPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(SACPluginActivator.class);
  private SACPlugin sac;
  //MFW web service endpoint
  private Endpoint endpoint = null;
  //MFW web service endpoint implementor
  private Object implementor = null;
  //port for MFW web service endpoint
//  private int mfwWSPort;  
  //url to the MFW service endpoint
  private String mfwWsUrl;
  //default availability interval
  private static final int DEFAULT_AVAILABILITY_INTERVAL = 10000;
  private int availabilityInterval;
  private long mfwId = 1;


  //Map containing SAC IDs and web service endpoint URLs
  private Map<Long, String> sacsUrls = new HashMap<Long, String>();


  public SACPluginActivator() {
    super(log);
    configure(readConfig());
  }

  public SACPluginActivator(Properties props) {
    super(log);
    configure(props);
  }

  private void configure(Properties props) {
/*
    try {
      this.mfwWSPort = Integer.parseInt(props.getProperty(Const.MFW_WS_PORT));
    } catch (NumberFormatException e) {
      log.error("Failed to read MFW web service port from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.MFW_WS_PORT + " got:" + props.getProperty(Const.MFW_WS_PORT) + " should be a valid integer port value.");
//      System.exit(-1);
    }
*/
    try {
      this.mfwWsUrl = props.getProperty(Const.MFW_WS_URL);
      if (mfwWsUrl == null) {
        log.error("Failed to read MFW WS URL from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.MFW_WS_URL);
      } else {
        log.debug("MFW_WS_URL: " + mfwWsUrl);
      }
      long webUiId = Long.parseLong(props.getProperty(Const.WEB_UI_ID));
      log.debug("WEB_UI_ID: " + webUiId);
      String webUiWsUrl = props.getProperty(Const.WEB_UI_WS_URL);
      if (webUiWsUrl == null) {
        log.error("Failed to read WEB UI WS URL from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.WEB_UI_WS_URL);
      } else {
        log.debug("WEB_UI_WS_URL: " + webUiWsUrl);
        sacsUrls.put(webUiId, webUiWsUrl);
      }
    } catch (NumberFormatException e) {
      log.error("Failed to read WEB UI ID from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.WEB_UI_ID + " got:" + props.getProperty(Const.WEB_UI_ID) + " should be a valid integer port value.");
    }

    String sacIdKey = "";
    try {
      int n = 1;
      while (true) {
        sacIdKey = Const.SAC_ID + n;
        String sacIdString = props.getProperty(sacIdKey);
        if (sacIdString == null) {
          break;
        }
        log.debug("SAC_ID_" + n + ": " + sacIdString);
        long sacId = Long.parseLong(sacIdString);
        String sacUrlKey = Const.SAC_WS_URL + n;
        String sacUrl = props.getProperty(sacUrlKey);
        if (sacUrl == null) {
          log.error("Failed to read SAC URL from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + sacUrlKey);
          break;
        }
        log.debug("SAC_URL_" + n + ": " + sacUrl);
        if (!sacsUrls.containsKey(sacId)) {
          sacsUrls.put(sacId, sacUrl);
        } else {
          log.error("SAC ID already in use. SAC discarded.");
        }
        n++;
      }
    } catch (NumberFormatException e) {
      log.error("Failed to read SAC ID from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + sacIdKey + " got:" + props.getProperty(sacIdKey) + " should be a valid integer port value.");
    }

    try {
      String mfwIdString = props.getProperty("MFW_ID");
      if (mfwIdString != null) {
        mfwId = Long.parseLong(mfwIdString);
      }
    } catch (NumberFormatException e) {
      log.error("Failed to read MFW ID from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key MFW_ID got:" + props.getProperty("MFW_ID") + " should be a valid integer value.");
    }

    String availabilityIntervalValue = props.getProperty(Const.AVAILABILITY_INTERVAL);
    availabilityInterval = DEFAULT_AVAILABILITY_INTERVAL;
    if (availabilityIntervalValue != null) {
      try {
        availabilityInterval = Integer.parseInt(availabilityIntervalValue);
      } catch (NumberFormatException e) {
        log.error("Failed to read availability interval from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + availabilityIntervalValue + ". Using defaults.");
      }
    }

    //this is here to redirect cxf log to the same logging system as the rest of the MFW
    System.setProperty("org.apache.cxf.Logger", "org.apache.cxf.common.logging.Slf4jLogger");
  }

  private Properties readConfig() {
    Properties props = new Properties();
    try {
      props.load(new FileInputStream(Const.CONFIGURATION_FILENAME));
    } catch (IOException e) {
      log.error("Failed to load configuration", e);
      throw new RuntimeException("Failed to load configuration", e);
      //TODO: these exit calls need to be enabled to prevent OSGI from loading a crazy combination..
//      System.exit(-1);
    }
    return props;
  }

  public void start(BundleContext bc) throws Exception {
    sac = new SACPlugin(bc, sacsUrls, availabilityInterval, mfwId);
    registerPlugin(bc, sac, null, SACPlugin.class.getName());
    startServer();

    for (Map.Entry<Long, String> entry : sacsUrls.entrySet()) {
      Long sac_id = entry.getKey();
      String sac_url = entry.getValue();
      SACClient sacClient = new SACClient(sac, sac_url, sac_id, mfwId);
      log.debug("Sending initial availability information to SAC (ID:" + sac_id + ")");
      boolean sacResponding = sacClient.initAvailability();
      if (sacResponding) {
        log.debug("SAC (ID:" + sac_id + ") received initial availability information.");
        sac.register(sac_id, sacClient);
      } else {
        log.debug("SAC (ID:" + sac_id + ") not responding to setAvailability request.");
      }
    }
  }

  public void stop(BundleContext bc) throws Exception {
    endpoint.stop();
  }

  public SACPlugin getSac() {
    return sac;
  }

  private void startServer() throws Exception {
    log.debug("Starting SAC_MFW_service");
    implementor = new SACMFWImpl(sac, mfwId);
    //String ip = InetAddress.getLocalHost().getHostAddress().toString();
    //String address = "http://" +ip+ ":" + mfwWSPort + "/MFWServices";
    //String address = "http://localhost:" + mfwWSPort + "/MFWServices";
    log.debug("Publishing MFW WS endpoint at:" + mfwWsUrl);
    endpoint = Endpoint.publish(mfwWsUrl, implementor);
    log.debug("SAC_MFW_service started");

  }

}
