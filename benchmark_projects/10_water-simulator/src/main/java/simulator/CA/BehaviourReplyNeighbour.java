package simulator.CA;


import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.core.behaviours.CyclicBehaviour;
import jade.core.behaviours.DataStore;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import java.util.Iterator;

import org.apache.log4j.Logger;

import simulator.ontology.AskWeightsFor;
import simulator.ontology.Parameter;
import simulator.ontology.StepAttr;
import simulator.util.ParameterAttributes;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */
public class BehaviourReplyNeighbour extends CyclicBehaviour{
	private static final long serialVersionUID = -8970863990310722224L;
		private Logger log = Logger.getLogger(BehaviourReplyNeighbour.class);
      private ConsumerAgent myAgent;
      private ParameterAttributes[] socialParameters;

      private MessageTemplate mt;

      // Constructor
      public BehaviourReplyNeighbour(ConsumerAgent a,MessageTemplate mt,
                                                        ParameterAttributes[] socialParameters,DataStore ds){
            super(a);
            myAgent = a;
            this.mt = mt;
            this.socialParameters = socialParameters;
            this.setDataStore(ds);
      }

      // ACTION

      public void action() {

        ACLMessage query = myAgent.receive(mt);
        ACLMessage resNot;
        if (query!= null){
           try{
             ContentElement ce = myAgent.getContentManager().extractContent(query);
             if ( ce instanceof AskWeightsFor){
                  resNot = query.createReply();
                  resNot.setPerformative(ACLMessage.INFORM);
                  resNot = replySocialQuery(query, resNot);
                  myAgent.send(resNot);
             }
           }
           catch(OntologyException oe){}
           catch(CodecException cex){}
        }
        else
	    block();

      }// END of action

      private ACLMessage replySocialQuery(ACLMessage query, ACLMessage resNot){

        // Answer the query
        // Fill the parameters' weights
        try{
          ContentElement ce = myAgent.getContentManager().extractContent(query);
          if (ce instanceof AskWeightsFor) {
             AskWeightsFor awf = (AskWeightsFor) ce;
             // Get stepId
             StepAttr st = (StepAttr) awf.getStep3();
             int stepId = st.getId().intValue();

             Iterator it = awf.getAllParameters();
             while(it.hasNext()){
                Parameter p = new Parameter();
                p = (Parameter)it.next();
                for(int i=0 ; i<socialParameters.length ; i++){
                    if (p.getName().equals(this.socialParameters[i].getName())  ){
                       float social = this.socialParameters[i].getSocialFunction().valueFor(stepId);
                       p.setWeight(new Float(social));
                    } // END if
                }// END for-i
             }//END while

             myAgent.getContentManager().fillContent(resNot,awf);
          }// END if
          else
              myAgent.onFailure(query);
        }
        catch (CodecException ce){log.error(ce.getStackTrace());}
        catch (OntologyException oe){log.error(oe.getStackTrace());}

        //TEST
//        Iterator receiver = resNot.getAllIntendedReceiver();
//        String s = ((AID)receiver.next()).getLocalName();
//        log.debug(myAgent.getLocalName() + " reply social to " + s);
        

        return resNot;

   } // END ReplySocialQuery

}// END BehaviourReplyNeighbour

