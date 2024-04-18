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
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;

import java.util.Collection;
import java.util.HashSet;
import java.util.Map;
import java.util.Properties;

/**
 * A base class for extending to create specific probes to the users needs. The term probe-agent here is a bit confusing,
 * This class (or its children) are instantiated for each probe configuration found in the configuration file. Thus this
 * practically describes a single "probe" entity, which is controlled by a generic "probe-agent".
 *
 * @author Teemu Kanstren
 */
public abstract class BaseProbeAgent implements Probe {
  protected ProbeInformation pi;

  public void init(Properties properties) {
    String targetName = properties.getProperty(Const.PROBE_TARGET_NAME);
    String targetType = properties.getProperty(Const.PROBE_TARGET_TYPE);
    String bmClass = properties.getProperty(Const.PROBE_BM_CLASS);
    String bmName = properties.getProperty(Const.PROBE_BM_NAME);
    String bmDescription = properties.getProperty(Const.PROBE_BM_DESCRIPTION);
    String probeName = properties.getProperty(Const.PROBE_NAME);
    int precision = Integer.parseInt(properties.getProperty(Const.PROBE_PRECISION));
    String xmlRpcUrl = properties.getProperty(Const.XMLRPC_URL);
    pi = new ProbeInformation(targetName, targetType, bmClass, bmName, bmDescription, probeName, precision, xmlRpcUrl);
  }

  public ProbeInformation getInformation() {
    return pi;
  }

  public void setBaseConfigurationParameters(Map<String, String> configuration) {
    String targetName = configuration.get(Const.PROBE_TARGET_NAME);
    String targetType = configuration.get(Const.PROBE_TARGET_TYPE);
    String bmClass = configuration.get(Const.PROBE_BM_CLASS);
    String bmName = configuration.get(Const.PROBE_BM_NAME);
    String bmDescription = configuration.get(Const.PROBE_BM_DESCRIPTION);
    String probeName = configuration.get(Const.PROBE_NAME);
    int precision = Integer.parseInt(configuration.get(Const.PROBE_PRECISION));
    String xmlRpcUrl = configuration.get(Const.XMLRPC_URL);
    pi = new ProbeInformation(targetName, targetType, bmClass, bmName, bmDescription, probeName, precision, xmlRpcUrl);
  }

  public Collection<ProbeConfiguration> getBaseConfigurationParameters() {
    Collection<ProbeConfiguration> config = new HashSet<ProbeConfiguration>();
    config.add(new ProbeConfiguration(Const.PROBE_TARGET_TYPE, "Target type", false, pi.getTargetType()));
    config.add(new ProbeConfiguration(Const.PROBE_BM_CLASS, "BM Class", false, pi.getBmClass()));
    config.add(new ProbeConfiguration(Const.PROBE_BM_NAME, "BM Name", false, pi.getBmName()));
    config.add(new ProbeConfiguration(Const.PROBE_BM_DESCRIPTION, "BM Description", false, pi.getBmDescription()));
    config.add(new ProbeConfiguration(Const.PROBE_NAME, "Probe name", false, pi.getProbeName()));
    config.add(new ProbeConfiguration(Const.PROBE_PRECISION, "Probe precision", true, pi.getPrecision()));
    config.add(new ProbeConfiguration(Const.XMLRPC_URL, "XMLRPC URL", true, pi.getXmlRpcUrl()));
    return config;
  }
}
