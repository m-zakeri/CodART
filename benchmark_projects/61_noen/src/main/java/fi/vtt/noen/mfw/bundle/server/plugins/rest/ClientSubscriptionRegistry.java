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
import java.util.HashMap;
import java.util.Map;

import fi.vtt.noen.mfw.bundle.server.plugins.rest.resources.ClientRequest;

public class ClientSubscriptionRegistry
{
    private Map<Long, ArrayList<ClientRequest>> subs;
    
    public ClientSubscriptionRegistry()
    {
        subs = new HashMap<Long, ArrayList<ClientRequest>>();
    }
    
    public void add( long subscribeId, ClientRequest client )
    {
        if ( subs.containsKey( subscribeId ) )
        {
            ArrayList<ClientRequest> clients = subs.get( subscribeId );
            if ( !clients.contains( client ) )
            {
                clients.add( client );
                subs.put( subscribeId, clients );
            }
        }
        else
        {
            ArrayList<ClientRequest> clients = new ArrayList<ClientRequest>();
            clients.add( client );
            subs.put( subscribeId, clients );
        }
    }
    
    public void remove( long subscribeId, ClientRequest client )
    {
        if ( subs.containsKey( subscribeId ) )
        {
            ArrayList<ClientRequest> clients = subs.get( subscribeId );
            if ( clients == null )
            {
                subs.remove( subscribeId );
            }
            else
            {
                clients.remove( client );
                if ( clients.size() == 0 )
                {
                    subs.remove( subscribeId );
                }
            }
        }
    }
    
    public ArrayList<ClientRequest> get( long subscribeId )
    {
        return subs.get( subscribeId );
    }
}
