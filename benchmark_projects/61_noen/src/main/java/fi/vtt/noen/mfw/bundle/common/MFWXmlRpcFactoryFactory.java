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

import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.client.XmlRpcSun15HttpTransportFactory;
import org.apache.xmlrpc.client.util.ClientFactory;

import java.net.URL;

/**
 * Provides some base features for XML-RPC clients as a base class to be extended.
 *
 * @author Teemu Kanstren
 */
public class MFWXmlRpcFactoryFactory {
  /**
   * Initializes the factory object to create new connections to the given url. The factory is used in the child class.
   *
   * @param url Address of the XMLRPC server to connect to.
   */
  public static ClientFactory createFactory(URL url) {
    XmlRpcClientConfigImpl xmlRpcConfig = new XmlRpcClientConfigImpl();
    xmlRpcConfig.setServerURL(url);
    xmlRpcConfig.setEnabledForExtensions(true);
    //todo: put these values in a configuration file
    xmlRpcConfig.setConnectionTimeout(5000);
    xmlRpcConfig.setReplyTimeout(5000);

    XmlRpcClient client = new XmlRpcClient();
    XmlRpcSun15HttpTransportFactory transportFactory = new XmlRpcSun15HttpTransportFactory(client);
    client.setTransportFactory(transportFactory);
    client.setConfig(xmlRpcConfig);
    return new ClientFactory(client);
  }
}
