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

@XmlRootElement(name="target")
@XmlType(propOrder = {"id", "name", "type"})
public class Target
{
  private String id;
  private String name;
  private String type;

  public Target(){}
  
  public Target( String id, String name, String type )
  {
    this.id = id;
    this.name = name;
    this.type = type;
  }

  @XmlElement
  public String getId()
  {
    return id;
  }

  @XmlElement
  public String getName()
  {
    return name;
  }

  @XmlElement
  public String getType()
  {
    return type;
  }
  
  public void setId( String id )
  {
    this.id = id;
  }
  
  public void setName( String name )
  {
    this.name = name;
  }
  
  public void setType( String type )
  {
    this.type = type;
  }
}
