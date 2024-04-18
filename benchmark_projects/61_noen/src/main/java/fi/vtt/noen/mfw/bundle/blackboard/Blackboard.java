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

import java.util.Collection;

/**
 * Interface to register the blackboard as an OSGI service.
 *
 * @see BlackboardImpl for more information.
 *
 * @author Teemu Kanstrén
 */
public interface Blackboard {
  /**
   * Used to link all knowledge sources/plugins to the blackboard.
   *
   * @param ks The knowledge source/plugin being registered.
   */
  public void register(KnowledgeSource ks);
  public void unregister(KnowledgeSource ks);
  public Collection<KnowledgeSource> getPlugins();
  public void process(DataObject data);
  public void shutdown();
}
