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

import fi.vtt.noen.mfw.bundle.blackboard.Blackboard;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.form.TextArea;
import org.apache.wicket.model.PropertyModel;
import org.apache.wicket.util.value.ValueMap;

/**
 * @author Teemu Kanstren
 */
public class NewDMForm extends Form<ValueMap> {
  private final static Logger log = new Logger(NewDMForm.class);
  private final ValueMap properties = new ValueMap();
  private final DerivedMeasuresPage parent;
  private final RegistryPlugin registry;

  public NewDMForm(String id, DerivedMeasuresPage parent, RegistryPlugin registry) {
    super(id);
    this.registry = registry;
    add(new TextArea("name", new PropertyModel<String>(properties, "name")));
    this.parent = parent;
  }

  @Override
  protected void onSubmit() {
    String name = properties.getString("name");
    //TODO: insert checks for valid name, give error msg if not
    log.debug("Name:"+name);
    Blackboard bb = WebUIPlugin.getInstance().locateBlackboard();
    registry.createDM(name, null);
    parent.update();
  }
}
