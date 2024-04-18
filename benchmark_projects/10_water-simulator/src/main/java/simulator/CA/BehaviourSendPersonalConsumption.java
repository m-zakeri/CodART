package simulator.CA;


import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.core.behaviours.DataStore;
import jade.core.behaviours.OneShotBehaviour;
import jade.lang.acl.ACLMessage;
import simulator.ontology.Consumes;
import simulator.ontology.WaterConsumption;
import simulator.util.AIDs;


/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


class BehaviourSendPersonalConsumption extends OneShotBehaviour implements AIDs{

	private static final long serialVersionUID = 1355295821319966877L;
	private ConsumerAgent myAgent;

    public BehaviourSendPersonalConsumption(ConsumerAgent a, DataStore ds){
      super(a);
      myAgent = a;
      this.setDataStore(ds);
    }

    public void action(){

      ACLMessage queryFromWSA = (ACLMessage) this.getDataStore().get(ConsumerAgent.QUERY_KEY);

      // Prepare reply to WSA
      ACLMessage consumption = queryFromWSA.createReply();
      consumption.setPerformative(ACLMessage.INFORM);
      try{
          ContentElement ce = myAgent.getContentManager().extractContent(queryFromWSA);
          if (ce instanceof Consumes) {
              Consumes cs = (Consumes) ce;

              // CONSUME WATER
              WaterConsumption wc = myAgent.consumeWater();
              cs.setPersonalConsumption(wc);
              myAgent.getContentManager().fillContent(consumption,cs);
          }
      }
      catch (CodecException ce){ce.printStackTrace();}
      catch (OntologyException oe){oe.printStackTrace();}

      //TEST
      //System.out.println(myAgent.getLocalName() + " : (consume water)" + wc.getQuantity().toString());

      // Send personal consumption to WSA
      myAgent.send(consumption);
    }

  } // Behaviour BehaviourSendPersonalConsumption