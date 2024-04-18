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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.historypage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistencePlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.Iterator;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class MeasurementHistoryDataProvider extends SortableDataProvider<Value> {
  private transient final static Logger log = new Logger(MeasurementHistoryDataProvider.class);
  private transient PersistencePlugin persistence;

  public MeasurementHistoryDataProvider(PersistencePlugin persistence) {
    this.persistence = persistence;
    setSort(Value.SortKey.MEASUREURI.toString(), true);
  }

  public Iterator<Value> iterator(int first, int count) {
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    List<Value> values = persistence.getValues(first, count, Value.SortKey.valueOf(key), sp.isAscending());
    //log.debug("values:"+values);
    return values.iterator();
/*    if (sp.isAscending()) {
      Collections.sort(measures, new ValueComparator(key, true));
    } else {
      Collections.sort(measures, new ValueComparator(key, false));
    }
    return measures.subList(i, i + i1).iterator();*/
  }

  public int size() {
    int valueCount = persistence.getValueCount();
    log.debug("valuecount:"+valueCount);
    return valueCount;
  }

  public IModel<Value> model(Value measure) {
    return new DetachableValueModel(measure);
  }
}