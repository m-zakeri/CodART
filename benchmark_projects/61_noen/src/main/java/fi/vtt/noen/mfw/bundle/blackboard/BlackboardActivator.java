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

package fi.vtt.noen.mfw.bundle.blackboard;

import fi.vtt.noen.mfw.bundle.common.KnowledgeSource;
import fi.vtt.noen.mfw.bundle.common.Logger;
import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceReference;

import java.util.Properties;

/**
 * @author Teemu Kanstren
 */
public class BlackboardActivator implements BundleActivator {
  private final static Logger log = new Logger(BlackboardActivator.class);
  private Blackboard bb;

  public void start(BundleContext bc) throws Exception {
    log.info("Starting up blackboard plugin");
    startBlackboard(bc);
  }

  public void stop(BundleContext bundleContext) throws Exception {
    bb.shutdown();
  }

  /**
   * Creates the blackboard, a listener for knowledge sources and captures all currently
   * registered knowledge sources. All existing knowledge sources are registered with the
   * blackboard at the time of creation and new ones are captured with the help of the
   * listener.
   *
   * @param bc Link to the OSGI container.
   * @throws Exception
   */
  public Blackboard startBlackboard(BundleContext bc) throws Exception {
    log.debug("Starting blackboard");
    bb = new BlackboardImpl();
    //we create a proxy to capture a log of interactions as needed
//    bb = (Blackboard) ServiceProxy.createProxy(bb, bc);

    bc.addServiceListener(new KnowledgeSourceListener(bb, bc));
    Properties props = new Properties();
    props.put("version", "1.0");
    bc.registerService(Blackboard.class.getName(), bb, props);
    ServiceReference[] ksRefs = bc.getServiceReferences(KnowledgeSource.class.getName(), null);
    if (ksRefs == null) {
      return bb;
    }
    for (ServiceReference ksRef : ksRefs) {
      log.debug("Found service:" + ksRef);
      KnowledgeSource ks = (KnowledgeSource) bc.getService(ksRef);
      bb.register(ks);
    }
    return bb;
  }

  public Blackboard getBlackboard() {
    return bb;
  }
}
