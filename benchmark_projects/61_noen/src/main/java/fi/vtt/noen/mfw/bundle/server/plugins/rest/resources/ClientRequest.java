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

package fi.vtt.noen.mfw.bundle.server.plugins.rest.resources;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlRootElement(name = "client")
@XmlType(propOrder = {"name", "endpoint", "session"})
public class ClientRequest
{    
  private String name;
  private String endpoint;
  private Session session;
  
  public ClientRequest(){}
  
  public ClientRequest( String name, String endpoint )
  {
      this.name = name;
      this.endpoint = endpoint;
  }
  
  public void setName( String name )
  {
    this.name = name;
  }
  
  public void setEndpoint( String endpoint )
  {
    this.endpoint = endpoint;
  }
  
  public void setSession( Session session )
  {
    this.session = session;
  }

  @XmlElement
  public String getName()
  {
    return name;
  }

  @XmlElement
  public String getEndpoint()
  {
    return endpoint;
  }

  @XmlElement
  public Session getSession()
  {
    return session;
  }
}

