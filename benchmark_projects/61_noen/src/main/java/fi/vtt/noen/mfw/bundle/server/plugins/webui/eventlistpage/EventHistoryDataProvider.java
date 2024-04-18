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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.eventlistpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistencePlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.Iterator;

/**
 * @author Teemu Kanstren
 */
public class EventHistoryDataProvider extends SortableDataProvider<ServerEvent> {
  private final static Logger log = new Logger(EventHistoryDataProvider.class);
  private PersistencePlugin persistence;

  public EventHistoryDataProvider(PersistencePlugin persistence) {
    this.persistence = persistence;
    setSort(ServerEvent.SortKey.TIME.toString(), true);
  }

  public Iterator<ServerEvent> iterator(int i1, int i2) {
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    return persistence.getEvents(i1, i2, ServerEvent.SortKey.valueOf(key), sp.isAscending()).iterator();
/*    if (sp.isAscending()) {
      Collections.sort(events, new EventComparator(key, true));
    } else {
      Collections.sort(events, new EventComparator(key, false));
    }
    return events.subList(i, i + i1).iterator();*/
  }

  public int size() {
    return persistence.getEventCount();
  }

  public IModel<ServerEvent> model(ServerEvent event) {
    return new DetachableEventModel(event);
  }
}