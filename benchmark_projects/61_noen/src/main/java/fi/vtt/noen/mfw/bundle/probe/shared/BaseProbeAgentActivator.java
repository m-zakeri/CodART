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
import fi.vtt.noen.mfw.bundle.common.Logger;
import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

/**
 * A base class for implementing the OSGI activator for probe-agents. Reads the configuration file to find the
 * specifications for the probes and based on the given Class definition creates the classes and configures them
 * according to the configuration file.
 * Configuration is defined in terms of prefix.probe1.parametername=value. The prefix is defined as specific for a
 * probe-agent, and numbering at the end is used to differentiate the probes from each other.
 *
 * @author Teemu Kanstren
 */
public abstract class BaseProbeAgentActivator implements BundleActivator {
  private final Logger log;
  //the configuration for the probe-agent, including configuration for all the probes it manages
  protected Properties config = null;
  //list of properties where each object represents configuration for a specific probe
  private Collection<Properties> probeProperties = new ArrayList<Properties>();
  //key=probe index in configuration file, value=probe implementation.
  private Map<Integer, Probe> probes = new HashMap<Integer, Probe>();
  //configuration prefix for this probe-agent
  private final String configPrefix;

  protected BaseProbeAgentActivator(Logger log, Properties config, String configPrefix) {
    this.log = log;
    this.config = config;
    this.configPrefix = configPrefix;
  }

  protected BaseProbeAgentActivator(Logger log, String configPrefix) {
    this.log = log;
    this.configPrefix = configPrefix;
    readConfig(Const.CONFIGURATION_FILENAME);
  }

  protected void readConfig(String fileName) {
    try {
      InputStream in = new FileInputStream(fileName);
      Properties props = new Properties();
      props.load(in);
      in.close();
      config = props;
    } catch (IOException e) {
      throw new RuntimeException("Unable to read required initialization properties from file '" + fileName + "'");
    }
  }

  /**
   * Register a single probe.
   *
   * @param bc The OSGI bundlecontext.
   * @param probeClass The class to instantiate as the probe controller.
   */
  protected void register(BundleContext bc, Class<? extends Probe> probeClass) {
    ProbeEventBus eventBus = new ProbeEventBus(bc);
    //-1 refers to having only one probe
    register(eventBus, bc, probeClass, -1);
  }

  /**
   * Register several probes.
   *
   * @param bc The OSGI bundlecontext.
   * @param probeClass The class to instantiate as the probe controller.
   */
  protected void registerMany(BundleContext bc, Class<? extends Probe> probeClass) {
    ProbeEventBus eventBus = new ProbeEventBus(bc);
    Set<String> keys = config.stringPropertyNames();
    log.debug("config:"+config);
    int n = 1;
    while (true) {
      //the key to access the paramaters of the next probe on the list in the properties map
      String testKey = configPrefix+".probe" + n + "." + Const.PROBE_TARGET_NAME;
      if (!keys.contains(testKey)) {
        log.debug("Parsed all probes, last key that was not found ="+testKey);
        break;
      }
      log.debug("Registering probe for index "+n);
      register(eventBus, bc, probeClass, n);
      //increate index and check if there are more probes configured
      n++;
    }
  }

  public Collection<Properties> getProbeProperties() {
    return probeProperties;
  }

  public Map<Integer, Probe> getProbes() {
    return probes;
  }

  /**
   * Creates a probe given the set of parameters.
   *
   * @param bc OSGI bundlecontext.
   * @param probeClass The class implementing the probe, will be instantiated with Class.newInstance()
   * @param configIndex The index to read the configuration for this probe from the configuration file.
   * @return The new probe.
   */
  protected Probe register(ProbeEventBus eventBus, BundleContext bc, Class<? extends Probe> probeClass, int configIndex) {
    try {
      Probe probe = probeClass.newInstance();
      return register(bc, probe, configIndex);
    } catch (Exception e) {
      log.error("Failed to register probe:" + probeClass, e);
      eventBus.event(getProbeInfo(configIndex), "Error while trying to initiate probe:" + e);
      return null;
    }
  }

  /**
   * Creates a probe given the set of parameters.
   *
   * @param bc OSGI bundlecontext.
   * @param probe The probe object.
   * @param configIndex The index to read the configuration for this probe from the configuration file.
   * @return The new probe.
   */
  protected Probe register(BundleContext bc, Probe probe, int configIndex) {
    //this must be in this order or the probe is registered with null information as bc.registerservice results in xmlrpc.register invocation..
    probe.init(configSubSetFor(configIndex));
    bc.registerService(Probe.class.getName(), probe, null);
    log.debug("probe " + configIndex + " registered");
    probes.put(configIndex, probe);
    return probe;
  }


  /**
   * Parses a subset of properties from the full set of properties to get only those relevant for a probe with the given index.
   *
   * @param n  Index of the probe for which the parameters should be collected.
   * @return The properties for the requested probe index.
   */
  public Properties configSubSetFor(int n) {
    Set<String> keys = config.stringPropertyNames();
    Properties probeProperties = new Properties();
    String prefix = configPrefix+".probe";
    //this means we have more than one probe to look for in the same file
    if (n > 0) {
      prefix += n;
    }
    prefix += ".";
    for (String key : keys) {
      if (!key.startsWith(prefix)) {
        continue;
      }
      String value = config.getProperty(key);
      key = key.substring(prefix.length());
      probeProperties.setProperty(key, value);
    }
    log.debug("probe " + n + ":" + probeProperties);
    this.probeProperties.add(probeProperties);
    return probeProperties;
  }

  protected ProbeInformation getProbeInfo(int n) {
    Properties props = configSubSetFor(n);
    String targetName = props.getProperty(Const.PROBE_TARGET_NAME);
    String targetType = props.getProperty(Const.PROBE_TARGET_TYPE);
    String bmClass = props.getProperty(Const.PROBE_BM_CLASS);
    String bmName = props.getProperty(Const.PROBE_BM_NAME);
    String bmDesc = props.getProperty(Const.PROBE_BM_DESCRIPTION);
    String probeName = props.getProperty(Const.PROBE_NAME);
    return new ProbeInformation(targetName, targetType, bmClass, bmName, bmDesc, probeName, 0, null);
  }
}
