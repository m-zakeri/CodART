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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmresultspage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.model.Model;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class BMResultsPage extends WebPage {
  private final static Logger log = new Logger(BMResultsPage.class);
  private WebUIPlugin webUi;

  public BMResultsPage() throws Exception {
    webUi = WebUIPlugin.getInstance();
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    createBMResultsList();
  }

  public void createBMResultsList() {
    List<BMResult> bmResults = readBMResults();
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new PropertyColumn(new Model<String>("time"), "time", "time"));
    columns.add(new PropertyColumn(new Model<String>("bm_id"), "bm_id", "bm_id") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });
    columns.add(new PropertyColumn(new Model<String>("device_id"), "device_id", "device_id") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });
    columns.add(new PropertyColumn(new Model<String>("value"), "value", "value"));
    columns.add(new PropertyColumn(new Model<String>("error"), "error", "error"));

    add(new DefaultDataTable("table", columns, new BMResultDataProvider(bmResults), 20));
  }

  private List<BMResult> readBMResults() {
    return webUi.getBMResults();
  }

}