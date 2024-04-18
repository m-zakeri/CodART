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

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.MFWXmlRpcFactoryFactory;
import fi.vtt.noen.mfw.bundle.server.shared.ServerAgent;
import org.apache.xmlrpc.client.util.ClientFactory;

import java.net.URL;
import java.util.List;
import java.util.Map;

/**
 * An XML-RPC client for calling a server-bundle.
 *
 * @author Teemu Kanstren
 */
public class XmlRpcServerClient implements ServerAgent {
  private final static Logger log = new Logger(XmlRpcServerClient.class);
  private ServerAgent server;
  private final URL url;

  public XmlRpcServerClient(URL url) {
    this.url = url;
    //we need this for osgi tricks
    ClassLoader classLoader = getClass().getClassLoader();
    ClientFactory factory = MFWXmlRpcFactoryFactory.createFactory(url);
    server = (ServerAgent) factory.newInstance(classLoader, ServerAgent.class);
  }

  public boolean measurement(long time, String measureURI, int precision, String value, long subscriptionId) {
    try {
      return server.measurement(time, measureURI, precision, value, subscriptionId);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
      return false;
    }
  }

  public void event(long time, String type, String source, String msg, long subscriptionId) {
    try {
      server.event(time, type, source, msg, subscriptionId);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
    }
  }

  public long register(Map<String, String> properties) {
    try {
      return server.register(properties);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
      throw new RuntimeException("Error while calling server over XMLRPC", e);
    }
  }

  public boolean keepAlive(long probeId) {
    try {
      return server.keepAlive(probeId);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
      throw new RuntimeException("Error while calling server over XMLRPC", e);
    }
  }

  public void unregister(long probeId) {
    try {
      server.unregister(probeId);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
    }
  }
 
  public void checkSubscriptions(long probeId, List<Long> subscriptionIds) {
    try {
      server.checkSubscriptions(probeId, subscriptionIds);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
    }
  }

  @Override
  public String toString() {
    return "XmlRpcServerClient{" +
            "url=" + url +
            '}';
  }

  public boolean BMReport(long time, String measureURI, String value,
      long subscriptionId, boolean matchReference, String reference) {
    try {
      return server.BMReport(time, measureURI, value, subscriptionId, matchReference, reference);
    } catch (Exception e) {
      log.error("Error while calling server over XMLRPC:"+this);
      log.debug("Exception", e);
      return false;
    }
  }

}
