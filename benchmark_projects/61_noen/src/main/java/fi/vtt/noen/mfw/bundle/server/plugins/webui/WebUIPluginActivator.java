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

package fi.vtt.noen.mfw.bundle.server.plugins.webui;

import fi.vtt.noen.mfw.bundle.common.BaseActivator;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage.DMMonitorPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.MFW;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.MFWClient;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.sacservice.MFWSACImpl;
import org.osgi.framework.BundleContext;

//import javax.xml.ws.Endpoint;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.util.Properties;

/**
 * OSGI activataor for the web ui.
 *
 * @author Teemu Kanstren
 */
public class WebUIPluginActivator extends BaseActivator {
  private final static Logger log = new Logger(WebUIPluginActivator.class); 
  private WebUIPlugin webUi;
  //SAC web service endpoint
//  private Endpoint endpoint = null;
  //SAC web service endpoint implementor
  private Object implementor = null;
  //port for MFW web service endpoint
//  private int mfwWSPort;
  //url to the SAC service endpoint
  private String webUIWSURL;
  //identifier for webUI SAC
  private long webUiId;
  //url to the MFW service endpoint
  private String mfwWsUrl;
  

  public WebUIPluginActivator() {
    super(log);
    configure(readConfig());
  }
  
  public WebUIPluginActivator(Properties props) {
    super(log);
    configure(props);
  }

  private void configure(Properties props) {
/*
    try {
      this.mfwWSPort = Integer.parseInt(props.getProperty(Const.MFW_WS_PORT));
    } catch (NumberFormatException e) {
      log.error("Failed to read MFW web service port from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.MFW_WS_PORT + " got:" + props.getProperty(Const.MFW_WS_PORT) + " should be a valid integer port value.");
    }
*/
    try {
      this.webUiId = Long.parseLong(props.getProperty(Const.WEB_UI_ID));
    } catch (NumberFormatException e) {
      log.error("Failed to read WEB UI ID from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.WEB_UI_ID + " got:" + props.getProperty(Const.WEB_UI_ID) + " should be a valid integer port value.");
    }
    this.webUIWSURL = props.getProperty(Const.WEB_UI_WS_URL);
    if (webUIWSURL == null) {
      log.error("Failed to read WEB UI WS URL from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.WEB_UI_WS_URL);
    }
    this.mfwWsUrl = props.getProperty(Const.MFW_WS_URL);
    if (mfwWsUrl == null) {
      log.error("Failed to read MFW WS URL from configuration file (" + Const.CONFIGURATION_FILENAME + ") with key " + Const.MFW_WS_URL);
    }
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
    log.debug("WebUI Plugin activated");
    
    webUi = new WebUIPlugin(bc);
    webUi.init();
    registerPlugin(bc, webUi, null, WebUIPlugin.class.getName());
    log.debug("WebUI start done");

    DMMonitorPlugin dmMonitor = new DMMonitorPlugin(bc);
    registerPlugin(bc, dmMonitor, null, DMMonitorPlugin.class.getName());
    webUi.setDMMonitor(dmMonitor);

    log.debug("Started DM monitor plugin");
    
    startServer();    
    //String ip = InetAddress.getLocalHost().getHostAddress().toString();    
    //MFWClient mfwClient = new MFWClient("http://" +ip+ ":" + mfwWSPort + "/MFWServices", webUiId);
    //MFWClient mfwClient = new MFWClient("http://localhost:" + mfwWSPort + "/MFWServices", webUiId);
    //MFWClient mfwClient = new MFWClient(mfwWsUrl, webUiId);
    log.debug("Requesting MFW information");
    //MFW mfwInfo = mfwClient.getMFW();
    //if (mfwInfo != null) {
    //  log.debug("Received MFW information. Registering MFWClient for WebUI");
    //  webUi.registerMFWClient(mfwClient);
    //}
    log.debug("Startup done");
  }

  public void stop(BundleContext bc) throws Exception {
//    endpoint.stop();
  }
  
  private void startServer() throws Exception {
//    log.debug("Starting WebUI MFW_SAC_service");
//    implementor = new MFWSACImpl(webUi, webUiId);
//    String address = webUIWSURL;
//    endpoint = Endpoint.publish(address, implementor);
//    log.debug("WebUI MFW_SAC_service started");

  }
  
  
}
