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

import fi.vtt.noen.mfw.bundle.common.Logger;
import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.server.PropertyHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcHandlerMapping;
import org.apache.xmlrpc.server.XmlRpcServerConfigImpl;
import org.apache.xmlrpc.webserver.XmlRpcServlet;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * @author Teemu Kanstren
 */
public class MfwXmlRpcServlet extends XmlRpcServlet {
  private final static Logger log = new Logger(MfwXmlRpcServlet.class);
  private static ThreadLocal<String> clientIpAddress = new ThreadLocal<String>();
  private final PropertyHandlerMapping handler;

  public MfwXmlRpcServlet(PropertyHandlerMapping handler) {
    this.handler = handler;
  }

  public static String getClientIp() {
    String ip = clientIpAddress.get();
    return ip;
  }

  @Override
  public void doPost(HttpServletRequest pRequest, HttpServletResponse pResponse) throws IOException, ServletException {
    try {
      XmlRpcServerConfigImpl config = (XmlRpcServerConfigImpl) getXmlRpcServletServer().getConfig();
      
      config.setEnabledForExceptions(true);
      String clientIp = pRequest.getRemoteAddr();
      clientIpAddress.set(clientIp);
//    clientPort.set(pRequest.getRemotePort());
//      log.debug("POST request is in processing");
      super.doPost(pRequest, pResponse);
    } catch (Exception e) {
      log.error("Error while handling XMLRPC POST message", e);
    }
//    log.debug("POST has been processed");
  }

  @Override
  protected XmlRpcHandlerMapping newXmlRpcHandlerMapping() throws XmlRpcException {
    return handler;
  }
}
