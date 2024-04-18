package simulator.SA.gui;


import jade.gui.GuiEvent;

import java.awt.*;
import javax.swing.*;

import org.apache.log4j.Logger;

import java.awt.event.*;

import java.util.Hashtable;

import simulator.SA.SimulationAgent;
import simulator.util.ConsumerAttributes;
import simulator.util.ConsumerType;
import de.progra.charting.*;
import de.progra.charting.model.*;
import de.progra.charting.render.*;
import de.progra.charting.swing.*;
import de.progra.charting.event.*;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ProgressGui extends JInternalFrame implements  ChartDataModelListener {
  private static final long serialVersionUID = 502015433522322368L;
  private Logger log = Logger.getLogger(ProgressGui.class);
  
  private JTabbedPane mainPanel = new JTabbedPane();
  private JPanel tab1 = new JPanel(new BorderLayout());
  private JPanel barPanel = new JPanel();
  private JPanel titlePanel = new JPanel();
  private JPanel centralPanel = new JPanel(new BorderLayout());
  private JPanel messagePanel = new JPanel(new GridLayout(1,1));
  private JPanel gridPanel = new JPanel(new GridLayout(0,1));

  private FlowLayout flowLayout1 = new FlowLayout(FlowLayout.CENTER,20,20);
  private FlowLayout flowLayout2 = new FlowLayout(FlowLayout.CENTER,20,20);

  private GridCanvas grid;

  private JTextArea messageArea = new JTextArea();
  private JScrollPane scrollMessage = new JScrollPane(messageArea);

  private JProgressBar progressBar = new JProgressBar();
  private JLabel title = new JLabel();
  private JButton startButton = new JButton();

  private ChartPanel chartPanel;
  private EditableChartDataModel chartDataModel;

  private SimulationAgent myAgent;
  @SuppressWarnings("unused")
private ConsumerAttributes[] consumers;



  //**************
  // Constructor *
  //**************

  public ProgressGui(SimulationAgent a) {
    this.myAgent = a;

    //************
    // Tab2

    gridPanel.setName("Grid");
    gridPanel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createEmptyBorder(10,10,10,10),
                                                           BorderFactory.createRaisedBevelBorder()));


    try { jbInit(); }
    catch(Exception e) { log.error(e.getStackTrace()); }

    //***********************
    // Chart Panel

    // Init some starting data
    double[][] model = {{0.0,0.1}};
    double[] columns = {0.0,1.0};
    String[] rows = {"Step Total"};
    String title = "Viewing Total Consumption";

    // Create an editable chart data model
    chartDataModel = new EditableChartDataModel(model, columns, rows);
    // Creating the Swing ChartPanel instead of DefaultChart
    chartPanel = new ChartPanel(chartDataModel, title, DefaultChart.LINEAR_X_LINEAR_Y);
    // Adding ChartRenderer as usual
    chartPanel.addChartRenderer(new LineChartRenderer(chartPanel.getCoordSystem(), chartDataModel), 1);
    // Register EventListener
    chartDataModel.addChartDataModelListener(this);


    //***************************

    this.setLocation(0,0);
    this.setSize(600,500);
    this.setClosable(true);
    this.setMaximizable(true);
    this.setIconifiable(true);
    this.setDefaultCloseOperation(JInternalFrame.DISPOSE_ON_CLOSE);
    this.getContentPane().add(mainPanel,null);
    mainPanel.add(tab1,null);
    mainPanel.add(gridPanel,null);
    mainPanel.setSelectedComponent(tab1);
    tab1.add(titlePanel, BorderLayout.NORTH);
    tab1.add(centralPanel,BorderLayout.CENTER);
    tab1.add(barPanel,BorderLayout.SOUTH);
    tab1.setFocusable(true);


    //chart panel is added to frame when the first result arrives (at updateGui method)

 }

  public void chartDataChanged(ChartDataModelEvent evt) {
      // The DataModel changed -> update display
      chartPanel.revalidate();
      repaint();
  }

  private void jbInit() throws Exception {

    //************
    // Tab1

    tab1.setName("Main");
    tab1.setBorder(BorderFactory.createEtchedBorder());

    //************
    //Bar Panel

    progressBar.setBorder(BorderFactory.createLoweredBevelBorder());
    progressBar.setPreferredSize(new Dimension(300, 25));
    progressBar.setStringPainted(true);
    startButton.setBorder(BorderFactory.createRaisedBevelBorder());
    startButton.setText("Start");
    startButton.addActionListener(new ActionListener(){
             public void actionPerformed(ActionEvent e){
                 GuiEvent ge = new GuiEvent((Object) this, SimulationAgent.START_BUTTON_GUI);
                 myAgent.postGuiEvent(ge);
                 startButton.setEnabled(false);
             }
         }); //addActionListener
    startButton.setEnabled(false);

    barPanel.setLayout(flowLayout1);
    barPanel.setBorder(BorderFactory.createEtchedBorder());
    barPanel.setPreferredSize(new Dimension(0,70));
    barPanel.add(startButton, null);
    barPanel.add(progressBar, null);


    //************
    //Title Panel

    title.setFont(new java.awt.Font("Serif", 1, 14));
    title.setBorder(BorderFactory.createRaisedBevelBorder());
    title.setPreferredSize(new Dimension(200, 30));
    title.setHorizontalAlignment(SwingConstants.CENTER);
    title.setHorizontalTextPosition(SwingConstants.LEADING);
    title.setText("Water Demand Simulator");
    titlePanel.setBorder(BorderFactory.createEtchedBorder());
    titlePanel.setPreferredSize(new Dimension(0,70));
    titlePanel.setLayout(flowLayout2);
    titlePanel.add(title, null);

    //************
    //Central Panel

    messagePanel.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createEmptyBorder(10,10,10,10),
                                                              BorderFactory.createLoweredBevelBorder()));
    messagePanel.add(scrollMessage);
    messagePanel.setPreferredSize(new Dimension(0,150));
    centralPanel.add(messagePanel,BorderLayout.SOUTH);

  }


  //***********
  // GRID
  //***********

  class GridCanvas extends Canvas implements MouseListener{

	private static final long serialVersionUID = 1664514449623126381L;

	//Internal use
    private final Color[] colors = {Color.BLUE,   Color.RED,  Color.GREEN,
                                    Color.YELLOW, Color.PINK, Color.ORANGE,
                                    Color.MAGENTA, Color.CYAN, Color.DARK_GRAY, };

    private int cellDimension = 20;
    private Hashtable typeColor = new Hashtable();
    private int x0,y0;
    private boolean[][] cellOccupied;


    //Inputs
    private int cells;
    @SuppressWarnings("unused")
	private ConsumerType[] consumerTypes;
    private ConsumerAttributes[] consumers;


    //Constructor
    @SuppressWarnings("unchecked")
	public GridCanvas(int gridDimension,ConsumerAttributes[] consumers,ConsumerType[] consumerTypes){

      this.cells = gridDimension;
      this.cellOccupied = new boolean[gridDimension+1][gridDimension+1];
      this.consumerTypes = consumerTypes;
      this.consumers = consumers;

      //Initialization
      for(int i=0;i<gridDimension;i++)
        for(int j=0;j<gridDimension;j++)
          this.cellOccupied[i][j] = false;

      try{
          for(int i=0;i<consumerTypes.length;i++)
              typeColor.put(consumerTypes[i].getName(),colors[i]);
      }
      catch(Exception e){log.error("Colors are limited... 9!!");}

      // Add Mouse Listener
      this.addMouseListener(this);

    }

    public void paint(Graphics g){

      Rectangle r = /*gridPanel.*/getBounds();

      x0 = Math.round((int)((r.width-(cells*cellDimension))/2));
      y0 = Math.round((int)((r.height-(cells*cellDimension))/2));

      g.setColor(Color.black);

      for(int i=0; i<=cells;i++){
        g.drawLine(x0,y0+(i*cellDimension),x0+(cells*cellDimension),y0+(i*cellDimension));
      }
      for(int i=0; i<=cells;i++){
        g.drawLine(x0+(i*cellDimension),y0,x0+(i*cellDimension),y0+(cells*cellDimension));
      }

      for(int i=0;i<consumers.length;i++){
        g.setColor(((Color)typeColor.get(consumers[i].getConsumerType())));
        g.fillRect(x0+1+(cellDimension*(consumers[i].getX()-1)),
                   y0+1+(cellDimension*(consumers[i].getY()-1)),19,19);
        //Map consumers position
        cellOccupied[consumers[i].getX()][consumers[i].getY()] = true;
      }

    }//END of paint()

    //MouseListener implementation
    public void mouseClicked(MouseEvent e){
      int x = ((e.getX()-x0)/cellDimension)+1;
      int y = ((e.getY()-y0)/cellDimension)+1;
      if(x>0 && x<=cells && y>0 && y<=cells){
          if(cellOccupied[x][y]){
              GuiEvent ge = new GuiEvent((Object) this, SimulationAgent.LAUNCH_CONSUMER_GUI);
              ge.addParameter("consumer_"+ x + "," + y);
              myAgent.postGuiEvent(ge);
          }
      }  else log.error("Out of range");
    }
    public void mouseReleased(MouseEvent e){}
    public void mousePressed(MouseEvent e){}
    public void mouseEntered(MouseEvent e){}
    public void mouseExited(MouseEvent e){}


  }


  /******************
   *  PUBLIC methods
   ******************/


  public void updateChart(double consumption, double step){
    if (step==1){
              centralPanel.add(chartPanel,BorderLayout.CENTER);
    }
    chartDataModel.insertValue(0, new Double(consumption), new Double(step));
  }


  public void updateBar(int v){ progressBar.setValue(v);}


  public void updateMessageArea(String message){
    this.messageArea.append(message + "\n");
    scrollMessage.getHorizontalScrollBar().setValue(100);
  }


  public void enableStartButton(boolean b){startButton.setEnabled(b); }

  public void paintGrid(int gridDimension,ConsumerAttributes[] consumers,ConsumerType[] consumerTypes){
    this.consumers = consumers;
    grid = new GridCanvas(gridDimension,consumers,consumerTypes);
    gridPanel.add(grid);
  }

}