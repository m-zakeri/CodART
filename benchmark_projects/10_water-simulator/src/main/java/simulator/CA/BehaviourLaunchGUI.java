package simulator.CA;

import org.apache.log4j.Logger;

import simulator.ontology.LaunchGUI;

import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.content.onto.basic.Action;
import jade.core.behaviours.CyclicBehaviour;
import jade.gui.GuiEvent;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;



/**
 * Consumer Agent's launch GUI behaviour.
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */
public class BehaviourLaunchGUI extends CyclicBehaviour{
	private static final long serialVersionUID = -8007416919898671713L;
	private Logger log = Logger.getLogger(BehaviourContactNeighbours.class);
	
	private ConsumerAgent myAgent;
    private MessageTemplate mT;

      // Constructor
      public BehaviourLaunchGUI(ConsumerAgent a, MessageTemplate mT){
            super(a);
            this.myAgent = a;
            this.mT = mT;
      }


      // ACTION

      public void action() {

        //MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.REQUEST);

        ACLMessage request = myAgent.receive(mT);
        if (request!= null){
         try{
           ContentElement ce = myAgent.getContentManager().extractContent(request);
            if (ce instanceof Action) {
                        Action rc = (Action) ce;
                        if (rc.getAction() instanceof LaunchGUI){
//                          LaunchGUI lg = (LaunchGUI) rc.getAction();
                          GuiEvent ge = new GuiEvent((Object)this,ConsumerAgent.GUI_REQUEST);
                          log.debug(myAgent.getLocalName() +" launched its own GUI");
                          myAgent.postGuiEvent(ge);
                        }
            }// END-if
         }
         catch (CodecException cee){ log.error(cee.getStackTrace()); }
         catch (OntologyException oe){ log.error(oe.getStackTrace());}
         catch (Exception ioe){ log.error(ioe.getStackTrace());}
        }// END-if
        else
	    block();

      }// END of action
}