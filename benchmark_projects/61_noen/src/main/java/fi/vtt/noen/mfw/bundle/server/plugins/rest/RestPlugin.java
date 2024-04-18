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

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

import org.osgi.framework.BundleContext;

import com.sun.jersey.core.util.Base64;

import fi.vtt.noen.mfw.bundle.common.BasePlugin;
import fi.vtt.noen.mfw.bundle.common.DataObject;
import fi.vtt.noen.mfw.bundle.common.KnowledgeSource;
import fi.vtt.noen.mfw.bundle.common.Logger;
import fi.vtt.noen.mfw.bundle.common.ProbeConfiguration;
import fi.vtt.noen.mfw.bundle.probe.shared.ProbeEvent;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistencePlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.persistence.PersistenceUser;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.registry.RegistryUser;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ClientRequest;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.FrameworkInfo;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.HistoryRequest;
import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.Session;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerPlugin;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerServiceListener;
import fi.vtt.noen.mfw.bundle.server.plugins.xmlrpc.ServerUser;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.BMDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeDisabled;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.ProbeRegistered;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.TargetDescription;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value;
import fi.vtt.noen.mfw.bundle.server.shared.datamodel.Value.SortKey;

/**
 * @author Teemu Kanstren
 */
public class RestPlugin extends BasePlugin implements KnowledgeSource, RegistryUser, ServerUser, PersistenceUser {
  private final static Logger log = new Logger(RestPlugin.class);
  private static RestPlugin restPlugin = null;
  //for the server-agent to communicate with the probe-agents
  private ServerPlugin server;
  //for accessing runtime state
  private RegistryPlugin registry;
  //provides bundle to database
  private PersistencePlugin persistence;
  //for sending BM results
//  private RestClient restClient;
  //(sac)Id for measurement subscriptions
  private long restId = -2;
  // registered clients
  private Map<String, ClientRequest> clients;
  // client subsciptions
  private ClientSubscriptionRegistry subs;

  public static RestPlugin getInstance() {
    return restPlugin;
  }

  public RestPlugin(BundleContext bc) {
    super(bc, log);

    //set up listeners to capture server-agent and registry services
    ServerServiceListener serverListener = new ServerServiceListener(bc, log, this);
    serverListener.init();

    RegistryServiceListener listener = new RegistryServiceListener(bc, log, this);
    listener.init();
    
    PersistenceServiceListener persListener = new PersistenceServiceListener( bc, log, this );
    persListener.init();

    restPlugin = this;

//    restClient = new RestClient();
    clients = new LinkedHashMap<String, ClientRequest>();
    subs = new ClientSubscriptionRegistry();
  }

  public void setServer(ServerPlugin server) {
    this.server = server;
  }

  public void setRegistry(RegistryPlugin registry) {
    this.registry = registry;
  }
  
  @Override
  public void setPersistence( PersistencePlugin persistence )
  {
    this.persistence = persistence;
  }

  public static void main(String[] args) {
    new RestPlugin(null).start();
  }

  public void start() {
  }

  public void stop() {

  }

  //Gives a list of available BM.
  public List<BMDescription> getAvailableBMList() {
    return registry.getAvailableBM();
  }
  
  public List<ProbeDescription> getProbes()
  {
      return registry.getProbes();
  }
  
  public ProbeDescription getProbeForBM( long bmId )
  {
      return registry.getProbeForBM( bmId );
  }
  
  public Collection<TargetDescription> getTargets()
  {
      return registry.getTargets();
  }

  //Requests for a given measurement to be provided
  public boolean requestBM(long bmId) {
    log.debug("requestBM");
    ProbeDescription probe = registry.getProbeForBM(bmId);
    long subscriptionId = registry.addMeasurementRequest(restId, probe.getBm(), probe.getProbeId());
    server.requestBM(bmId, subscriptionId);
    return true;
  }

  public void requestBaseMeasure( String base64auth, long bmId )
  {
    ClientRequest client = clients.get( extractAuthentication( base64auth ) );
    log.debug( "Client (" + client.getName() + ") is requesting base measure, id=" + bmId );
    ProbeDescription probe = registry.getProbeForBM(bmId);
    long subscriptionId = registry.addMeasurementRequest(restId, probe.getBm(), probe.getProbeId());
    server.requestBM(bmId, subscriptionId);
  }

  //Requests for a given measurement to be provided
  public void subscribeToBM(long bmId, long interval) {
    log.debug("subscribeToBM");
    ProbeDescription probe = registry.getProbeForBM(bmId);
    long subscriptionId = registry.addSubscription(restId, probe.getBm(), interval, probe.getProbeId());
    server.subscribeToBM(bmId, interval, subscriptionId);
  }

  public void subscribeBaseMeasure( String authHeader, long id, long interval )
  {
    ProbeDescription probe = registry.getProbeForBM( id );
    
    long subscriptionId = registry.addSubscription(restId, probe.getBm(), interval, probe.getProbeId());
    server.subscribeToBM(id, interval, subscriptionId);
    
    ClientRequest client = clients.get( extractAuthentication( authHeader ) );
    subs.add( subscriptionId, client );
  }

  //removes an existing subscription
  public void unSubscribeToBM(long bmId) {
    log.debug("unSubscribeToBM");
    long subscriptionId = registry.getIdForSubscription(restId, bmId);
    server.unSubscribeToBM(bmId, subscriptionId);
    registry.removeSubscription(restId, subscriptionId);
  }

  public void unsubscribeBaseMeasure( String authHeader, long id )
  {
    long subscriptionId = registry.getIdForSubscription(restId, id);
    server.unSubscribeToBM(id, subscriptionId);
    registry.removeSubscription(restId, subscriptionId);
    
    ClientRequest client = clients.get( extractAuthentication( authHeader ) );
    subs.remove( subscriptionId, client );
  }

  public void bmValue(Value value) {
    log.debug("received BM value");

    long subscriptionId = value.getSubscriptionId();
    long sacId = registry.getSacIdForSubscription(subscriptionId);

    if (sacId == restId) {
      log.debug("subscriptionId: " + subscriptionId + ", sacId: " + sacId);
      ArrayList<ClientRequest> clients = subs.get( subscriptionId );
      //if one time measurement remove subscription from registry
      if (registry.getFrequencyForSubscription(subscriptionId) == 0) {
        registry.removeSubscription(restId, subscriptionId);
        for ( ClientRequest client : clients )
        {
            subs.remove( subscriptionId, client );
        }
      }
      
      for ( ClientRequest client : clients )
      {
        log.debug( "send value to: " + client.getName() +",(" + client.getEndpoint() +")" );
        try
        {
          new RestClientEndpoint( client.getEndpoint() ).measurement( value );             
        }
        catch ( Exception e )
        {
          e.printStackTrace();
        }
      }
    }
  }
  
  public void event( DataObject data )
  {
      log.debug("received probe event");
      ProbeEvent pe = null;
      ProbeRegistered pr = null;
      ProbeDisabled pd = null;
      
      if ( data instanceof ProbeEvent )
      {
        pe = (ProbeEvent)data;
      }
      else if ( data instanceof ProbeRegistered )
      {
        pr = (ProbeRegistered)data;
      }
      else if ( data instanceof ProbeDisabled )
      {
        pd = (ProbeDisabled)data;
      }
      
      for ( ClientRequest client : clients.values() )
      {
        log.debug( "send value to: " + client.getName() +",(" + client.getEndpoint() +")" );
        try
        {
          RestClientEndpoint rce = new RestClientEndpoint( client.getEndpoint() );
          if ( pe != null ) rce.probeEvent( pe );
          if ( pr != null ) rce.probeRegistered( pr );
          if ( pd != null ) rce.probeDisabled( pd );
        }
        catch ( Exception e )
        {
          e.printStackTrace();
        }
      }
  }

  //list of information to be received from the blackboard
  public Set getCommands() {
    return createCommandSet(Value.class);
  }

  public void process(DataObject data) {
    if (data instanceof Value) {
      Value value = (Value) data;
      log.debug("received value:" + value);
      bmValue(value);
    }
    else if ( data instanceof ProbeEvent || data instanceof ProbeRegistered || data instanceof ProbeDisabled )
    {
      event( data );
    }
  }

  public String getName() {
    return RestPlugin.class.getName();
  }

  public Session registerClient( String base64auth, ClientRequest client )
  {
    log.debug( "Registering client: " + client );
    String authentication = extractAuthentication( base64auth );
      
    // if client has already registered, all subscriptions should be released
    if ( clients.containsKey( authentication ) )
    {
      clients.remove( authentication );
      
      //TODO: release all subsciptions here:
      
      //TODO: add mechanism for outdating session
    }
      
    // create new session for the client
    UUID id = UUID.randomUUID();
    Session session = new Session( id );
    client.setSession( session );
    
    clients.put( authentication, client );
    
    return session;
  }

  public boolean isAlive( String base64auth )
  {
    return clients.containsKey( extractAuthentication( base64auth ) );
  }

  public boolean isAuthorized( String base64auth )
  {
    String authentication = extractAuthentication( base64auth );
    boolean authorized = false;
      
    if ( authentication.length() > 0 )
    {
      // now we are ready to check authentication string
      String decoded = Base64.base64Decode( authentication );
      log.debug( "Decoded authentication string: " + decoded );
      String[] userpass = decoded.split( ":" );
      
      log.debug( "User credentials: ["+userpass[0]+":"+userpass[1]+"]" );
      
      String pass = "password";
      String user = "username";
      
//      try
//      {
//        MessageDigest md5 = MessageDigest.getInstance( "SHA-256" );
//        pass = new String( md5.digest( "password".getBytes() ) );
//        
//        log.debug( "Accepted password md5 digest: " + pass );
//      }
//      catch ( NoSuchAlgorithmException e )
//      {
//        // TODO Auto-generated catch block
//        e.printStackTrace();
//      }
      

      // check username and password from database?
      
      if ( user.equals( userpass[0] ) && pass.equals( userpass[1] ) )
      {
        authorized = true;          
      }
    }
    
    return authorized;
  }
  
  // helper method for splitting authorization header
  private String extractAuthentication( String auth )
  {
    String result = "";

    if ( auth != null )
    {
      String[] items = auth.split( " " );
        
      if ( items.length == 2 && "Basic".equals( items[0] ) )
      {
        result = items[1];
      }
    }
    
    return result;
  }

  public Collection<ProbeConfiguration> getProbeConfiguration( long probeId )
  {
    return server.requestProbeConfigurationParameters( probeId );
  }

  public boolean setProbeConfiguration( long probeId, Map<String,String> configuration )
  {
    boolean success = false;
    try
    {
      success = server.setProbeConfiguration( probeId, configuration );
    }
    catch ( Exception e )
    {
      log.error( "Failed to set probe (" + probeId + ") configuration.", e );
    }
    
    return success;
  }

  public FrameworkInfo getFrameworkInfo()
  {
    FrameworkInfo info = new FrameworkInfo( "-1", getName() );
    return info;
  }

  public List<Value> getHistory( HistoryRequest request )
  {
    long start = request.getStart();
    long end = request.getEnd();
    Long[] bmids = new Long[request.getBms().size()];
    request.getBms().toArray( bmids );
    List<Value> data = persistence.getValues( start, end, bmids, SortKey.TIME, true );
    return data;
  }
}
