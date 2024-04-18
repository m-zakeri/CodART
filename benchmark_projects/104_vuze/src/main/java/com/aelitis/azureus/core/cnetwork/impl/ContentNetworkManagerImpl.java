/*
 * Created on Nov 20, 2008
 * Created by Paul Gardner
 * 
 * Copyright 2008 Vuze, Inc.  All rights reserved.
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License only.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */


package com.aelitis.azureus.core.cnetwork.impl;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.*;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.core3.util.AEDiagnostics;
import org.gudy.azureus2.core3.util.AEDiagnosticsEvidenceGenerator;
import org.gudy.azureus2.core3.util.AEDiagnosticsLogger;
import org.gudy.azureus2.core3.util.AEThread2;
import org.gudy.azureus2.core3.util.Constants;
import org.gudy.azureus2.core3.util.Debug;
import org.gudy.azureus2.core3.util.FileUtil;
import org.gudy.azureus2.core3.util.IndentWriter;
import org.gudy.azureus2.core3.util.SimpleTimer;
import org.gudy.azureus2.core3.util.TimerEvent;
import org.gudy.azureus2.core3.util.TimerEventPerformer;

import com.aelitis.azureus.core.cnetwork.ContentNetwork;
import com.aelitis.azureus.core.cnetwork.ContentNetworkException;
import com.aelitis.azureus.core.cnetwork.ContentNetworkListener;
import com.aelitis.azureus.core.cnetwork.ContentNetworkManager;
import com.aelitis.azureus.core.custom.Customization;
import com.aelitis.azureus.core.custom.CustomizationManager;
import com.aelitis.azureus.core.custom.CustomizationManagerFactory;

import com.aelitis.azureus.core.util.CopyOnWriteList;
import com.aelitis.azureus.core.vuzefile.VuzeFile;
import com.aelitis.azureus.core.vuzefile.VuzeFileComponent;
import com.aelitis.azureus.core.vuzefile.VuzeFileHandler;
import com.aelitis.azureus.core.vuzefile.VuzeFileProcessor;

public class 
ContentNetworkManagerImpl 
	implements ContentNetworkManager, AEDiagnosticsEvidenceGenerator
{
	private static final boolean LOAD_ALL_NETWORKS	= true;
	
	private static final String CONFIG_FILE		= "cnetworks.config";
	
	private static ContentNetworkManagerImpl singleton = new ContentNetworkManagerImpl();
		

	public static void
	preInitialise()
	{
		VuzeFileHandler.getSingleton().addProcessor(
			new VuzeFileProcessor()
			{
				public void
				process(
					VuzeFile[]		files,
					int				expected_types )
				{
					for (int i=0;i<files.length;i++){
						
						VuzeFile	vf = files[i];
						
						VuzeFileComponent[] comps = vf.getComponents();
						
						for (int j=0;j<comps.length;j++){
							
							VuzeFileComponent comp = comps[j];
							
							if ( comp.getType() == VuzeFileComponent.COMP_TYPE_CONTENT_NETWORK ){
								
								try{								
									((ContentNetworkManagerImpl)getSingleton()).importNetwork( comp.getContent());
								
									comp.setProcessed();
									
								}catch( Throwable e ){
									
									log( "Failed to import from vuze file", e );
							
									Debug.out( e );
								}
							}
						}
					}
				}
			});		
	}
	
	public static ContentNetworkManager
	getSingleton()
	{
		return( singleton );
	}
	
	private List<ContentNetworkImpl>	networks = new ArrayList<ContentNetworkImpl>();
	
	private CopyOnWriteList<ContentNetworkListener>	listeners = new CopyOnWriteList<ContentNetworkListener>();
	
	protected
	ContentNetworkManagerImpl()
	{
		loadConfig();
		
		addNetwork( new ContentNetworkVuze( this ));
		
		AEDiagnostics.addEvidenceGenerator( this );
		
		CustomizationManager cust_man = CustomizationManagerFactory.getSingleton();
		
		Customization cust = cust_man.getActiveCustomization();
		
		if ( cust != null ){
			
			String cust_name 	= COConfigurationManager.getStringParameter( "cnetworks.custom.name", "" );
			String cust_version = COConfigurationManager.getStringParameter( "cnetworks.custom.version", "0" );
			
			boolean	new_name 	= !cust_name.equals( cust.getName());
			boolean	new_version = Constants.compareVersions( cust_version, cust.getVersion() ) < 0;
			
			if ( new_name || new_version ){
				
				try{
					InputStream[] streams = cust.getResources( Customization.RT_CNETWORKS );
					
					for (int i=0;i<streams.length;i++){
						
						InputStream is = streams[i];
						
						try{
							VuzeFile vf = VuzeFileHandler.getSingleton().loadVuzeFile(is);
							
							if ( vf != null ){
								
								VuzeFileComponent[] comps = vf.getComponents();
								
								for (int j=0;j<comps.length;j++){
									
									VuzeFileComponent comp = comps[j];
									
									int type = comp.getType();
									
									if ( type == VuzeFileComponent.COMP_TYPE_CONTENT_NETWORK ){
										
										try{
												// change here as we always add all networks upfront so
												// we always set the customisation flag regardless of
												// whether existing or not
											
											ContentNetwork imported = importNetwork( comp.getContent());
											
											imported.setPersistentProperty( ContentNetwork.PP_IS_CUSTOMIZATION, true );
											
											comp.setProcessed();
											
										}catch( Throwable e ){
											
											log( "Failed to import customisation network", e );
										}
									}
								}
							}
						}finally{
							
							try{
								is.close();
								
							}catch( Throwable e ){
							}
						}
					}
				}finally{
					
					COConfigurationManager.setParameter( "cnetworks.custom.name", cust.getName());
					COConfigurationManager.setParameter( "cnetworks.custom.version", cust.getVersion());
				}
			}
		}
		
		
		SimpleTimer.addPeriodicEvent(
				"MetaSearchRefresh",
				23*60*60*1000,
				new TimerEventPerformer()
				{
					public void 
					perform(
						TimerEvent 	event ) 
					{
						checkForUpdates();
					}
				});
		
		if ( networks.size() > 1 || LOAD_ALL_NETWORKS ){
			
			new AEThread2( "CNetwork:init",	true )
			{
				public void
				run()
				{
					checkForUpdates();
				}
			}.start();
		}
	}
	
	protected void
	checkForUpdates()
	{
	}
	
	protected ContentNetworkImpl
	importNetwork(
		Map		content )
	
		throws IOException
	{
		ContentNetworkImpl network = ContentNetworkImpl.importFromBEncodedMapStatic( this, content );
		
		return( addNetwork( network ));
	}
	
	// @see com.aelitis.azureus.core.cnetwork.ContentNetworkManager#addContentNetwork(long)
	public void 
	addContentNetwork(
		final long 	id ) 
	
		throws ContentNetworkException
	{
	}
	
	public ContentNetwork
	getContentNetworkForURL(
		String		url )
	{
		try{
			String	host = new URL( url ).getHost();
			
			for ( ContentNetwork cn: getContentNetworks()){
				
				String	site = (String)cn.getProperty( ContentNetwork.PROPERTY_SITE_HOST );
				
				if ( site != null && site.endsWith( host )){
					
					return( cn );
				}
			}
		}catch( Throwable e ){
			
			Debug.printStackTrace(e);
		}
		
		return( null );
	}
	
	public ContentNetwork
	getStartupContentNetwork()
	{
		ContentNetwork[] networks = getContentNetworks();
		
		for ( ContentNetwork network: networks ){
			
			if ( network.isStartupNetwork()){
				
				return( network );
			}
		}
		
		return( getContentNetwork( ContentNetwork.CONTENT_NETWORK_VUZE ));
	}
	
	public ContentNetwork[] 
	getContentNetworks() 
	{
		synchronized( this ){
			
			return((ContentNetwork[])networks.toArray( new ContentNetworkImpl[ networks.size()] ));
		}
	}
	
	public ContentNetworkImpl 
	getContentNetwork(
		long id ) 
	{
		synchronized( this ){
			
			for ( int i=0;i<networks.size();i++ ){
					
				ContentNetworkImpl network = networks.get(i);
				
				if ( network.getID() == id ){
				
					return( network );
				}
			}
			
			return( null );
		}
	}
	
	protected ContentNetworkImpl
	addNetwork(
		ContentNetworkImpl		network )
	{
		boolean	replace = false;
		
		synchronized( this ){
		
			Iterator<ContentNetworkImpl> it = networks.iterator();
			
			while( it.hasNext()){
				
				ContentNetworkImpl existing_network = it.next();
				
				if ( existing_network.getID() == network.getID()){
					
					if ( network.getVersion() > existing_network.getVersion()){
						
						try{
							existing_network.updateFrom( network );
						
						}catch( Throwable e ){
							
							Debug.printStackTrace( e );
						}
						
						network = existing_network;
						
						replace = true;
						
						break;
						
					}else{
						
						log( "Network " + existing_network.getString() + " already up to date" );
						
						return( existing_network );
					}
				}
			}

			if ( replace ){
			
				log( "Updated network: " + network.getString());
				
			}else{
				
				log( "Added network: " + network.getString());
				
				networks.add( network );
			}
			
				// we never persist the vuze network
			
			if ( network.getID() != ContentNetwork.CONTENT_NETWORK_VUZE ){
				
				saveConfig();
			}
		}
		
		Iterator<ContentNetworkListener>	 it = (Iterator<ContentNetworkListener>)listeners.iterator();
		
		while( it.hasNext()){
			
			try{
				if ( replace ){
					
					it.next().networkChanged( network );
					
				}else{
					
					it.next().networkAdded( network );
				}
			}catch( Throwable e ){
				
				Debug.out( e );
			}
		}
		
		return( network );
	}
	
	protected void
	removeNetwork(
		ContentNetworkImpl		network )
	{
		synchronized( this ){

			if ( !networks.remove( network )){
				
				return;
			}
		
			network.destroy();
			
			saveConfig();
		}
		
		log( "Removed network: " + network.getString());
		
		Iterator<ContentNetworkListener>	 it = (Iterator<ContentNetworkListener>)listeners.iterator();
		
		while( it.hasNext()){
			
			try{
				it.next().networkRemoved( network );
				
			}catch( Throwable e ){
				
				Debug.out( e );
			}
		}
	}
	
	protected void
	loadConfig()
	{
		if ( FileUtil.resilientConfigFileExists( CONFIG_FILE )){
			
			Map	map = FileUtil.readResilientConfigFile( CONFIG_FILE );
			
			List list = (List)map.get( "networks" );
			
			if ( list != null ){
				
				for (int i=0;i<list.size();i++){
					
					Map	cnet_map = (Map)list.get(i);
					
					try{
						
						ContentNetworkImpl cn = ContentNetworkImpl.importFromBEncodedMapStatic( this, cnet_map );
						
						if ( cn.getID() != ContentNetwork.CONTENT_NETWORK_VUZE ){
							
							networks.add( cn );
						}
					}catch( Throwable e ){
						
						log( "Failed to load " + cnet_map, e );
					}
				}
			}
		}
	}
	
	protected void
	saveConfig()
	{
		Map	map = new HashMap();
		
		List list = new ArrayList();
		
		map.put( "networks", list );
		
		Iterator<ContentNetworkImpl> it = networks.iterator();
		
		while( it.hasNext()){
			
			ContentNetworkImpl network = it.next();

			if ( network.getID() == ContentNetwork.CONTENT_NETWORK_VUZE ){
				
				continue;
			}
			
			Map	cnet_map = new HashMap();
			
			try{
				network.exportToBEncodedMap( cnet_map );
			
				list.add( cnet_map );
				
			}catch( Throwable e ){
				
				log( "Failed to save " + network.getName(), e );
			}
		}
		
		if ( list.size() == 0 ){
			
			FileUtil.deleteResilientConfigFile( CONFIG_FILE );
			
		}else{
			
			FileUtil.writeResilientConfigFile( CONFIG_FILE, map );
		}
	}
	
	public void
	addListener(
		ContentNetworkListener		listener )
	{
		listeners.add( listener );
	}
	
	public void
	removeListener(
		ContentNetworkListener		listener )
	{
		listeners.remove( listener );
	}
	
	public void
	generate(
		IndentWriter		writer )
	{
		writer.println( "Content Networks" );
			
		try{
			writer.indent();

			synchronized( this ){
				
				Iterator<ContentNetworkImpl> it = networks.iterator();
				
				while( it.hasNext()){
					
					ContentNetworkImpl network = it.next();
					
					writer.println( network.getString());
				}
			}			
		}finally{
			
			writer.exdent();
		}
	}
	
	public static void 
	log(
		String 		s,
		Throwable 	e )
	{
		AEDiagnosticsLogger diag_logger = AEDiagnostics.getLogger( "CNetworks" );

		diag_logger.log( s );
		diag_logger.log( e );
	}
	
	public static void 
	log(
		String 	s )
	{	
		AEDiagnosticsLogger diag_logger = AEDiagnostics.getLogger( "CNetworks" );

		diag_logger.log( s );
	}
}
