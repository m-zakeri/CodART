package simulator.SA.gui;

import jade.gui.GuiEvent;
import jade.wrapper.AgentController;
import jade.wrapper.ControllerException;
import jade.wrapper.StaleProxyException;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Hashtable;
import javax.swing.JDesktopPane;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;

import org.apache.log4j.Logger;

import simulator.DAWN;
import simulator.SA.SimulationAgent;
import simulator.util.Discrete;
import simulator.util.Function;
import simulator.util.Linear;
import simulator.util.MetDataFunction;
import simulator.util.Raise;
import simulator.util.Random;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class SuiteGUI extends JFrame {
	private static final long serialVersionUID = 1051723621263416876L;
    private Logger log = Logger.getLogger(SuiteGUI.class);
	
	public static final Integer BACKGROUND_LAYER = new Integer(1);

	public static final Integer TOP_LAYER = new Integer(2);

	public static final String[] pricingScenarios = {
			"Water price remains unchanged", "The real water price remains unchanged",
			 };

	private SimulationAgent myAgent;

	private ScenarioDesignWizard scenarioDesignWizard;

	private Object[] scenarioInputs = new Object[9];

	private JDesktopPane mainPanel = new JDesktopPane();

	private JMenuBar menuBar = new JMenuBar();

	private JMenu[] menus = { new JMenu("Scenarios"), new JMenu("Tools"),
			new JMenu("Help") };

	private JMenuItem[][] menuItems = {
			{ new JMenuItem("New Scenario"), new JMenuItem("Load Scenario"),
					new JMenuItem("Save Scenario"), null,
					new JMenuItem("Start Simulation"), new JMenuItem("Exit") },
			{ null/*new JMenuItem("Save Results")*/,
					new JMenuItem("Launch Jade RMA") },
			{ new JMenuItem("About DAWN...") } };

	private JMenu editMenu = new JMenu("Edit...");

	private JMenuItem[] editSubmenu = { new JMenuItem("Simulation Parameters"),
			new JMenuItem("Demand Curve Paremeters"),
			new JMenuItem("Meteorological Data File Location"),
			new JMenuItem("Pricing Policy") };

	private JMenu saveResultsMenu = new JMenu("Save results...");

	private JMenuItem[] saveResultsSubmenu = { new JMenuItem("Total results"),
			new JMenuItem("All consumers' results") };

	private Hashtable menuActions = new Hashtable();

	// TEST
	// Temporary !!!!!!!!
	private Function[] availableFunctions = new Function[7];

	private Linear linear = new Linear();

	private Random random1 = new Random();

	private Random random2 = new Random();

	private Discrete discrete = new Discrete();

	private Raise raise = new Raise();

	private MetDataFunction metData = new MetDataFunction();

	private Raise price = new Raise();

	{
		random1.setFunctionName("RANDOM-INT");
		random2.setFunctionName("RANDOM-FL");
		random2.setFloat();
		price.setFunctionName("PRICE");
		price.setFunctionRepresentation(" Y = a * [ln(price)]^n ");
		availableFunctions[0] = linear;
		availableFunctions[1] = discrete;
		availableFunctions[2] = random1;
		availableFunctions[3] = random2;
		availableFunctions[4] = raise;
		availableFunctions[5] = metData;
		availableFunctions[6] = price;

	}

	@SuppressWarnings("deprecation")
	public SuiteGUI(SimulationAgent a) {
		this.myAgent = a;
		init();
		this.setTitle("DAWN: Distributed Agent-based Water Demand Simulator");
		this.setSize(600, 500);
		this.show();
	}

	@SuppressWarnings("unchecked")
	private void init() {
		int hashTableIndex = 1;
		menuActions.put("End Wizard", new Integer(0));

		//Scenario menu
		for (int i = 0; i < menuItems[0].length; i++) {
			if (i >= 3 && i <= 5)
				menus[0].addSeparator();
			if (i == 3)
				menus[0].add(editMenu);
			else {
				menus[0].add(menuItems[0][i]);
				menuItems[0][i].addActionListener(new menuActionListener());
				//HashTable
				menuActions.put(menuItems[0][i].getActionCommand(),
						new Integer(hashTableIndex));
				hashTableIndex++;
			}
		}
		// create edit Submenu
		for (int i = 0; i < editSubmenu.length; i++) {
			editMenu.add(editSubmenu[i]);
			editSubmenu[i].addActionListener(new menuActionListener());
			//HashTable
			menuActions.put(editSubmenu[i].getActionCommand(), new Integer(
					hashTableIndex));
			hashTableIndex++;
		}

		//Disable Start Simulation button until allInputs[] is loaded (from wizard or file loading)
		menus[0].getItem(6).setEnabled(false);
		//Disable edit option until allInputs[] is loaded (from wizard or file loading)
		menus[0].getItem(4).setEnabled(false);

		//Tools menu
		for (int i = 0; i < menuItems[1].length; i++) {
			if (i == 0)
				menus[1].add(saveResultsMenu);
			else {
				menus[1].add(menuItems[1][i]);
				menuItems[1][i].addActionListener(new menuActionListener());
				//HashTable
				menuActions.put(menuItems[1][i].getActionCommand(),
						new Integer(hashTableIndex));
				hashTableIndex++;
			}
		}

		// create save results Submenu
		for (int i = 0; i < saveResultsSubmenu.length; i++) {
			saveResultsMenu.add(saveResultsSubmenu[i]);
			saveResultsSubmenu[i].addActionListener(new menuActionListener());
			//HashTable
			menuActions.put(saveResultsSubmenu[i].getActionCommand(),
					new Integer(hashTableIndex));
			hashTableIndex++;
		}

		//Help menu
		for (int i = 0; i < menuItems[2].length; i++) {
			menus[2].add(menuItems[2][i]);
			menuItems[2][i].addActionListener(new menuActionListener());
			//HashTable
			menuActions.put(menuItems[2][i].getActionCommand(), new Integer(
					hashTableIndex));
			hashTableIndex++;
		}

		for (int i = 0; i < menus.length; i++)
			menuBar.add(menus[i]);

		this.setJMenuBar(menuBar);
		this.getContentPane().add(mainPanel, null);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}

	class menuActionListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			GuiEvent ge;
			File chosenFile;
			switch (((Integer) menuActions.get(e.getActionCommand()))
					.intValue()) {
			case 0: // Wizard Ended
				scenarioInputs = scenarioDesignWizard.packedInputs();
				ge = new GuiEvent((Object) this, SimulationAgent.WIZARD_ENDED);
				for (int i = 0; i < scenarioInputs.length; i++)
					ge.addParameter(scenarioInputs[i]);
				myAgent.postGuiEvent(ge);
				//Enable start simulation option & edit option
				menus[0].getItem(6).setEnabled(true);
				menus[0].getItem(4).setEnabled(true);
				break;
			case 1: //New scenario
				// Start scenario design wizard
				scenarioDesignWizard = new ScenarioDesignWizard(
						SuiteGUI.TOP_LAYER, mainPanel, availableFunctions,
						pricingScenarios, this);
				break;
			case 2: // Load Scenario
				chosenFile = loadFile("Scenario");
				ge = new GuiEvent((Object) this, SimulationAgent.LOAD_SCENARIO);
				ge.addParameter(chosenFile);
				myAgent.postGuiEvent(ge);
				//Enable start simulation button & edit option
				if (chosenFile != null) {
					menus[0].getItem(6).setEnabled(true);
					menus[0].getItem(4).setEnabled(true);
				}
				break;
			case 3: // Save Scenario
				chosenFile = saveFile("Scenario");
				ge = new GuiEvent((Object) this, SimulationAgent.SAVE_SCENARIO);
				ge.addParameter(chosenFile);
				myAgent.postGuiEvent(ge);
				break;
			case 4: //Start Simulation
				ge = new GuiEvent((Object) this,
						SimulationAgent.START_SIMULATION_MENU);
				myAgent.postGuiEvent(ge);
				break;
			case 5: //Exit
				System.exit(0);
				break;
			case 6: // edit simulation parameters
				ge = new GuiEvent((Object) this,
						SimulationAgent.EDIT_SIMULATION_PARAMETERS);
				myAgent.postGuiEvent(ge);
				break;
			case 7: // edit demand curve parameters
				ge = new GuiEvent((Object) this,
						SimulationAgent.EDIT_DEMAND_CURVE_PARAMETERS);
				ge.addParameter(SuiteGUI.this.availableFunctions);
				myAgent.postGuiEvent(ge);
				break;
			case 8: // edit met data file
				chosenFile = loadFile("Met Data File");
				ge = new GuiEvent((Object) this,
						SimulationAgent.EDIT_METDATA_FILE);
				ge.addParameter(chosenFile);
				myAgent.postGuiEvent(ge);
				break;
			case 9: // edit pricing policy
				ge = new GuiEvent((Object) this,
						SimulationAgent.EDIT_PRICING_POLICY);
				ge.addParameter(SuiteGUI.pricingScenarios);
				myAgent.postGuiEvent(ge);
				break;
			case 10: //Launch RMA
				try {
					AgentController rma = DAWN.mainContainer
							.createNewAgent("rma", "jade.tools.rma.rma", null);
					rma.start();
				} catch (StaleProxyException spe) {
					log.error(spe.getStackTrace());
				} catch (ControllerException ce) {
					log.error(ce.getStackTrace());
				}
				break;
			case 11: //Save Results
				chosenFile = saveFile("Results");
				ge = new GuiEvent((Object) this, SimulationAgent.SAVE_RESULTS);
				ge.addParameter(chosenFile);
				myAgent.postGuiEvent(ge);
				break;
			case 12: //Save Results
				chosenFile = saveDirectory();
				ge = new GuiEvent((Object) this,
						SimulationAgent.SAVE_CONSUMERS_RESULTS);
				ge.addParameter(chosenFile);
				myAgent.postGuiEvent(ge);
				break;
			case 13: //About
				ge = new GuiEvent((Object) this,
						SimulationAgent.ABOUT);
				myAgent.postGuiEvent(ge);
				break;
			default:
				log.info(e.getActionCommand());
			}
		}
	}

	private File loadFile(String title) {

		String msg = "";
		File chosenFile;


		// instantiate file chooser
		JFileChooser chooser = new JFileChooser(System.getProperty("user.dir"));

		// file chooser properties
		chooser.setControlButtonsAreShown(true);
		chooser.setDialogType(JFileChooser.CUSTOM_DIALOG);
		chooser.setAcceptAllFileFilterUsed(true);
		chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
		chooser.setMultiSelectionEnabled(false);
		chooser.setSelectedFile(null);
		chooser.setDialogTitle("Load " + title);
		double w = (mainPanel.getBounds().getWidth() / 2) - 40;
		double h = (mainPanel.getBounds().getHeight() / 2) - 40;
		chooser.setLocation((int) w, (int) h);

		int returnValue = chooser.showDialog(mainPanel, "Load " + title);
		if (returnValue == JFileChooser.APPROVE_OPTION) {
			chosenFile = chooser.getSelectedFile();
			if (chosenFile != null) {
				JOptionPane.showMessageDialog(mainPanel,
						"Loading from this file: " + chosenFile.getPath(),
						"Load " + title, JOptionPane.INFORMATION_MESSAGE);
				return chosenFile;
			}
		} else if (returnValue == JFileChooser.CANCEL_OPTION) {
			msg = "User cancelled operation. No file was chosen.";
		} else if (returnValue == JFileChooser.ERROR_OPTION) {
			msg = "An error occured. No file was chosen.";
		} else {
			msg = "Unknown operation occured.";
		}

		JOptionPane.showMessageDialog(mainPanel, msg, "Load " + title,
				JOptionPane.INFORMATION_MESSAGE);
		return null;

	}

	private File saveFile(String title) {

		String msg = "";
		File chosenFile;

		// instantiate file chooser
		JFileChooser chooser = new JFileChooser(System.getProperty("user.dir"));

		// file chooser properties
		chooser.setControlButtonsAreShown(true);
		chooser.setDialogType(JFileChooser.SAVE_DIALOG);
		chooser.setAcceptAllFileFilterUsed(true);
		chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
		chooser.setMultiSelectionEnabled(false);
		chooser.setSelectedFile(null);
		chooser.setDialogTitle("Save " + title);
		double w = (mainPanel.getBounds().getWidth() / 2) - 40;
		double h = (mainPanel.getBounds().getHeight() / 2) - 40;
		chooser.setLocation((int) w, (int) h);

		int returnValue = chooser.showSaveDialog(mainPanel);
		if (returnValue == JFileChooser.APPROVE_OPTION) {
			chosenFile = chooser.getSelectedFile();
			if (chosenFile != null) {
				JOptionPane.showMessageDialog(mainPanel,
						"Saving in this file: " + chosenFile.getPath(), "Save "
								+ title, JOptionPane.INFORMATION_MESSAGE);
				return chosenFile;
			}
		} else if (returnValue == JFileChooser.CANCEL_OPTION) {
			msg = "User cancelled operation. No file was chosen.";
		} else if (returnValue == JFileChooser.ERROR_OPTION) {
			msg = "An error occured. No file was chosen.";
		} else {
			msg = "Unknown operation occured.";
		}

		JOptionPane.showMessageDialog(mainPanel, msg, "Save scenario",
				JOptionPane.INFORMATION_MESSAGE);
		return null;

	}// END of saveFile()

	private File saveDirectory() {

		String msg = "";
		File chosenFile;

		// instantiate file chooser
		JFileChooser chooser = new JFileChooser(System.getProperty("user.dir"));

		// file chooser properties
		chooser.setControlButtonsAreShown(true);
		chooser.setDialogType(JFileChooser.SAVE_DIALOG);
		chooser.setAcceptAllFileFilterUsed(true);
		chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		chooser.setMultiSelectionEnabled(false);
		chooser.setSelectedFile(null);
		chooser.setDialogTitle("Choose a directory to save consumers' results");
		double w = (mainPanel.getBounds().getWidth() / 2) - 40;
		double h = (mainPanel.getBounds().getHeight() / 2) - 40;
		chooser.setLocation((int) w, (int) h);

		int returnValue = chooser.showSaveDialog(mainPanel);
		if (returnValue == JFileChooser.APPROVE_OPTION) {
			chosenFile = chooser.getSelectedFile();
			if (chosenFile != null) {
				JOptionPane.showMessageDialog(mainPanel,
						"Consumers' results will be saved in : "
								+ chosenFile.getPath(), "Directory",
						JOptionPane.INFORMATION_MESSAGE);
				return chosenFile;
			}
		} else if (returnValue == JFileChooser.CANCEL_OPTION) {
			msg = "User cancelled operation. No directory was chosen.";
		} else if (returnValue == JFileChooser.ERROR_OPTION) {
			msg = "An error occured. No directory was chosen.";
		} else {
			msg = "Unknown operation occured.";
		}

		JOptionPane.showMessageDialog(mainPanel, msg,
				"Save consumers' results", JOptionPane.INFORMATION_MESSAGE);
		return null;

	}// END of saveDirectory()

	public void addToMainPanel(JInternalFrame jif, Integer layer) {
		mainPanel.add(jif, layer);
	}

	public void errorMessage(String msg) {
		JOptionPane.showMessageDialog(mainPanel, msg, "ERROR",
				JOptionPane.ERROR_MESSAGE);
	}

}// END SuiteGUI
