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

import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.KnowledgeSource;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

/**
 * Main class for the implementation of the blackboard. The name refers to an architectural pattern
 * where data is exchanged through a blackboard. The data is made available on the blackboard and
 * a set of knowledge sources monitor it for interesting data. Once interesting data is made available
 * these knowledge sources each process the data. In some cases they add new, processed data to the
 * blackboard that other knowledge sources can process. In other cases, they do something else with
 * the data, such as display it in a user-interface or guide an external sensor based on the values.
 *
 * @author Teemu Kanstren
 */
public class BlackboardImpl implements Blackboard {
  private final static Logger log = new Logger(BlackboardImpl.class);
  /** List of registered knowledge source plugins. */
  private Collection<KnowledgeSource> plugins = new HashSet<KnowledgeSource>();
  //this is used to disable the blackboard on shutdown so no new services can use it while it is shutting down
  private boolean disabled = false;

  /**
   * @see Blackboard
   */
  public synchronized void register(KnowledgeSource plugin) {
    if (disabled) return;

    log.debug("registering plugin:" + plugin);
    plugins.add(plugin);
  }

  /**
   * Each plugin can invoke this method to have the blackboard process some data. The blackboard will them check
   * all registered plugins and if they subscribe to this given data. If some are subscribing to it, they will
   * be provided with the data.
   *
   * @param dataObject The data to be processed.
   */
  public void process(DataObject dataObject) {
    Collection<KnowledgeSource> kss = getPlugins();
    for (KnowledgeSource ks : kss) {
      Set commands = ks.getCommands();
      if (commands == null) {
        continue;
      }
      if (commands.contains(dataObject.getClass())) {
        try {
          log.start("--Blackboard.process("+dataObject.getType()+") ks:"+ks);
//          if (dataObject instanceof ServerEvent) {
//            Thread.dumpStack();
//          }
          ks.process(dataObject);
//          log.complete("--Blackboard.process("+dataObject.getType()+") ks:"+ks);
        } catch (Exception e) {
          log.error("Error in processing data", e);
        }
      }
    }
  }

  public synchronized void unregister(KnowledgeSource plugin) {
    log.debug("Unregistering plugin:" + plugin);
    plugins.remove(plugin);
  }

  public synchronized Collection<KnowledgeSource> getPlugins() {
    Collection<KnowledgeSource> copy = new HashSet<KnowledgeSource>();
    copy.addAll(plugins);
    return copy;
  }

  public synchronized void shutdown() {
    disabled = true;
    plugins.clear();
  }
}
