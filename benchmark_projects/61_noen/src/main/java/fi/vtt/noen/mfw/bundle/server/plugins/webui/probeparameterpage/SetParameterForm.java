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
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.mfwclient.ProbeParameter;
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.form.TextArea;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.value.ValueMap;

import java.util.List;

public class SetParameterForm extends Form<ValueMap> {
  private final static Logger log = new Logger(SetParameterForm.class);
  private final ValueMap properties = new ValueMap();
  private final ProbeParameterPage parent;

  public SetParameterForm(String id, ProbeParameterPage parent) {
    super(id);
    add(new TextArea("paramname", new PropertyModel<String>(properties, "paramname")));
    add(new TextArea("paramvalue", new PropertyModel<String>(properties, "paramvalue")));
    this.parent = parent;
  }

  @Override
  protected void onSubmit() {
    String paramName = properties.getString("paramname");
    String paramValue = properties.getString("paramvalue");
    try {
      String probeIdString = parent.getProbeId();
      long probeId = Long.parseLong(probeIdString);
      log.debug("ProbeId:"+probeId);
      log.debug("ParamName:"+paramName);
      log.debug("ParamValue:"+paramValue);
      WebUIPlugin webUI = WebUIPlugin.getInstance();
      webUI.setProbeParameter(probeId, paramName, paramValue);
      List<ProbeParameter> params = webUI.getProbeParameters(probeId);
      parent.update(params, probeIdString);
      
    } catch (Exception e) {
      //log.debug("Error   ");
    }
    
  }
}
