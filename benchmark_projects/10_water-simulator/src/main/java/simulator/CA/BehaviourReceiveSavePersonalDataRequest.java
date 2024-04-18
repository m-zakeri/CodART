package simulator.CA;


import java.io.File;

import org.apache.log4j.Logger;

import simulator.ontology.*;

import jade.core.behaviours.CyclicBehaviour;

import jade.gui.GuiEvent;

import jade.content.ContentElement;
import jade.content.onto.basic.Action;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class BehaviourReceiveSavePersonalDataRequest extends CyclicBehaviour{

	private static final long serialVersionUID = -3367453254602681418L;
	private Logger log = Logger.getLogger(BehaviourReceiveSavePersonalDataRequest.class); 
      private ConsumerAgent myAgent;
      private MessageTemplate mT;

      // Constructor
      public BehaviourReceiveSavePersonalDataRequest(ConsumerAgent a, MessageTemplate mT){
            super(a);
            this.myAgent = a;
            this.mT = mT;
      }

      // ACTION

      public void action() {

        //MessageTemplate mt = MessageTemplate.MatchPerformative(ACLMessage.REQUEST);

        ACLMessage request = myAgent.receive(this.mT);
        if (request!= null){
         try{
           ContentElement ce = myAgent.getContentManager().extractContent(request);
            if (ce instanceof Action) {
                        Action rc = (Action) ce;
                        if (rc.getAction() instanceof SavePersonalData){
                          SavePersonalData lg = (SavePersonalData) rc.getAction();
                          SavingPath sp = lg.getToDirectory();
                          GuiEvent ge = new GuiEvent((Object)this,ConsumerAgent.SAVE_RESULTS);
                          File directoryPath = new File(sp.getDirectory());
                          ge.addParameter(directoryPath);
                          myAgent.postGuiEvent(ge);
                        }
            }// END-if
         }
         catch (CodecException cee){log.error(cee.getStackTrace()); }
         catch (OntologyException oe){ log.error(oe.getStackTrace());}
         catch (Exception ioe){ log.error(ioe.getStackTrace());}
        }// END-if
        else
	    block();

      }// END of action
}
