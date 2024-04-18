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

import org.apache.xmlrpc.XmlRpcException;
import org.apache.xmlrpc.XmlRpcRequest;
import org.apache.xmlrpc.server.RequestProcessorFactoryFactory;

/**
 * Specific implementation of the Apache XML-RPC factory implementation that allows for customized
 * processing of specific calls. This is to avoid the standard mechanism of Apache XMLRPC which is to
 * re-create a handler object every time. This customization allows all handlers to share the state of the
 * probe-agent plugin.
 *
 * @author Teemu Kanstren
 */
public class MFWRequestProcessFactoryFactory implements RequestProcessorFactoryFactory {
  private final static Logger log = new Logger(MFWRequestProcessFactoryFactory.class);
  private final RequestProcessorFactory factory = new MFWRequestProcessorFactory();
  //all message requests are forwarded to the probe-agent stored in this variable
  private final Object agent;

  public MFWRequestProcessFactoryFactory(Object agent) {
    this.agent = agent;
  }

  public RequestProcessorFactory getRequestProcessorFactory(Class aClass) throws XmlRpcException {
    return factory;
  }

  private class MFWRequestProcessorFactory implements RequestProcessorFactory {
    public Object getRequestProcessor(XmlRpcRequest xmlRpcRequest) throws XmlRpcException {
      return agent;
    }
  }
}
