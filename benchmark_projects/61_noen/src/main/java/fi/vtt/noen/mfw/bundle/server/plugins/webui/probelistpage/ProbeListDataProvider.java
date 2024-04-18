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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class ProbeListDataProvider extends SortableDataProvider<ProbeListItem> {
  private final static Logger log = new Logger(ProbeListDataProvider.class);
  private RegistryPlugin registry;

  public ProbeListDataProvider(RegistryPlugin registry) {
    this.registry = registry;
    setSort("endpoint", true);
  }

  public Iterator<ProbeListItem> iterator(int i, int i1) {
    List<ProbeDescription> registeredProbes = registry.getProbes();
    List<ProbeListItem> probes = new ArrayList<ProbeListItem>(registeredProbes.size());
    for (ProbeDescription probe : registeredProbes) {
      probes.add(new ProbeListItem(probe));
    }
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(probes, new ProbeComparator(key, true));
    } else {
      Collections.sort(probes, new ProbeComparator(key, false));
    }
    return probes.subList(i, i + i1).iterator();
  }

  public int size() {
    return registry.getProbes().size();
  }

  public IModel<ProbeListItem> model(ProbeListItem probe) {
    return new DetachableProbeModel(probe);
  }
}
