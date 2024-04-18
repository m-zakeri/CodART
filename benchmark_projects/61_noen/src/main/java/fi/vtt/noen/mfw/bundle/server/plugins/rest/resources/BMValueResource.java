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

import fi.vtt.noen.mfw.bundle.common.Logger;

import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.core.MediaType;

//to test sending bm results via REST interface

@Path("/bmvalue/{bmid}")
public class BMValueResource {
  private final static Logger log = new Logger(BMValueResource.class);

  @POST
  @Consumes(MediaType.APPLICATION_XML)
  public void setBMResult(@PathParam("bmid") String bmId, BMValue value) {
    log.debug("-----------BMValue received");
    log.debug("-----------bmId: " + bmId);
    log.debug("-----------time: " + value.getTime());
    log.debug("-----------value: " + value.getValue());
  }
}   