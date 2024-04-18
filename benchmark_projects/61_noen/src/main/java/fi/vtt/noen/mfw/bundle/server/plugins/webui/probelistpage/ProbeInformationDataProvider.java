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
public class ProbeInformationDataProvider extends SortableDataProvider<WicketValuePair> {
  private final static Logger log = new Logger(ProbeInformationDataProvider.class);
  private List<WicketValuePair> rows;

  public ProbeInformationDataProvider() {
    rows = new ArrayList<WicketValuePair>();
    setSort("key", true);
  }

  public void setProbe(ProbeListItem probe) {
    rows.clear();
    addRow("endpoint", probe.getEndpoint());
    addRow("measureURI", probe.getMeasureURI());
    addRow("probeName", probe.getProbeName());
    addRow("precision", "" + probe.getPrecision());
  }

  private void addRow(String key, String value) {
    WicketValuePair pair = new WicketValuePair(key, value);
    rows.add(pair);
  }

  public Iterator<? extends WicketValuePair> iterator(int i, int i1) {
    SortParam sp = getSort();
    log.debug("sort:" + sp);
    String key = sp.getProperty();
    log.debug("xx sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(rows, new ValuePairComparator(key, true));
    } else {
      Collections.sort(rows, new ValuePairComparator(key, false));
    }
    return rows.subList(i, i + i1).iterator();
  }

  public int size() {
    return rows.size();
  }

  public IModel<WicketValuePair> model(WicketValuePair valuePair) {
    return new DetachableValuePairModel(valuePair);
  }
}
