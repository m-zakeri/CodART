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
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.DMDefinition;
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.form.TextArea;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.value.ValueMap;

import java.util.Collection;
import java.util.List;

/**
 * @author Teemu Kanstren
 */
public class AttachBMForm extends Form<ValueMap> {
  private final static Logger log = new Logger(AttachBMForm.class);
  private final ValueMap properties = new ValueMap();
  private final DerivedMeasuresPage parent;
  private final RegistryPlugin registry;

  public AttachBMForm(String id, DerivedMeasuresPage parent, RegistryPlugin registry) {
    super(id);
    this.registry = registry;
    add(new TextArea("attachbmid", new PropertyModel<String>(properties, "attachbmid")));
    this.parent = parent;
  }

  @Override
  protected void onSubmit() {
    int bmid = properties.getAsInteger("attachbmid");
    //TODO: insert checks for valid name, give error msg if not
    log.debug("BMId:"+bmid);
    DMDefinition dm = parent.getSelected();
    List<BMDescription> requiredBm = dm.getRequiredBM();
    //TODO: update plugin instances from WebUIPlugin
//    BundleContext bc = WebUIPlugin.getInstance().getBundleContext();
    Collection<BMDescription> bms = registry.getAvailableBM();
    for (BMDescription bm : bms) {
      if (bm.getBmId() == bmid) {
        //this will actually link the BM to the DM also in registry since the list object is shared..
        requiredBm.add(bm);
        break;
      }
    }
    parent.update();
  }
}