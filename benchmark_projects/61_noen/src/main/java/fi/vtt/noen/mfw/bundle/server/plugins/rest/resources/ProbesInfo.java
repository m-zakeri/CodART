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

import java.util.ArrayList;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlRootElement(name = "probesInfo")
@XmlType(propOrder = {"targets", "baseMeasures", "probes"})
public class ProbesInfo
{
  private ArrayList<Target> targets;
  private ArrayList<BaseMeasure> baseMeasures;
  private ArrayList<Probe> probes;

  public ProbesInfo(){}

  @XmlElement
  public ArrayList<Target> getTargets()
  {
    return targets;
  }

  @XmlElement
  public ArrayList<BaseMeasure> getBaseMeasures()
  {
    return baseMeasures;
  }

  @XmlElement
  public ArrayList<Probe> getProbes()
  {
    return probes;
  }
  
  public void setTargets( ArrayList<Target> targets )
  {
    this.targets = targets;
  }
  
  public void setBaseMeasures( ArrayList<BaseMeasure> baseMeasures )
  {
    this.baseMeasures = baseMeasures;
  }
  
  public void setProbes( ArrayList<Probe> probes )
  {
    this.probes = probes;
  }
}