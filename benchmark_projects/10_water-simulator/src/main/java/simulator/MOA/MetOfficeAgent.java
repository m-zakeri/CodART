package simulator.MOA;


import jade.content.ContentElement;
import jade.content.lang.Codec;
import jade.content.lang.Codec.CodecException;
import jade.content.lang.sl.SLCodec;
import jade.content.onto.OntologyException;
import jade.core.Agent;
import jade.domain.FIPAAgentManagement.FailureException;
import jade.domain.FIPAAgentManagement.NotUnderstoodException;
import jade.domain.FIPAAgentManagement.RefuseException;
import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.proto.AchieveREResponder;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Vector;

import org.apache.log4j.Logger;

import simulator.ontology.HasMetData;
import simulator.ontology.MetData;
import simulator.ontology.WDS_Ontology;
import simulator.util.AIDs;

/**
 * Met Office Agent is responsible for met data.When asked by WSA for the met data
 * of a specific time period, sends the right data back. Extends Jade's Agent class</p>
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class MetOfficeAgent extends Agent implements AIDs {
	
	private static final long serialVersionUID = 9053161619902067226L;
	private Logger log = Logger.getLogger(MetOfficeAgent.class);
// Ontology
  private Codec codec = new SLCodec();
  private WDS_Ontology ontology = WDS_Ontology.getInstance();

  // Read from arguments
  private File metDataFile;
  private int simulationDuration; // in steps
  private int simulationStep; // in months
  
  //Stores all met data for this simulation as FileData objects. Vector's index indicates the step
  private Vector metData = new Vector(0,1);



  public void setup() {

        unpackArguments();
        readMetDataFromFile();

        //Register language(SL) and ontology
        getContentManager().registerLanguage(codec);
        getContentManager().registerOntology(ontology);

        MessageTemplate mt = MessageTemplate.and(
                    MessageTemplate.MatchPerformative(ACLMessage.QUERY_REF),
                    MessageTemplate.MatchOntology(ontology.getName()));

        addBehaviour(new BehaviourReplyMetDataQuery(this,mt));
  }



  /**
   * <p>Title: BehaviourReplyMetDataQuery (MOA)</p>
   * <p>Description: MOA replies a query message about met data for a specific step simulation.
   * Communication follows FIPA protocol</p>
   * <p>Copyright: Copyright (c) 2003</p>
   * <p>Company: AUTH </p>
   * @author Vartalas Panagiotis
   * @version 1.0
   */

    class BehaviourReplyMetDataQuery extends AchieveREResponder {

	private static final long serialVersionUID = 409706462182524692L;

		MetOfficeAgent myAgent;

        boolean sentAgree = false;

	//Constructor
        public BehaviourReplyMetDataQuery(MetOfficeAgent a, MessageTemplate mt) {
	    super(a, mt, null);
            myAgent = a;
	}

	protected ACLMessage prepareResponse(ACLMessage query) throws RefuseException, NotUnderstoodException {
	    sentAgree=false;
	    // for future use
            int firstResponse;

           if (query.getLanguage().equals(codec.getName())){
               // I undestood the query
               firstResponse = 0;
           }
           else{
               // I didn't understand !!
               firstResponse = 2;
           }

	    ACLMessage response = query.createReply();

	    switch (firstResponse){
	      case 0 : {//send an AGREE
                         // jump first response and don't sent AGREE message !!!!
                         //response.setPerformative(ACLMessage.AGREE);
                         response = null;
                         sentAgree = true;
                         break;
		       }
              case 1 : { //send a REFUSE
                         response.setPerformative(ACLMessage.REFUSE);
                         break;
                       }
              case 2 : { //send a NOT UNDERSTOOD
                          response.setPerformative(ACLMessage.NOT_UNDERSTOOD);
                          response.setContent("Wrong Language or Ontology...");
                          break;
                       }
              case 3 : { //send an out of sequence Message
		         response.setPerformative(ACLMessage.SUBSCRIBE);
                         break;
                       }
              case 4 : { //send an INFORM
		         response.setPerformative(ACLMessage.INFORM);
                         break;
                       }
              default : {//check the time out expiration in initiator.
		          response = null;
                        }

	    }
	    //TEST
            //System.out.println("MOA  --> is sending "+(response==null?"no":(response.getPerformative()==ACLMessage.SUBSCRIBE?"an out-of-sequence":ACLMessage.getPerformative(response.getPerformative())))+ " response to the protocol initiator." );
	    return response;
	}

	protected ACLMessage prepareResultNotification(ACLMessage query, ACLMessage response) throws FailureException {

            // for future use
	    int secondResponse = 0;
            // Create reply message
            ACLMessage resNot = query.createReply();

	    if(sentAgree){
		switch (secondResponse){
                  case 0 : { //SENDING INFORM
                             resNot.setPerformative(ACLMessage.INFORM);
                                // Get content
                             try{
                                  ContentElement ce = myAgent.getContentManager().extractContent(query);
                                  if (ce instanceof HasMetData) {

                                        HasMetData hd = (HasMetData) ce;
                                        // get step ID
                                        Integer stepId = hd.getStep1().getId();

                                        // Fill content with meteorological data
                                        MetData data = new MetData();

                                        // meteorological data reading
                                        data.setTemperature(readTemperature(stepId));

                                        data.setRainfall(readRainfall(stepId));

                                        hd.setData(data);

                                        myAgent.getContentManager().fillContent(resNot,hd);
                                 }
                             }
                             catch (CodecException ce){
                               ce.printStackTrace();
                             }
                             catch (OntologyException oe){
                               oe.printStackTrace();
                             }
                             break;
                           }

                  case 1 : {  // sending FAILURE
		              resNot.setPerformative(ACLMessage.FAILURE);
                              break;
                           }
                  case 2 : {  //sending out of sequence message
		              resNot.setPerformative(ACLMessage.SUBSCRIBE);
                              break;
                           }
		  default : { // sending no message checking TIMEOUT of Initiator.
                              resNot = null;
		            }
		}
	    }else {
		// the inform message has been already sent.
		resNot = null;
	    }

            //TEST
            //System.out.println("MOA --> is sending "+(resNot==null?"no":(resNot.getPerformative()==ACLMessage.SUBSCRIBE?"an out-of-sequence":ACLMessage.getPerformative(resNot.getPerformative())))+ " result notification to the protocol initiator." );
	    return resNot;
	}
    } // End of inner class MyRequestResponder


    /**
     * "Unpack" the arguments MOA receives when is born. The arguments are elements of an object array.
     * The first argument is the simulation duration and the second the file where the met data are
     * stored. Is called first in setup method.
     */
    private void unpackArguments(){
      Object[] arguments = this.getArguments();
      this.simulationDuration = ((Integer)arguments[0]).intValue();
      this.metDataFile = (File)arguments[1];
      this.simulationStep = ((Integer)arguments[2]).intValue();
    }

    /**
     * All met data needed for the simulation, are read from the met file and stored in metData Vector().
     * Met data file is opened only here. After this method is called, MOA accesses met data from the Vector.
     */
    @SuppressWarnings("unchecked")
	private void readMetDataFromFile(){
      try{ FileReader source = new FileReader(this.metDataFile);
           BufferedReader reader = new BufferedReader(source);
            String str;
            int readRecords=0;

            while ( ((str = reader.readLine()) != null) && (readRecords < this.simulationDuration*this.simulationStep)){

                FileData fd = parseString(str);

                if (fd != null ){
                    this.metData.addElement(fd);
                    readRecords++;
                }

                
                log.debug(str + ",");
            }
            reader.close();
      }
      catch(FileNotFoundException fnff){ log.error("File not found : " + fnff.getMessage());}

      catch(IOException e){log.error(e.getStackTrace());}

    }// END readMetDataFromFile()


    /**
     * Parses the record and "translate" it into a temperature value and a rainfall value. The record
     * follows the specified format : [temperature] [rainfall] \n
     * @param record one line (string) read from met data File
     * @return FileData Object with temperature and rainfall properties filled
     */
    private FileData parseString(String record){

       float temperature = 0;

       String temp="";
       for(int i=0 ; i<record.length() ; i++){
          if( ( ((int)record.charAt(i) >=48) && ((int)record.charAt(i) <=57) )
                                                                      || record.charAt(i) == '.'){
              temp+= record.charAt(i);
          }// END-if
          else if (record.charAt(i) == ' ' && !temp.equals("")){
                   temperature = Float.valueOf(temp).floatValue();
                   temp="";
               }


       }//END-for

       if (temperature == 0 || temp == "") return null;

       return (new FileData(temperature,Float.valueOf(temp).floatValue()));

    }// END method parseString()

    /**
     * Returns the temperature as a Float for the specified simulation step
     * @param step the step for which to read the temperature
     * @return the temperature as a Float value
     */
    private Float readTemperature(Integer step){
        FileData fd = (FileData) metData.elementAt((step.intValue()-1)*simulationStep);
        // step checking (maybe)
        return (new Float(fd.getTemperature()));
    }

    /**
     * Returns the rainfall as a Float for the specified simulation step
     * @param step the step for which to read the rainfall
     * @return the rainfall as a Float value
     */
    private Float readRainfall(Integer step){
        FileData fd = (FileData) metData.elementAt((step.intValue()-1)*simulationStep);
        return (new Float(fd.getRainfall()));
    }


    /**
     * <p>Title: FileData</p>
     * <p>Description: MOA's inner class for storing temperature and rainfall values, read from met data
     * file, per step in metData Vector </p>
     * <p>Copyright: Copyright (c) 2003</p>
     * <p>Company: AUTH </p>
     * @author Vartalas Panagiotis
     * @version 1.0
     */
    private class FileData {

        // step implied by position in Vector
        //private int step;
        private float temperature;
        private float rainfall;

       FileData(/*int step, */float temperature,float rainfall){
          //this.step = step;
          this.temperature = temperature;
          this.rainfall = rainfall;
       }

       //public int getStep(){return this.step;}
       public float getTemperature(){return this.temperature;}
       public float getRainfall(){return this.rainfall;}

    }// END of inner class


} // END of MOA