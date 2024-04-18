/*
 * UserInterfaceMain.java
 *
 * Created on 9. Oktober 2003, 19:50
 */

package org.gudy.azureus2.ui.common;

import java.io.FileReader;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringReader;

import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.net.Socket;

import java.text.SimpleDateFormat;

import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.StringTokenizer;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;

import org.apache.log4j.Appender;
import org.apache.log4j.ConsoleAppender;
import org.apache.log4j.Logger;
import org.apache.log4j.PatternLayout;
import org.apache.log4j.varia.DenyAllFilter;

import com.aelitis.azureus.core.*;
import com.aelitis.azureus.core.impl.AzureusCoreSingleInstanceClient;
import com.aelitis.azureus.launcher.Launcher;

import org.gudy.azureus2.core3.config.COConfigurationManager;
import org.gudy.azureus2.ui.common.IUserInterface;
import org.gudy.azureus2.ui.common.UserInterfaceFactory;
/**
 *
 * @author  Tobias Minich
 */
public class Main {
  
  public static String DEFAULT_UI = "swt";
  
  public static StartServer start = null;
  
  protected static AzureusCore	core;
  
  private static CommandLine parseCommands(String[] args, boolean constart) {
    
    if (args==null)
      return null;
    
    CommandLineParser parser = new PosixParser();
    Options options = new Options();
    options.addOption("h", "help", false, "Show this help.");
 
    OptionBuilder.withLongOpt("exec");
    OptionBuilder.hasArg();
    OptionBuilder.withArgName("file");
    OptionBuilder.withDescription("Execute script file. The file should end with 'logout', otherwise the parser thread doesn't stop.");
    options.addOption( OptionBuilder.create('e'));
    
    OptionBuilder.withLongOpt("command");
    OptionBuilder.hasArg();
    OptionBuilder.withArgName("command");
    OptionBuilder.withDescription("Execute single script command. Try '-c help' for help on commands.");
    options.addOption(OptionBuilder.create('c'));
    
    OptionBuilder.withLongOpt("ui");
    OptionBuilder.withDescription("Run <uis>. ',' separated list of user interfaces to run. The first one given will respond to requests without determinable source UI (e.g. further torrents added via command line).");
    OptionBuilder.withArgName("uis");
    OptionBuilder.hasArg();
    options.addOption(OptionBuilder.create('u'));
    
    CommandLine commands = null;
    try {
      commands = parser.parse(options, args, true);
    } catch( ParseException exp ) {
      Logger.getLogger("azureus2").error("Parsing failed.  Reason: " + exp.getMessage(), exp);
      if (constart)
        System.exit(2);
    }
    if (commands.hasOption('h')) {
      if (constart) {
        HelpFormatter hf = new HelpFormatter();
        hf.printHelp("java org.gudy.azureus2.ui.common.Main", "Optionally you can put torrent files to add to the end of the command line.\r\n", options, "Available User Interfaces: swt (default), web, console\r\nThe default interface is not started if you give either the '-e' or '-c' option (But you can start it by hand with '-u').", true);
        System.exit(0);
      }
    }
    return commands;
  }
  
  public static void initRootLogger() {
    if (Logger.getRootLogger().getAppender("ConsoleAppender")==null) {
      Appender app;
      app = new ConsoleAppender(new PatternLayout(PatternLayout.TTCC_CONVERSION_PATTERN));
      app.setName("ConsoleAppender");
      app.addFilter( new DenyAllFilter() );  //'log off' by default
      Logger.getRootLogger().addAppender(app);
    }
  }
  
  public static void main(String[] args) {
	  if(Launcher.checkAndLaunch(Main.class, args))
		  return;
	  
		// This *has* to be done first as it sets system properties that are read and cached by Java
		
	COConfigurationManager.preInitialise();
 
    String  mi_str = System.getProperty( "MULTI_INSTANCE" );
    
    boolean mi = mi_str != null && mi_str.equalsIgnoreCase("true");

    initRootLogger();
    
    try{
       	CommandLine commands = parseCommands(args, true);

       	if ( commands != null && directLaunch( args, commands )){
       		
       		return;
       	}
       	 
       		// don't create core until we know we really need it
       	
    	if( mi ){
    		
    		System.out.println( "MULTI_INSTANCE enabled" );
    		
    	   	core = AzureusCoreFactory.create();

    		processArgs(args, core, commands);
    		
    		return;
    	}
      
    	start = new StartServer();
      
	    if ((start == null) || (start.getServerState()==StartServer.STATE_FAULTY)) {
	    	
	 
	    	new StartSocket( args );
	    	
	    }else{
	    	
	   
	      core = AzureusCoreFactory.create();


	      start.start();
	      
	      processArgs(args, core, commands);
	    }
    }catch( AzureusCoreException e ){
    	
    	System.out.println( "Start fails:" );
    	
    	e.printStackTrace();
    }
  }
  
  public static void shutdown() {
    if (start!=null){
    	
      start.stopIt();
    }
    
    if ( core != null ){
    	try{
    		core.stop();
    		
    	}catch( AzureusCoreException e ){
    		
    		System.out.println( "Stop fails:" );
    		
    		e.printStackTrace();
    	}
    }
    
    SimpleDateFormat temp = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss");
    Logger.getLogger("azureus2").fatal("Azureus stopped at "+temp.format(new Date()));
    //System.exit(0);	- we don't want to force quit, wait until other threads have completed
    // so that resume data etc is saved....
  }
  
  	public static boolean 
  	directLaunch(
  		String[] 		args, 
  		CommandLine 	commands) 
  	{
  			// frig to support launch of SWT ui via this means pending a proper rewrite
  			// of this stuff
  		
  		if ( commands.hasOption('u')) {
    	  
  			String uinames = commands.getOptionValue('u');
       
  			if ( uinames.indexOf(',') != -1 ){
  				
  				return( false );
  			}
  			
  			if ( !uinames.equalsIgnoreCase( DEFAULT_UI )){
  				
  				return( false );
  			}
  		}
           
  		try{
  			String uiclass = "org.gudy.azureus2.ui." + DEFAULT_UI + ".Main";
  	   
  			Class	main_class = Class.forName( uiclass );
  		
  			Method main_method = main_class.getMethod( "main", new Class[]{ String[].class });
  			
   			main_method.invoke( null, new Object[]{ commands.getArgs()});
  			
  			return( true );
  			
  		}catch( Throwable e ){
  			
  			e.printStackTrace();
  			
  			return( false );
  		}
  }
  
  public static void 
  processArgs(
  	String[] 		args, 
  	AzureusCore 	new_core, 
	CommandLine 	commands) 
  {
    if (commands==null) {
      commands = parseCommands(args, false);
    }
    if (((commands!=null) && (args.length>0)) || (new_core != null)) {
      if (UIConst.UIS == null) {
        UIConst.UIS = new HashMap();
      }
      if (commands.hasOption('u')) {
        String uinames = commands.getOptionValue('u');
        if (uinames.indexOf(',')==-1) {
          if (!UIConst.UIS.containsKey(uinames))
          UIConst.UIS.put(uinames,UserInterfaceFactory.getUI(uinames));
        } else {
          StringTokenizer stok = new StringTokenizer(uinames, ",");
          while (stok.hasMoreTokens()) {
            String uin = stok.nextToken();
            if (!UIConst.UIS.containsKey(uin))
              UIConst.UIS.put(uin,UserInterfaceFactory.getUI(uin));
          }
        }
      } else {
        if (UIConst.UIS.isEmpty() && !commands.hasOption('c') && !commands.hasOption('e'))
          UIConst.UIS.put(DEFAULT_UI, UserInterfaceFactory.getUI(DEFAULT_UI));
      }

      Iterator uis = UIConst.UIS.values().iterator();
      boolean isFirst = true;
      String [] theRest = commands.getArgs();
      while (uis.hasNext()) {
        IUserInterface ui = (IUserInterface) uis.next();
        ui.init(isFirst, (UIConst.UIS.size()>1));
        theRest = ui.processArgs(theRest);
        isFirst = false;
      }

      if ( new_core != null ){
      	
        SimpleDateFormat temp = new SimpleDateFormat("dd-MMM-yyyy HH:mm:ss");
        
        UIConst.startTime = new Date();
        
        Logger.getLogger("azureus2").fatal("Azureus started at "+temp.format(UIConst.startTime));
        
        UIConst.setAzureusCore( new_core );
      }

      uis = UIConst.UIS.values().iterator();
      while (uis.hasNext())
        ((IUserInterface) uis.next()).startUI();
           
      Class clConsoleInput;
      Constructor conConsoleInput =null;
      try {
      	clConsoleInput = Class.forName("org.gudy.azureus2.ui.console.ConsoleInput");
      	
      		// change this and you'll need to change the parameters below....
      	
      	Class params[] = {String.class, AzureusCore.class, Reader.class, PrintStream.class, Boolean.class};
      	
      	conConsoleInput=clConsoleInput.getConstructor(params);
      } catch (Exception e) {
      	e.printStackTrace();
      }
      if (commands.hasOption('e')) {
      	if (conConsoleInput != null) {
	        try {
	        	Object params[] = {commands.getOptionValue('e'), new_core, new FileReader(commands.getOptionValue('e')), System.out, Boolean.FALSE};
	        	conConsoleInput.newInstance(params);
	        } catch (java.io.FileNotFoundException e) {
	          Logger.getLogger("azureus2").error("Script file not found: "+e.toString());
	        } catch (Exception e) {
	        	Logger.getLogger("azureus2").error("Error invocating the script processor: "+e.toString());
	        }
      	} else
      		Logger.getLogger("azureus2").error("ConsoleInput class not found. You need the console ui package to use '-e'");
      }
      
      if (commands.hasOption('c')) {
      	if (conConsoleInput != null) {
	        String comm = commands.getOptionValue('c');
	        comm+="\nlogout\n";
	        Object params[] = {commands.getOptionValue('c'), UIConst.getAzureusCore(), new StringReader(comm), System.out, Boolean.FALSE};
	        try {
	        	conConsoleInput.newInstance(params);
	        } catch (Exception e) {
	        	Logger.getLogger("azureus2").error("Error invocating the script processor: "+e.toString());
	        }
      	} else
      		Logger.getLogger("azureus2").error("ConsoleInput class not found. You need the console ui package to use '-e'");
      }
      
      openTorrents(theRest);
    } else {
      Logger.getLogger("azureus2").error("No commands to process");
    }
  }
  
  public static void openTorrents(String[] torrents) {
    if ((UIConst.UIS!=null) && (!UIConst.UIS.isEmpty()) && (torrents.length>0)) {
      for(int l=0; l<torrents.length; l++) {
        ((IUserInterface) UIConst.UIS.values().toArray()[0]).openTorrent(torrents[l]);
      }
    }
  }
  
  public static class StartSocket {
    public StartSocket(String args[]) {
      Socket sck = null;
      PrintWriter pw = null;
      try {
        System.out.println("StartSocket: passing startup args to already-running process.");
        
		// NOTE - this formatting is also used by AzureusCoreSingleInstanceClient and other org.gudy.azureus2.ui.swt.StartSocket
        
        sck = new Socket("127.0.0.1",6880);
        pw = new PrintWriter(new OutputStreamWriter(sck.getOutputStream()));
        StringBuffer buffer = new StringBuffer(AzureusCoreSingleInstanceClient.ACCESS_STRING+";args;");
        for(int i = 0 ; i < args.length ; i++) {
          String arg = args[i].replaceAll("&","&&").replaceAll(";","&;");
          buffer.append(arg);
          buffer.append(';');
        }
        pw.println(buffer.toString());
        pw.flush();
      } catch(Exception e) {
        e.printStackTrace();
      } finally {
        try {
          if (pw != null)
            pw.close();
        } catch (Exception e) {
        }
        try {
          if (sck != null)
            sck.close();
        } catch (Exception e) {
        }
      }
    }
  }
}
