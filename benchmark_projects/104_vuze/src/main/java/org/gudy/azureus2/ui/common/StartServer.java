/*
 * Created on 8 juil. 2003
 *
 */
package org.gudy.azureus2.ui.common;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

import org.apache.log4j.Logger;

import com.aelitis.azureus.core.impl.AzureusCoreSingleInstanceClient;

/**
 * @author Olivier
 * 
 */
public class StartServer extends Thread {

  private ServerSocket socket;
  private int state;
  private Main main;

  private boolean bContinue;
  public static final int STATE_FAULTY = 0;
  public static final int STATE_LISTENING = 1;

  public StartServer() {
    super("Start Server");
    try {
      socket = new ServerSocket(6880, 50, InetAddress.getByName("127.0.0.1")); //NOLAR: only bind to localhost
      state = STATE_LISTENING;
      Logger.getLogger("azureus2").info("StartServer: listening on 127.0.0.1:6880 for passed torrent info");
    } catch (Exception e) {
      state = STATE_FAULTY;

		// DON'T USE LOGGER here as we DON't want to initialise all the logger stuff
		// and in particular AEDiagnostics config dirty stuff!!!!

      System.out.println( "StartServer ERROR: unable to bind to 127.0.0.1:6880 for passed torrent info");
    }
  }

  public void run() {
    bContinue = true;
    while (bContinue) {
      BufferedReader br = null;
      try {
        Socket sck = socket.accept();
        String address = sck.getInetAddress().getHostAddress();
        if (address.equals("localhost") || address.equals("127.0.0.1")) {
          br = new BufferedReader(new InputStreamReader(sck.getInputStream()));
          String line = br.readLine();
          //System.out.println("received : " + line);
          if (line != null) {
            //            main.showMainWindow();
            StringTokenizer st = new StringTokenizer(line, ";");
            List argsList = new ArrayList();
            while( st.hasMoreElements() )
              argsList.add(st.nextToken().replaceAll("&;", ";").replaceAll("&&", "&"));
            if (argsList.size() > 1 )
            {
              String checker = (String) argsList.remove(0);
              if (checker.equals(AzureusCoreSingleInstanceClient.ACCESS_STRING)) {
                if (argsList.get(0).equals("args")) {
                  argsList.remove(0);                  
                  String newargs[] = new String[argsList.size()];
                  argsList.toArray(newargs);
                  Main.processArgs(newargs, null, null);
                } else {
                  Logger.getLogger("azureus2").error("Something strange was sent to the StartServer: " + line);
                }
              } else {
				Logger.getLogger("azureus2").error("StartServer: Wrong access token.");
              }
            }
          }
        }
        sck.close();

      } catch (Exception e) {
        if (!(e instanceof SocketException))
          e.printStackTrace();
        bContinue = false;
      } finally {
        try {
          if (br != null)
            br.close();
        } catch (Exception e) {
        }
      }
    }
  }

  public void stopIt() {
    bContinue = false;
    try {
      socket.close();
    } catch (Exception e) {
    }
  }
  /**
   * @return
   */
  public int getServerState() {
    return state;
  }

}
