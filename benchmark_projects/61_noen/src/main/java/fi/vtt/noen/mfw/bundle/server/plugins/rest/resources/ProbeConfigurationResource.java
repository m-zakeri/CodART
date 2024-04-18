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

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.HeaderParam;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response.Status;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.RestPlugin;


@Path("/client/probeconfiguration/{probeid}")
public class ProbeConfigurationResource {
  private final static Logger log = new Logger(ProbeConfigurationResource.class);
  private RestPlugin restPlugin;

  @GET
  @Produces( MediaType.APPLICATION_XML )
  public ProbeConfiguration getProbeConfiguration(@HeaderParam("authorization") String authHeader, @PathParam("probeid") String probeId ) {

    log.debug("probeConfiguration request: " + probeId);
    restPlugin = RestPlugin.getInstance();
    ProbeConfiguration pc = null; 
        
    if ( restPlugin.isAlive( authHeader ) )
    {
        // get configuration
        Collection<fi.vtt.noen.mfw.bundle.common.ProbeConfiguration> pcs = restPlugin.getProbeConfiguration( Long.parseLong( probeId ) );
        
        pc = new ProbeConfiguration();
        ArrayList<Parameter> parameters = new ArrayList<Parameter>();
        
        for ( fi.vtt.noen.mfw.bundle.common.ProbeConfiguration p : pcs )
        {
            parameters.add( new Parameter( p.getName(), p.getValue() ) );
        }
        pc.setValues( parameters );
    }
    else
    {
      throw new WebApplicationException( Status.BAD_REQUEST );
    }
    
    return pc;
  }

  @POST
  @Consumes(MediaType.APPLICATION_XML)
  public void setProbeConfgiuration(@HeaderParam("authorization") String authHeader, @PathParam("probeid") String probeId, ProbeConfiguration configuration ){

    log.debug("probeConfiguration change request: " + probeId + ", config=" + configuration);
    restPlugin = RestPlugin.getInstance();

    if ( restPlugin.isAlive( authHeader ) )
    {
      Map<String, String> parameters = new HashMap<String, String>();
      ArrayList<Parameter> config = configuration.getValues();
      
      log.debug( "  new parameters: " + config );
      
      if ( config != null )
      {
          for ( Parameter p : configuration.getValues() )
          {
            parameters.put( p.getKey(), p.getValue() );
          }
      }
      
      boolean success = restPlugin.setProbeConfiguration( Long.parseLong( probeId ), parameters );
      
      if ( !success )
      {
          throw new WebApplicationException( Status.NOT_ACCEPTABLE );
      }
    }
    else
    {
      throw new WebApplicationException( Status.BAD_REQUEST );
    }
  }
}   