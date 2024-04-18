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

@XmlRootElement(name="bm")
@XmlType(propOrder = {"id", "name", "clas", "description", "targetid", "datatype"})
public class BaseMeasure
{
  private String id;
  private String name;
  private String clas;
  private String description;
  private String targetid;
  private String datatype;

  public BaseMeasure() {}
  
  public BaseMeasure( String id, String name, String clas, String desc, String targetid, String datatype )
  {
    this.id = id;
    this.name = name;
    this.clas = clas;
    this.description = desc;
    this.targetid = targetid;
    this.datatype = datatype;
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
  public String getClas()
  {
    return clas;
  }

  @XmlElement
  public String getDescription()
  {
    return description;
  }

  @XmlElement
  public String getTargetid()
  {
    return targetid;
  }

  @XmlElement
  public String getDatatype()
  {
    return datatype;
  }
  
  public void setId( String id )
  {
    this.id = id;
  }
  
  public void setName( String name )
  {
    this.name = name;
  }
  
  public void setClas( String clas )
  {
    this.clas = clas;
  }
  
  public void setDescription( String description )
  {
    this.description = description;
  }
  
  public void setTargetid( String targetid )
  {
    this.targetid = targetid;
  }
  
  public void setDatatype( String datatype )
  {
    this.datatype = datatype;
  }
}
