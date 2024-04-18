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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.availabilitypage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.Collections;
import java.util.Iterator;
import java.util.List;

public class BMListDataProvider extends SortableDataProvider<BMDesc> {
  private final static Logger log = new Logger(BMListDataProvider.class);
  private final List<BMDesc> bms;

  public BMListDataProvider(List<BMDesc> bms) {
    this.bms = bms;
    setSort("name", true);
  }

  public Iterator<BMDesc> iterator(int i, int i1) {
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(bms, new BMComparator(key, true));
    } else {
      Collections.sort(bms, new BMComparator(key, false));
    }
    return bms.subList(i, i + i1).iterator();
  }

  public int size() {
    return bms.size();
  }

  public IModel<BMDesc> model(BMDesc bm) {
    return new DetachableBMModel(bm);
  }
}
