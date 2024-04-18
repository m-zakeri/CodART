package simulator.SA;




import jade.content.ContentElement;
import jade.content.lang.Codec;
import jade.content.lang.Codec.CodecException;
import jade.content.lang.sl.SLCodec;
import jade.content.onto.OntologyException;
import jade.content.onto.basic.Action;
import jade.core.AID;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.OneShotBehaviour;
import jade.gui.GuiAgent;
import jade.gui.GuiEvent;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.wrapper.AgentController;
import jade.wrapper.ControllerException;
import jade.wrapper.StaleProxyException;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Vector;

import javax.swing.UIManager;
import javax.swing.event.InternalFrameAdapter;
import javax.swing.event.InternalFrameEvent;

import org.apache.log4j.Logger;

import simulator.DAWN;
import simulator.SA.gui.AboutFrame;
import simulator.SA.gui.DemandCurveParameterFrame;
import simulator.SA.gui.PricingPolicyFrame;
import simulator.SA.gui.ProgressGui;
import simulator.SA.gui.ReviewGUI;
import simulator.SA.gui.SimulationParametersFrame;
import simulator.SA.gui.SuiteGUI;
import simulator.ontology.LaunchGUI;
import simulator.ontology.SavePersonalData;
import simulator.ontology.SavingPath;
import simulator.ontology.Start;
import simulator.ontology.StepAttr;
import simulator.ontology.StepTotalConsumption;
import simulator.ontology.WDS_Ontology;
import simulator.ontology.WaterConsumption;
import simulator.util.AIDs;
import simulator.util.ConsumerAttributes;
import simulator.util.ConsumerType;
import simulator.util.Function;
import simulator.util.ParameterAttributes;


/**
 * The Simulatation Agent is the heart of the system. 
 * It is the first agent that is launched so it is responsible for 
 * collecting all inputs of scenario's design (StartUpWizard gui). 
 * After that launches  * progress GUI and it is in charge of starting
 * every simulation step by sending stepID to SA. Finally, it collects 
 * step result which is presented to the user via the Progress GUI
 * 
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class SimulationAgent extends GuiAgent {

  private static final long serialVersionUID = -8861903386335599576L;
  
  public static final int START_SIMULATION_MENU = 1000;
  public static final int LAUNCH_CONSUMER_GUI = 1001;
  public static final int START_BUTTON_GUI = 1002;
  public static final int LOAD_SCENARIO = 1003;
  public static final int SAVE_SCENARIO = 1004;
  public static final int WIZARD_ENDED = 1005;
  public static final int SAVE_RESULTS = 1006;
  public static final int EDIT_SIMULATION_PARAMETERS = 1007;
  public static final int EDIT_DEMAND_CURVE_PARAMETERS = 1008;
  public static final int EDIT_METDATA_FILE = 1009;
  public static final int EDIT_PRICING_POLICY = 1010;
  public static final int SIMULATION_PARAMETERS_INPUT = 1011;
  public static final int PRICING_POLICY_INPUT = 1012;
  public static final int REVIEW_COMBOS_CHANGED = 1013;
  public static final int PARAMETER_INPUT = 1014;
  public static final int SAVE_CONSUMERS_RESULTS = 1015;
  public static final int ABOUT = 1016;

  // Ontology
  private WDS_Ontology ontology = WDS_Ontology.getInstance();
  private Codec codec = new SLCodec();

  // Gui parameters
  private static int gridDimension;
  private static int sightLimit;
  private static int population;
  private static int simulationDuration;
  private static int simulationStep;
  private static Boolean consumptionLN;
  private static int parametersNumber;
  private static ConsumerType[] consumerTypes;
  private static ParameterAttributes[][] demandCurveParameters;
  private static File metDataFile;
  private static Vector priceData = new Vector(0,1);
  private static float distributionMean;
  private static float distributionDeviation;

  private float initialConsumption=0;

  private static int stepId=1;

  private SuiteGUI suiteGUI;
  private ProgressGui progressGui;
  private ReviewGUI reviewGUI;

  //All consumers that SA launches
  private ConsumerAttributes[] consumers;

  //Store consumptions
  private Vector consumptions = new Vector(0,1);
  //{ consumptions.addElement(new Float(0));}

  // logger
  Logger log = Logger.getLogger(SimulationAgent.class); 
  protected void setup() {

      // Register language and ontology
      getContentManager().registerLanguage(codec);
      getContentManager().registerOntology(ontology);

      // Set the look and feel
      try { UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());}
      catch(Exception e) { log.error(e.getStackTrace()); }

      // Launch Suite GUI
      suiteGUI = new SuiteGUI(this);

      // Receive step results and update progress GUI
      addBehaviour(new BehaviourReceiveStepResult(this));
      addBehaviour(new BehaviourHandleOutOfSequenceMessages(this));


  }

  /**
   * "Unpack" the inputs SA receives from GUI (load operation or scenario design Wizard).
   * The arguments are elements of an object array.
   * @param ev Gui Event received by startUpWizard
   */

  //Vector temp1 = new Vector(0,1);

  private void unpackGuiInputs(GuiEvent ev){


      // Simulation Parameters
      gridDimension = ((Integer) ev.getParameter(0)).intValue();
      sightLimit = ((Integer) ev.getParameter(1)).intValue();
      population = ((Integer) ev.getParameter(2)).intValue();
      simulationDuration = ((Integer) ev.getParameter(3)).intValue();
      simulationStep = ((Integer) ev.getParameter(4)).intValue();

      //Consumer Types
      Vector temp = (Vector)ev.getParameter(5);
      consumerTypes = new ConsumerType[temp.size()];
      temp.copyInto(consumerTypes);

      SimulationAgent.consumptionLN = (Boolean) ev.getParameter(6);
      parametersNumber = ((Integer) ev.getParameter(7)).intValue();

      demandCurveParameters = new ParameterAttributes[SimulationAgent.consumerTypes.length][SimulationAgent.parametersNumber];

      //All parameters for all consumers types
      //Stored in demandCurveParameters array
      // rows indicate i consumer type
      // columns indicate j parameter of the demand curve
      temp = (Vector) ev.getParameter(8);

      int k=0;
      for(int j = 0 ; j< SimulationAgent.consumerTypes.length ; j++)
         for(int i = 0 ; i< SimulationAgent.parametersNumber ; i++){
            demandCurveParameters[j][i] = (ParameterAttributes) temp.elementAt(k);
            k++;
         }

      metDataFile = (File) ev.getParameter(9);
      priceData = (Vector) ev.getParameter(10);

      Vector distributionData = (Vector) ev.getParameter(11);

      distributionMean = ((Float)distributionData.elementAt(0)).floatValue();
      distributionDeviation = ((Float)distributionData.elementAt(1)).floatValue();

  }//END of unpackArguments()


  /**
   * Launching the consumer agents, MOA and WSA. Called from BehaviourStartSimulation
   */

  private void instantiatePlatform(){

      // A new simulation is started
      this.initialConsumption = 0;


      try{

        // BUILD THE GRID
        GridGenerator grid = new GridGenerator(gridDimension,population);
        Vector consumers = grid.getConsumers();

        // Instatiate GaussGenerator
        GaussGenerator gaussGenerator = new GaussGenerator(SimulationAgent.distributionMean,
                                                           SimulationAgent.distributionDeviation);

        int counter = 0; // Counts the consumers

        //distributeTypesToAgents();

        for(int t = 0; t < consumerTypes.length ; t++){

            // LAUNCH A POPULATION OF A SPECIFIED AGENT TYPE
            for (int i=0; i < consumerTypes[t].getMembers() ; i++){

              ((ConsumerAttributes)consumers.elementAt(counter)).setConsumerType(consumerTypes[t].getName());

              // get n-agent's neighbours
              Vector neighbours = new Vector(0);
              if(SimulationAgent.sightLimit!=0)
                neighbours = grid.getNeighbours((ConsumerAttributes)consumers.elementAt(counter),sightLimit);

              // Prepare demand curve parameters
              ParameterAttributes[] myParameters = demandCurveParameters[t];

              // Prepare arguments to pass
              Object[] consumerArguments = new Object[4 + myParameters.length];

              //  convention : first argument --> initial consumption (step=0)
              //               second argument --> AP / MP (price type)
              //               third argument --> neighbours
              //               fourth argument --> consumption LN
              //               fifth argument --> number of demand curve parameters

              consumerArguments[0] = gaussGenerator.getRandomInitialConsumption();

              this.initialConsumption += ((Float)consumerArguments[0]).floatValue();

              consumerArguments[1] = priceData.elementAt(5);

              consumerArguments[2] = neighbours;

              consumerArguments[3] = SimulationAgent.consumptionLN;

              for(int k=0 ; k < myParameters.length ; k++)
                  consumerArguments[k+4] = myParameters[k];

              // Launching one consumer agent of this group ( ConsumerType[t] )

              this.progressGui.updateMessageArea(
                         ((ConsumerAttributes)consumers.elementAt(counter)).getName() + " is launched");
              AgentController cons = DAWN.jadeContainer.createNewAgent
                            (((ConsumerAttributes)consumers.elementAt(counter)).getName(), "simulator.CA.ConsumerAgent", consumerArguments);
              cons.start();

              // for next consumer from the list
              counter++;

            } // END of an agent TYPE

        }// END (t)

        // SA property
        for(int i=0; i<consumers.size();i++)
          ((ConsumerAttributes)consumers.elementAt(i)).setAID(new AID(
                                            ((ConsumerAttributes)consumers.elementAt(i)).getName(),false));

        this.consumers = new ConsumerAttributes[consumers.size()];
        consumers.copyInto(this.consumers);



        if (SimulationAgent.metDataFile.getPath() != "") {
              // Prepare Arguments
              Object[] metOfficeArguments = {
            		  new Integer(SimulationAgent.simulationDuration), 
            		  SimulationAgent.metDataFile, 
            		  new Integer(SimulationAgent.simulationStep) };

              //**********************************************************
              // MET OFFICE AGENT LAUNCHED
              this.progressGui.updateMessageArea("MetOfficeAgent is launched");
              AgentController metOffice = DAWN.jadeContainer.createNewAgent
                            ("metOffice", "simulator.MOA.MetOfficeAgent", metOfficeArguments);
              metOffice.start();
        }

        //Prepare WSA's arguments

        Object[] supplierArguments = new Object[5];

        supplierArguments[0] = new Boolean( (SimulationAgent.metDataFile.getPath() != "")?true:false);
        supplierArguments[1] = consumers;
        supplierArguments[2] = priceData;
        supplierArguments[3] = new Integer(SimulationAgent.simulationStep);

        //**********************************************************
        // WATER SUPPLIER AGENT LAUNCHED
        this.progressGui.updateMessageArea("WaterSupplierAgent is launched");
        AgentController supplier = DAWN.jadeContainer.createNewAgent
                      ("supplier", "simulator.WSA.WaterSupplierAgent", supplierArguments);
        supplier.start();

      }
      catch (StaleProxyException spe){
    	  log.error(spe.getStackTrace());
      }
      catch (ControllerException ce){
    	  log.error(ce.getStackTrace());
      }
  }



  /**
   * AGENT OPERATIONS FOLLOWING GUI EVENTS
   * @param ev Gui Event
   */


  protected void onGuiEvent(GuiEvent ev){

     int[] selections = new int[2];

     switch(ev.getType()){

        case START_SIMULATION_MENU   : 
        								log.info("Selected: START_SIMULATION_MENU");
        								this.addBehaviour(new BehaviourStartSimulation(this));
        								break;

        case LAUNCH_CONSUMER_GUI     : log.info("Selected: LAUNCH_CONSUMER_GUI");
        						       sendGuiRequestMessage((String)ev.getParameter(0));
		   								
                                       break;

        case START_BUTTON_GUI        : stepId = 1;
			                           log.info("Selected: START_BUTTON_GUI");
                                       addBehaviour(new BehaviourStartSimulationStep
                                                             (SimulationAgent.this, new Integer(stepId)));
                                       progressGui.updateMessageArea("******Simulation Started******");
                                       break;
        case LOAD_SCENARIO           : 
        								log.info("Selected: LOAD_SCENARIO" );
        								if (((File)ev.getParameter(0)) != null){
                                                loadScenarioFromFile((File)ev.getParameter(0));
                                                launchReviewGui();
        								}
        								break;
        case SAVE_SCENARIO           :  log.info("Selected: SAVE_SCENARIO" );
        								if (((File)ev.getParameter(0)) != null)
                                                saveScenarioToFile((File)ev.getParameter(0));
                                       break;
        case WIZARD_ENDED            : log.info("Selected: WIZARD_ENDED" );
        								unpackGuiInputs(ev);
                                       launchReviewGui();
                                       break;
        case SAVE_RESULTS            : log.info("Selected: SAVE_RESULTS" );
        								if (((File)ev.getParameter(0)) != null)
                                                saveResultsToFile((File)ev.getParameter(0));
                                       break;
        case SAVE_CONSUMERS_RESULTS  : log.info("Selected: SAVE_CONSUMERS_RESULTS" );
        								if (((File)ev.getParameter(0)) != null)
                                               sendSaveResultsRequestToConsumers((File)ev.getParameter(0));
                                       break;
        case EDIT_SIMULATION_PARAMETERS :log.info("Selected: EDIT_SIMULATION_PARAMETERS" );
                                        SimulationParametersFrame simulationParametersFrame =
                                                     new SimulationParametersFrame(this,
                                                                                   SimulationAgent.population,
                                                                                   SimulationAgent.gridDimension,
                                                                                   SimulationAgent.sightLimit,
                                                                                   SimulationAgent.simulationDuration,
                                                                                   SimulationAgent.simulationStep);
                                        //Launch simulationParametersFrame
                                        suiteGUI.addToMainPanel(simulationParametersFrame,
                                                                                      SuiteGUI.TOP_LAYER);
                                        simulationParametersFrame.show();
                                        break;
        case SIMULATION_PARAMETERS_INPUT : log.info("Selected: SIMULATION_PARAMETERS_INPUT" );
                                       setSimulationParameters(ev);
                                       distributeTypesToAgents();
                                       reviewGUI.updateSimulationParametersLabels(SimulationAgent.population,
                                    		   SimulationAgent.gridDimension,
                                    		   SimulationAgent.sightLimit,
                                    		   SimulationAgent.simulationDuration,
                                    		   SimulationAgent.simulationStep);
                                       break;
        case EDIT_DEMAND_CURVE_PARAMETERS : log.info("Selected: EDIT_DEMAND_CURVE_PARAMETERS" );
                                       selections = reviewGUI.getCombosSelections();
                                       DemandCurveParameterFrame demandCurveParameterFrame =
                                            new DemandCurveParameterFrame(this,
                                                 (Function[])ev.getParameter(0),
                                                 SimulationAgent.consumerTypes[selections[0]],
                                                 SimulationAgent.demandCurveParameters[selections[0]][selections[1]]);
                                       suiteGUI.addToMainPanel(demandCurveParameterFrame,SuiteGUI.TOP_LAYER);
                                       demandCurveParameterFrame.show();
                                       break;
        case PARAMETER_INPUT         :  log.info("Selected: PARAMETER_INPUT" );
        								selections = reviewGUI.getCombosSelections();
                                        SimulationAgent.demandCurveParameters[selections[0]][selections[1]] =
                                                                  (ParameterAttributes)ev.getParameter(0);
                                        reviewGUI.updateDemandCurveParameter(
                                              SimulationAgent.demandCurveParameters[selections[0]][selections[1]]);
                                       break;
        case REVIEW_COMBOS_CHANGED   : log.info("Selected: REVIEW_COMBOS_CHANGED" );
        								selections = reviewGUI.getCombosSelections();
                                       reviewGUI.updateDemandCurveParameter(
                                              SimulationAgent.demandCurveParameters[selections[0]][selections[1]]);

                                       break;

        case EDIT_METDATA_FILE       : log.info("Selected: EDIT_METDATA_FILE" );
        								if (((File)ev.getParameter(0)) != null){
                                              SimulationAgent.metDataFile = (File)ev.getParameter(0);
                                              reviewGUI.updateFileLabel(((File)ev.getParameter(0)).getPath());
                                       }
                                       break;
        case EDIT_PRICING_POLICY     : log.info("Selected: EDIT_PRICING_POLICY" );
        								PricingPolicyFrame pricingPolicyFrame =
                                                     new PricingPolicyFrame(this,
                                                                            (String[])ev.getParameter(0),
                                                                            SimulationAgent.priceData);
                                        //Launch simulationParametersFrame
                                        suiteGUI.addToMainPanel(pricingPolicyFrame,SuiteGUI.TOP_LAYER);
                                        pricingPolicyFrame.show();

                                       break;
        case PRICING_POLICY_INPUT :    log.info("Selected: PRICING_POLICY_INPUT" );
        								SimulationAgent.priceData = (Vector)ev.getParameter(0);
                                       updatePricingPolicyToReviewGUI();
                                       break;
       
        case ABOUT :                   log.info("Selected: ABOUT" ); 				   
        	                           AboutFrame ab = new AboutFrame();
        							   suiteGUI.addToMainPanel(ab,SuiteGUI.TOP_LAYER);
                                       ab.show();
                          			   break;
     }// Switch

  }// END onGuiEvent


  /**
   *
   * BehaviourStartSimulation starts the simulation : instantiates progressGUI, instantiates Platform</p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
   */

  private class BehaviourStartSimulation extends OneShotBehaviour{

	private static final long serialVersionUID = 4852389811841434827L;
	private SimulationAgent myAgent;

      BehaviourStartSimulation(SimulationAgent a){
          super(a);
          this.myAgent = a;
      }


      @SuppressWarnings("unchecked")
	public void action(){

            // Empty consumptions' Vector (last executed scenario's values)
            SimulationAgent.this.consumptions.removeAllElements();

            // Instatiate simulation progress GUI
            progressGui = new ProgressGui(SimulationAgent.this);
            suiteGUI.addToMainPanel(progressGui,SuiteGUI.TOP_LAYER);
            progressGui.setLocation(50,50);
            progressGui.show();
            progressGui.addInternalFrameListener(new InternalFrameAdapter(){
                public void internalFrameClosed(InternalFrameEvent e){
                   AgentController cons;
                   try{
                       for(int i=0; i<SimulationAgent.this.consumers.length ; i++){
                        cons = DAWN.jadeContainer.getAgent(SimulationAgent.this.consumers[i].getName());
                        cons.suspend();
                        cons.kill();
                       }
                       cons = DAWN.jadeContainer.getAgent("metOffice");
                       cons.kill();
                       cons = DAWN.jadeContainer.getAgent("supplier");
                       cons.kill();
                   }
                   catch(ControllerException ce){
                	   log.error(ce.getStackTrace());
                   }
                }
            });
            // Launch agents
            instantiatePlatform();

            // Set initial consumption
            this.myAgent.consumptions.addElement(new Float(this.myAgent.initialConsumption));
            progressGui.updateChart((double)this.myAgent.initialConsumption, 0);

            progressGui.updateMessageArea("Painting grid...Wait");
            progressGui.paintGrid(SimulationAgent.gridDimension,myAgent.consumers,SimulationAgent.consumerTypes);
            progressGui.enableStartButton(true);
     }

  }// END of BehaviourStartSimulation



  /**
   * BehaviourStartSimulationStep sends the Message to WSA that starts one simulation step</p>
  * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
   */


  private class BehaviourStartSimulationStep extends OneShotBehaviour implements AIDs{

	private static final long serialVersionUID = 5552139150976590116L;

	private SimulationAgent myAgent;

     private Integer step;

     /**
      * CONSTRUCTOR
      * The SA's behaviour that starts one simulation step by informing Water Supplier Agent
      * @param a Simulation Agent
      * @param step step's ID to start
      */


     public BehaviourStartSimulationStep(SimulationAgent a,Integer step) {
         super(a);
         myAgent = a;
         this.step = step;
     }

     // ACTION
     public void action() {

         // Create message
         ACLMessage startMsg = new ACLMessage(ACLMessage.REQUEST);
         startMsg.addReceiver(WATER_SUPPLIER);
         startMsg.setLanguage(myAgent.codec.getName());
         startMsg.setOntology(myAgent.ontology.getName());

         // Create content
           // Fill concept
         StepAttr step = new StepAttr();
         step.setId(this.step);
           // Fill agentAction
         Start aa = new Start();
         aa.setSimulationStep(step);
           // Fill message content
         Action act = new Action(WATER_SUPPLIER,aa);
         try{
            myAgent.getContentManager().fillContent(startMsg,act);
            myAgent.send(startMsg);
         }
         catch (CodecException ce){ log.error(ce.getStackTrace()); }
         catch (OntologyException oe){ log.error(oe.getStackTrace());}

     } // End of action

  } // End BehaviourStartSimStep


  /**
   * BehaviourReceiveStepResult receives step results and updates progressGUI</p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
   */

  private class BehaviourReceiveStepResult extends CyclicBehaviour implements AIDs{

	private static final long serialVersionUID = 1781630253559756364L;
	private SimulationAgent myAgent;

      // Constructor
      public BehaviourReceiveStepResult(SimulationAgent a){
            super(a);
            myAgent = a;
      }


      // ACTION

      @SuppressWarnings("unchecked")
	public void action() {

        MessageTemplate mt = MessageTemplate.and(
            MessageTemplate.MatchSender(WATER_SUPPLIER),
            MessageTemplate.MatchPerformative(ACLMessage.INFORM));

        ACLMessage receivedMsg = myAgent.receive(mt);


        if (receivedMsg!= null){
            //TEST
            log.info("SA : " + receivedMsg.getContent());

            try{
               ContentElement ce = myAgent.getContentManager().extractContent(receivedMsg);
               if (ce instanceof StepTotalConsumption) {
                     StepTotalConsumption tc = (StepTotalConsumption) ce;
                     WaterConsumption wc = (WaterConsumption) tc.getStepConsumption();
                     // store result and update GUI
                     myAgent.consumptions.addElement(wc.getQuantity());
                     myAgent.progressGui.updateChart((double)wc.getQuantity().floatValue(),(double)stepId);
               }
            }
            catch (CodecException ce){ log.error(ce.getStackTrace()); }
            catch (OntologyException oe){ log.error(oe.getStackTrace()); }
            catch (Exception ioe){ log.error(ioe.getStackTrace()); }

            // TEMP GUI
            if (stepId >=simulationDuration){
                myAgent.progressGui.updateBar(100);
                myAgent.progressGui.updateMessageArea("**** Simulation Ended ****");
            }
            else{
                 myAgent.progressGui.updateBar(Math.round((stepId*100)/simulationDuration));
                 stepId++;
                 myAgent.addBehaviour(new BehaviourStartSimulationStep(myAgent,new Integer(stepId)));
            }
        }
        else
	    block();

      }// END of action

  }// END Behaviour


  /**
   * BehaviourReceiveOutOfSequenceMessages handles all out of sequence messages. All message are shown on ProgressGUI</p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
   */

  private class BehaviourHandleOutOfSequenceMessages extends CyclicBehaviour implements AIDs{

	private static final long serialVersionUID = 2774341201231523471L;
	private SimulationAgent myAgent;

      // Constructor
      public BehaviourHandleOutOfSequenceMessages(SimulationAgent a){
            super(a);
            myAgent = a;
      }


      // ACTION

      public void action() {

        MessageTemplate mt = MessageTemplate.not(MessageTemplate.and(
                                                  MessageTemplate.MatchPerformative(ACLMessage.INFORM),
                                                  MessageTemplate.MatchSender(WATER_SUPPLIER)));

        ACLMessage receivedMsg = myAgent.receive(mt);

        if (receivedMsg!= null)
            myAgent.progressGui.updateMessageArea("[ " + receivedMsg.getSender().getLocalName() + " ]  :  "
                                                                          + receivedMsg.getContent() );
        else
	    block();

      }// END of action

  }// END BehaviourHandleOutOfSequenceMessages

  /**
   * Sends a REQUEST message to a consumer agent to launch its personal GUI
   * @param agentName The CA's name to which the message is sent
   */
  private void sendGuiRequestMessage(String agentName){
      boolean found = false;
      int i=-1;
      ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
      while(!found && i<this.consumers.length){
        i++;
        if (consumers[i].getName().equals(agentName))
            found=true;
      }
      msg.addReceiver(consumers[i].getAID());
      msg.setLanguage(codec.getName());
      msg.setOntology(ontology.getName());
      // Create content
      LaunchGUI lg = new LaunchGUI();
      Action act = new Action(consumers[i].getAID(),lg);
      try{
          getContentManager().fillContent(msg,act);
          send(msg);
      }
      catch (CodecException ce){ log.error(ce.getStackTrace()); }
      catch (OntologyException oe){ log.error(oe.getStackTrace());}

  }

  private void sendSaveResultsRequestToConsumers(File directoryPath){

      for(int i=0 ; i<this.consumers.length ; i++){
          ACLMessage msg = new ACLMessage(ACLMessage.REQUEST);
          msg.addReceiver(consumers[i].getAID());
          msg.setLanguage(codec.getName());
          msg.setOntology(ontology.getName());
          // Create content
          SavingPath sp = new SavingPath();
          sp.setDirectory(directoryPath.getPath());
          SavePersonalData spd = new SavePersonalData();
          spd.setToDirectory(sp);
          Action act = new Action(consumers[i].getAID(),spd);
          try{
              getContentManager().fillContent(msg,act);
              send(msg);
          }
          catch (CodecException ce){ log.error(ce.getStackTrace());}
          catch (OntologyException oe){ log.error(oe.getStackTrace());}
      }

  }// END of method


  private int saveScenarioToFile(File fileName){
    int ok = 0;
    String errorMsg = "An error occured while saving scenario";
    try{
      FileOutputStream out = new FileOutputStream(fileName);
      ObjectOutputStream s = new ObjectOutputStream(out);
      //s.writeObject(temp1);
      // Simulation Parameters
      s.writeObject(new Integer(gridDimension));
      s.writeObject(new Integer(sightLimit));
      s.writeObject(new Integer(population));
      s.writeObject(new Integer(simulationDuration));
      s.writeObject(new Integer(simulationStep));
      //Consumer Types
      s.writeObject(consumerTypes);
      s.writeObject(SimulationAgent.consumptionLN);
      s.writeObject(demandCurveParameters);

      s.writeObject(metDataFile);
      s.writeObject(priceData);
      s.writeObject(new Float(distributionMean));
      s.writeObject(new Float(distributionDeviation));
      s.flush();
    }
    catch(FileNotFoundException fnfe){log.error(fnfe.getStackTrace()); ok = 1;this.suiteGUI.errorMessage(errorMsg);}
    catch(IOException ioe){log.error(ioe.getStackTrace()); ok = 2;this.suiteGUI.errorMessage(errorMsg);}

    return ok;
  }

   private int loadScenarioFromFile(File fileName){
    int ok = 0;
    String errorMsg = "An error occured while loading scenario";
    try{
      FileInputStream in = new FileInputStream(fileName);
      ObjectInputStream s = new ObjectInputStream(in);

      // Simulation Parameters
      SimulationAgent.gridDimension = ((Integer)s.readObject()).intValue();
      SimulationAgent.sightLimit = ((Integer)s.readObject()).intValue();
      SimulationAgent.population = ((Integer)s.readObject()).intValue();
      SimulationAgent.simulationDuration = ((Integer)s.readObject()).intValue();
      SimulationAgent.simulationStep = ((Integer)s.readObject()).intValue();

      //Consumer Types
      SimulationAgent.consumerTypes = (ConsumerType[])s.readObject();

      SimulationAgent.consumptionLN = (Boolean)s.readObject();

      SimulationAgent.demandCurveParameters = (ParameterAttributes[][])s.readObject();

      SimulationAgent.metDataFile = (File)s.readObject();
      SimulationAgent.priceData = (Vector)s.readObject();
      SimulationAgent.distributionMean = ((Float)s.readObject()).floatValue();
      SimulationAgent.distributionDeviation = ((Float)s.readObject()).floatValue();

    }
    catch(FileNotFoundException fnfe){log.error(fnfe.getStackTrace()); ok = 1;this.suiteGUI.errorMessage(errorMsg);}
    catch(IOException ioe){log.error(ioe.getStackTrace()); ok = 2;this.suiteGUI.errorMessage(errorMsg);}
    catch(ClassNotFoundException cnfe){log.error(cnfe.getStackTrace());; ok = 3;this.suiteGUI.errorMessage(errorMsg);}

    return ok;
  }

  private int saveResultsToFile(File fileName){
    int ok = 0;
    String errorMsg = "An error occured while saving results";

    try{
        FileWriter out = new FileWriter(fileName);
        out.write("Step\tTotal Consumption\n");
        for (int i = 0 ; i<this.consumptions.capacity(); i++){

            out.write(new Integer(i).toString());
            out.write('\t');
            out.write(((Float)this.consumptions.elementAt(i)).toString());
            out.write('\n');
        }
        out.close();
    }
    catch(FileNotFoundException fnfe){log.error(fnfe.getStackTrace()); ok = 1;this.suiteGUI.errorMessage(errorMsg);}
    catch(IOException ioe){log.error(ioe.getStackTrace()); ok = 2; this.suiteGUI.errorMessage(errorMsg);}
    return ok;
  }

  private void launchReviewGui(){
    try{
      //Launch reviewGUI
      reviewGUI = new ReviewGUI(this);
      suiteGUI.addToMainPanel(reviewGUI,SuiteGUI.BACKGROUND_LAYER);
      reviewGUI.setMaximum(true);
      // Update labels
      reviewGUI.updateSimulationParametersLabels(SimulationAgent.population,SimulationAgent.gridDimension,SimulationAgent.sightLimit,
    		  SimulationAgent.simulationDuration,SimulationAgent.simulationStep);
      //elementAt [1] ---> scenario parameters
      reviewGUI.updatePricingPolicyLabels(((Float)SimulationAgent.priceData.elementAt(3)).floatValue(),
                                          ((Float)SimulationAgent.priceData.elementAt(4)).floatValue(),
                                          SuiteGUI.pricingScenarios[
                                                       ((Integer)SimulationAgent.priceData.elementAt(0)).intValue()],
                                           ((Integer)SimulationAgent.priceData.elementAt(2)).intValue() );
      int temp = 7;
      reviewGUI.setPriceTableSize(((Integer)SimulationAgent.priceData.elementAt(6)).intValue());
      for(int i=0; i < ((Integer)SimulationAgent.priceData.elementAt(6)).intValue(); i++){
          reviewGUI.updatePriceTable(new Integer(i+1),i,0);
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,1);
          temp++;
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,2);
          temp++;
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,3);
          temp++;
      }

      for(int i=0; i < SimulationAgent.consumerTypes.length; i++){
        reviewGUI.updateTypesCombo(SimulationAgent.consumerTypes[i].getName());
      }
      reviewGUI.updateFileLabel(SimulationAgent.metDataFile.getPath());

      for(int i=0; i < SimulationAgent.demandCurveParameters[0].length; i++){
        reviewGUI.updateCurveCombo(SimulationAgent.demandCurveParameters[0][i].getName());
      }
      int [] selections = reviewGUI.getCombosSelections();
      reviewGUI.updateDemandCurveParameter(SimulationAgent.demandCurveParameters[selections[0]][selections[1]]);

      //update Demand Curve Representation on review GUI
      String demandCurve = (SimulationAgent.consumptionLN.booleanValue()?"lnC":"C");
      for (int i=0 ; i<SimulationAgent.demandCurveParameters[0].length ; i++){
          if (i==0)
              demandCurve += " = ";
          else
              demandCurve += " + ";
          demandCurve += "e" + i + " " + (SimulationAgent.demandCurveParameters[0][i].getLn()?"Ln(":"") +
                                SimulationAgent.demandCurveParameters[0][i].getName() +
                               (SimulationAgent.demandCurveParameters[0][i].getLn()?")":"");

          if ( (i%4) == 3)
                demandCurve += "\n";
      }
      reviewGUI.updateDemandCurveRepresentation(demandCurve);
      reviewGUI.show();
    }
    catch(Exception e){log.error(e.getStackTrace());}
  }

  private void setSimulationParameters(GuiEvent ge){

    // Simulation Parameters
      SimulationAgent.population = ((Integer) ge.getParameter(0)).intValue();
      SimulationAgent.gridDimension = ((Integer) ge.getParameter(1)).intValue();
      SimulationAgent.sightLimit = ((Integer) ge.getParameter(2)).intValue();
      SimulationAgent.simulationDuration = ((Integer) ge.getParameter(3)).intValue();
      SimulationAgent.simulationStep = ((Integer) ge.getParameter(4)).intValue();

  }

  private void updatePricingPolicyToReviewGUI(){
      this.reviewGUI.updatePricingPolicyLabels(((Float)SimulationAgent.priceData.elementAt(3)).floatValue(),
                                               ((Float)SimulationAgent.priceData.elementAt(4)).floatValue(),
                                               SuiteGUI.pricingScenarios[
                                                       ((Integer)SimulationAgent.priceData.elementAt(0)).intValue()],
                                               ((Integer)SimulationAgent.priceData.elementAt(2)).intValue() );
      int temp = 7;
      reviewGUI.setPriceTableSize(((Integer)SimulationAgent.priceData.elementAt(6)).intValue());
      for(int i=0; i < ((Integer)SimulationAgent.priceData.elementAt(6)).intValue(); i++){
          reviewGUI.updatePriceTable(new Integer(i+1),i,0);
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,1);
          temp++;
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,2);
          temp++;
          reviewGUI.updatePriceTable(SimulationAgent.priceData.elementAt(temp),i,3);
          temp++;
      }

  }

  private void distributeTypesToAgents(){
     int total = 0;
     for(int i=0; i<(SimulationAgent.consumerTypes.length-1) ; i++){
        int temp = Math.round((SimulationAgent.consumerTypes[i].getPercentage().floatValue()/100) * SimulationAgent.population);
        SimulationAgent.consumerTypes[i].setMembers(temp);
        total += temp;
     }
     SimulationAgent.consumerTypes[SimulationAgent.consumerTypes.length-1].setMembers(Math.abs(population-total));

  }

}// END Simulator Agent