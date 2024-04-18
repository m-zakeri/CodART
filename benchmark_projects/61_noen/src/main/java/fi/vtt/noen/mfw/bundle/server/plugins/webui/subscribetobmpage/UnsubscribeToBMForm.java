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
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.form.TextArea;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.value.ValueMap;


public class UnsubscribeToBMForm extends Form<ValueMap> {
  private final static Logger log = new Logger(UnsubscribeToBMForm.class);
  private final ValueMap properties = new ValueMap();

  public UnsubscribeToBMForm(String id) {
    super(id);
    add(new TextArea("bmid", new PropertyModel<String>(properties, "bmid")));
    add(new TextArea("deviceid", new PropertyModel<String>(properties, "deviceid")));
  }

  @Override
  protected void onSubmit() {
    String bmId = properties.getString("bmid");
    String deviceId = properties.getString("deviceid");
    try {
      log.debug("bmId:"+bmId);
      log.debug("deviceId:"+deviceId);
      WebUIPlugin webUI = WebUIPlugin.getInstance();
      webUI.unsubscribeToBM(Long.parseLong(bmId), Long.parseLong(deviceId));
      
    } catch (Exception e) {
      //log.debug("Error   ");
    }
    
  }
}
