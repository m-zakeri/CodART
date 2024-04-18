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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.subscribetobmpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.availabilitypage.BMDesc;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.availabilitypage.BMListDataProvider;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.Availability;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.BM;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.model.Model;

import java.util.ArrayList;
import java.util.List;

public class SubscribeToBMPage extends WebPage {
  private final static Logger log = new Logger(SubscribeToBMPage.class);
  private WebUIPlugin webUI;
  List<BMDesc> bms;

  public SubscribeToBMPage() {
    webUI = WebUIPlugin.getInstance();
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    
    Availability availability = webUI.getAvailability();
    
    bms = new ArrayList<BMDesc>();
    if (availability != null) {
      BMDesc bmDesc;
      for (BM bm : availability.getBM()) {
        if (!bm.getDeviceId().isEmpty()) {
          bmDesc = new BMDesc(bm.getId(), bm.getDeviceId().get(0), bm.getClazz(), bm.getName(), bm.getDescription(), bm.isDisabled());
        } else {
          bmDesc = new BMDesc(bm.getId(), 0, bm.getClazz(), bm.getName(), bm.getDescription(), bm.isDisabled());
        }
        bms.add(bmDesc);
      }
    }

    createBMList(bms);
    
    createSubscribeToBMForm();
    
    createUnsubscribeToBMForm();
    
  }
  
  public void createBMList(List<BMDesc> bms) {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new PropertyColumn(new Model<String>("bmId"), "bmId", "bmId") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });
    columns.add(new PropertyColumn(new Model<String>("deviceId"), "deviceId", "deviceId") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    columns.add(new PropertyColumn(new Model<String>("clazz"), "clazz", "clazz"));
    columns.add(new PropertyColumn(new Model<String>("name"), "name", "name"));
    columns.add(new PropertyColumn(new Model<String>("description"), "description", "description"));

    DefaultDataTable bmTable = new DefaultDataTable("bmtable", columns, new BMListDataProvider(bms), 8);
    add(bmTable);
  }

  private void createSubscribeToBMForm() {
    SubscribeToBMForm subscribeToBMForm = new SubscribeToBMForm("subscribeToBMForm");
    add(subscribeToBMForm);
  }
  private void createUnsubscribeToBMForm() {
    UnsubscribeToBMForm unsubscribeToBMForm = new UnsubscribeToBMForm("unsubscribeToBMForm");
    add(unsubscribeToBMForm);
  }

}
