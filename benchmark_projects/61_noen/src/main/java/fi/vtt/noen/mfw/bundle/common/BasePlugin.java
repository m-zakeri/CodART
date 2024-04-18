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

import fi.vtt.noen.mfw.bundle.blackboard.Blackboard;
import org.osgi.framework.BundleContext;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceReference;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;

/**
 * A base plugin to provide shared functionality for other plugins connecting to the blackboard.
 *
 * @author Teemu Kanstren
 */
public abstract class BasePlugin implements KnowledgeSource {
  //the blackboard this plugin is connected to
  protected Blackboard bb;
  //the OSGI bundlecontext for the container this is connected to
  protected final BundleContext bc;
  private final Logger log;

  //for testing
  protected BasePlugin(BundleContext bc, Logger log, Blackboard bb) {
    this.bc = bc;
    this.log = log;
    this.bb = bb;
  }

  protected BasePlugin(BundleContext bc, Logger log) {
    this.bc = bc;
    this.log = log;
    BlackboardListener listener = new BlackboardListener(bc, this);
    bc.addServiceListener(listener);
    pullBlackboard();
  }

  //@see KnowledgeSource
  public Set<Class> getCommands() {
    return createCommandSet();
  }

  //@see KnowledgeSource
  //this base implementation throws an exception for any given data, as some plugins may not subscribe to any
  //data but just provide some to the blackboard.
  public void process(DataObject data) {
    throw new IllegalStateException(getClass().getName()+".process() should never happen.");
  }

  //grabs the blackboard from the OSGI container if available
  public void pullBlackboard() {
    ServiceReference[] bbs = new ServiceReference[0];
    try {
      bbs = bc.getServiceReferences(Blackboard.class.getName(), null);
    } catch (InvalidSyntaxException e) {
      throw new RuntimeException("Failed to get OSGI service references for Blackboard", e);
    }
    if (bbs == null) {
      return;
    }
    if (bbs.length > 1) {
      throw new RuntimeException("More than one blackboard found: Only one supported");
    }
    for (ServiceReference bbRef : bbs) {
      log.debug("Found blackboard:" + bbRef);
      setBlackboard((Blackboard) bc.getService(bbRef));
    }
  }

  public void setBlackboard(Blackboard bb) {
    this.bb = bb;
    if (bb == null) {
      throw new NullPointerException("Blackboard cannot be null for an bundle");
    }
    bb.register(this);
  }

  //the name of class is given as the plugin name by default. for a superclass this should give the superclass name (right?).
  public String getName() {
    return getClass().getName();
  }

  //a convenience method to allow a superclass to create a list of subscribed data types more easily
  public Set<Class> createCommandSet(Class<? extends DataObject>... commands) {
    Set<Class> result = new HashSet<Class>();
    for (Class command : commands) {
      result.add(command);
    }
    return result;
  }

  public Properties readConfiguration() throws IOException {
    Properties props = new Properties();
    InputStream configStream = new FileInputStream(Const.CONFIGURATION_FILENAME);
    props.load(configStream);
    return props;
  }
}
