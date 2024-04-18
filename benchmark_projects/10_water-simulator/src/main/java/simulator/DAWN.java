package simulator;

import org.apache.log4j.Logger;

import jade.core.Runtime;
import jade.core.Profile;
import jade.core.ProfileImpl;
import jade.wrapper.*;

/**
 * DAWN Main Method for start up
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


public class DAWN {
  private static Logger log = Logger.getLogger(DAWN.class);
  // SA launches CAs on jadeContainer and SuiteGUI launces RMA on MainContainer
  public static AgentContainer jadeContainer;
  public static MainContainer mainContainer;

  public static void main(String[] args){

    try {

      // Get a hold on JADE runtime
      Runtime rt = Runtime.instance();

      // Exit the JVM when there are no more containers around
      rt.setCloseVM(true);

      // Launch a complete platform on the default port 1099
      // create a default Profile
      Profile pMain = new ProfileImpl();
      mainContainer = rt.createMainContainer(pMain);

      // set now the default Profile to start a container
      ProfileImpl pContainer = new ProfileImpl();
      log.info("Launching the agent container ..."+ pContainer + "\n");
      jadeContainer = rt.createAgentContainer(pContainer);

      log.info("Launching the Simulation Agent  on the container-1 ...");
      AgentController simulator = jadeContainer.createNewAgent("simulator", "simulator.SA.SimulationAgent", null);
      simulator.start();
    }
    catch(StaleProxyException spe){
      spe.printStackTrace();
    }
    catch(ControllerException ce) {
      ce.printStackTrace();
    }

  }

}
