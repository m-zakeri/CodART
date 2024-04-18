package simulator.CA;

import org.apache.log4j.Logger;

import simulator.CA.ConsumerAgent;

import simulator.ontology.*;
import simulator.util.AIDs;



import jade.core.behaviours.OneShotBehaviour;
import jade.core.behaviours.DataStore;

import jade.content.ContentElement;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;

import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;

/**
 * CA behaviour to receive price & met data and store them to Datastore for 
 * later use
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

class BehaviourReceivePriceAndMetData extends OneShotBehaviour implements AIDs{
	private static final long serialVersionUID = 159728795644167290L;
	private Logger log = Logger.getLogger(BehaviourReceivePriceAndMetData.class);
	private ConsumerAgent myAgent;

    public BehaviourReceivePriceAndMetData(ConsumerAgent a, DataStore ds){
        super(a);
        myAgent = a;
        this.setDataStore(ds);
    } // Constructor


    // ACTION

    public void action(){

       MessageTemplate mt = MessageTemplate.and(
                      MessageTemplate.MatchSender(WATER_SUPPLIER),
                      MessageTemplate.MatchPerformative(ACLMessage.QUERY_REF));

       ACLMessage query = myAgent./*blockingR*/receive(mt);
       if(query != null){
           // Ontology check
           if (query.getOntology().equals(myAgent.ontology.getName())){
              this.getDataStore().put(ConsumerAgent.QUERY_KEY,query);
              // Store STEP_KEY for later use
              try{
                ContentElement ce = myAgent.getContentManager().extractContent(query);
                if (ce instanceof Consumes){
                   Consumes cs = (Consumes) ce;
                   StepAttr st = (StepAttr)cs.getStep2();
                   this.getDataStore().put(ConsumerAgent.STEP_KEY,st.getId());
                }
                else
                  myAgent.onFailure(query);
              }
              catch (CodecException ce){log.error(ce.getStackTrace());}
              catch (OntologyException oe){log.error(oe.getStackTrace());}

              //TEST
              log.debug(myAgent.getLocalName().toString() + " : (ReceivePrice&Met)" );
           }
           else{
              myAgent.onFailure(query);
           }
       }// END-if-outer
       else{
          this.block();
          this.parent.reset();
       }
    } // ACTION



  } // Behaviour