package simulator.WSA;



import jade.content.ContentElement;
import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;
import jade.core.behaviours.DataStore;
import jade.lang.acl.ACLMessage;
import jade.proto.AchieveREInitiator;

import java.util.Vector;

import org.apache.log4j.Logger;

import simulator.ontology.Consumes;
import simulator.ontology.MetData;
import simulator.ontology.PriceBlock;
import simulator.ontology.StepAttr;
import simulator.ontology.StepTotalConsumption;
import simulator.ontology.WaterConsumption;
import simulator.util.AIDs;
import simulator.util.ConsumerAttributes;

/**
 * <p>Title: BehaviourQueryConsumers</p>
 * <p>Description: WSA behaviour using QUERY-REF protocol to ask all consumers agents their consumption
 * for the given price and met data</p>
 * @author Panagiotis Vartalas
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

class BehaviourQueryConsumers extends AchieveREInitiator implements AIDs{

	private static final long serialVersionUID = 3921159876104072024L;
	private Logger log = Logger.getLogger(BehaviourQueryConsumers.class);
	private WaterSupplierAgent myAgent;

    //TEST
    private static int test;

    // All consumers agents
    private ConsumerAttributes[] consumers;


    // All price data from GUI
    @SuppressWarnings("unused")
	private Vector priceData;
    private int pricingScenario;
    @SuppressWarnings("unused")
	private Vector scenarioVariables = new Vector(0,1);
    private int simulationStep;
    private int reviewPeriod;
    private float CPI;
    private float CPIpercentage;
    // Price Type AP / MP
    @SuppressWarnings("unused")
	private String priceType;
    private int numberOfBlocks;
    private int[][] priceBlocksLimits;
    private float[] blocksPrices;

    // Actual water price (sent to CAs)
    private float[] actualPrices;
    // Reviewed water price (sent to SA)
    private float[] currentPrices;



    public BehaviourQueryConsumers(WaterSupplierAgent a, ACLMessage query, ConsumerAttributes[] consumers,
                               Vector priceData,Integer simulationStep,DataStore ds){
      super(a,query);
      this.myAgent = a;
      this.consumers = consumers;
      this.priceData = priceData;
      this.simulationStep = simulationStep.intValue();
      this.setDataStore(ds);

      this.pricingScenario = ((Integer)priceData.elementAt(0)).intValue();
      /////////////////////////////////////
      this.scenarioVariables = (Vector) priceData.elementAt(1);
      this.reviewPeriod = ((Integer)priceData.elementAt(2)).intValue();
      this.CPI = ((Float)priceData.elementAt(3)).floatValue();
      this.CPIpercentage = ((Float)priceData.elementAt(4)).floatValue();
      this.priceType = (String)priceData.elementAt(5);
      this.numberOfBlocks = ((Integer)priceData.elementAt(6)).intValue();
      this.priceBlocksLimits = new int[numberOfBlocks][2];
      this.blocksPrices = new float[numberOfBlocks];
      int j = 7;
      for(int i = 0; i<this.numberOfBlocks;i++){
        this.priceBlocksLimits[i][0] = ((Integer)priceData.elementAt(j)).intValue();
        j++;
        this.priceBlocksLimits[i][1] = ((Integer)priceData.elementAt(j)).intValue();
        j++;
        this.blocksPrices[i] = ((Float)priceData.elementAt(j)).floatValue();
        j++;
        //TEST
        //System.out.println(priceBlocksLimits[i][0] + "/" + priceBlocksLimits[i][1] + "/" + blocksPrices[i]);
      }

      this.actualPrices = new float[this.numberOfBlocks];
      this.currentPrices = new float[this.numberOfBlocks];
      //TEST
      test = consumers.length;

    }


    @SuppressWarnings("unchecked")
	protected Vector prepareRequests(ACLMessage msg){

        Vector v = new Vector();
        ACLMessage msg1 = myAgent.createQueryMsg();
        for (int i=0 ; i<consumers.length ; i++){
            msg1.addReceiver(consumers[i].getAID());
        }


        try{ // Fill message content
              myAgent.getContentManager().fillContent(msg1,prepareQueryMessageForConsumers());
              v.addElement(msg1);
        }
        catch (CodecException ce){ ce.printStackTrace(); }
        catch (OntologyException oe){ oe.printStackTrace(); }
         // TEST
        log.info("WSA - CA : " + msg1.getContent());
        return v;
    }

    protected void handleAgree(ACLMessage msg) {}

    protected void handleInform(ACLMessage msg) {
      //TEST
      if (test!=0)
          test--;
      else test = consumers.length;
      if((test%5)==0){
        log.debug("WSA : waiting  " + test + " more messages");
        /*ACLMessage fmsg = new ACLMessage(ACLMessage.FAILURE);
        fmsg.setContent("Waiting " + test + " more messages");
        myAgent.onFailure(fmsg);*/
      }

    }

    protected void handleFailure(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleRefuse(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleNotUnderstood(ACLMessage msg) { myAgent.onFailure(msg);}
    protected void handleOutOfSequence(ACLMessage msg) { myAgent.onFailure(msg);}

    protected void handleAllResponses(Vector responses){  }

    @SuppressWarnings("unused")
	private void onSuccess(ACLMessage msg){}

    protected void handleAllResultNotifications(Vector resultNotifications){

        // All personal consumptions arrived
        float stepTotal = 0;

        // Calculate step total consumption
        for(int i=0 ; i<resultNotifications.size() ; i++){
            ACLMessage msg = (ACLMessage) resultNotifications.elementAt(i);
            if (msg.getPerformative() == ACLMessage.INFORM){
               try{
                    ContentElement ce = myAgent.getContentManager().extractContent(msg);
                    if (ce instanceof Consumes) {
                        Consumes cs = (Consumes) ce;
                        WaterConsumption wc = (WaterConsumption) cs.getPersonalConsumption();
                        //////******
                        stepTotal += wc.getQuantity().floatValue();
                        this.getDataStore().put(WaterSupplierAgent.STEP_TOTAL_KEY,new Float(stepTotal));
                    }
               }
               catch (CodecException ce){ ce.printStackTrace(); }
               catch (OntologyException oe){ oe.printStackTrace(); }

            }
            else { myAgent.onFailure(msg);}
        }

        // Send Step result
        sendStepResultsToSA(stepTotal);
    }

    /**
     * Prepares query message for consumers. Fills stepID, temperature, rainfall and water price
     * @return A predicate Consumes filled with all appropriate values
     */
    private Consumes prepareQueryMessageForConsumers(){

        // Predicate
        Consumes cs = new Consumes();

        // Prepare content
          // Fill concepts
        StepAttr step = new StepAttr();
        step.setId(((Integer)this.getDataStore().get(WaterSupplierAgent.STEP_ID_KEY)));
        // Fill Predidate
        cs.setStep2(step);

        MetData md = new MetData();
        md.setTemperature(((Float)this.getDataStore().get(WaterSupplierAgent.TEMPERATURE_KEY)));
        md.setRainfall(((Float)this.getDataStore().get(WaterSupplierAgent.RAINFALL_KEY)));

        // Fill Predidate
        cs.setMeteoData(md);

        WaterConsumption wc = new WaterConsumption();
        // Fill Predidate
        cs.setPersonalConsumption(wc);  // empty

        // Fill price policy

        //Check if it's time for policy reviewing
        int currentStep = ((Integer)this.getDataStore().get(WaterSupplierAgent.STEP_ID_KEY)).intValue();
        int currentmonth = currentStep*this.simulationStep;
        if (( currentmonth % reviewPeriod) == 1){
          //Review pricing Policy
          reviewPricingPolicy(currentmonth);
        }

        PriceBlock[] blocks = currentPricingPolicy(0);
        for(int i=0 ; i<this.numberOfBlocks ; i++){
            cs.addPricingScale(blocks[i]);
        }

        return cs;

    }

    private PriceBlock[] currentPricingPolicy(int k){

        PriceBlock[] blocks = new PriceBlock[this.numberOfBlocks];

        for(int i=0 ; i<this.numberOfBlocks ; i++){
          blocks[i] = new PriceBlock();
          blocks[i].setNo(new Integer(i+1));
          blocks[i].setLimitDown(new Integer(this.priceBlocksLimits[i][0]));
          blocks[i].setLimitUp(new Integer(this.priceBlocksLimits[i][1]));
          if (k == 0)
            blocks[i].setPrice(new Float(this.actualPrices[i]));
          else
            blocks[i].setPrice(new Float(this.currentPrices[i]));
        }

        return blocks;
    }

    private void reviewPricingPolicy(int currentmonth){
    	
      // Calculate CPI
      float currentCPI = (float) (this.CPI*Math.pow((1+this.CPIpercentage/100/12),currentmonth));
      log.debug("current CPI at month " + currentmonth + " is " + currentCPI);
      
//      int years;
//      int months = currentStep * this.simulationStep;
//      if( (months%12) == 0 )
//          years = (months/12) - 1;
//      else
//          years = months/12;
//
//      for (int i = 0 ; i < years ; i++)
//          currentCPI = currentCPI * (1+(this.CPIpercentage/100));

      switch (this.pricingScenario){
          case 0 :scenario0(currentCPI);
                  break;
          case 1 :scenario1(currentCPI);
                  break;
                  
      }
    }

    // To timologio tou nerou paramenei sta8ero (meiwnetai h pragmatikh timh tou)
    private void scenario0(float currentCPI){
        for(int i=0 ; i < this.numberOfBlocks ; i++){
            this.actualPrices[i] = (this.blocksPrices[i] * 100) / currentCPI;
            this.currentPrices[i] = this.blocksPrices[i];
        }

    }

    // To timologio anaprosarmozetai wste h pragmatikh timh tou neroy na paramenei sta8erh
    private void scenario1(float currentCPI){
        for(int i=0 ; i < this.numberOfBlocks ; i++){
            this.actualPrices[i] = (this.blocksPrices[i] * 100) / this.CPI;
            this.currentPrices[i] = (this.actualPrices[i] * currentCPI) / 100;
        }

    }

    /**
     * Sends the step result to SA
     * @param stepTotal The step's total consumption
     */
    private void sendStepResultsToSA(float stepTotal){

           // Prepare INFORM message to Simulator Agent
            ACLMessage msg = new ACLMessage(ACLMessage.INFORM);
            msg.addReceiver(SIMULATOR);
            msg.setLanguage(myAgent.codec.getName());
            msg.setOntology(myAgent.ontology.getName());

            // Predicate
            StepTotalConsumption tc = new StepTotalConsumption();

            // Prepare content
                // Fill concepts
            StepAttr step = new StepAttr();
            step.setId(((Integer)this.getDataStore().get(WaterSupplierAgent.STEP_ID_KEY)));
            // Fill Predidate
            tc.setStep4(step);

            WaterConsumption wc = new WaterConsumption();
//            stepTotal = (stepTotal);
            wc.setQuantity(new Float(stepTotal));
            // Fill Predidate
            tc.setStepConsumption(wc);

            // Fill Predidate with price policy
            PriceBlock[] blocks = currentPricingPolicy(1);
            for(int i=0 ; i<blocks.length ; i++){
                tc.addWaterPrice(blocks[i]);
            }

            // Fill message content
            try{
               myAgent.getContentManager().fillContent(msg,tc);
               myAgent.send(msg);
            }
            catch (CodecException ce){
               ce.printStackTrace();
            }
            catch (OntologyException oe){
               oe.printStackTrace();
            }


    }
}// END of behaviour