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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.derivedmeasurepage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMValue;
import org.apache.wicket.Component;
import org.apache.wicket.extensions.markup.html.repeater.data.grid.ICellPopulator;
import org.apache.wicket.extensions.markup.html.repeater.data.table.AbstractColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.basic.Label;
import org.apache.wicket.markup.html.form.TextArea;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.markup.repeater.Item;
import org.apache.wicket.model.IModel;
import org.apache.wicket.model.Model;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.value.ValueMap;
import org.apache.wicket.version.undo.Change;
import org.osgi.framework.BundleContext;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class DerivedMeasuresPage extends WebPage implements RegistryUser {
  private final static Logger log = new Logger(DerivedMeasuresPage.class);
  private DMDefinition selected;
  private DMInformationDataProvider dmInformationDataProvider;
  private List<DMDefinition> dms;
  private ScriptForm scriptForm;
  private ValueMap bmVariableProperties = new ValueMap();
  private final List<Component> conditionallyVisible = new ArrayList<Component>();
  private RegistryPlugin registry;

  public DerivedMeasuresPage() {
    BundleContext bc = WebUIPlugin.getInstance().getBundleContext();
    RegistryServiceListener listener = new RegistryServiceListener(bc, log, this);
    listener.init();

    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
    add(new Label("selectedLabel", new PropertyModel<String>(this, "selectedDMLabel")));
    createDMTable();
    createDMValueTable();
    createDMInformation();
    createBMVariableList();
    createDMScriptForm();
    createNewDMForm();
    createAttachBMForm();
    updateVisibilities();
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }

  @Override
  protected void onBeforeRender() {
    super.onBeforeRender();

  }

  private void createAttachBMForm() {
    AttachBMForm attachBM = new AttachBMForm("attachBMForm", this, registry);
    conditionallyVisible.add(attachBM);
    add(attachBM);
  }

  private void createNewDMForm() {
    NewDMForm newDM = new NewDMForm("newDMForm", this, registry);
    add(newDM);
  }

  private void createDMScriptForm() {
    scriptForm = new ScriptForm("scriptForm");
    conditionallyVisible.add(scriptForm);
    add(scriptForm);
  }

  private void createBMVariableList() {
    TextArea textArea = new TextArea("bmvariables", new PropertyModel<String>(bmVariableProperties, "bmvariables"));
    conditionallyVisible.add(textArea);
    add(textArea);
  }

  private void updateBMVariableList() {
    String variables = "//This will be appended to the beginning of your script to define BM variables\n";
    if (selected != null) {
      log.debug("building BM variable list for:"+selected.getRequiredBM());
      for (BMDescription bm : selected.getRequiredBM()) {
        variables += "bm"+bm.getBmId()+" = <value>\n";
      }
    }
    bmVariableProperties.put("bmvariables", variables);
  }

  public void createDMInformation() {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();
    columns.add(new PropertyColumn(new Model<String>("id"), "id", "id"));
    columns.add(new PropertyColumn(new Model<String>("targetId"), "targetId", "targetId"));
    columns.add(new PropertyColumn(new Model<String>("measureId"), "measureId", "measureId"));
    columns.add(new PropertyColumn(new Model<String>("precision"), "precision", "precision") {
      @Override
      public String getCssClass() {
        return "numeric";
      }
    });
    dmInformationDataProvider = new DMInformationDataProvider(registry);
    DefaultDataTable dmInformationTable = new DefaultDataTable("dminformation", columns, dmInformationDataProvider, 8);
    conditionallyVisible.add(dmInformationTable);
    add(dmInformationTable);
  }

  private void createDMTable() {
    dms = registry.getDerivedMeasures();
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new AbstractColumn<DMDefinition>(new Model<String>("Actions")) {
      public void populateItem(Item<ICellPopulator<DMDefinition>> cellItem, String componentId, IModel<DMDefinition> model) {
        cellItem.add(new ActionPanel(DerivedMeasuresPage.this, componentId, model));
      }
    });

    columns.add(new PropertyColumn(new Model<String>("name"), "name", "name"));

    DefaultDataTable dmTable = new DefaultDataTable("dmtable", columns, new DMListDataProvider(dms), 8);
    dmTable.setOutputMarkupId(true);
    add(dmTable);
  }

  private void createDMValueTable() {
    List<DMValue> dmValues = createDMValueList();
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new PropertyColumn(new Model<String>("id"), "id", "id"));
    columns.add(new PropertyColumn(new Model<String>("name"), "name", "name"));
    columns.add(new PropertyColumn(new Model<String>("value"), "value", "value"));
    columns.add(new PropertyColumn(new Model<String>("missing BM"), "missingBM", "missingBM"));

    DefaultDataTable dmValueTable = new DefaultDataTable("dmvaluetable", columns, new DMValueListDataProvider(dmValues), 8);
    dmValueTable.setOutputMarkupId(true);
    conditionallyVisible.add(dmValueTable);
    add(dmValueTable);
  }

  private List<DMValue> createDMValueList() {
    WebUIPlugin webui = WebUIPlugin.getInstance();
    List<DMValue> dmValues = new ArrayList<DMValue>();
    for (DMDefinition dm : dms) {
      DMValue dmValue = webui.getDMMonitor().getValueFor(dm.getId());
      dmValues.add(dmValue);
      log.debug("Added DM value:"+dmValue);
    }
    return dmValues;
  }

  /**
   * @return string representation of selected probe property
   */
  public String getSelectedDMLabel() {
    if (selected == null) {
      return "No DM Selected";
    } else {
      return selected.getName();
    }
  }

  /**
   * @return selected contact
   */
  public DMDefinition getSelected() {
    return selected;
  }

  /**
   * sets selected contact
   *
   * @param selected
   */
  public void setSelected(DMDefinition selected) {
    addStateChange(new Change() {
      private final DMDefinition old = DerivedMeasuresPage.this.selected;

      @Override
      public void undo() {
        DerivedMeasuresPage.this.selected = old;
        dmInformationDataProvider.setDM(old);
      }
    });
    this.selected = selected;
    dmInformationDataProvider.setDM(selected);
    scriptForm.setDM(selected);
    updateBMVariableList();
    updateVisibilities();
  }

  public void update() {
    dms.clear();
    List<DMDefinition> dms2 = registry.getDerivedMeasures();
    this.dms.addAll(dms2);
    dmInformationDataProvider.setDM(selected);
    updateBMVariableList();
  }

  private void updateVisibilities() {
    boolean visible = (selected != null);
    for (Component component : conditionallyVisible) {
      component.setVisible(visible);
    }
  }
}
