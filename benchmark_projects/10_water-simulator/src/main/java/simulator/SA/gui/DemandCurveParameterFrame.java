package simulator.SA.gui;

import jade.gui.GuiEvent;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;

import org.apache.log4j.Logger;

import simulator.SA.SimulationAgent;
import simulator.util.ConsumerType;
import simulator.util.Function;
import simulator.util.ParameterAttributes;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class DemandCurveParameterFrame extends JInternalFrame {

	private static final long serialVersionUID = 1208279781892420981L;

	private Logger log = Logger.getLogger(DemandCurveParameterFrame.class);
	private boolean flagFunctionSelected = false;

	private boolean flagSocialSelected = false;

	private String consumerTypeName;

	private String[] availableFunctionsNames;

	private Function[] availableFunctions;

	private ParameterAttributes parameter;

	private SimulationAgent myAgent;

	private int maxConstants = 0;

	//auxiliary
	private Hashtable functionNameToComboIndex = new Hashtable();

	private Hashtable socialNameToComboIndex = new Hashtable();

	// Constructor
	@SuppressWarnings("unchecked")
	public DemandCurveParameterFrame(SimulationAgent agent,
			Function[] availableFunctions, ConsumerType consumerType,
			ParameterAttributes parameter) {

		this.myAgent = agent;
		this.consumerTypeName = consumerType.getName();
		this.parameter = parameter;
		this.availableFunctions = availableFunctions;
		this.availableFunctionsNames = new String[availableFunctions.length];

		//Add available functions names to Combos (functionCombo & socialCombo)

		int countItems = 0; // auxiliary
		String hashKey;
		for (int i = 0; i < availableFunctions.length; i++) {
			availableFunctionsNames[i] = availableFunctions[i]
					.getFunctionName();
			this.functionCombo.addItem(availableFunctionsNames[i]);
			hashKey = availableFunctionsNames[i];
			functionNameToComboIndex.put(hashKey, new Integer(i));
			if (!(availableFunctionsNames[i].equals("MetDATA") || availableFunctionsNames[i]
					.equals("PRICE"))) {
				this.socialCombo.addItem(availableFunctionsNames[i]);
				socialNameToComboIndex.put(availableFunctionsNames[i]
						.toString(), new Integer(countItems));
				countItems++;
			}//END if
		}

		this.maxConstants = findMaxConstants();
		this.simpleLabels = new JLabel[2][maxConstants];
		defineSimpleLabels();
		this.simpleTextFields = new JTextField[2][maxConstants];
		defineSimpleTextFields();
		this.functionCombo.addActionListener(new functionComboListener());
		this.socialCombo.addActionListener(new socialComboListener());

		// Fill in labels
		this.setTitle("Editing " + parameter.getName() + " of "
				+ consumerType.getName() + " consumer Type");
		this.titleLabel1.setText(this.consumerTypeName + " Consumer Type");
		this.titleLabel2.setText("Demand Curve Parameter : "
				+ parameter.getName());

		// fill in elasticity and functions' constants
		fillSimpleTextFields();

		contentPane.add(titlePanel, BorderLayout.NORTH);
		contentPane.add(centerPanel, BorderLayout.CENTER);
		centerPanel.add(inputPanel);
		centerPanel.add(functionPanel);
		centerPanel.add(socialPanel);
		contentPane.add(endPanel, BorderLayout.SOUTH);

		if (parameter.getName().equals("TEMPERATURE")
				|| parameter.getName().equals("RAINFALL")) {
			functionCombo.setEnabled(false);
			flagFunctionSelected = true;
			functionCombo.setSelectedItem("MetDATA");

		} // if
		else if (parameter.isSocial())
			socialCombo.setEnabled(true);

	}// END of constructor

	// GUI setup
	private JPanel contentPane = (JPanel) this.getContentPane();
	{
		contentPane.setLayout(new BorderLayout());
		this.setClosable(true);
		this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
		this.setResizable(false);
		this.setSize(new Dimension(650, 400));

	}

	//*******************************************************
	// TITLE PANEL
	private JPanel titlePanel = new JPanel(new GridLayout(2, 1, 5, 5));
	{
		titlePanel.setBorder(BorderFactory.createEtchedBorder());
		titlePanel.setPreferredSize(new Dimension(0, 150));
	}

	//*******************************************************
	private JPanel subTitlePanel = new JPanel(new FlowLayout(FlowLayout.CENTER,
			5, 5));
	{
		titlePanel.add(subTitlePanel, null);
	}

	private JLabel titleLabel1 = new JLabel();
	{
		titleLabel1.setFont(new java.awt.Font("Dialog", 1, 12));
		titleLabel1.setBorder(BorderFactory.createRaisedBevelBorder());
		titleLabel1.setHorizontalAlignment(SwingConstants.CENTER);
		titleLabel1.setHorizontalTextPosition(SwingConstants.CENTER);
		subTitlePanel.add(titleLabel1, null);
	}

	private JLabel titleLabel2 = new JLabel();
	{
		titleLabel2.setFont(new java.awt.Font("Dialog", 1, 12));
		titleLabel2.setHorizontalAlignment(SwingConstants.CENTER);
		titleLabel2.setHorizontalTextPosition(SwingConstants.CENTER);
		titleLabel2.setForeground(SystemColor.textText);
		titlePanel.add(titleLabel2, null);
	}

	//***************************END of title panel***************************

	//*******************************************************
	// Center PANEL
	private JPanel centerPanel = new JPanel(new GridLayout(3, 1, 0, 0));
	{
		centerPanel.setBorder(BorderFactory.createEtchedBorder());
	}

	//*******************************************************
	// INPUT PANEL

	private JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,
			15, 20));
	{
		inputPanel.setBorder(BorderFactory.createEtchedBorder());
	}

	//*******************************************************

	private JLabel inputLabelElasticity = new JLabel("Elasticity  :");
	{
		inputLabelElasticity.setFont(new java.awt.Font("Dialog", 1, 12));
		inputLabelElasticity.setBorder(BorderFactory.createEtchedBorder());
		inputLabelElasticity.setHorizontalAlignment(SwingConstants.CENTER);
		inputLabelElasticity.setHorizontalTextPosition(SwingConstants.CENTER);
		inputPanel.add(inputLabelElasticity, null);
	}

	private JTextField textFieldElasticity = new JTextField(7);
	{
		textFieldElasticity.setBorder(BorderFactory.createLoweredBevelBorder());
		inputPanel.add(textFieldElasticity, null);
	}

	private JLabel inputLabelFunction = new JLabel("Function");
	{
		inputLabelFunction.setFont(new java.awt.Font("Dialog", 1, 12));
		inputLabelFunction.setHorizontalAlignment(SwingConstants.CENTER);
		inputLabelFunction.setHorizontalTextPosition(SwingConstants.CENTER);
		inputPanel.add(inputLabelFunction, null);
	}

	private JComboBox functionCombo = new JComboBox();
	{
		inputPanel.add(functionCombo, null);
	}

	private JLabel inputLabelSocial = new JLabel("Social Function");
	{
		inputLabelSocial.setFont(new java.awt.Font("Dialog", 1, 12));
		inputLabelSocial.setHorizontalAlignment(SwingConstants.CENTER);
		inputLabelSocial.setHorizontalTextPosition(SwingConstants.CENTER);
		inputPanel.add(inputLabelSocial, null);
	}

	private JComboBox socialCombo = new JComboBox();
	{
		socialCombo.setEnabled(false);
		inputPanel.add(socialCombo, null);
	}

	//***************************END of Input Panel**********************

	private JLabel[][] simpleLabels;

	private JTextField[][] simpleTextFields;

	//*******************************************************
	// Function PANEL

	private JPanel functionPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,
			5, 5));
	{
		functionPanel.setName("FUNCTION");
	}

	//*******************************************************
	// Social PANEL

	private JPanel socialPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,
			5, 5));
	{
		socialPanel.setName("SOCIAL");
	}

	//*******************************************************
	// End PANEL

	private JPanel endPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 10,
			10));
	{
		endPanel.setBorder(BorderFactory.createEtchedBorder());
		titlePanel.setPreferredSize(new Dimension(0, 60));
	}

	//*******************************************************

	private JButton cancelButton = new JButton("    Cancel    ");
	{

		cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
		endPanel.add(cancelButton, null);
		cancelButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				try {
					DemandCurveParameterFrame.this.setClosed(true);
				} catch (java.beans.PropertyVetoException ex) {
				}
			}
		});
	}

	private JButton okButton = new JButton("   OK   ");
	{
		okButton.setBorder(BorderFactory.createRaisedBevelBorder());
		endPanel.add(okButton, null);
		okButton.addActionListener(new ActionListener() {
			@SuppressWarnings("unchecked")
			public void actionPerformed(ActionEvent ev) {
				if (flagFunctionSelected
						&& (parameter.isSocial() ? flagSocialSelected : true)) {
					try {

						int i = 0;
						boolean ok = true;

						// Saving this consumer type parameters
						ParameterAttributes pa = DemandCurveParameterFrame.this.parameter;
						pa.setElasticity(new Float(textFieldElasticity
								.getText()).floatValue());
						pa
								.setDemandCurveFunction((Function) availableFunctions[functionCombo
										.getSelectedIndex()].getClass()
										.newInstance());

						//***************************
						if (functionCombo.getSelectedItem().equals("PRICE"))
							pa.getDemandCurveFunction()
									.setFunctionName("PRICE");
						if (functionCombo.getSelectedItem()
								.equals("RANDOM-INT"))
							pa.getDemandCurveFunction().setFunctionName(
									"RANDOM-INT");
						if (functionCombo.getSelectedItem().equals("RANDOM-FL"))
							pa.getDemandCurveFunction().setFunctionName(
									"RANDOM-FL");
						//****************************

						Vector v = new Vector(0);
						Iterator it = pa.getDemandCurveFunction()
								.getFunctionConstants();

						while (it.hasNext()) {
							Function.FunctionConstant fc = (Function.FunctionConstant) it
									.next();

							if (fc.asFloat())
								fc.setConstantValue(new Float(
										simpleTextFields[0][i].getText())
										.floatValue());
							else
								ok = fc.setConstantValue(simpleTextFields[0][i]
										.getText());

							if (!ok)
								new Float("zong!!");

							v.addElement(fc);

							i++;

						}// while

						pa.getDemandCurveFunction().setFunctionConstants(v);

						// if it is social PARAMETER
						if (pa.getDemandCurveFunction().getFunctionName()
								.equals("MetDATA")
								|| pa.getDemandCurveFunction()
										.getFunctionName().equals("PRICE"))
							parameter.setSocial(false);

						else if (parameter.isSocial()) {
							pa.setSocial(true);
							pa
									.setSocialFunction((Function) availableFunctions[socialCombo
											.getSelectedIndex()].getClass()
											.newInstance());

							//********************************
							if (socialCombo.getSelectedItem().equals(
									"RANDOM-INT"))
								pa.getSocialFunction().setFunctionName(
										"RANDOM-INT");
							if (socialCombo.getSelectedItem().equals(
									"RANDOM-FL"))
								pa.getSocialFunction().setFunctionName(
										"RANDOM-FL");
							//********************************

							i = 0;
							Vector v2 = new Vector(0);
							it = pa.getSocialFunction().getFunctionConstants();

							while (it.hasNext()) {
								Function.FunctionConstant fc = (Function.FunctionConstant) it
										.next();
								if (fc.asFloat())
									fc.setConstantValue(new Float(
											simpleTextFields[1][i].getText())
											.floatValue());
								else
									ok = fc
											.setConstantValue(simpleTextFields[1][i]
													.getText());

								if (!ok)
									new Float("zong!!");

								v2.addElement(fc);

								i++;
							}

							pa.getSocialFunction().setFunctionConstants(v2);

						}

						// Inform Simulation Agent
						GuiEvent ge = new GuiEvent(
								(Object) this,
								SimulationAgent.PARAMETER_INPUT);
						ge.addParameter(pa);
						DemandCurveParameterFrame.this.myAgent.postGuiEvent(ge);

						DemandCurveParameterFrame.this.setVisible(false);

						/*if(index >= demandCurveParameters.length-1){
						 Step3_1Frame.this.setVisible(false);
						 step3.setVisible(true);
						 }
						 else if (JOptionPane.showConfirmDialog(Step3_1Frame.this,"Continue to next Parameter","Confirm",
						 JOptionPane.YES_NO_OPTION,JOptionPane.QUESTION_MESSAGE)== JOptionPane.YES_OPTION){

						 // Reset flag and fields
						 flagFunctionSelected = false;
						 flagSocialSelected = false;
						 textFieldElasticity.setText("");
						 //Next parameter
						 index++;

						 Step3_1Frame.this.setTitle("Scenario Design Wizard - Step 3 - " + (index+1) + "/" + demandCurveParameters.length);
						 titleLabel2.setText("Demand Curve Parameter : " + demandCurveParameters[index].getName());

						 functionPanel.removeAll();
						 functionPanel.validate();
						 functionPanel.setBorder(BorderFactory.createEmptyBorder());

						 socialPanel.removeAll();
						 socialPanel.validate();
						 socialPanel.setBorder(BorderFactory.createEmptyBorder());

						 socialCombo.setEnabled(
						 demandCurveParameters[index].getSocial().booleanValue()?true:false);


						 if(demandCurveParameters[index].getName().equals("TEMPERATURE") ||
						 demandCurveParameters[index].getName().equals("RAINFALL")){
						 functionCombo.setEnabled(false);
						 flagFunctionSelected=true;
						 functionCombo.setSelectedItem("MetDATA");

						 } // if-temperature
						 else
						 functionCombo.setEnabled(true);

						 } // ELSE-if*/
					} catch (NumberFormatException nfe) {
						JOptionPane.showMessageDialog(
								DemandCurveParameterFrame.this,
								"Invalid INPUTS !!!", "Error",
								JOptionPane.ERROR_MESSAGE);
					} catch (IllegalAccessException iae) {
						log.error(iae.getStackTrace());
					} catch (InstantiationException ie) {
						log.error(ie.getStackTrace());
					}

				}// IF  for Flags
				else { // functions are not selected
					JOptionPane.showMessageDialog(
							DemandCurveParameterFrame.this,
							"Select Functions !!!", "Error",
							JOptionPane.ERROR_MESSAGE);
				}
			}// Action performed
		});
	} // END okButton

	//***************************END of End Panel**********************

	private int findMaxConstants() {
		for (int i = 0; i < availableFunctions.length; i++)
			if (availableFunctions[i].constantsNumber() > maxConstants)
				maxConstants = availableFunctions[i].constantsNumber();
		return maxConstants;
	}

	private void defineSimpleLabels() {
		for (int j = 0; j < 2; j++)
			for (int i = 0; i < maxConstants; i++) {
				simpleLabels[j][i] = new JLabel();
				simpleLabels[j][i].setFont(new java.awt.Font("Dialog", 1, 12));
				simpleLabels[j][i]
						.setHorizontalTextPosition(SwingConstants.CENTER);
				simpleLabels[j][i].setSize(new Dimension(20, 15));
			}

	}

	private void defineSimpleTextFields() {
		for (int j = 0; j < 2; j++)
			for (int i = 0; i < maxConstants; i++) {
				simpleTextFields[j][i] = new JTextField(4);
				simpleTextFields[j][i].setBorder(BorderFactory
						.createLoweredBevelBorder());
			}

	}

	private void createParametersPanel(JPanel panel, Function function) {
		int j = ((panel.getName() == "FUNCTION") ? 0 : 1);
		String title = ((panel.getName() == "FUNCTION") ? "Function  :"
				: "Social Function  :");

		panel.setBorder(BorderFactory.createCompoundBorder(BorderFactory
				.createTitledBorder(BorderFactory
						.createLineBorder(SystemColor.BLACK), title + "   "
						+ function.getFunctionName().toLowerCase() + "    "
						+ function.getFunctionRepresentation()), BorderFactory
				.createEmptyBorder(5, 5, 5, 5)));

		int i = 0;
		Iterator it = function.getFunctionConstants();
		while (it.hasNext()) {
			Function.FunctionConstant fc = (Function.FunctionConstant) it
					.next();
			simpleLabels[j][i].setText(fc.getConstantName() + " : ");
			panel.add(simpleLabels[j][i], null);
			simpleTextFields[j][i].setText(function.getFunctionName().equals(
					"MetDATA") ? "1" : "");
			panel.add(simpleTextFields[j][i], null);
			i++;
		}
		panel.validate();

	} // End createParametersPanel

	private void fillSimpleTextFields() {

		this.flagFunctionSelected = true;
		this.flagSocialSelected = true;

		this.textFieldElasticity.setText(Float.toString(parameter
				.getElasticity()));

		String name = parameter.getDemandCurveFunction().getFunctionName();

		this.functionCombo.setSelectedIndex(((Integer) functionNameToComboIndex
				.get(name)).intValue());

		if (parameter.isSocial()) {
			name = parameter.getSocialFunction().getFunctionName();
			this.socialCombo.setSelectedIndex(((Integer) socialNameToComboIndex
					.get(name)).intValue());
		}

		Iterator it = parameter.getDemandCurveFunction().getFunctionConstants();
		int i = 0;
		while (it.hasNext()) {
			Function.FunctionConstant fc = (Function.FunctionConstant) it
					.next();
			this.simpleTextFields[0][i].setText(Float.toString(fc
					.getConstantFValue()));
			i++;
		}
		if (parameter.isSocial()) {
			it = parameter.getSocialFunction().getFunctionConstants();
			i = 0;
			while (it.hasNext()) {
				Function.FunctionConstant fc = (Function.FunctionConstant) it
						.next();
				this.simpleTextFields[1][i].setText(Float.toString(fc
						.getConstantFValue()));
				i++;
			}
		}

	}

	//***************************************************************************
	// Listeners
	private class functionComboListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			if ("comboBoxChanged".equals(e.getActionCommand())) {
				functionPanel.removeAll();
				functionPanel.validate();
				flagFunctionSelected = true;
				if (functionCombo.getSelectedItem().toString()
						.equals("MetDATA")
						|| functionCombo.getSelectedItem().toString().equals(
								"PRICE")) {
					// to pass the ok test and will be changed
					flagSocialSelected = true;
					socialCombo.setEnabled(false);
					socialPanel.removeAll();
					socialPanel.setBorder(BorderFactory.createEmptyBorder());
					socialPanel.validate();
				} else if (parameter.isSocial()) {
					socialCombo.setEnabled(true);
				}
				createParametersPanel(functionPanel,
						availableFunctions[functionCombo.getSelectedIndex()]);
			}//END if
		}//END actionPerformed
	}// END of social Combo Listener

	private class socialComboListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			if ("comboBoxChanged".equals(e.getActionCommand())) {
				socialPanel.removeAll();
				socialPanel.validate();
				flagSocialSelected = true;
				createParametersPanel(socialPanel,
						availableFunctions[socialCombo.getSelectedIndex()]);
			}
		}
	}

}// END of DemandCurveParameterFrame