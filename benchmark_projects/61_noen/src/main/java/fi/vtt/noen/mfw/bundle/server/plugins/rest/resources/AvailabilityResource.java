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

package fi.vtt.noen.mfw.bundle.server.plugins.rest.resources;

import fi.vtt.noen.mfw.bundle.server.plugins.rest.RestPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import java.util.List;

@Path("/availability")
public class AvailabilityResource {
  private RestPlugin restPlugin;

  @GET
  @Produces(MediaType.APPLICATION_XML)
  public Availability getBMAvailability() {

    restPlugin = RestPlugin.getInstance();
    List<BMDescription> bms = restPlugin.getAvailableBMList();

    Availability availability = new Availability();

    if (!bms.isEmpty()) {
      for (BMDescription bmDesc : bms) {
        /*
        BM bm = new BM();
        bm.setBmId(1);
        bm.setBmClass("class");
        bm.setBmName("name");
        bm.setBmDescription("description");
        availability.addBm(bm);*/

        BM bm = new BM();
        bm.setBmId(bmDesc.getBmId());
        bm.setBmClass(bmDesc.getBmClass());
        bm.setBmName(bmDesc.getBmName());
        bm.setBmDescription(bmDesc.getBmDescription());
        availability.addBm(bm);
      }
    }

    return availability;

  }

}   