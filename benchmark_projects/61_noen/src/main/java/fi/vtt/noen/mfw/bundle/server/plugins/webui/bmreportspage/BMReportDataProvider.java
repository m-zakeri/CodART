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
import org.apache.wicket.extensions.markup.html.repeater.util.SortParam;
import org.apache.wicket.extensions.markup.html.repeater.util.SortableDataProvider;
import org.apache.wicket.model.IModel;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

import fi.vtt.noen.mfw.bundle.server.plugins.webui.WebUIPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMReport;

/**
 * @author Teemu Kanstr�n
 */
public class BMReportDataProvider extends SortableDataProvider<BMReport> {
  private final static Logger log = new Logger(BMReportDataProvider.class);
  private WebUIPlugin webUi;
  private boolean matchReference;
  List<BMReport> bmReportsFiltered;

  public BMReportDataProvider(WebUIPlugin webUi, boolean matchReference) {
    this.webUi = webUi;
    this.matchReference = matchReference;
    setSort("measure_uri", true);
  }

  public Iterator<BMReport> iterator(int i, int i1) {
    List<BMReport> bmReports = webUi.getBMReports();
    bmReportsFiltered = new ArrayList<BMReport>();
    if (matchReference) {
      for (BMReport bmReport : bmReports) {
        if (bmReport.isMatchReference()) {
          bmReportsFiltered.add(bmReport);
        } 
      }
    } else {
      for (BMReport bmReport : bmReports) {
        if (!bmReport.isMatchReference()) {
          bmReportsFiltered.add(bmReport);
        } 
      }
    }    
    SortParam sp = getSort();
    String key = sp.getProperty();
    log.debug("sort key:" + key);
    if (sp.isAscending()) {
      Collections.sort(bmReportsFiltered, new ValueComparator(key, true));
    } else {
      Collections.sort(bmReportsFiltered, new ValueComparator(key, false));
    }
    return bmReportsFiltered.subList(i, i + i1).iterator();
  }

  public int size() {
    List<BMReport> bmReports = webUi.getBMReports();
    bmReportsFiltered = new ArrayList<BMReport>();
    if (matchReference) {
      for (BMReport bmReport : bmReports) {
        if (bmReport.isMatchReference()) {
          bmReportsFiltered.add(bmReport);
        } 
      }
    } else {
      for (BMReport bmReport : bmReports) {
        if (!bmReport.isMatchReference()) {
          bmReportsFiltered.add(bmReport);
        } 
      }
    } 
    return bmReportsFiltered.size();
  }

  public IModel<BMReport> model(BMReport bmReport) {
    return new DetachableBMReportModel(bmReport);
  }
}