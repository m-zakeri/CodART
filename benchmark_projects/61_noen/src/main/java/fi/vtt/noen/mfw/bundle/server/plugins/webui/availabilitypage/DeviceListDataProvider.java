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

public class DeviceListDataProvider extends SortableDataProvider<DeviceDesc> {
  private final static Logger log = new Logger(DeviceListDataProvider.class);
  private final List<DeviceDesc> devices;

  public DeviceListDataProvider(List<DeviceDesc> devices) {
    this.devices = devices;
    setSort("name", true);
  }

  public Iterator<DeviceDesc> iterator(int i, int i1) {
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(devices, new DeviceComparator(key, true));
    } else {
      Collections.sort(devices, new DeviceComparator(key, false));
    }
    return devices.subList(i, i + i1).iterator();
  }

  public int size() {
    return devices.size();
  }

  public IModel<DeviceDesc> model(DeviceDesc deviceDesc) {
    return new DetachableDeviceModel(deviceDesc);
  }
}
