package simulator.WSA;



import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.core.behaviours.DataStore;
import jade.lang.acl.ACLMessage;
import jade.proto.AchieveREInitiator;

import java.util.Vector;

import org.apache.log4j.Logger;

import simulator.ontology.HasMetData;
import simulator.ontology.MetData;
import simulator.ontology.StepAttr;
import simulator.util.AIDs;

/**
 * <p>Title: BehaviourMetDataQuery </p>
 * <p>Description: Beahaviour using QUERY-REF protocol for asking MOA the Temperature and RainFall
 * variables </p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


class BehaviourMetDataQuery extends AchieveREInitiator implements AIDs{

	private static final long serialVersionUID = 5608112376124330764L;
	private Logger log = Logger.getLogger(BehaviourMetDataQuery.class);
	private WaterSupplierAgent myAgent;

    public BehaviourMetDataQuery(WaterSupplierAgent a, ACLMessage queryMsg, DataStore ds){
        super(a,queryMsg);
        myAgent = a;
        this.setDataStore(ds);
    }

    @SuppressWarnings("unchecked")
	protected Vector prepareRequests(ACLMessage msg){

        Vector v = new Vector();
        ACLMessage msg1 = myAgent.createQueryMsg();
        msg1.addReceiver(MET_OFFICE);

        // Prepare content
            // Fill concept
        StepAttr step = new StepAttr();
        step.setId(((Integer)this.getDataStore().get(WaterSupplierAgent.STEP_ID_KEY)));

        MetData md = new MetData();

            // Fill Predidate
        HasMetData hsd = new HasMetData();
        hsd.setStep1(step);
        hsd.setData(md);

        try{
              // Fill message content
              myAgent.getContentManager().fillContent(msg1,hsd);
              v.addElement(msg1);
        }
        catch (CodecException ce){ ce.printStackTrace(); }
        catch (OntologyException oe){ oe.printStackTrace(); }

        return v;

    } // END prepareRequests


    protected void handleAgree(ACLMessage msg) { log.debug("Agreed");}

    protected void handleInform(ACLMessage msg) { onSuccess(msg);}

    protected void handleFailure(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleRefuse(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleNotUnderstood(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleOutOfSequence(ACLMessage msg) { myAgent.onFailure(msg);}



    private void onSuccess(ACLMessage msg){

            try{
                ContentElement ce = myAgent.getContentManager().extractContent(msg);
                if (ce instanceof HasMetData) {
                            HasMetData hd = (HasMetData) ce;
                            // Stores received met data in the shared datastore
                            this.getDataStore().put(WaterSupplierAgent.TEMPERATURE_KEY,hd.getData().getTemperature());
                            this.getDataStore().put(WaterSupplierAgent.RAINFALL_KEY,hd.getData().getRainfall());
                            //TEST
                            //System.out.println("\nWSA got from MOA : " + msg.getContent());
                }
                else{ myAgent.onFailure(msg); }
             }
             catch (CodecException ce){
               ce.printStackTrace();
             }
             catch (OntologyException oe){
               oe.printStackTrace();
             }
    } // END onSuccess

} // END BehaviourMetDataQuery



