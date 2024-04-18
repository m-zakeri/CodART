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

import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.AvailabilityResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.BMRequestResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.BMValueResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.MeasurementHistoryResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ProbeConfigurationResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ProbesResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.RegisterClientResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.RequestBaseMeasureResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.RequestFrameworkInfoResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ShutdownResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.SubscribeBaseMeasureResource;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.SubscriptionResource;

import javax.ws.rs.core.Application;
import java.util.HashSet;
import java.util.Set;

/**
 * @author Teemu Kanstren
 */
public class JerseyApplication extends Application {
  @Override
  public Set<Class<?>> getClasses() {
    Set<Class<?>> resources = new HashSet<Class<?>>();
    resources.add(ShutdownResource.class);
    
    // new ones
    resources.add(RegisterClientResource.class);
    resources.add(ProbesResource.class);
    resources.add(RequestBaseMeasureResource.class);
    resources.add(MeasurementHistoryResource.class);
    resources.add(SubscribeBaseMeasureResource.class);
    resources.add(ProbeConfigurationResource.class);
    resources.add(RequestFrameworkInfoResource.class);
    
    
    resources.add(AvailabilityResource.class);
    resources.add(SubscriptionResource.class);
    //resources.add(UnsubscriptionResource.class);
    resources.add(BMRequestResource.class);
    //MFW listens bm results itself. just for testing 
    resources.add(BMValueResource.class);
    return resources;
  }

}
