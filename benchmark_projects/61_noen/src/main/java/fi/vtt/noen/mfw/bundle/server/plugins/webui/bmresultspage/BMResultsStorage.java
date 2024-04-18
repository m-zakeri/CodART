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

package fi.vtt.noen.mfw.bundle.server.plugins.webui.bmresultspage;

//import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

public class BMResultsStorage {
  private final Vector<BMResult> bmResults = new Vector<BMResult>(100);
  private final int maxLimit = 1000;
  
  public synchronized void addBMResult(BMResult bmResult) {
    // limit the maximum size of bm results by removing the oldest one
    if (bmResults.size() >= maxLimit) {
      bmResults.remove(0);
    }
    bmResults.add(bmResult);
  }

  public synchronized List<BMResult> getBmResults() {
    return bmResults;
  }
  
}
