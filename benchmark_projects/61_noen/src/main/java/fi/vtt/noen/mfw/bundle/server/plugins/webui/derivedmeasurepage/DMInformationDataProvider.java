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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage.BMListItem;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage.DetachableBMModel;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class DMInformationDataProvider extends SortableDataProvider<BMListItem> {
  private final static Logger log = new Logger(DMInformationDataProvider.class);
  private List<BMListItem> rows;
  private Collection<BMDescription> requiredMeasures;
  private DMDefinition dm;
  private final RegistryPlugin registry;

  public DMInformationDataProvider(RegistryPlugin registry) {
    this.registry = registry;
    rows = new ArrayList<BMListItem>();
    setSort("id", true);
  }

  public void setDM(DMDefinition dm) {
    this.dm = dm;
    rows.clear();
    if (dm == null) {
      return;
    }
    requiredMeasures = dm.getRequiredBM();
    List<BMDescription> actual = registry.getAvailableBM();
    for (BMDescription bm : requiredMeasures) {
      for (BMDescription ap : actual) {
        if (bm.matches(ap)) {
          bm = ap;
        }
      }
      rows.add(new BMListItem(bm, null));
    }
  }

  public Iterator<BMListItem> iterator(int i, int i1) {
    SortParam sp = getSort();
    log.debug("sort:" + sp);
    String key = sp.getProperty();
    log.debug("xx sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(rows, new BMComparator(key, true));
    } else {
      Collections.sort(rows, new BMComparator(key, false));
    }
    return rows.subList(i, i + i1).iterator();
  }

  public int size() {
    return rows.size();
  }

  public IModel<BMListItem> model(BMListItem bm) {
    return new DetachableBMModel(bm);
  }
}
