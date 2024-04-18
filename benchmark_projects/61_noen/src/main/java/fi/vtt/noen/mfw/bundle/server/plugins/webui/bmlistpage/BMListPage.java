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
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage.ActionPanel;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage.ProbeInformationDataProvider;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage.ProbeListDataProvider;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.probelistpage.ProbeListItem;
import org.apache.wicket.ajax.AbstractAjaxTimerBehavior;
import org.apache.wicket.ajax.AjaxRequestTarget;
import org.apache.wicket.extensions.markup.html.repeater.data.grid.ICellPopulator;
import org.apache.wicket.extensions.markup.html.repeater.data.table.AbstractColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.basic.Label;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.markup.repeater.Item;
import org.apache.wicket.model.IModel;
import org.apache.wicket.model.Model;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.time.Duration;
import org.apache.wicket.version.undo.Change;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Provides a list of probes currently connected.
 * Links to the .html page with the same name (ProbeListPage.html).
 *
 * @author Teemu Kanstren
 */
public class BMListPage extends WebPage implements RegistryUser {
  private final static Logger log = new Logger(BMListPage.class);
  //the table of BM information
  private transient DefaultDataTable bmTable;
  //provides access to overall runtime state
  private transient RegistryPlugin registry;
  private transient RegistryServiceListener listener;
  private WebUIPlugin webUIPlugin;

  public BMListPage() {
    webUIPlugin = WebUIPlugin.getInstance();
    BundleContext bc = webUIPlugin.getBundleContext();
    listener = new RegistryServiceListener(bc, log, this);
    listener.init();

    //CSS stylesheet
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));

    createBMList();
    addAjaxUpdater();
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  //provide a list of current base measures
  public void createBMList() {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new PropertyColumn(new Model<String>("bmId"), "bmId", "bmId") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    columns.add(new PropertyColumn(new Model<String>("measureURI"), "measureURI", "measureURI"));
    columns.add(new PropertyColumn(new Model<String>("bmDescription"), "bmDescription", "bmDescription"));
    columns.add(new PropertyColumn(new Model<String>("value"), "value", "value"));

    Map<String,String> latestValues = webUIPlugin.getLatestValues();
    bmTable = new DefaultDataTable("bmtable", columns, new BMListDataProvider(registry, latestValues), 50);
    bmTable.setOutputMarkupId(true);
    add(bmTable);
  }

  //add ajax updater to keep updating probe delays every 1 second
  public void addAjaxUpdater() {
    // add the timer behavior to the page and make it update all
    // other components as well
    add(new AbstractAjaxTimerBehavior(Duration.seconds(1)) {
      /**
       * @see org.apache.wicket.ajax.AbstractAjaxTimerBehavior#onTimer(org.apache.wicket.ajax.AjaxRequestTarget)
       */
      protected void onTimer(AjaxRequestTarget target) {
        target.addComponent(bmTable);
      }
    });
  }

  @Override
  protected void onDetach() {
    listener.stop();
    super.onDetach();
  }
}
