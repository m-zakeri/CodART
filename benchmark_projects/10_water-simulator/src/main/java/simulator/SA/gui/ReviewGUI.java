package simulator.SA.gui;

import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

import javax.swing.table.*;

import simulator.SA.SimulationAgent;
import simulator.util.Function;
import simulator.util.ParameterAttributes;

import java.util.Iterator;

import jade.gui.GuiEvent;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ReviewGUI extends JInternalFrame {
	private static final long serialVersionUID = 941186244140493719L;

	BorderLayout borderLayout1 = new BorderLayout();

	JPanel jPanel1 = new JPanel();

	GridLayout gridLayout1 = new GridLayout();

	TitledBorder titledBorder1;

	JLabel populationLabel = new JLabel();

	JLabel sightLabel = new JLabel();

	JLabel stepLabel = new JLabel();

	JLabel durationLabel = new JLabel();

	JLabel gridLabel = new JLabel();

	JPanel jPanel2 = new JPanel();

	TitledBorder titledBorder2;

	BorderLayout borderLayout2 = new BorderLayout();

	JPanel jPanel3 = new JPanel();

	JPanel parameterPanel = new JPanel();

	GridLayout gridLayout2 = new GridLayout();

	JPanel jPanel5 = new JPanel();

	JLabel jLabel6 = new JLabel();

	JComboBox typesCombo = new JComboBox();

	JPanel jPanel6 = new JPanel();

	JLabel jLabel7 = new JLabel();

	JComboBox curveCombo = new JComboBox();

	TitledBorder titledBorder3;

	JPanel jPanel7 = new JPanel();

	JLabel metFileLabel = new JLabel();

	GridLayout gridLayout3 = new GridLayout();

	JPanel jPanel8 = new JPanel();

	BorderLayout borderLayout3 = new BorderLayout();

	TitledBorder titledBorder4;

	JPanel jPanel9 = new JPanel();

	JLabel scenarioLabel = new JLabel();

	GridLayout gridLayout4 = new GridLayout();

	JLabel cpiLabel = new JLabel();

	JLabel percentageLabel = new JLabel();

	JLabel reviewLabel = new JLabel();

	JPanel priceBlocksPanel = new JPanel();

	TitledBorder titledBorder5;

	FlowLayout flowLayout2 = new FlowLayout();

	JScrollPane jScrollPane1 = new JScrollPane();

	GridLayout gridLayout5 = new GridLayout();

	PriceTableModel tableModel = new PriceTableModel();

	JTable priceBlocksTable = new JTable(tableModel);

	JTabbedPane tabPane = new JTabbedPane();

	GridLayout gridLayout6 = new GridLayout();

	JPanel demandCurvePanel = new JPanel();

	JPanel socialParameterPanel = new JPanel();

	Border border1;

	GridLayout gridLayout7 = new GridLayout();

	JLabel functionSocialLabel = new JLabel();

	GridLayout gridLayout8 = new GridLayout();

	TitledBorder titledBorder6;

	JPanel jPanel4 = new JPanel();

	JLabel elasticityLabel = new JLabel();

	JLabel functionLabel = new JLabel();

	GridLayout gridLayout9 = new GridLayout();

	JPanel demandTitledPanel = new JPanel();

	GridLayout gridLayout10 = new GridLayout();

	JLabel constantsLabel = new JLabel();

	TitledBorder titledBorder7;

	JPanel socialTitledPanel = new JPanel();

	TitledBorder titledBorder8;

	JLabel constantsSocialLabel = new JLabel();

	GridLayout gridLayout11 = new GridLayout();

	JPanel jPanel10 = new JPanel();

	JTextArea demandCurveLabel = new JTextArea();

	JScrollPane jScrollPane2 = new JScrollPane(demandCurveLabel);

	Border border2;

	Border border3;

	FlowLayout flowLayout1 = new FlowLayout();

	GridLayout gridLayout12 = new GridLayout();

	private SimulationAgent myAgent;

	public ReviewGUI(SimulationAgent myAgent) {
		this.myAgent = myAgent;
		try {
			jbInit();
			ActionListener listener = new CombosListener();
			this.curveCombo.addActionListener(listener);
			this.typesCombo.addActionListener(listener);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void jbInit() throws Exception {
		titledBorder1 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "Simulation Parameters");
		titledBorder2 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "Consumer Types");
		titledBorder3 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "Parameter");
		titledBorder4 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "Pricing Policy");
		titledBorder5 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "Price Blocks");
		border1 = BorderFactory.createEmptyBorder(5, 0, 5, 0);
		titledBorder6 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)),
				"function  represenation");
		titledBorder7 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)),
				"function representation");
		titledBorder8 = new TitledBorder(BorderFactory.createEtchedBorder(
				Color.white, new Color(165, 163, 151)), "");
		border2 = BorderFactory.createEmptyBorder(5, 25, 5, 25);
		border3 = BorderFactory.createEmptyBorder(20, 0, 0, 0);
		this.getContentPane().setLayout(borderLayout1);
		jPanel1.setBorder(titledBorder1);
		jPanel1.setPreferredSize(new Dimension(100, 130));
		jPanel1.setLayout(gridLayout1);
		populationLabel.setHorizontalAlignment(SwingConstants.CENTER);
		populationLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		populationLabel.setText("Population :");
		gridLayout1.setRows(5);
		sightLabel.setHorizontalAlignment(SwingConstants.CENTER);
		sightLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		sightLabel.setText("Sight limit :");
		stepLabel.setText("Simulation step :");
		stepLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		stepLabel.setHorizontalAlignment(SwingConstants.CENTER);
		durationLabel.setText("Duration :");
		durationLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		durationLabel.setHorizontalAlignment(SwingConstants.CENTER);
		gridLabel.setText("Grid dimension :");
		gridLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		gridLabel.setHorizontalAlignment(SwingConstants.CENTER);
		jPanel2.setLayout(borderLayout2);
		jPanel2.setBorder(titledBorder2);
		parameterPanel.setBorder(titledBorder3);
		parameterPanel.setPreferredSize(new Dimension(300, 10));
		parameterPanel.setLayout(gridLayout6);
		jPanel3.setLayout(gridLayout2);
		gridLayout2.setColumns(1);
		gridLayout2.setRows(3);
		jPanel5.setLayout(flowLayout1);
		jLabel6.setToolTipText("");
		jLabel6.setText("Consumer Types");
		jLabel7.setToolTipText("");
		jLabel7.setText("Demand Curve Parameters");
		jPanel7.setBorder(BorderFactory.createEtchedBorder());
		jPanel7.setPreferredSize(new Dimension(10, 35));
		jPanel7.setLayout(gridLayout3);
		metFileLabel.setHorizontalAlignment(SwingConstants.CENTER);
		metFileLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		metFileLabel.setText("Meteorological data file");
		jPanel8.setBorder(titledBorder4);
		jPanel8.setPreferredSize(new Dimension(100, 170));
		jPanel8.setLayout(borderLayout3);
		scenarioLabel.setHorizontalAlignment(SwingConstants.CENTER);
		scenarioLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		scenarioLabel.setText("Scenario :");
		jPanel9.setLayout(gridLayout4);
		gridLayout4.setRows(4);
		cpiLabel.setHorizontalAlignment(SwingConstants.CENTER);
		cpiLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		cpiLabel.setText("CPI : ");
		percentageLabel.setHorizontalAlignment(SwingConstants.CENTER);
		percentageLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		percentageLabel.setText("Increasing Percentage :");
		reviewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		reviewLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		reviewLabel.setText("Reviewing period :");
		priceBlocksPanel.setBorder(titledBorder5);
		priceBlocksPanel.setPreferredSize(new Dimension(300, 200));
		priceBlocksPanel.setLayout(gridLayout5);
		jPanel6.setLayout(flowLayout2);
		jScrollPane1.setBorder(null);
		demandCurvePanel.setLayout(gridLayout7);
		demandCurvePanel.setBorder(border1);
		gridLayout7.setColumns(1);
		gridLayout7.setRows(2);
		functionSocialLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		functionSocialLabel.setHorizontalAlignment(SwingConstants.CENTER);
		socialParameterPanel.setLayout(gridLayout8);
		gridLayout8.setColumns(1);
		gridLayout8.setRows(2);
		elasticityLabel.setToolTipText("");
		elasticityLabel.setHorizontalAlignment(SwingConstants.CENTER);
		elasticityLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		elasticityLabel.setText("elasticity : ");
		functionLabel.setToolTipText("");
		functionLabel.setHorizontalAlignment(SwingConstants.CENTER);
		functionLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		functionLabel.setText("function :");
		jPanel4.setLayout(gridLayout9);
		gridLayout9.setRows(2);
		demandTitledPanel.setLayout(gridLayout10);
		constantsLabel.setHorizontalAlignment(SwingConstants.CENTER);
		constantsLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		demandTitledPanel.setBorder(titledBorder7);
		socialTitledPanel.setBorder(titledBorder8);
		socialTitledPanel.setLayout(gridLayout11);
		constantsSocialLabel.setHorizontalTextPosition(SwingConstants.CENTER);
		constantsSocialLabel.setHorizontalAlignment(SwingConstants.CENTER);
		jPanel10.setLayout(gridLayout12);
		jPanel10.setBorder(border2);
		demandCurveLabel.setPreferredSize(new Dimension(140, 70));
		demandCurveLabel.setEditable(false);
		demandCurveLabel.setMargin(new Insets(5, 5, 5, 5));
		//demandCurveLabel.setColumns(20);
		//demandCurveLabel.setRows(3);
		flowLayout2.setHgap(0);
		flowLayout2.setVgap(0);
		jPanel5.setBorder(border3);
		jPanel6.setBorder(border3);
		jScrollPane2.setToolTipText("");
		jPanel4.add(elasticityLabel, null);
		jPanel4.add(functionLabel, null);
		demandCurvePanel.add(jPanel4, null);
		demandCurvePanel.add(demandTitledPanel, null);
		demandTitledPanel.add(constantsLabel, null);
		this.getContentPane().add(jPanel1, BorderLayout.NORTH);
		jPanel1.add(populationLabel, null);
		jPanel1.add(gridLabel, null);
		jPanel1.add(sightLabel, null);
		jPanel1.add(durationLabel, null);
		jPanel1.add(stepLabel, null);
		this.getContentPane().add(jPanel2, BorderLayout.CENTER);
		jPanel2.add(jPanel3, BorderLayout.CENTER);
		jPanel3.add(jPanel5, null);
		jPanel5.add(jLabel6, null);
		jPanel5.add(typesCombo, null);
		jPanel3.add(jPanel10, null);
		jPanel10.add(jScrollPane2, null);
		jPanel3.add(jPanel6, null);
		jPanel6.add(jLabel7, null);
		jPanel6.add(curveCombo, null);
		jPanel2.add(parameterPanel, BorderLayout.EAST);
		parameterPanel.add(tabPane, null);
		jPanel2.add(jPanel7, BorderLayout.SOUTH);
		jPanel7.add(metFileLabel, null);
		this.getContentPane().add(jPanel8, BorderLayout.SOUTH);
		jPanel8.add(jPanel9, BorderLayout.CENTER);
		jPanel9.add(scenarioLabel, null);
		jPanel9.add(reviewLabel, null);
		jPanel9.add(cpiLabel, null);
		jPanel9.add(percentageLabel, null);
		jPanel8.add(priceBlocksPanel, BorderLayout.EAST);
		priceBlocksPanel.add(jScrollPane1, null);
		jScrollPane1.getViewport().add(priceBlocksTable, null);

		socialParameterPanel.add(functionSocialLabel, null);
		socialParameterPanel.add(socialTitledPanel, null);
		socialTitledPanel.add(constantsSocialLabel, null);
		tabPane.add(demandCurvePanel, "demandCurvePanel");
		tabPane.add(socialParameterPanel, "Social");
	}

	private class PriceTableModel extends AbstractTableModel {

		private static final long serialVersionUID = -3773432964986979034L;

		private String[] columnsNames = { "Block No", "Limit Down", "Limit Up",
				"Price" };

		int rows = 10;

		private Object[][] data = new Object[rows][4];

		public void setRows(int rows) {
			data = new Object[rows][4];
		}

		public int getColumnCount() {
			return columnsNames.length;
		}

		public int getRowCount() {
			return data.length;
		}

		public String getColumnName(int col) {
			return columnsNames[col];
		}

		public Object getValueAt(int row, int col) {
			return data[row][col];
		}

		public void setValueAt(Object value, int row, int col) {
			data[row][col] = value;
			this.fireTableDataChanged();// fireTableCellUpdated(row,col);
		}

		public boolean isCellEditable(int row, int column) {
			return false;
		}

	} // END of PriceTable class

	private class CombosListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			GuiEvent ge = new GuiEvent((Object) this,
					SimulationAgent.REVIEW_COMBOS_CHANGED);
			ReviewGUI.this.myAgent.postGuiEvent(ge);
		}
	}

	public void updateSimulationParametersLabels(int population,
			int gridDimension, int sightLimit, int duration, int simulationStep) {
		this.populationLabel.setText("Population : " + population
				+ " Consumer Agents");
		this.gridLabel.setText("Grid dimension : " + gridDimension);
		this.durationLabel.setText("Simulation duration : " + duration
				+ " simulation steps");
		this.stepLabel.setText("Simulation step : " + simulationStep
				+ " month(s)");
		this.sightLabel.setText("Sight limit : " + sightLimit);
	}

	public void updatePricingPolicyLabels(float cpi, float percentageCPI,
			String scenario, int reviewPeriod) {
		this.cpiLabel.setText("Consumer Price Index (CPI) " + cpi);
		this.percentageLabel.setText("CPI increases " + percentageCPI
				+ " % per year");
		this.scenarioLabel.setText("Pricing policy : " + scenario);
		this.reviewLabel.setText("Policy reviewed every " + reviewPeriod
				+ " simulation step(s)");
	}

	public void updateTypesCombo(String consumerTypeName) {
		this.typesCombo.addItem(consumerTypeName);
	}

	public void updateCurveCombo(String curveParameterName) {
		this.curveCombo.addItem(curveParameterName);
	}

	public void updateFileLabel(String metDataFilePath) {
		this.metFileLabel.setText("Meteorological data file : "
				+ metDataFilePath);
	}

	public void setPriceTableSize(int rows) {
		this.tableModel.setRows(rows);
	}

	public void updatePriceTable(Object value, int row, int column) {
		this.tableModel.setValueAt(value, row, column);
	}

	public int[] getCombosSelections() {
		int[] temp = { this.typesCombo.getSelectedIndex(),
				this.curveCombo.getSelectedIndex() };
		return temp;
	}

	public void updateDemandCurveRepresentation(String curve) {
		this.demandCurveLabel.append(curve);
	}

	public void updateDemandCurveParameter(ParameterAttributes parameter) {
		this.elasticityLabel.setText(" elasticity : "
				+ parameter.getElasticity());
		this.functionLabel.setText("Function : "
				+ parameter.getDemandCurveFunction().getFunctionName()
						.toLowerCase());
		this.demandTitledPanel.setBorder(BorderFactory.createTitledBorder(
				BorderFactory.createLineBorder(SystemColor.BLACK), parameter
						.getDemandCurveFunction().getFunctionRepresentation()));
		Iterator it = parameter.getDemandCurveFunction().getFunctionConstants();
		String temp = "";
		while (it.hasNext()) {
			Function.FunctionConstant fc = (Function.FunctionConstant) it
					.next();
			temp += fc.getConstantName() + " = " + fc.getConstantFValue()
					+ "   ";
		}
		this.constantsLabel.setText(temp);

		if (parameter.isSocial()) {
			this.functionSocialLabel.setText("Function : "
					+ parameter.getSocialFunction().getFunctionName()
							.toLowerCase());
			this.socialTitledPanel.setBorder(BorderFactory.createTitledBorder(
					BorderFactory.createLineBorder(SystemColor.BLACK),
					parameter.getSocialFunction().getFunctionRepresentation()));
			it = parameter.getSocialFunction().getFunctionConstants();
			temp = "";
			while (it.hasNext()) {
				Function.FunctionConstant fc = (Function.FunctionConstant) it
						.next();
				temp += fc.getConstantName() + " = " + fc.getConstantFValue()
						+ "   ";
			}
			this.constantsSocialLabel.setText(temp);
		} else {
			this.functionSocialLabel.setText("");
			this.socialTitledPanel.setBorder(BorderFactory.createTitledBorder(
					BorderFactory.createLineBorder(SystemColor.BLACK), ""));
			this.constantsSocialLabel.setText("");
		}

	}

}//end of  ReviewGUI class