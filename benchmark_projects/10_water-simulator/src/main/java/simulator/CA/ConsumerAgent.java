package simulator.CA;

import jade.gui.*;
import jade.core.AID;

import jade.core.behaviours.SequentialBehaviour;
import jade.core.behaviours.DataStore;

import jade.content.lang.Codec;
import jade.content.lang.sl.SLCodec;

import jade.lang.acl.ACLMessage;
import jade.lang.acl.MessageTemplate;
import jade.content.ContentElement;

import jade.content.lang.Codec.CodecException;
import jade.content.onto.OntologyException;

import jade.content.AgentAction;
import jade.content.onto.basic.Action;

import java.util.Vector;
import java.util.Iterator;
import java.util.Hashtable;
import java.io.*;

import org.apache.log4j.Logger;

import simulator.CA.gui.ConsumerGUI;
import simulator.ontology.*;
import simulator.util.*;

/**
 * Consumer Agent
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ConsumerAgent extends GuiAgent {
	private Logger log = Logger.getLogger(ConsumerAgent.class);
	private static final long serialVersionUID = -534407554583019863L;

	public static final int GUI_REQUEST = 100;

	public static final int SAVE_RESULTS = 101;

	// DataStore KEYS
	protected static final String STEP_KEY = "CurrentStepId";

	protected static final String QUERY_KEY = "QueryFromWSA";

	protected static final String REPLIES_KEY = "RepliesFromNeighbourhood";

	// Ontology
	protected Codec codec = new SLCodec();

	protected WDS_Ontology ontology = WDS_Ontology.getInstance();

	// Neighbours taken from arguments
	private ConsumerAttributes[] myNeighbours;

	// Price Type (average/marginal)
	private String priceType;

	private boolean consumptionLn;

	private Float initialConsumption;

	// Demand Curve parameters taken from arguments
	private ParameterAttributes[] myParameters;

	// The subset of demand curve parameters that are social (used in GUI & consumerWater())
	private ParameterAttributes[] socialParameters = new ParameterAttributes[0];

	// Key = social parameter name
	// Value = position in myParameters array
	private Hashtable socialHashTable = new Hashtable();

	//All weights stored
	private Object[] socialParametersWeightsPerStep;

	// Every step consumption is stored here
	private Vector personalConsumptions = new Vector(0, 1);

	// One common datastore for all behaviours
	private DataStore myDataStore = new DataStore();

	// GUI
	private ConsumerGUI myGui;

	public void setup() {

		// Register SLCodec (language) and Ontology
		getContentManager().registerLanguage(codec);
		getContentManager().registerOntology(ontology);

		// Get arguments and fill the array myNeighbours
		// Get arguments and fill the array myParameters
		unpackArguments("");

		// BEHAVIOURS
		MatchRequestContent match1 = new MatchRequestContent(new LaunchGUI());
		MessageTemplate template1 = new MessageTemplate(match1);
		MessageTemplate mT1 = MessageTemplate.and(MessageTemplate
				.MatchPerformative(ACLMessage.REQUEST), template1);

		MatchRequestContent match2 = new MatchRequestContent(
				new SavePersonalData());
		MessageTemplate template2 = new MessageTemplate(match2);
		MessageTemplate mT2 = MessageTemplate.and(MessageTemplate
				.MatchPerformative(ACLMessage.REQUEST), template2);
		/////////////////////////
		addBehaviour(new BehaviourLaunchGUI(this, mT1));
		addBehaviour(new BehaviourReceiveSavePersonalDataRequest(this, mT2));
		////////////////////////

		SequentialBehaviour behaviourSeq = new SequentialBehaviour(this) {
			private static final long serialVersionUID = 6617016302747624329L;

			public int onEnd() {
				reset();
				myAgent.addBehaviour(this);
				return super.onEnd();
			}
		};

		behaviourSeq.addSubBehaviour(new BehaviourReceivePriceAndMetData(this,
				myDataStore));

		// If no neighbours OR no social parameters don't add these behaviours
		// BehaviourContactBehaviour & BehaviourReplyNeighbours

		if (myNeighbours.length != 0) {
			socialParameters = socialParameters(myParameters);
			if (socialParameters.length != 0) {
				//Initialize storage
				socialParametersWeightsPerStep = new Object[socialParameters.length];
				for (int i = 0; i < socialParameters.length; i++) {
					Vector v = new Vector(1, 1);
					socialParametersWeightsPerStep[i] = v;
				}

				behaviourSeq.addSubBehaviour(new BehaviourContactNeighbours(
						this, createQueryMsgForNeighbourhood(),
						socialParameters, myDataStore));

				MatchNeighbourhood myMatch = new MatchNeighbourhood(
						myNeighbours);
				MessageTemplate myTemplate = new MessageTemplate(myMatch);

				MessageTemplate mT = MessageTemplate.and(MessageTemplate
						.MatchPerformative(ACLMessage.QUERY_REF), myTemplate);
				addBehaviour(new BehaviourReplyNeighbour(this, mT,
						socialParameters, myDataStore));

			}// END if-inner
		}//ENd if

		behaviourSeq.addSubBehaviour(new BehaviourSendPersonalConsumption(this,
				myDataStore));

		addBehaviour(behaviourSeq);

	} // SETUP

	/**
	 * unpackArguments :
	 * @param str PRINT for printing the neighbours List
	 */

	@SuppressWarnings("unchecked")
	private void unpackArguments(String str) {

		// get the list with your neighbours
		Object[] allArguments = getArguments();

		// firsst argument initial consumption
		initialConsumption = (Float) allArguments[0];

		personalConsumptions.addElement(initialConsumption);

		// second argument AP/ MP price type
		priceType = allArguments[1].toString();

		// third argument neighbours
		Vector neighs = (Vector) allArguments[2];
		this.myNeighbours = new ConsumerAttributes[neighs.size()];
		neighs.copyInto(this.myNeighbours);

		this.consumptionLn = ((Boolean) allArguments[3]).booleanValue();

		for (int i = 0; i < this.myNeighbours.length; i++)
			this.myNeighbours[i].setAID(new AID(this.myNeighbours[i].getName(),
					false));

		// fourth argument demand curve parameters
		this.myParameters = new ParameterAttributes[allArguments.length - 4];

		// Get Parameters
		for (int i = 4; i < allArguments.length; i++) {
			ParameterAttributes p = (ParameterAttributes) allArguments[i];
			this.myParameters[i - 4] = p;
		}

		if (this.myNeighbours.length == 0) {
			log.info(this.getLocalName() + " has NO Neighbours !!! ");
		} else if (str.equals("PRINT")) {
			for (int i = 0; i < this.myNeighbours.length; i++) {
				log.info(this.getLocalName() + " : "
						+ this.myNeighbours[i].getName());
			} // FOR
			log.info(this.getLocalName() + " : PARAMETERS -->");
			for (int i = 0; i < myParameters.length; i++) {
				log.info(this.myParameters[i].getName() + "  ");
			} // FOR
		} // if

	}// END of unpackArguments()

	@SuppressWarnings("unchecked")
	private ParameterAttributes[] socialParameters(
			ParameterAttributes[] myParameters) {

		Vector v = new Vector(0);
		for (int i = 0; i < myParameters.length; i++) {
			if (myParameters[i].isSocial()) {
				v.addElement(myParameters[i]);
				socialHashTable.put(myParameters[i].getName(), new Integer(v
						.indexOf(myParameters[i])));
			}
		}

		ParameterAttributes[] send = new ParameterAttributes[v.size()];
		v.copyInto(send);

		return send;

	}

	/**
	 * CreateQueryMsgForNeighbourhood
	 * @return : A FIPA_QUERY message in SL language and domain's ontology to be send
	 * to this agent's neighbours
	 */
	protected ACLMessage createQueryMsgForNeighbourhood() {

		ACLMessage msg = new ACLMessage(ACLMessage.QUERY_REF);
		msg.setProtocol(jade.domain.FIPANames.InteractionProtocol.FIPA_QUERY);
		for (int i = 0; i < myNeighbours.length; i++) {
			msg.addReceiver(myNeighbours[i].getAID());
		}
		msg.setLanguage(codec.getName());
		msg.setOntology(ontology.getName());

		return msg;
	}

	/**
	 *  onFailure(ACLMessage msg)
	 * @param msg
	 */

	protected void onFailure(ACLMessage msg) {
		ACLMessage failure = new ACLMessage(ACLMessage.FAILURE);
		failure.addReceiver(AIDs.SIMULATOR);
		failure.setContent(msg.getSender() + " -  " + msg.getContent());
		send(failure);
	}

	/**
	 * consumeWater : calculate personal water consumption for this simulation step
	 * @param step : simulation step number
	 * @return
	 */

	@SuppressWarnings("unchecked")
	protected WaterConsumption consumeWater() {

		// Temporary method variables
		int step = 0;
		float temperature = 0, rainfall = 0, consumption = 0, socialization = 0;
		float p, price = 0;

		ACLMessage queryFromWSA = (ACLMessage) myDataStore.get(QUERY_KEY);
		Vector neighboursReplies = (Vector) ((myDataStore.get(REPLIES_KEY) == null) ? null
				: myDataStore.get(REPLIES_KEY));

		// filled with VariableAttributes from all social replies
		Vector allWeights = new Vector(0);

		// Read all new data from WSA's query
		try {
			ContentElement ce = getContentManager()
					.extractContent(queryFromWSA);
			if (ce instanceof Consumes) {
				Consumes cs = (Consumes) ce;
				// Read simulation step Id
				StepAttr sa = cs.getStep2();
				step = sa.getId().intValue();

				// Read met data (temperature & rainfall)
				MetData md = cs.getMeteoData();
				temperature = md.getTemperature().floatValue();
				rainfall = md.getRainfall().floatValue();

				// Read water price
				price = calculatePriceVariable(queryFromWSA,
						((Float) this.personalConsumptions.lastElement())
								.floatValue());

				// Read all new data from socialization
				if ((myNeighbours.length != 0) && (neighboursReplies != null)) {
					Iterator ite = neighboursReplies.iterator();
					while (ite.hasNext()) {
						ce = getContentManager().extractContent(
								(ACLMessage) ite.next());
						if (ce instanceof AskWeightsFor) {
							AskWeightsFor av = (AskWeightsFor) ce;
							Iterator iteIn = av.getAllParameters();
							while (iteIn.hasNext()) {
								Parameter va = (Parameter) iteIn.next();
								allWeights.addElement(va);
							}

						}// END if

					}// END while-out
				}
			}
		} catch (CodecException ce) {
			log.error(ce.getStackTrace());
		} catch (OntologyException oe) {
			log.error(oe.getStackTrace());
		}

		// Socialization TOO...
		Parameter[] vas = new Parameter[allWeights.size()];
		allWeights.copyInto(vas);

		for (int i = 0; i < this.myParameters.length; i++) {
			if (this.myParameters[i].isSocial()
					&& (this.myNeighbours.length != 0)) {
				for (int j = 0; j < vas.length; j++) {
					if (vas[j].getName().equals(this.myParameters[i].getName()))
						socialization += vas[j].getWeight().floatValue(); //Sum all weights for this parameter
				}
				p = this.myParameters[i].valueFor(socialization);
				Integer k = (Integer) socialHashTable.get(this.myParameters[i]
						.getName());
				((Vector) socialParametersWeightsPerStep[k.intValue()])
						.addElement(new Float(socialization));
				try {
					myGui.updateSocialTable(socialization, step, k.intValue());
				} catch (Exception e) {
				}
				socialization = 0;
			}
			// maybe checking based on function type (MetData)
			else if (this.myParameters[i].getName().toUpperCase().equals(
					"TEMPERATURE"))
				p = this.myParameters[i].valueFor(temperature);
			else if (this.myParameters[i].getName().toUpperCase().equals(
					"RAINFALL"))
				p = this.myParameters[i].valueFor(rainfall);
			else if (this.myParameters[i].getDemandCurveFunction()
					.getFunctionName().equals("PRICE"))
				p = this.myParameters[i].valueFor(price);
			else
				p = this.myParameters[i].valueFor((this.myParameters[i]
						.isSocial() ? 0 : (float) step));

			consumption += p;

			
			log.debug(this.myParameters[i].getName() + ": " + p + "\t");

		} // END FOR

		// always consumption is stored in (m3)
		consumption = (this.consumptionLn ? (float) Math.exp(consumption)
				: consumption);

		log.debug(this.getLocalName() + " CONSUME : " + consumption);

		WaterConsumption wc = new WaterConsumption();
		wc.setQuantity(new Float(consumption));

		// store your consumption
		personalConsumptions.addElement(new Float(consumption));
		try {
			myGui.updateChart((double) consumption, (double) step);
		} catch (NullPointerException npe) {
		}

		return wc;

	}

	/**
	 * calculatePriceVariable : checks whether to use Average Price or Marginal Price
	 * @param queryFromWSA the message with price blocks
	 * @param previousConsumption the previous personal consumption
	 * @return the price value to be used in demand curve
	 */
	private float calculatePriceVariable(ACLMessage queryFromWSA,
			float lastConsumption) {

		float previousConsumption = (this.consumptionLn ? (float) Math
				.log(lastConsumption) : lastConsumption);

		if (previousConsumption < 0) {
			previousConsumption = (float) 0.1;
			this.sendFailureMessage("My last consumption was <0...");
		}

		PriceBlock[] priceBlocks;
		float price = 0;
		try {
			ContentElement ce = getContentManager()
					.extractContent(queryFromWSA);
			Consumes cs = (Consumes) ce;
			Object[] temp = cs.getPricingScale().toArray();
			priceBlocks = new PriceBlock[temp.length];
			for (int i = 0; i < priceBlocks.length; i++) {
				priceBlocks[i] = (PriceBlock) temp[i];
			}

			if (this.priceType.equals("AP"))
				price = getAveragePrice(priceBlocks, previousConsumption);
			else if (this.priceType.equals("MP"))
				price = getMarginalPrice(priceBlocks, previousConsumption);
		} catch (CodecException coe) {
			log.error(coe.getStackTrace());
		} catch (OntologyException one) {
			log.error(one.getStackTrace());
		}
		return price;

	}

	private float getAveragePrice(PriceBlock[] priceBlocks,
			float previousConsumption) {
		boolean ok = false;
		int i = 0;
		float AP = 0;

		while (!ok && i < priceBlocks.length) {

			if (priceBlocks[i].getLimitUp().intValue() > previousConsumption) {
				ok = true;
				AP = (AP + (priceBlocks[i].getPrice().floatValue() * (previousConsumption - priceBlocks[i]
						.getLimitDown().intValue())))
						/ previousConsumption;
			} else {
				int d = priceBlocks[i].getLimitUp().intValue()
						- priceBlocks[i].getLimitDown().intValue();
				AP = AP + (d * priceBlocks[i].getPrice().floatValue());
				i++;
			}

		}// End of while-loop

		// 1 KLIMAKA -->PAGIO
		if (i == 0)
			AP = priceBlocks[0].getPrice().floatValue();// * priceBlocks[0].getLimitUp().floatValue() )
		//previousConsumption;
		//TEST
		log.debug("Price policy is now: " + "i,AP = " + i + "  " + AP);
		return AP;
	}

	private float getMarginalPrice(PriceBlock[] priceBlocks,
			float previousConsumption) {
		boolean ok = false;
		int i = 0;
		float MP = 0;

		while (!ok) {
			if (priceBlocks[i].getLimitUp().intValue() > previousConsumption) {
				ok = true;
				MP = priceBlocks[i].getPrice().floatValue();
			} else
				i++;
		}//END of while-loop

		if (i == 0)
			MP = priceBlocks[1].getPrice().floatValue();
		return MP;
	}

	/**
	 *  MatchNeighbourhood : help inner class for matching neighbours AIDs
	 * <p>Title: Simulator</p>
	 * <p>Description: </p>
	 * <p>Copyright: Copyright (c) 2003</p>
	 * <p>Company: </p>
	 * @author Vartalas Panagiotis
	 * @version 1.0
	 */

	class MatchNeighbourhood implements MessageTemplate.MatchExpression {

		private static final long serialVersionUID = 5136444092348930313L;

		ConsumerAttributes[] neighbours;

		// Constructor
		MatchNeighbourhood(ConsumerAttributes[] t) {
			neighbours = t;
		}

		//This method verifies if the ACLMessage was sent from one of the expected senders.
		public boolean match(ACLMessage msg) {

			AID sender = msg.getSender();
			boolean out = false;
			int i = 0;
			while (!out && i < neighbours.length) {
				if (sender.equals(neighbours[i].getAID()))
					out = true;
				i++;
			}

			return out;
		}

	} // END MatchNeighbourhood

	/**
	 *
	 * <p>Title: Simulator</p>
	 * <p>Description: </p>
	 * <p>Copyright: Copyright (c) 2003</p>
	 * <p>Company: </p>
	 * @author Vartalas Panagiotis
	 * @version 1.0
	 */

	class MatchRequestContent implements MessageTemplate.MatchExpression {
		private static final long serialVersionUID = 4393818617360583909L;

		int myAction;

		// Constructor
		MatchRequestContent(AgentAction action) {
			if (action instanceof LaunchGUI)
				this.myAction = 0;
			else if (action instanceof SavePersonalData)
				this.myAction = 1;
		}

		//This method verifies the action of the Request ACLMessage.
		public boolean match(ACLMessage msg) {
			try {
				ContentElement ce = ConsumerAgent.this.getContentManager()
						.extractContent(msg);
				if (ce instanceof Action) {
					Action rc = (Action) ce;
					switch (myAction) {
					case 0:
						if (rc.getAction() instanceof LaunchGUI)
							return true;
						break;
					case 1:
						if (rc.getAction() instanceof SavePersonalData)
							return true;
						break;
					default:
						return false;
					}

				}// END-if
			} catch (CodecException cee) {
				log.error(cee.getStackTrace());
			} catch (OntologyException oe) {
				log.error(oe.getStackTrace());
			} catch (Exception ioe) {
				log.error(ioe.getStackTrace());
			}

			return false;
		}

	} // END MatchRequestContent

	public void onGuiEvent(GuiEvent e) {
		switch (e.getType()) {
		case GUI_REQUEST:
			launchGui();
			break;
		case SAVE_RESULTS:
			if (((File) e.getParameter(0)) != null)
				if (saveResultsToFile((File) e.getParameter(0)) != 0)
					sendFailureMessage("An error occured while saving results");
			break;

		}
	}

	/**
	 * launchGui
	 */
	private void launchGui() {

		myGui = new ConsumerGUI(this, personalConsumptions, myNeighbours,
				socialParameters, socialParametersWeightsPerStep);
		ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
		reply.addReceiver(AIDs.SIMULATOR);
//		reply.addReceiver(new AID("dawn", false));
		reply.setContent("my GUI is launched");
		send(reply);
	}

	/**
	 *
	 * @param directory
	 * @return
	 */

	private int saveResultsToFile(File directory) {
		int ok = 0;

		try {
			String fileName = directory.getPath() + "\\"
					+ this.getAID().getLocalName() + ".txt";
			@SuppressWarnings("unused") File file = new File(fileName);
			FileWriter out = new FileWriter(fileName);
			out.write("Step\tTotal Consumption\t"
					+ (this.consumptionLn ? " (lnC) " : ""));
			out
					.write("\n------------------------------------------------------\n");
			for (int i = 0; i < this.personalConsumptions.capacity(); i++) {

				out.write(new Integer(i).toString());
				out.write('\t');
				out.write(((Float) this.personalConsumptions.elementAt(i))
						.toString());

				if (this.consumptionLn) {
					out.write('\t');
					out.write('\t');
					float LNconsumption = (float) Math
							.log(((Float) this.personalConsumptions
									.elementAt(i)).floatValue());
					out.write(Float.toString(LNconsumption));
				}
				out.write('\n');
			}

			out.write("\n\n***********************************\n");
			out.write("Neighbourhood\n");
			out.write("***********************************\n");
			out.write("Neighbour\tConsumer Type\n");
			out.write("-----------------------------------\n");
			for (int i = 0; i < this.myNeighbours.length; i++) {

				out.write(this.myNeighbours[i].getName());
				out.write('\t');
				out.write(this.myNeighbours[i].getConsumerType());
				out.write('\n');
			}

			if (this.socialParameters.length > 0) {
				out
						.write("\n\n****************************************************\n");
				out.write("Socialization\n");
				out
						.write("****************************************************\n");
				out.write("Step");

				for (int i = 0; i < this.socialParameters.length; i++)
					out.write("\t" + this.socialParameters[i].getName());

				out
						.write("\n----------------------------------------------------");

				for (int i = 0; i < ((Vector) this.socialParametersWeightsPerStep[0])
						.capacity(); i++) {
					out.write('\n');
					out.write(new Integer(i + 1).toString());

					for (int j = 0; j < this.socialParametersWeightsPerStep.length; j++) {
						out.write('\t');
						out
								.write(((Float) ((Vector) this.socialParametersWeightsPerStep[j])
										.elementAt(i)).toString());

					}// for-j
				}// for-i
			}
			out.close();
		} catch (FileNotFoundException fnfe) {
			log.error(fnfe.getStackTrace());
			ok = 1;
		} catch (IOException ioe) {
			log.error(ioe.getStackTrace());
			ok = 2;
		}

		ACLMessage reply = new ACLMessage(ACLMessage.INFORM);
		reply.addReceiver(AIDs.SIMULATOR);
		reply.setContent("my personal data are saved");
		send(reply);

		return ok;
	}

	private void sendFailureMessage(String msg) {
		ACLMessage reply = new ACLMessage(ACLMessage.FAILURE);
		reply.addReceiver(AIDs.SIMULATOR);
//		reply.addReceiver(new AID("dawn", false));
		reply.setContent(msg);
		send(reply);
	}
} // END of AGENT

