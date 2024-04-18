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
import java.util.List;

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
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;


@Path("/client/history")
public class MeasurementHistoryResource {
  private final static Logger log = new Logger(MeasurementHistoryResource.class);
  private RestPlugin restPlugin;

  @POST
  @Consumes( MediaType.APPLICATION_XML )
  @Produces( MediaType.APPLICATION_XML )
  public MeasurementHistory requestHistory( @HeaderParam("authorization") String authHeader, HistoryRequest request ) {
    restPlugin = RestPlugin.getInstance();
    
    log.debug("measurementHistory request");

    MeasurementHistory measurementHistory = null;
    
    if ( restPlugin.isAlive( authHeader ) )
    {
        measurementHistory = new MeasurementHistory();
        
        // read measurements history from database according to requested time interval
        // and push it to the client        
        List<Value> measurements = restPlugin.getHistory( request );
        
        ArrayList<MeasurementValue> values = new ArrayList<MeasurementValue>();
        
        // conversion to rest class
        if ( measurements != null )
        {
            for ( Value value : measurements )
            {
                String bmid = Long.toString( value.getBm().getBmId() );
                Long timestamp = value.getTime().getTime();
                values.add( new MeasurementValue( bmid, value.valueString(), timestamp ) );
            }
        }
        
        measurementHistory.setValues( values );
    }
    else
    {
        throw new WebApplicationException( Status.BAD_REQUEST );
    }
    
    return measurementHistory;
  }
}   