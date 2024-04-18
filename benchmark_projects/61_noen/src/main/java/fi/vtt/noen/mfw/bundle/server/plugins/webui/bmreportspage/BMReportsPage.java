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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmreportspage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMReport;

import org.apache.wicket.RequestCycle;
import org.apache.wicket.ajax.AbstractAjaxTimerBehavior;
import org.apache.wicket.ajax.AjaxRequestTarget;
import org.apache.wicket.extensions.markup.html.repeater.data.grid.ICellPopulator;
import org.apache.wicket.extensions.markup.html.repeater.data.table.AbstractColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.markup.repeater.Item;
import org.apache.wicket.model.IModel;
import org.apache.wicket.model.Model;
import org.apache.wicket.util.time.Duration;

import java.util.ArrayList;
import java.util.List;

public class BMReportsPage extends WebPage {
  private final static Logger log = new Logger(BMReportsPage.class);
  private transient WebUIPlugin webUi;
  private transient DefaultDataTable bmReportTable1;
  private transient DefaultDataTable bmReportTable2;

  public BMReportsPage() throws Exception {
    webUi = WebUIPlugin.getInstance();
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    createBMReportsList();
    addAjaxUpdater();
  }

  public void createBMReportsList() {
    
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();
    columns.add(new PropertyColumn(new Model<String>("measureTime"), "measureTime", "measureTime"));
    columns.add(new PropertyColumn(new Model<String>("measureURI"), "measureURI", "measureURI"));
    //columns.add(new PropertyColumn(new Model<String>("referenceValue"), "referenceValue", "referenceValue"));
    
    List<IColumn<?>> columns2 = new ArrayList<IColumn<?>>();
    columns2.add(new AbstractColumn<BMReport>(new Model<String>("Actions")) {
      public void populateItem(Item<ICellPopulator<BMReport>> cellItem, String componentId, IModel<BMReport> model) {
        cellItem.add(new ActionPanel(BMReportsPage.this, componentId, model));
      }
    });
    columns2.add(new PropertyColumn(new Model<String>("measureTime"), "measureTime", "measureTime"));
    columns2.add(new PropertyColumn(new Model<String>("measureURI"), "measureURI", "measureURI"));
    columns2.add(new PropertyColumn(new Model<String>("referenceValue"), "referenceValue", "referenceValue"));
    columns2.add(new PropertyColumn(new Model<String>("currentValue"), "currentValue", "currentValue"));
    
    bmReportTable1 = new DefaultDataTable("table", columns, new BMReportDataProvider(webUi, true), 10);
    bmReportTable1.setOutputMarkupId(true);
    bmReportTable2 = new DefaultDataTable("table2", columns2, new BMReportDataProvider(webUi, false), 10);
    bmReportTable2.setOutputMarkupId(true);    
    add(bmReportTable1);
    add(bmReportTable2);
  }
  
  private List<BMReport> readBMReports() {
    return webUi.getBMReports();
  }
  
  //add ajax updater to keep updating tables every 5 seconds
  public void addAjaxUpdater() {
    add(new AbstractAjaxTimerBehavior(Duration.seconds(5)) {
      /**
       * @see org.apache.wicket.ajax.AbstractAjaxTimerBehavior#onTimer(org.apache.wicket.ajax.AjaxRequestTarget)
       */
      protected void onTimer(AjaxRequestTarget target) {
        target.addComponent(bmReportTable1);
        target.addComponent(bmReportTable2);
      }
    });
  }

  public void changeReference(BMReport bmReport) {
    log.debug("changeReference called");
    webUi.setReference(bmReport);
  }

  @Override
  protected void onDetach() {
    super.onDetach();
    webUi.clearBMReports();
  }
}