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
import java.util.List;

import javax.ws.rs.GET;
import javax.ws.rs.HeaderParam;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response.Status;

import org.mortbay.log.Log;

import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.RestPlugin;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;

@Path("/client/probes")
public class ProbesResource {
  private final static Logger log = new Logger(ProbesResource.class);
  private RestPlugin restPlugin;

  @GET
  @Produces(MediaType.APPLICATION_XML)
  public ProbesInfo getProbes( @HeaderParam("authorization") String authHeader )
  {
    restPlugin = RestPlugin.getInstance();
    
    log.debug( "get probes, auth: " + authHeader );
    
    ProbesInfo probesInfo = null;
    
    if ( restPlugin.isAlive( authHeader ) )
    {
        probesInfo = new ProbesInfo();
        
        Collection<TargetDescription> tds = restPlugin.getTargets();
        List<BMDescription> bms = restPlugin.getAvailableBMList();
        List<ProbeDescription> pds = restPlugin.getProbes();
        
        ArrayList<Target> targets = new ArrayList<Target>();
        ArrayList<BaseMeasure> baseMeasures = new ArrayList<BaseMeasure>();
        ArrayList<Probe> probes = new ArrayList<Probe>();
        
        for ( TargetDescription td : tds )
        {
            String tid = Long.toString( td.getTargetId() );
            targets.add( new Target( tid, td.getTargetName(), td.getTargetType() ) );
        }

        for ( BMDescription bmd : bms )
        {
            String tid = Long.toString( bmd.getTarget().getTargetId() );
            String bid = Long.toString( bmd.getBmId() );
            baseMeasures.add( new BaseMeasure( bid, bmd.getBmName(), bmd.getBmClass(), bmd.getBmDescription(), tid, bmd.getDataType().name() ) );
            /*
            ProbeDescription pd = restPlugin.getProbeForBM( bmd.getBmId() );

            String pid = Long.toString( pd.getProbeId() );
            probes.add( new Probe( pid, pd.getProbeName(), bid ) );
            */
        }
        
        
        for ( ProbeDescription pd : pds )
        {
            String pid = Long.toString( pd.getProbeId() );
            String bid = Long.toString( pd.getBm().getBmId() );
            probes.add( new Probe( pid, pd.getProbeName(), bid ) );
        }
        
//        targets.add( new Target( "target-01", "Target name", "Target type" ) );
//        baseMeasures.add( new BaseMeasure( "bm-01", "BaseMeasure name", "BaseMeasure clas", "BaseMeasure description", "target-01", "String" ) );
//        baseMeasures.add( new BaseMeasure( "bm-02", "BaseMeasure name 2", "BaseMeasure clas 2", "BaseMeasure description 2", "target-01", "Boolean" ) );
//        probes.add( new Probe( "probe-01", "Probe name", "bm-01" ) );
//        probes.add( new Probe( "probe-02", "Probe name 2", "bm-02" ) );
        
        probesInfo.setTargets( targets );
        probesInfo.setBaseMeasures( baseMeasures );
        probesInfo.setProbes( probes );
        //List<BMDescription> bms = restPlugin.getAvailableBMList();
    }
    else
    {
        throw new WebApplicationException( Status.BAD_REQUEST );
    }
    
    return probesInfo;
  }

}   