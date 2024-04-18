/*
 * Created on 9 sept. 2003
 * Copyright (C) 2003, 2004, 2005, 2006 Aelitis, All Rights Reserved.
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 *
 * AELITIS, SAS au capital de 46,603.30 euros
 * 8 Allee Lenotre, La Grille Royale, 78600 Le Mesnil le Roi, France.
 *
 */
package org.gudy.azureus2.ui.swt;

import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Event;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Listener;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;
import org.gudy.azureus2.core3.torrent.*;
import org.gudy.azureus2.core3.util.*;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.tracker.client.TRTrackerAnnouncer;
import org.gudy.azureus2.ui.swt.components.shell.ShellFactory;

/**
 * @author Olivier
 * 
 */
public class TrackerChangerWindow {
  public TrackerChangerWindow(final DownloadManager[] dms ) {
    final Shell shell = ShellFactory.createMainShell(SWT.DIALOG_TRIM );
    shell.setText(MessageText.getString("TrackerChangerWindow.title"));
    Utils.setShellIcon(shell);
    GridLayout layout = new GridLayout();
    shell.setLayout(layout);

    Label label = new Label(shell, SWT.NONE);
    Messages.setLanguageText(label, "TrackerChangerWindow.newtracker");    
    GridData gridData = new GridData();
    gridData.widthHint = 400;
    label.setLayoutData(gridData);

    final Text url = new Text(shell, SWT.BORDER);
    gridData = new GridData(GridData.FILL_HORIZONTAL);
    gridData.widthHint = 400;
    url.setLayoutData(gridData);
    Utils.setTextLinkFromClipboard(shell, url, false, false);

    Label labelSeparator = new Label(shell,SWT.SEPARATOR | SWT.HORIZONTAL);
    gridData = new GridData(GridData.FILL_HORIZONTAL);
    labelSeparator.setLayoutData(gridData);

    Composite panel = new Composite(shell, SWT.NONE);
    gridData = new GridData(GridData.FILL_HORIZONTAL);
    panel.setLayoutData(gridData);
    layout = new GridLayout();
    layout.numColumns = 3;
    panel.setLayout(layout);        
 
    
    
    label = new Label( panel, SWT.NONE );
    gridData = new GridData(GridData.FILL_HORIZONTAL);
    label.setLayoutData(gridData );
    
    Button ok = new Button(panel, SWT.PUSH);
    ok.setText(MessageText.getString("Button.ok"));
    gridData = new GridData();
    gridData.widthHint = 70;
    gridData.horizontalAlignment = GridData.END;
    ok.setLayoutData(gridData);
    shell.setDefaultButton(ok);
    ok.addListener(SWT.Selection, new Listener() {
   
      public void handleEvent(Event event) {
        try {
        	String[] _urls = url.getText().split( "," );
        	
        	List<String>	urls = new ArrayList<String>();
        	
    		for ( String url: _urls ){
    			
    			url = url.trim();
    			
    			if ( url.length() > 0 ){
    				
    				try{
    					new URL( url );
    					
    					urls.add( 0, url );
    					
    				}catch( Throwable e ){
    					
    					Debug.out( "Invalid URL: " + url );
    				}
    			}
    		}
    		
        	for ( DownloadManager dm: dms ){
        		
	        	TOTorrent	torrent = dm.getTorrent();
	        	
	        	if ( torrent != null ){
	        	
	        		for ( String url: urls ){
	        		
	        			TorrentUtils.announceGroupsInsertFirst( torrent, url );
	        		}
	        		
	        		TorrentUtils.writeToFile( torrent );
	        	
	        		TRTrackerAnnouncer announcer = dm.getTrackerClient();
	        		
	        		if ( announcer != null ){
	        	
	        			announcer.resetTrackerUrl(false);
	        		}
	        	}
        	}
        	
        	shell.dispose();
        }
        catch (Exception e) {
        	Debug.printStackTrace( e );
        }
      }
    });

    Button cancel = new Button(panel, SWT.PUSH);
    cancel.setText(MessageText.getString("Button.cancel"));
    gridData = new GridData();
    gridData.widthHint = 70;
    gridData.horizontalAlignment = GridData.END;
    cancel.setLayoutData(gridData);
    cancel.addListener(SWT.Selection, new Listener() {
   
      public void handleEvent(Event event) {
        shell.dispose();
      }
    });

    shell.pack();
	Utils.centreWindow( shell );
    Utils.createURLDropTarget(shell, url);
    shell.open();
  }
}
