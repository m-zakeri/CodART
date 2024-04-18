package simulator.CA.gui;


import jade.gui.GuiEvent;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Enumeration;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;
import javax.swing.table.AbstractTableModel;

import simulator.CA.ConsumerAgent;
import simulator.util.ConsumerAttributes;
import simulator.util.ParameterAttributes;
import de.progra.charting.DefaultChart;
import de.progra.charting.event.ChartDataModelEvent;
import de.progra.charting.event.ChartDataModelListener;
import de.progra.charting.model.EditableChartDataModel;
import de.progra.charting.model.ObjectChartDataModel;
import de.progra.charting.render.LineChartRenderer;
import de.progra.charting.render.PieChartRenderer;
import de.progra.charting.swing.ChartPanel;


/**
 * <p>Title: Simulator</p>
 * <p>Description: </p>
 * <p>Copyright: Copyright (c) 2003</p>
 * <p>Company: </p>
 * @author Vartalas Panagiotis
 * @version 1.0
 */

public class ConsumerGUI extends JFrame implements  ChartDataModelListener, TableModelListener{

	private static final long serialVersionUID = -8962775059023388498L;
	private ConsumerAgent myAgent;
    private JMenuBar menuBar = new JMenuBar();
    private JMenu[] menu = {new JMenu("File")};
    private JMenuItem[] items = {new JMenuItem("Save results"),new JMenuItem("Exit")};

    private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setSize(new Dimension(650,500));
              this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

      }

    private JTabbedPane panel = new JTabbedPane();
    private JPanel consumptionPanel = new JPanel(new BorderLayout());
    private JPanel neighboursPanel = new JPanel(new BorderLayout());
    private JPanel socialParametersPanel = new JPanel(new BorderLayout());
    {
      consumptionPanel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLoweredBevelBorder(),
                                                            BorderFactory.createEmptyBorder(30,30,30,30)));
      neighboursPanel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLoweredBevelBorder(),
                                                            BorderFactory.createEmptyBorder(30,30,30,30)));
      socialParametersPanel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLoweredBevelBorder(),
                                                            BorderFactory.createEmptyBorder(30,30,30,30)));
    }

    // Consumption Panel components
    //*****************************

      // Create an editable chart data model
    private EditableChartDataModel chartDataModel;
      // Creating the Swing ChartPanel instead of DefaultChart
    private ChartPanel chartPanel;


    // Neighbouhood Panel components
    //******************************

    private String[] columnsNamesN = {"Neighbour Name","Consumer Type"};
    private JTable neighsTable = new JTable();
    private JScrollPane scroll2 = new JScrollPane(neighsTable);
    private TableDataModel neighsTableDataModel;

      // Create data model
    private ObjectChartDataModel pieChartDataModel;
      // Creating the Swing ChartPanel instead of DefaultChart
    private ChartPanel pieChartPanel;



    // Socialization Panel components
    //*******************************
    private String[] columnsNamesS;// = {"Step No","Parameter 1","Parameter 2","Parameter 3"};
    private JTable socialTable = new JTable();
    private JScrollPane scroll3 = new JScrollPane(socialTable);
    private TableDataModel socialTableDataModel;



    //Constructor
    @SuppressWarnings({"unchecked","deprecation"})
	public ConsumerGUI(ConsumerAgent a,Vector consumptions, ConsumerAttributes[] myNeighbours,
                                                                ParameterAttributes[] socialParameters,
                                                                Object[] socialParametersWeightsPerStep){

      this.myAgent = a;

      //Menu
      this.menu[0].add(items[0]);
      this.menu[0].addSeparator();
      this.menu[0].add(items[1]);
      menuBar.add(menu[0]);
      this.setJMenuBar(menuBar);
      items[0].addActionListener(new menuActionListener());
      items[1].addActionListener(new menuActionListener());

      //Consumption Panel
      //*****************

      // Init some starting data
      double[][] chartModel = {{0.0,0.1}};
      double[] chartColumns = {0.0,1.0};
      String[] chartRows = {"Consumption"};
      String chartTitle = "Viewing " + myAgent.getLocalName()+ " Consumption";
      chartDataModel = new EditableChartDataModel(chartModel,chartColumns,chartRows);
      chartPanel = new ChartPanel(chartDataModel,chartTitle, DefaultChart.LINEAR_X_LINEAR_Y);
        // Adding ChartRenderer as usual
      chartPanel.addChartRenderer(new LineChartRenderer(chartPanel.getCoordSystem(), chartDataModel), 1);
        // Register EventListener
      chartDataModel.addChartDataModelListener(this);

      //Update data model with new consumtpions
      for(int i = 0; i<consumptions.size() ; i++){
        chartDataModel.insertValue(0, new Double(((Float)consumptions.elementAt(i)).doubleValue()),
                                                                                           new Double(i));
      }


      //Neighbours Panel
      //****************

      if(myNeighbours.length != 0 ){
          // Define model for neighboursTable
        neighsTableDataModel = new TableDataModel(columnsNamesN,myNeighbours.length);
        neighsTable.setModel(neighsTableDataModel);

          // Fill in neighbours
        Vector consumerTypes = new Vector(0);
        neighsTable.setValueAt(myNeighbours[0].getName(),0,0);
        neighsTable.setValueAt(myNeighbours[0].getConsumerType(),0,1);
        consumerTypes.addElement(myNeighbours[0].getConsumerType());

        for(int i=1; i<myNeighbours.length;i++){
            neighsTable.setValueAt(myNeighbours[i].getName(),i,0);
            neighsTable.setValueAt(myNeighbours[i].getConsumerType(),i,1);
            //Count consumer types in my neighbourhood
            Enumeration e = consumerTypes.elements();
            boolean contains = false;
            while(e.hasMoreElements() && !contains){
              if (myNeighbours[i].getConsumerType().equals((String)e.nextElement())){
                contains = true;
              }
              else if (!e.hasMoreElements())
                consumerTypes.addElement(myNeighbours[i].getConsumerType());
            }
        }//END for

        int[][] pieModel = new int [consumerTypes.size()][1];     // Create data array

        String[] pieColumns = {"1"};  // Create x-axis values

        String[] pieRows = new String[consumerTypes.size()];   // Create data set title
        consumerTypes.copyInto(pieRows);

        String pieTitle = "Consumer Types Distribution in my Neighbourhood";  // Create diagram title

        //Fill in model (count neighbours of each consumer type)
        for(int j=0 ; j<myNeighbours.length ; j++){
            int i=0;
            boolean counted = false;
            while( (i<consumerTypes.size()) && !counted ){
               if (myNeighbours[j].getConsumerType().equals(pieRows[i])){
                          pieModel[i][0]++;
                          counted = true;
               }
               else
                      i++;
            }// END while
        }//END j-loop

        //rows: consumer type + percentage
        for(int i=0;i<consumerTypes.size();i++){
            float percentage = (pieModel[i][0]*100)/myNeighbours.length;
            pieRows[i] = ((String)consumerTypes.elementAt(i)) + " : " + percentage + "%";
        }


        pieChartDataModel = new ObjectChartDataModel(pieModel, pieColumns, pieRows);

          // Create chart with default coordinate system
        pieChartPanel = new ChartPanel(pieChartDataModel, pieTitle);

          // Add a line chart renderer
        pieChartPanel.addChartRenderer(new PieChartRenderer(pieChartDataModel),1);
        //pieChartPanel.setBorder(BorderFactory.createEtchedBorder());

      }//END if-neighbours!=0




      //SocializationTab
      //****************
       if (socialParameters.length!= 0){
          // Define model for socialTable
          columnsNamesS = new String[socialParameters.length+1];
          columnsNamesS[0] = "Step No";
          for(int i=1;i<columnsNamesS.length;i++)
            columnsNamesS[i] = socialParameters[i-1].getName();

          socialTableDataModel = new TableDataModel(columnsNamesS,
                                  ((Vector)socialParametersWeightsPerStep[socialParameters.length-1]).size());
          socialTableDataModel.addTableModelListener(this);
          socialTable.setModel(socialTableDataModel);


          // Fill in social parametrs

          for(int i=0; i<((Vector)socialParametersWeightsPerStep[0]).size() ;i++){
             socialTable.setValueAt(new Integer(i+1),i,0);
             for(int j=1 ; j< columnsNamesS.length ; j++)
               socialTable.setValueAt(((Vector)socialParametersWeightsPerStep[j-1]).elementAt(i),i,j);

          }
      }

      contentPane.add(panel);
      panel.addTab("Consumption",consumptionPanel);
      consumptionPanel.add(chartPanel,BorderLayout.CENTER);
      panel.addTab("Neighbourhood",neighboursPanel);
      scroll2.setPreferredSize(new Dimension(0,200) );
      neighboursPanel.add(scroll2,BorderLayout.NORTH);
      if (myNeighbours.length != 0){
               neighboursPanel.setPreferredSize(new Dimension(this.getWidth(),250));
               neighboursPanel.add(pieChartPanel,BorderLayout.CENTER);
      }
      panel.addTab("Socializition",socialParametersPanel);
      socialParametersPanel.add(scroll3,BorderLayout.CENTER);

      this.setTitle("Water Demand Simulator - " + myAgent.getLocalName() + "  Status");
      this.setLocation(50,50);
      this.show();

    }// END of constructor



    /*******************************************
     * tableDataModel
     * <p>Title: Simulator</p>
     * <p>Description: </p>
     * <p>Copyright: Copyright (c) 2003</p>
     * <p>Company: </p>
     * @author Vartalas Panagiotis
     * @version 1.0
     */

    private class TableDataModel extends AbstractTableModel{

		private static final long serialVersionUID = -7463336493241742489L;
		private String[] columnsNames;
        private Object[] data;

        public TableDataModel(String[] colNames,int rowsCount){
            columnsNames = colNames;
            data = new Object[columnsNames.length];
            for(int i=0; i < columnsNames.length ; i++)
              data[i] = new Vector(0,1);
        }

        public int getRowCount() {return ((Vector)data[columnsNames.length-1]).size();}
        public int getColumnCount() {return columnsNames.length;}
        public String getColumnName(int col) { return columnsNames[col];}
        public Object getValueAt(int row, int column){ return ((Vector)data[column]).elementAt(row);}
        @SuppressWarnings("unchecked")
		public void setValueAt(Object value,int row,int column){
          ((Vector)data[column]).addElement(value);
          this.fireTableDataChanged();
        }
        public boolean isCellEditable(int row,int column){return false;}

        //Used only for socialTable
        @SuppressWarnings("unchecked")
		public void addValueAtColumn(Object value,int step, int column){
          if(column !=1)
            ((Vector)data[column]).addElement(value);
          else{
              ((Vector)data[0]).addElement(new Integer(step));
              ((Vector)data[1]).addElement(value);
          }
          this.fireTableDataChanged();
        }

    }// END of model


    /**
     * Implementation of ChartDataModelListener
     * @param evt
     */

    public void chartDataChanged(ChartDataModelEvent evt) {
      // The DataModel changed -> update display
      chartPanel.revalidate();
      repaint();
    }

    public void tableChanged(TableModelEvent e){
      socialTable.revalidate();
      repaint();
    }

    public void updateChart(double consumption, double step){
      chartDataModel.insertValue(0, new Double(consumption), new Double(step));
    }

    public void updateSocialTable(float value, int step, int column){
      socialTableDataModel.addValueAtColumn(new Float(value),step,column+1);
    }

    class menuActionListener implements ActionListener{
        @SuppressWarnings("deprecation")
		public void actionPerformed(ActionEvent e){
           GuiEvent ge;

           if (e.getActionCommand() == "Save results") {
              // Save Scenario
              ge = new GuiEvent((Object) this, ConsumerAgent.SAVE_RESULTS);
              ge.addParameter(saveFile());
              myAgent.postGuiEvent(ge);
           }
           else ConsumerGUI.this.hide();

        }
    }// End of menuActionListener

    private File saveFile(){

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
        chooser.setDialogTitle("Save Results");
        double w = (contentPane.getBounds().getWidth()/2)-40;
        double h = (contentPane.getBounds().getHeight()/2)-40;
        chooser.setLocation((int)w,(int)h);

        int returnValue = chooser.showSaveDialog(contentPane);
	if (returnValue == JFileChooser.APPROVE_OPTION) {
	         chosenFile = chooser.getSelectedFile();
		    if (chosenFile != null) {
		        JOptionPane.showMessageDialog(contentPane,"Saving in this directory : " + chosenFile.getPath()
                                                          ,"Save ",JOptionPane.INFORMATION_MESSAGE);
                        return chosenFile;
	            }
        } else if (returnValue == JFileChooser.CANCEL_OPTION) {
	         msg = "User cancelled operation. No directory was chosen.";
	    } else if (returnValue == JFileChooser.ERROR_OPTION) {
	         msg = "An error occured. No directory was chosen.";
	        } else {
	                 msg =  "Unknown operation occured.";
	                }

        JOptionPane.showMessageDialog(contentPane,msg,"Save scenario",JOptionPane.INFORMATION_MESSAGE);
        return null;


  }

}// END of GUI