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
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceUser;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.model.Model;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.List;

/**
 * Provides a history of measurement values for the MFW. A page with a table of the values.
 *
 * @author Teemu Kanstren
 */
public class HistoryPage extends WebPage implements PersistenceUser {
  private transient final static Logger log = new Logger(HistoryPage.class);
  private transient PersistencePlugin persistence;
  private transient PersistenceServiceListener listener;

  public HistoryPage() {
    BundleContext bc = WebUIPlugin.getInstance().getBundleContext();
    listener = new PersistenceServiceListener(bc, log, this);
    listener.init();

    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    createHistoryList();
  }

  public void setPersistence(PersistencePlugin persistence) {
    this.persistence = persistence;
  }

  public void createHistoryList() {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    //first parameter = displayed name, second = sort key passed to dataprovider, third = key used to retrieve table values from data objects
    columns.add(new PropertyColumn(new Model<String>("time"), Value.SortKey.TIME.toString(), "time"));
    columns.add(new PropertyColumn(new Model<String>("measureURI"), Value.SortKey.MEASUREURI.toString(), "measureURI"));
    columns.add(new PropertyColumn(new Model<String>("value"), Value.SortKey.VALUE.toString(), "value"));
    columns.add(new PropertyColumn(new Model<String>("precision"), Value.SortKey.PRECISION.toString(), "precision") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    add(new DefaultDataTable("table", columns, new MeasurementHistoryDataProvider(persistence), 50));
  }

  @Override
  protected void onDetach() {
    if (listener != null) {
      listener.stop();
    }
    super.onDetach();
  }
}