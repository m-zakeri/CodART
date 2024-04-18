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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.probeparameterpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.ProbeParameter;
import org.apache.wicket.extensions.markup.html.repeater.data.table.DefaultDataTable;
import org.apache.wicket.extensions.markup.html.repeater.data.table.IColumn;
import org.apache.wicket.extensions.markup.html.repeater.data.table.PropertyColumn;
import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.basic.Label;
import org.apache.wicket.markup.html.resources.StyleSheetReference;
import org.apache.wicket.model.Model;

import java.util.ArrayList;
import java.util.List;

public class ProbeParameterPage extends WebPage {
  private final static Logger log = new Logger(ProbeParameterPage.class);
  private final long sacId = 1;
  private String probeIdString = "";
  private List<ProbeParameter> params;

  public ProbeParameterPage() {
    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));
       
    createProbeIdLabel();
    createGetParametersForm();
    createSetParameterForm();
    
    if (params != null) {
      createParameterList(params);
    } else {
      params = new ArrayList<ProbeParameter>();
      createParameterList(params);
    }
  }
  
  
  public void createParameterList(List<ProbeParameter> params) {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    columns.add(new PropertyColumn(new Model<String>("name"), "name", "name"));
    columns.add(new PropertyColumn(new Model<String>("description"), "description", "description"));
    columns.add(new PropertyColumn(new Model<String>("value"), "value", "value"));
    columns.add(new PropertyColumn(new Model<String>("mandatory"), "mandatory", "mandatory"));

    DefaultDataTable parameterTable = new DefaultDataTable("parametertable", columns, new ParameterListDataProvider(params), 8);
    add(parameterTable);
  }
  
  private void createProbeIdLabel() {
    Label probeIdLabel = new Label("currentprobeid", probeIdString);
    add(probeIdLabel);
  }
  
  private void replaceProbeIdLabel() {
    Label probeIdLabel = new Label("currentprobeid", probeIdString);
    replace(probeIdLabel);
  }
  
  private void createGetParametersForm() {
    GetParametersForm getParameters = new GetParametersForm("getParametersForm", this);
    add(getParameters);
  }
  
  private void createSetParameterForm() {
    SetParameterForm setParameter = new SetParameterForm("setParameterForm", this);
    add(setParameter);
  }
  
  public String getProbeId() {
    return probeIdString;
  }
  
  public void update(List<ProbeParameter> params2, String probeId) {
    this.probeIdString = probeId;
    replaceProbeIdLabel();
    this.params.clear();
    this.params.addAll(params2);
  }

}
