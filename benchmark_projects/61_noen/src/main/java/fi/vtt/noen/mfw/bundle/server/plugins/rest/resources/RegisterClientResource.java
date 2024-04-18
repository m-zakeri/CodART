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

import javax.ws.rs.Consumes;
import javax.ws.rs.HeaderParam;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response.Status;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.RestPlugin;


@Path("/client/register")
public class RegisterClientResource {
  private final static Logger log = new Logger(RegisterClientResource.class);
  private RestPlugin restPlugin;

  @POST
  @Consumes( MediaType.APPLICATION_XML )
  @Produces( MediaType.APPLICATION_XML )
  public Session registerClient( @HeaderParam("authorization") String authHeader, ClientRequest client ) {
    restPlugin = RestPlugin.getInstance();
    
    log.debug("Registering new client ("+client.getName()+":"+client.getEndpoint()+") with auth-header: " + authHeader );

    Session session = null;
    
    if ( restPlugin.isAuthorized( authHeader ) )
    {
        if ( client != null && client.getName() != null && client.getEndpoint() != null )
        {
            session = restPlugin.registerClient( authHeader, client );
            log.debug("Session: " + session.getId() );
        }
        else
        {
            throw new WebApplicationException( Status.BAD_REQUEST );
        }
    }
    else
    {
        throw new WebApplicationException( Status.UNAUTHORIZED );
    }
    
    return session;
  }
}   