package simulator.WSA;

import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.content.onto.basic.Action;
import jade.core.behaviours.DataStore;
import jade.core.behaviours.OneShotBehaviour;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import simulator.ontology.Start;
import simulator.util.AIDs;

/**
 * <p>Title: BehaviourWaitStartStep</p>
 * <p>Description: WSA behaviour for just waiting a message from SA to start N step</p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */
class BehaviourWaitStartStep extends OneShotBehaviour implements AIDs{

private static final long serialVersionUID = 1699234409030797957L;
private WaterSupplierAgent myAgent;

  public BehaviourWaitStartStep(WaterSupplierAgent a, DataStore ds){
        super(a);
        this.myAgent = a;
        this.setDataStore(ds);
  }

  public void action(){
        MessageTemplate mt = MessageTemplate.and(
                 MessageTemplate.MatchPerformative(ACLMessage.REQUEST),
                 MessageTemplate.MatchOntology(myAgent.ontology.getName())
        );

        ACLMessage receivedMsg = myAgent.blockingReceive(mt);

        try{
            ContentElement ce = myAgent.getContentManager().extractContent(receivedMsg);
                    if (ce instanceof Action) {
                        Action rc = (Action) ce;
                        Start st = (Start) rc.getAction();
                        // Stores stepId in the shared datastore
                        this.getDataStore().put(WaterSupplierAgent.STEP_ID_KEY,st.getSimulationStep().getId());
                    }
        }
        catch (CodecException ce){
               ce.printStackTrace();
        }
        catch (OntologyException oe){
               oe.printStackTrace();
        }
        catch (Exception ioe){
              ioe.printStackTrace();
        }
  }
}