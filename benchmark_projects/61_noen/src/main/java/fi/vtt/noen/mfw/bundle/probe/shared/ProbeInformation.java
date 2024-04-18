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

package fi.vtt.noen.mfw.bundle.probe.shared;

import fi.vtt.noen.mfw.bundle.common.Const;

/**
 * This describes a probe. It is basically the same as a base measure description since at this point a base measure is the same
 * as a probe. This is because all of these properties listed here also apply to each base measure. It is thus not different in
 * any way to call something a probe or a base measure. The separate terms are still kept since it seems conceptually clearer..
 * The only difference here is the probe description field. If there are several probes capable of providing a single base
 * measure, the probe description is what should set them apart. If they have the same measureURI, they are considered to provide
 * the same base measure. A measureURI consists of targetName,targetType,bmClass,bmName value combination.
 *
 * @author Teemu Kanstren
 */
public class ProbeInformation {
  //property of the target of measurement, defined typically in a configuration file. part of measure identifier
  private final String targetName;
  //property of the target of measurement, defined typically in a configuration file. part of measure identifier
  private final String targetType;
  //property of the base measure from a probe, defined typically in a configuration file. part of measure identifier
  private final String bmClass;
  //property of the base measure from a probe, defined typically in a configuration file. part of measure identifier
  private final String bmName;
  //property of the base measure from a probe, defined typically in a configuration file. freeform text, only for human input
  private final String bmDescription;
  //name of the probe..
  private final String probeName;
  //precision of the probe, that is how good is the measurement provided. bigger is better. if several have the same measurement identifier properties, the one with highest precision is taken.
  private final int precision;
  //url where the server-agent can invoke this probe-agent over xmlrpc
  private final String xmlRpcUrl;

  public ProbeInformation(String targetName, String targetType, String bmClass, String bmName, String bmDescription, String probeDescription, int precision, String xmlRpcUrl) {
    this.targetName = targetName;
    this.targetType = targetType;
    this.bmClass = bmClass;
    this.bmName = bmName;
    this.bmDescription = bmDescription;
    this.probeName = probeDescription;
    this.precision = precision;
    this.xmlRpcUrl = xmlRpcUrl;
  }

  public String getTargetType() {
    return targetType;
  }

  public String getBmName() {
    return bmName;
  }

  public String getProbeName() {
    return probeName;
  }

  public String getTargetName() {
    return targetName;
  }

  public String getBmClass() {
    return bmClass;
  }

  public String getBmDescription() {
    return bmDescription;
  }

  public int getPrecision() {
    return precision;
  }

  public String getMeasureURI() {
    return Const.createMeasureURI(targetType, targetName, bmClass, bmName);
  }

  public String getXmlRpcUrl() {
    return xmlRpcUrl;
  }

  @Override
  public String toString() {
    return "ProbeInformation{" +
            "targetName='" + targetName + '\'' +
            ", targetType='" + targetType + '\'' +
            ", bmClass='" + bmClass + '\'' +
            ", bmName='" + bmName + '\'' +
            ", bmDescription='" + bmDescription + '\'' +
            ", probeDescription='" + probeName + '\'' +
            ", precision=" + precision +
            '}';
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;

    ProbeInformation that = (ProbeInformation) o;

    if (precision != that.precision) return false;
    if (bmClass != null ? !bmClass.equals(that.bmClass) : that.bmClass != null) return false;
    if (bmDescription != null ? !bmDescription.equals(that.bmDescription) : that.bmDescription != null) return false;
    if (bmName != null ? !bmName.equals(that.bmName) : that.bmName != null) return false;
    if (probeName != null ? !probeName.equals(that.probeName) : that.probeName != null)
      return false;
    if (targetName != null ? !targetName.equals(that.targetName) : that.targetName != null) return false;
    if (targetType != null ? !targetType.equals(that.targetType) : that.targetType != null) return false;

    return true;
  }

  @Override
  public int hashCode() {
    int result = targetName != null ? targetName.hashCode() : 0;
    result = 31 * result + (targetType != null ? targetType.hashCode() : 0);
    result = 31 * result + (bmClass != null ? bmClass.hashCode() : 0);
    result = 31 * result + (bmName != null ? bmName.hashCode() : 0);
    result = 31 * result + (bmDescription != null ? bmDescription.hashCode() : 0);
    result = 31 * result + (probeName != null ? probeName.hashCode() : 0);
    result = 31 * result + precision;
    return result;
  }
}
