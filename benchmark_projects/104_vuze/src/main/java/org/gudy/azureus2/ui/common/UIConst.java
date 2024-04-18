/*
 * Created on 10.11.2003
 *
 * To change the template for this generated file go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
package org.gudy.azureus2.ui.common;

import java.util.Date;
import java.util.HashMap;

import com.aelitis.azureus.core.*;

import org.apache.log4j.Logger;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.ui.common.IUserInterface;
import org.gudy.azureus2.ui.common.UserInterfaceFactory;

/**
 * @author tobi
 *
 * To change the template for this generated type comment go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
public class 
UIConst 
{
  public static Date 			startTime;
  public static HashMap 		UIS;
  
  private static AzureusCore	azureus_core;
  private static boolean        must_init_core;
  
  public static void
  setAzureusCore(
  	AzureusCore		_azureus_core )
  {
  	azureus_core	= _azureus_core;
  	must_init_core = !azureus_core.isStarted();
  }
  
  public static synchronized AzureusCore
  getAzureusCore()
  {
	  if (must_init_core) {
	        try {azureus_core.start();}
	        catch( AzureusCoreException e ) {
	      		Logger.getLogger("azureus2").error("Start fails", e);
	        }
	        must_init_core = false;
	  }
  	return( azureus_core );
  }
  
  public static GlobalManager
  getGlobalManager()
  {
  	return( azureus_core.getGlobalManager());
  }
  
  public static void shutdown() {
    Main.shutdown();
  }
  
  public static synchronized boolean 
  startUI(String ui, String[] args) {
    if (UIS.containsKey(ui))
      return false;
    IUserInterface uif = UserInterfaceFactory.getUI(ui);
    uif.init(false, true);
    if (args!=null)
      uif.processArgs(args);
    uif.startUI();
    UIS.put(ui, uif);
    return true;
  }

}
