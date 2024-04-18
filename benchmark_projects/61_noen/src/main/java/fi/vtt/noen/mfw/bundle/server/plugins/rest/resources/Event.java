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

@XmlRootElement(name="event")
@XmlType(propOrder = {"type", "description"})
public class Event
{
  private String type;
  private String description;

  public Event(){}
  
  public Event( String type, String description )
  {
    this.type = type;
    this.description = description;
  }

  @XmlElement
  public String getType()
  {
    return type;
  }

  @XmlElement
  public String getDescription()
  {
    return description;
  }
  
  public void setType( String type )
  {
    this.type = type;
  }
  
  public void setDescription( String description )
  {
    this.description = description;
  }
}
