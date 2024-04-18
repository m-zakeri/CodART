package simulator.CA;

import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.core.behaviours.DataStore;
import jade.lang.acl.ACLMessage;
import jade.proto.AchieveREInitiator;

import java.util.Vector;

import org.apache.log4j.Logger;

import simulator.ontology.AskWeightsFor;
import simulator.ontology.Parameter;
import simulator.ontology.StepAttr;
import simulator.util.AIDs;
import simulator.util.ParameterAttributes;


/**
 * Consumer Agent's behaviour for contacting to its neighbours.
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

class BehaviourContactNeighbours extends AchieveREInitiator implements AIDs {
	
	private static final long serialVersionUID = 4131694655800331793L;
	
	private Logger log = Logger.getLogger(BehaviourContactNeighbours.class);
	
	private ConsumerAgent myAgent;
	
	private ParameterAttributes[] parametersToAsk;
	
	public BehaviourContactNeighbours(ConsumerAgent a, ACLMessage query,
			ParameterAttributes[] parametersToAsk, DataStore ds) {
		super(a, query);
		myAgent = a;
		this.setDataStore(ds);
		this.parametersToAsk = parametersToAsk;
	}
	
	protected Vector prepareRequests(ACLMessage msg) {
		
		Vector<ACLMessage> v = new Vector<ACLMessage>();
		ACLMessage msg1 = myAgent.createQueryMsgForNeighbourhood();
		try { // Fill message content
			myAgent.getContentManager()
			.fillContent(msg1, fillParametersToAsk());
		} catch (CodecException ce) {
			log.error(ce.getStackTrace());
		} catch (OntologyException oe) {
			log.error(oe.getStackTrace());
		}
		
		v.addElement(msg1);
		
		//TEST
		log.debug(myAgent.getLocalName() + " : (Contact Neighs) ");
		
		return v;
	} // Prepare Requests
	
	protected void handleAgree(ACLMessage msg) {
		log.debug("Agreed CA-" + msg.getSender().getLocalName());
	}
	
	protected void handleInform(ACLMessage msg) {
		onSuccess(msg);
	}
	
	protected void handleFailure(ACLMessage msg) {
		myAgent.onFailure(msg);
	}
	
	protected void handleRefuse(ACLMessage msg) {
		myAgent.onFailure(msg);
	}
	
	protected void handleNotUnderstood(ACLMessage msg) {
		myAgent.onFailure(msg);
	}
	
	protected void handleOutOfSequence(ACLMessage msg) {
		myAgent.onFailure(msg);
	}
	
	protected void handleAllResponses(Vector responses) {
	}
	
	protected void handleAllResultNotifications(Vector resultNotifications) {
		// Store replies to DataStore
		this.getDataStore().put(ConsumerAgent.REPLIES_KEY, resultNotifications);
		
		//TEST
		log.debug(myAgent.getLocalName() + " : (got replies) ");
		
	}// Result Not
	
	private void onSuccess(ACLMessage msg) {
		log.debug(myAgent.getLocalName() + " i by "
				+ msg.getSender().getLocalName());
	}
	
	/****************************
	 *  fillParametersToAsk()
	 *
	 * @return
	 */
	
	private AskWeightsFor fillParametersToAsk() {
		
		AskWeightsFor awf = new AskWeightsFor();
		StepAttr st = new StepAttr();
		st.setId((Integer) this.getDataStore().get(ConsumerAgent.STEP_KEY));
		awf.setStep3(st);
		
		for (int i = 0; i < parametersToAsk.length; i++) {
			Parameter temp = new Parameter();
			temp.setName(parametersToAsk[i].getName());
			awf.addParameters(temp);
		}
		
		return awf;
	}
	
}// END BehaviourContactNeighbours