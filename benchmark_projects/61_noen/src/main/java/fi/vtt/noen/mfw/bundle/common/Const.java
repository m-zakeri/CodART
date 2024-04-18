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

package fi.vtt.noen.mfw.bundle.common;

/**
 * Contains shared constant values for the different MFW implementation elements.
 *
 * @author Teemu Kanstren
 */
public class Const {
  //server-agent xmlrpc address in probe-agent configuration
  public static final String MFW_SERVER_URL_KEY = "server_agent_url";
  //configuration port for where probe-agent will listen to xmlrpc messages
  public static final String PROBE_AGENT_PORT_KEY = "probe_agent_xmlrpc_port";
  //configuration port for where server-agent will listen to xmlrpc messages
  public static final String SERVER_AGENT_PORT_KEY = "server_agent_xmlrpc_port";
  //configuration parameter for how often the probe-agent sends keep-alive messages to the server-agent
  public static final String KEEP_ALIVE_INTERVAL = "keep-alive_interval";
  //configuration parameter for how often the probe-agent checks for new measurement requests if no notify() is done
  public static final String MEASUREMENT_CHECK_INTERVAL = "measurement_check_interval";
  //a property given by probe-agent when registering to the server-agent. defines the probe-agent xmlrpc address.
  public static final String XMLRPC_URL = "xmlrpc_url";
  //describes the base measure "class" for a probe
  public static final String PROBE_BM_CLASS = "bm_class";
  //base measure name for a probe
  public static final String PROBE_BM_NAME = "bm_name";
  //base measure description for a probe
  public static final String PROBE_BM_DESCRIPTION = "bm_description";
  //the name of a probe
  public static final String PROBE_NAME = "description";
  //precision of a probe, integer, higher is better probe with better measurements
  public static final String PROBE_PRECISION = "precision";
  //the name of the target of measurement for a probe
  public static final String PROBE_TARGET_NAME = "target_name";
  //the type of the target of measurement for a probe
  public static final String PROBE_TARGET_TYPE = "target_type";
  //configuration key for ssh probe script file name
  public static final String SSH_SCRIPT_FILENAME = "ssh_script_file";
  //configuration key for ssh probe script file contents
  public static final String SSH_SCRIPT_FILE_CONTENTS = "ssh_script_file_contents";
  //configuration key for ssh probe user name to do the login on the target
  public static final String SSH_USERNAME = "ssh_username";
  //configuration key for ssh probe password to do the login on the target
  public static final String SSH_PASSWORD = "ssh_password";
  //configuration key for ssh probe giving the shell command to execute the given script
  public static final String SSH_SCRIPT_COMMAND = "ssh_command";
  //prefix for ssh probe-agent configuration file
  public static final String SSH_CONFIG_PREFIX = "ssh";
  //prefix for http probe-agent configuration file
  public static final String HTTP_CONFIG_PREFIX = "http";
  //prefix for test probe-agent configuration file
  public static final String TEST_PROBE_AGENT_CONFIG_PREFIX = "test";
  //provided as an error msg to the server-agent when a probe-agent is unable to produce a suitable measurement value.
  public static final String ERROR_MSG_NO_VALID_VALUE = "No valid measurement value available.";
  //not used atm but left here as a reminder that java.util.Formatter can be used to format this type of a string
  public static final String ERROR_UNSUPPORTED_MEASURE_TYPE = "Probe returned unsupported data type for value:%1$.";
  //the port where the server-agent provides the WSDL interface
//  public static final String MFW_WS_PORT = "mfw_ws_port";
  //the address to the MFW web service
  public static final String MFW_WS_URL = "mfw_ws_url";
  //the address to the SAC web service
  public static final String SAC_WS_URL = "sac_ws_url_";
  //the identifier of the SAC
  public static final String SAC_ID = "sac_id_";
  //the address to the web ui SAC webservice
  public static final String WEB_UI_WS_URL = "web_ui_ws_url";
  //the identifier of the web ui (sac id)
  public static final String WEB_UI_ID = "web_ui_id";
  //name of the filename from which all the configuration of agents is always read
  public static final String CONFIGURATION_FILENAME = "noen-mfw.properties";
  public static final int ERROR_CODE_ILLEGAL_ARGUMENTS_FOR_PROBE = -1;
  //maximum time (in milliseconds) for not receiving a keep-alive message from a probe before "disabling" that probe
  public static final String MAX_KEEPALIVE_DELAY = "max_keepalive_delay";
  //time to wait between trying to reconnect to server
  public static final String RETRY_DELAY = "retry_delay";
  //a configuration file property that describes a probe-agent and a server-agent connecting locally
  public static final String LOCAL_LINK_IN_USE = "local_link";
  //a url that describes a probe-agent and a server-agent connecting locally
  public static final String LOCAL_LINK_ENDPOINT_URL = "mfw://local";
  public static final String XMLRPC_PORT = "xmlrpc_port";
  public static final String REST_CLIENT_ENDPOINT_URL = "rest_client_endpoint";
  public static final String THREAD_POOL_SIZE = "thread_pool_size";
  public static final String TASK_TIMEOUT = "task_timeout";
  public static final String SUBSCRIPTION_CHECK_INTERVAL = "subscription_check_interval";
  public static final String AVAILABILITY_INTERVAL = "availability_interval";

  public static String createMeasureURI(String targetType, String targetName, String bmClass, String bmName) {
    return "MFW://"+targetType+"/"+targetName+"/"+bmClass+"/"+bmName;
  }
}

