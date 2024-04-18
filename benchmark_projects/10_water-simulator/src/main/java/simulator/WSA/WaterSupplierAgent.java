package simulator.WSA;



import jade.content.lang.Codec;
import jade.content.lang.sl.SLCodec;
import jade.core.Agent;
import jade.core.behaviours.DataStore;
import jade.core.behaviours.SequentialBehaviour;
import jade.lang.acl.ACLMessage;

import java.util.Vector;

import simulator.ontology.WDS_Ontology;
import simulator.util.AIDs;
import simulator.util.ConsumerAttributes;

/**
 * <p>Title: WaterSupplierAgent </p>
 * <p>Description: Waits the step number from SA , asks MOA for met data, informs consumers about price
 * and met data and finally calculates step's total consumption and sends it to SA  </p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class WaterSupplierAgent extends Agent implements AIDs{

  private static final long serialVersionUID = 8293008733009089544L;
// DataStore KEYS
  protected static final String STEP_ID_KEY = "StepId";
  protected static final String TEMPERATURE_KEY = "TemperatureForStep";
  protected static final String RAINFALL_KEY = "RainfallForStep";
  protected static final String STEP_TOTAL_KEY = "StepTotalConsumption";

  // Ontology
  protected Codec codec = new SLCodec();
  protected WDS_Ontology ontology = WDS_Ontology.getInstance();

  // All Consumers Agents in this simulation
  private ConsumerAttributes[] allConsumers;

  // The inputs argument
  private boolean queryMOA;
  private Vector priceData;
  private Integer simulationStep;



  public void setup() {

       // Register SLCodec (language)
       getContentManager().registerLanguage(codec);
       getContentManager().registerOntology(ontology);

       // Get arguments (queryMOA , consumers , priceData)
       unpackArguments();

       DataStore ds = new DataStore();

       // In case MOA isn't launched
       // (these values are read in BehaviourQueryConsumers to fill in the message)
       ds.put(TEMPERATURE_KEY,new Float("0"));
       ds.put(RAINFALL_KEY,new Float("0"));

       SequentialBehaviour myBehaviour = new SequentialBehaviour(this){
       private static final long serialVersionUID = -5425911877378817619L;

			public int onEnd(){
                  reset();
                  myAgent.addBehaviour(this);
                  return super.onEnd();
              }
       };

       myBehaviour.addSubBehaviour(new BehaviourWaitStartStep(this,ds));

       // query if there is a parameter with MetData type
       if (queryMOA)
             myBehaviour.addSubBehaviour(new BehaviourMetDataQuery(this,createQueryMsg(),ds));

       myBehaviour.addSubBehaviour(new BehaviourQueryConsumers(this,createQueryMsg(),allConsumers,
                                                   priceData, this.simulationStep,ds));
       addBehaviour(myBehaviour);
  }

  /**
   * "Unpack" the arguments WSA receives when is born. The arguments are elements of an object array.
   * The first argument is a boolean value indicating whether WSA has to query MOA about met data.
   * It is true in case one of demand curve parameters has a function of type MetDataFunction.
   * The second argument is a Vector of all consumers (as ConsumerAttributes objects).
   * The third is all price data that will be passed to BehaviourQueryConsumers.
   */
  private void unpackArguments(){

     // get the list with the consumers
     Object[] allArguments = getArguments();

     queryMOA = ((Boolean)allArguments[0]).booleanValue();
     Vector v = (Vector) allArguments[1];
     allConsumers = new ConsumerAttributes[v.size()];
     v.copyInto(allConsumers);

     priceData = (Vector) allArguments[2];
     simulationStep = (Integer)allArguments[3];

  }// END of unpackArguments()

  /**
   * Creates an ACLMessage with QUERY_REF performative, FIPA_QUERY in protocol slot,
   * WSA's language and ontology selected.
   * @return The ACLMessage
   */
  protected ACLMessage createQueryMsg(){

        ACLMessage msg = new ACLMessage(ACLMessage.QUERY_REF);
        msg.setProtocol(jade.domain.FIPANames.InteractionProtocol.FIPA_QUERY);
        msg.setLanguage(codec.getName());
        msg.setOntology(ontology.getName());
        return msg;
  }

  /**
   * It's called when something goes wrong. WSA sents a message to SA in order to be displayed on progress
   * GUI
   * @param msg The message to be send to SA
   */
  protected void onFailure(ACLMessage msg){

        ACLMessage failureMsg = new ACLMessage(ACLMessage.FAILURE);
        failureMsg.addReceiver(SIMULATOR);
        failureMsg.setContent(msg.getSender() + " - " +  msg.getContent());
        send(failureMsg);
    }

} // END of AGENT