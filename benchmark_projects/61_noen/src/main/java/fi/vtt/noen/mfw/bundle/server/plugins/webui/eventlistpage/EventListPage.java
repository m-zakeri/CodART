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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.eventlistpage;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistencePlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceUser;
import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ServerEvent;
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
 * A page showing the list of events in the MFW.
 *
 * @author Teemu Kanstren
 */
public class EventListPage extends WebPage implements PersistenceUser {
  private final static Logger log = new Logger(EventListPage.class);
  private PersistencePlugin persistence;
  private PersistenceServiceListener listener;

  public EventListPage() {
    BundleContext bc = WebUIPlugin.getInstance().getBundleContext();
    listener = new PersistenceServiceListener(bc, log, this);
    listener.init();

    add(new StyleSheetReference("listpageCSS", getClass(), "style.css"));

    createEventList();
  }

  //the persistenceplugin is used to access the event history from the DB
  public void setPersistence(PersistencePlugin persistence) {
    this.persistence = persistence;
  }

  public void createEventList() {
    List<IColumn<?>> columns = new ArrayList<IColumn<?>>();

    //first parameter = displayed name, second = sort key passed to dataprovider, third = key used to retrieve table values from data objects
    columns.add(new PropertyColumn(new Model<String>("timeString"), ServerEvent.SortKey.TIME.toString(), "timeString"));
    columns.add(new PropertyColumn(new Model<String>("source"), ServerEvent.SortKey.TIME.toString(), "source"));
    columns.add(new PropertyColumn(new Model<String>("message"), ServerEvent.SortKey.MESSAGE.toString(), "message"));

    add(new DefaultDataTable("table", columns, new EventHistoryDataProvider(persistence), 50));

  }

  @Override
  protected void onDetach() {
    if (listener != null) {
      listener.stop();
    }
    super.onDetach();
  }
}
