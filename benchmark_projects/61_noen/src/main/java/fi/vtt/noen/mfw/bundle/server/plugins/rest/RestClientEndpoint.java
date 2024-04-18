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

package fi.vtt.noen.mfw.bundle.server.plugins.rest;


import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.WebResource;
import fi.vtt.noen.mfw.bundle.common.Const;
import fi.vtt.noen.mfw.bundle.common.DataType;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEvent;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.BMValue;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Event;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.MeasurementHistory;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.MeasurementValue;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;

import javax.ws.rs.core.MediaType;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Properties;


/**
 * @author Petri Heinonen
 */
public class RestClientEndpoint {
  private final static Logger log = new Logger(RestClientEndpoint.class);
  private WebResource wr;

  public RestClientEndpoint( String url ) {
    log.debug("Initializing REST plugin with endpoint "+url);
    Client client = Client.create();
    wr = client.resource(url);
    log.debug("REST plugin initialized");
  }

  public void measurement(Value value) {
    log.debug("Sending BM results via REST interface");
    // TODO Need to handle multiple measurement values
    // There should be a queue for measurements that comes during
    // measurement result sending time interval
    MeasurementHistory values = new MeasurementHistory();
    MeasurementValue m = new MeasurementValue( Long.toString( value.getBm().getBmId() ), value.getString(), value.getTime().getTime() );
    ArrayList<MeasurementValue> ms = new ArrayList<MeasurementValue>();
    ms.add( m );
    values.setValues( ms );
    
    wr.path("client/measurements").type(MediaType.APPLICATION_XML).post(values);
  }
  
  public void probeEvent( ProbeEvent pe )
  {
    Event e = new Event( DataType.PROBE_EVENT.name(), "Probe event occurred." );
    wr.path( "client/event" ).type( MediaType.APPLICATION_XML ).post( e );
  }
  
  public void probeRegistered( ProbeRegistered pr )
  {
    Event e = new Event( DataType.PROBE_REGISTERED.name(), "Probe registered." );
    wr.path( "client/event" ).type( MediaType.APPLICATION_XML ).post( e );
  }
  
  public void probeDisabled( ProbeDisabled pd )
  {
    Event e = new Event( DataType.PROBE_DISABLED.name(), "Probe disabled." );
    wr.path( "client/event" ).type( MediaType.APPLICATION_XML ).post( e );
  }
}