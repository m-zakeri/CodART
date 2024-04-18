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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage.BMComparator;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * @author Teemu Kanstr�n
 */
public class BMListDataProvider extends SortableDataProvider<BMListItem> {
  private final static Logger log = new Logger(BMListDataProvider.class);
  private final RegistryPlugin registry;
  private final Map<String, String> latestValues;

  public BMListDataProvider(RegistryPlugin registry, Map<String, String> latestValues) {
    this.registry = registry;
    this.latestValues = latestValues;
    setSort("targetId", true);
  }

  public Iterator<BMListItem> iterator(int i, int i1) {
    List<BMDescription> bms = registry.getAvailableBM();
    bms = bms.subList(i, i + i1);
    List<BMListItem> list = new ArrayList<BMListItem>();
    for (BMDescription bm : bms) {
      String value = latestValues.get(bm.getMeasureURI());
      BMListItem listItem = new BMListItem(bm, value);
      list.add(listItem);
    }

    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(list, new BMComparator(key, true));
    } else {
      Collections.sort(list, new BMComparator(key, false));
    }
    return list.iterator();
  }

  public int size() {
    return registry.getAvailableBM().size();
  }

  public IModel<BMListItem> model(BMListItem bm) {
    return new DetachableBMModel(bm);
  }
}
