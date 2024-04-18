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

import java.util.Set;

/**
 * Common interface for all plugins/knowledge sources.
 *
 * @author Teemu Kanstren
 */
public interface KnowledgeSource {
  /** Provide the plugin reference to the Blackboard for a means to return something to the user. */
//  public void setBlackboard(Blackboard blackboard);
  /** The returned values define what messages the blackboard send to the process method. */
  public Set<Class> getCommands();
  /** Process a data object that is requested by the plugin. Called by blackboard when data for which this
   * plugin is subscribing to becomes available. The data value is given as parameter. */
  public void process(DataObject data);
  //name of the plugin
  public String getName();
}
