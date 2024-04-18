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
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.bmlistpage.BMListDataProvider;
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
public class ProbeListPage extends WebPage implements RegistryUser {
  private final static Logger log = new Logger(ProbeListPage.class);
  //the table of probe information
  private transient DefaultDataTable probeTable;
  //provides access to overall runtime state
  private transient RegistryPlugin registry;
  private transient RegistryServiceListener listener;

  public ProbeListPage() {
    WebUIPlugin webUIPlugin = WebUIPlugin.getInstance();
    BundleContext bc = webUIPlugin.getBundleContext();
    listener = new RegistryServiceListener(bc, log, this);
    listener.init();

    //CSS stylesheet
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));

    createProbeList();
    addAjaxUpdater();
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  //create a table providing information about all available probes
  public void createProbeList() {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();
    //first parameter = displayed name, second = sort key passed to dataprovider, third = key used to retrieve table values from data objects
    columns.add(new PropertyColumn(new Model<String>("probeId"), "probeId", "probeId") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    columns.add(new PropertyColumn(new Model<String>("bmName"), "bmName", "bmName"));
    columns.add(new PropertyColumn(new Model<String>("probeName"), "probeName", "probeName"));
    columns.add(new PropertyColumn(new Model<String>("measureURI"), "measureURI", "measureURI"));
    columns.add(new PropertyColumn(new Model<String>("precision"), "precision", "precision") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    columns.add(new PropertyColumn(new Model<String>("delay"), "delay", "delay") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });

    probeTable = new DefaultDataTable("probetable", columns, new ProbeListDataProvider(registry), 50);
    probeTable.setOutputMarkupId(true);
    add(probeTable);
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
        target.addComponent(probeTable);
      }
    });
  }

  @Override
  protected void onDetach() {
    listener.stop();
    super.onDetach();
  }
}
