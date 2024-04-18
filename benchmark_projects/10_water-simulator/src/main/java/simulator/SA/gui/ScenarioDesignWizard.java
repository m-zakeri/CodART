package simulator.SA.gui;



import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.SystemColor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JDesktopPane;
import javax.swing.JFileChooser;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.ListCellRenderer;
import javax.swing.SwingConstants;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.TableModel;

import org.apache.log4j.Logger;

import simulator.util.ConsumerType;
import simulator.util.Function;
import simulator.util.ParameterAttributes;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ScenarioDesignWizard {

  private Logger log = Logger.getLogger(ScenarioDesignWizard.class);
	private JDesktopPane mainPanel;
  private Integer layer;
  private ActionListener suite;
  private Function[] availableFunctions;
  private String[] availablePricingScenarios;

  private Integer[] simulationParameters = new Integer[5];

  // Parameters list
  // Filled  with Parameter objects (local use)
  // Store name,ln,social
  private Parameter[] demandCurveParameters;

  // Filled  with ConsumerType objects (util)
  private Vector consumerTypes = new Vector(0);

  // All parameters for each consumer type
  private Vector consumerTypeParameters = new Vector(0,1);

  // local use step2 - step4
  private Boolean launchMOA = new Boolean(false);

  //Left side of demand curve (step2)
  private Boolean consumptionLn;

  private File metDataFile = new File("");

  private Vector priceData = new Vector(0,1);
  private Vector distributionData = new Vector(0,1);


  private JInternalFrame step1;
  private JInternalFrame step2;
  private JInternalFrame step3;
  @SuppressWarnings("unused") private JInternalFrame step4;
  private JInternalFrame step5;
  private JInternalFrame step6;


  //Constructor
  public ScenarioDesignWizard(Integer layer,JDesktopPane mainPanel,Function[] availableFunctions,
                                                String[] availablePricingScenarios,ActionListener suite){

      this.mainPanel = mainPanel;
      this.layer = layer;
      this.availableFunctions = availableFunctions;
      this.availablePricingScenarios = availablePricingScenarios;
      this.suite = suite;

      step1 = new Step1Frame();
      step2 = new Step2Frame();

      // first step start
      step1.setLocation(50,50);
      step1.show();
  }



  /****************************************************************************
   *                              STEP 1
   ****************************************************************************/

  private class Step1Frame extends JInternalFrame{

	private static final long serialVersionUID = 8034923647921247581L;
	private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(400, 350));
              this.setTitle("STEP 1/6 - Scenario Design Wizard");
      }

      //*******************************************************
      // DATA PANEL

      private JPanel dataPanel = new JPanel(new GridLayout(0,1,5,5));
      {
        contentPane.add(dataPanel,  BorderLayout.CENTER);
      }

      //*******************************************************

      private JPanel panel1 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,5));
      {
        dataPanel.add(panel1,null);
      }
            private JLabel label1 = new JLabel("Grid Dimension  :");
            {
              label1.setFont(new java.awt.Font("Dialog", 1, 12));
              label1.setBorder(BorderFactory.createEtchedBorder());
              label1.setPreferredSize(new Dimension(150, 17));
              label1.setHorizontalAlignment(SwingConstants.CENTER);
              label1.setHorizontalTextPosition(SwingConstants.CENTER);
              panel1.add(label1,null);
            }
            private JTextField textField1 = new JTextField(10);
            {
              textField1.setBorder(BorderFactory.createLoweredBevelBorder());
              panel1.add(textField1,null);
            }

      private JPanel panel2 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,5));
      {
        dataPanel.add(panel2,null);
      }
            private JLabel label2 = new JLabel("Sight Limit  :");
            {
              label2.setFont(new java.awt.Font("Dialog", 1, 12));
              label2.setBorder(BorderFactory.createEtchedBorder());
              label2.setPreferredSize(new Dimension(150, 17));
              label2.setHorizontalAlignment(SwingConstants.CENTER);
              label2.setHorizontalTextPosition(SwingConstants.CENTER);
              panel2.add(label2,null);
            }
            private JTextField textField2 = new JTextField(10);
            {
              textField2.setBorder(BorderFactory.createLoweredBevelBorder());
              panel2.add(textField2,null);
            }

      private JPanel panel3 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,5));
      {
        dataPanel.add(panel3,null);
      }
            private JLabel label3 = new JLabel("Consumers Population :");
            {
              label3.setFont(new java.awt.Font("Dialog", 1, 12));
              label3.setBorder(BorderFactory.createEtchedBorder());
              label3.setPreferredSize(new Dimension(150, 17));
              label3.setHorizontalAlignment(SwingConstants.CENTER);
              label3.setHorizontalTextPosition(SwingConstants.CENTER);
              panel3.add(label3,null);
            }
            private JTextField textField3 = new JTextField(10);
            {
              textField3.setBorder(BorderFactory.createLoweredBevelBorder());
              panel3.add(textField3,null);
            }

      private JPanel panel4 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,5));
      {
        dataPanel.add(panel4,null);
      }
            private JLabel label4 = new JLabel("Duration :");
            {
              label4.setFont(new java.awt.Font("Dialog", 1, 12));
              label4.setBorder(BorderFactory.createEtchedBorder());
              label4.setPreferredSize(new Dimension(80, 17));
              label4.setHorizontalAlignment(SwingConstants.CENTER);
              label4.setHorizontalTextPosition(SwingConstants.CENTER);
              panel4.add(label4,null);
            }
            private JTextField textField4 = new JTextField(5);
            {
              textField4.setBorder(BorderFactory.createLoweredBevelBorder());
              panel4.add(textField4,null);
            }
            private JLabel label5 = new JLabel("year(s)");
            {
              label5.setFont(new java.awt.Font("Dialog", 1, 12));
              label5.setHorizontalAlignment(SwingConstants.CENTER);
              label5.setHorizontalTextPosition(SwingConstants.CENTER);
              panel4.add(label5,null);
            }
            private JTextField textField5 = new JTextField(5);
            {
              textField5.setBorder(BorderFactory.createLoweredBevelBorder());
              textField5.setText("0");
              panel4.add(textField5,null);
            }
            private JLabel label6 = new JLabel("month(s)");
            {
              label6.setFont(new java.awt.Font("Dialog", 1, 12));
              label6.setHorizontalAlignment(SwingConstants.CENTER);
              label6.setHorizontalTextPosition(SwingConstants.CENTER);
              panel4.add(label6,null);
            }


      private JPanel panel5 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,5));
      {
        dataPanel.add(panel5,null);
      }
            private JLabel label7 = new JLabel("Time Step :");
            {
              label7.setFont(new java.awt.Font("Dialog", 1, 12));
              label7.setBorder(BorderFactory.createEtchedBorder());
              label7.setPreferredSize(new Dimension(80, 17));
              label7.setHorizontalAlignment(SwingConstants.CENTER);
              label7.setHorizontalTextPosition(SwingConstants.CENTER);
              panel5.add(label7,null);
            }
            private JTextField textField6 = new JTextField(5);
            {
              textField6.setBorder(BorderFactory.createLoweredBevelBorder());
              panel5.add(textField6,null);
            }
            private JLabel label8 = new JLabel("month(s)");
            {
              label8.setFont(new java.awt.Font("Dialog", 1, 12));
              label8.setHorizontalAlignment(SwingConstants.CENTER);
              label8.setHorizontalTextPosition(SwingConstants.CENTER);
              panel5.add(label8,null);
            }

      //***************************END of Data Panel****************************



      //*******************************************************
      // NAVIGATION PANEL

      private JPanel navigationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,30,10));
      {
        navigationPanel.setBorder(BorderFactory.createEtchedBorder());
        navigationPanel.setPreferredSize(new Dimension(0,40));
        contentPane.add(navigationPanel,  BorderLayout.SOUTH);
      }

      //*******************************************************

      private JButton cancelButton = new JButton("     Cancel    ");
      {
        cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(cancelButton,null);
        cancelButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){
                  try{Step1Frame.this.setClosed(true);}
                  catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.setEnabled(false);
      } // END previousButton

      private JButton nextButton = new JButton("    Next >>    ");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);
        nextButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if (checkConstraints()) {
                    saveInputs();
                    step1.setVisible(false);
                    step2.setLocation(50,50);
                    step2.setVisible(true);
                }
            }
        });
      } // END nextButton

      //***************************END of Navigation Panel**********************

      private boolean checkConstraints(){
          boolean t=false;
          String warnings = "";


          try{
            Integer gridSize = new Integer(textField1.getText());
            Integer sightLimit = new Integer(textField2.getText());
            Integer population = new Integer(textField3.getText());
            Integer durYears = new Integer(textField4.getText());
            Integer durMonths = new Integer(textField5.getText());
            Integer step = new Integer(textField6.getText());
            // Errors
            if (population.intValue() > (gridSize.intValue()*gridSize.intValue())){
              JOptionPane.showMessageDialog(this,"Grid is too small for this population !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
              t=false;
            }
            else if (step.intValue() == 0) {
                    JOptionPane.showMessageDialog(this,"Step time can't be zero !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
                    t=false;
                 }
                 else{    // No fatal errors
                          t = true;

                          // WARNINGS
                          if ( sightLimit.intValue() > gridSize.intValue()){
                            warnings = "Sight Limit is larger than Grid Size !!!";
                            textField2.setText(gridSize.toString());
                          }
                          if ( population.intValue() == 0 )
                            warnings += "\nConsumers population is zero !!!";
                          if ( durYears.intValue()==0 && durMonths.intValue()==0)
                            warnings += "\nDuration is zero !!!";

                          if (!warnings.equals(""))
                            t=(JOptionPane.showConfirmDialog(this,warnings + "\nContinue anyway?","Warning",JOptionPane.YES_NO_OPTION)==JOptionPane.YES_OPTION)
                                  ?true:false;
                      }

          }
          catch (NumberFormatException nfe){
            JOptionPane.showMessageDialog(this,"Fill in ALL fields with INTEGERs !!!","Error",
                                                                               JOptionPane.ERROR_MESSAGE);
            t=false;
          }

          return t;
      }


      private void saveInputs(){
        simulationParameters[0] = new Integer(textField1.getText());
        simulationParameters[1] = new Integer(textField2.getText());
        simulationParameters[2] = new Integer(textField3.getText());
        simulationParameters[3] = new Integer( ( (Integer.parseInt(textField4.getText())*12) +
                                                                      Integer.parseInt(textField5.getText()) )
                                              / Integer.parseInt(textField6.getText())
                                              );
        simulationParameters[4] = new Integer(Integer.parseInt(textField6.getText()));
      }

      Step1Frame(){ mainPanel.add(this,layer);}

  }// END of Step1Frame



   /****************************************************************************
   *                              STEP 2
   ****************************************************************************/

  private class Step2Frame extends JInternalFrame{

	private static final long serialVersionUID = -2574807796499095054L;
	private boolean parametersListChanged = true;


      // Constructor
      Step2Frame(){ mainPanel.add(this,layer);}

      private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(500, 380));
              this.setTitle("STEP 2/6 - Scenario Design Wizard");
      }

      //*******************************************************
      // INPUT PANEL

      private JPanel inputPanel = new JPanel(new GridLayout(2,1,0,0));
      {
        inputPanel.setBorder(BorderFactory.createEtchedBorder());
        inputPanel.setPreferredSize(new Dimension(0,80));
        contentPane.add(inputPanel,  BorderLayout.NORTH);
      }

      //*******************************************************

      private JPanel upperPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,10,0));
      {
        upperPanel.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));
        inputPanel.add(upperPanel, null);
      }

      private JLabel labelCon = new JLabel("Consumption");
            {
              labelCon.setFont(new java.awt.Font("Dialog", 1, 12));
              labelCon.setBorder(BorderFactory.createEtchedBorder());
              labelCon.setHorizontalAlignment(SwingConstants.CENTER);
              labelCon.setHorizontalTextPosition(SwingConstants.CENTER);
              upperPanel.add(labelCon,null);
            }
      private JCheckBox boxConsumptionLN = new JCheckBox("Log");
            {
              upperPanel.add(boxConsumptionLN,null);
            }

      private JPanel lowerPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,10,0));
      {
        lowerPanel.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));
        inputPanel.add(lowerPanel, null);
      }

      private JLabel label = new JLabel("Parameter Name :");
            {
              label.setFont(new java.awt.Font("Dialog", 1, 12));
              label.setBorder(BorderFactory.createEtchedBorder());
              label.setHorizontalAlignment(SwingConstants.CENTER);
              label.setHorizontalTextPosition(SwingConstants.CENTER);
              lowerPanel.add(label,null);
            }
      private JTextField textField = new JTextField(12);
            {
              textField.setBorder(BorderFactory.createLoweredBevelBorder());
              lowerPanel.add(textField,null);
            }
      private JCheckBox box1 = new JCheckBox("Log");
            {
              lowerPanel.add(box1,null);
            }
      private JCheckBox box2 = new JCheckBox("Social");
            {
              lowerPanel.add(box2,null);
            }
//***************************END of input panel*********************************


      //*******************************************************
      // Control PANEL

      private JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,5,40));
      {
        controlPanel.setBorder(BorderFactory.createEtchedBorder());
        controlPanel.setPreferredSize(new Dimension(120,0));
        contentPane.add(controlPanel,  BorderLayout.EAST);
      }

      //*******************************************************

      private JButton addButton = new JButton("     Add...      ");
      {
        addButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(addButton,null);
        addButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){

                 textField.setEnabled(true);
                 box2.setEnabled(true);

                // add to model (Default model list)
                if(!textField.getText().equals("")){
                   if(checkModel(textField.getText()))
                      model.addElement(new Parameter(textField.getText(),
                                                     new Boolean(box1.isSelected()),
                                                     new Boolean(box2.isSelected())
                                                    )
                                      );
                   else{
                      JOptionPane.showMessageDialog(Step2Frame.this,"A Parameter with this name already exists !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
                   }
                }
                textField.setText("");
                box1.setSelected(false);
                box2.setSelected(false);

                parametersListChanged = true;

              } // actionPerformed
        });


      } // END addButton

      private boolean checkModel(String parameterName){
             boolean result = true;
             Enumeration e = model.elements();
             while(e.hasMoreElements() && result){
                Parameter p = (Parameter) e.nextElement();
                if (p.getName().equals(parameterName))
                        result = false;
             }
             return result;
      }

      private JButton editButton = new JButton("     Edit...     ");
      {
        editButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(editButton);
        editButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
              if(list.getSelectedIndex() != -1){
                Parameter p = (Parameter) model.elementAt(list.getSelectedIndex());
                if(p.getName().equals("TEMPERATURE") || p.getName().equals("RAINFALL")){
                  textField.setText(p.getName());
                  textField.setEnabled(false);
                  box1.setSelected(p.getLn().booleanValue());
                  box2.setSelected(false);
                  box2.setEnabled(false);
                  model.removeElementAt(list.getSelectedIndex());
                }
                else{
                    textField.setText(p.getName());
                    box1.setSelected(p.getLn().booleanValue());
                    box2.setSelected(p.getSocial().booleanValue());
                    model.removeElementAt(list.getSelectedIndex());
                }

                parametersListChanged = true;

              }
            }
        });
      } // END editButton

      private JButton removeButton = new JButton("   Remove   ");
      {
        removeButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(removeButton);
        removeButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
               if(list.getSelectedIndex() != -1){
                 Parameter p = (Parameter) model.elementAt(list.getSelectedIndex());
                 if(p.getName().equals("TEMPERATURE") || p.getName().equals("RAINFALL")){
                   if(JOptionPane.showConfirmDialog(Step2Frame.this,p.getName() + " will be removed from Parameters List. Are U sure?"
                                          ,"Confirm",JOptionPane.YES_NO_OPTION) == JOptionPane.YES_OPTION){
                        model.removeElementAt(list.getSelectedIndex());
                        parametersListChanged =true;
                   }
                 }
                 else{
                    model.removeElementAt(list.getSelectedIndex());
                    parametersListChanged = true;
                 }
               }

            }
        });
      } // END remove Button

      //***************************END of Control Panel**********************




      //*******************************************************
      // LIST PANEL

      private JPanel listPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,10,10));
      {
        listPanel.setBorder(BorderFactory.createEtchedBorder());

        contentPane.add(listPanel,  BorderLayout.CENTER);
      }

      //*******************************************************

      private DefaultListModel model = new DefaultListModel();
      private JList list = new JList(model);
      {
        list.setCellRenderer(new ListRenderer());
        model.addElement(new Parameter("TEMPERATURE",new Boolean(false), new Boolean(false) ));
        model.addElement(new Parameter("RAINFALL",new Boolean(false), new Boolean(false) ));
      }
      private JScrollPane scroll = new JScrollPane(list);
      {
        scroll.setPreferredSize(new Dimension(300,200));
        listPanel.add(scroll,null);
      }

      //***************************END of List Panel**********************


      //*******************************************************
      // NAVIGATION PANEL

      private JPanel navigationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,30,10));
      {
        navigationPanel.setBorder(BorderFactory.createEtchedBorder());
        navigationPanel.setPreferredSize(new Dimension(0,40));
        contentPane.add(navigationPanel,  BorderLayout.SOUTH);
      }

      //*******************************************************

      private JButton cancelButton = new JButton("    Cancel    ");
      {

        cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(cancelButton,null);
        cancelButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){
                  try{Step2Frame.this.setClosed(true);}
                  catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                step2.setVisible(false);
                step1.setVisible(true);
            }
        });
      } // END previousButton

      private JButton nextButton = new JButton("    Next >>    ");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);
        nextButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
              if(model.size()!=0){
                step2.setVisible(false);

                // define size
                demandCurveParameters = new Parameter[model.size()];   // Store name,ln,social


            //******************************* save data *******************
                Enumeration e = model.elements();
                int i = 0;
                while (e.hasMoreElements()){
                    Parameter p = new Parameter();
                    p = (Parameter) e.nextElement();
                    demandCurveParameters[i] = p;
                    i++;
                }

                ScenarioDesignWizard.this.consumptionLn =
                                                new Boolean(Step2Frame.this.boxConsumptionLN.isSelected());
                // Next Step
                if (parametersListChanged) {
                      // for step3
                      step3 = new Step3Frame();
                      consumerTypes.removeAllElements();
                      consumerTypeParameters.removeAllElements();
                      parametersListChanged = false;
                }

                step3.setLocation(50,50);
                step3.setVisible(true);
              }
              else{
                   JOptionPane.showMessageDialog(Step2Frame.this,"NO Parameters defined !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
              }
            }
        });
      } // END nextButton

      //***************************END of Navigation Panel**********************

      // RENDER
      class ListRenderer implements ListCellRenderer{
          @SuppressWarnings("unused")
		private boolean focused = false;

          private JPanel panel;
          private JLabel label;
          private JCheckBox box1,box2;

          public ListRenderer(){
            panel = new JPanel(new GridLayout(1,3,0,0));
            label = new JLabel();
            box1 = new JCheckBox("Log");
            box1.setPreferredSize(new Dimension(50,25));
            box2 = new JCheckBox("Social");

            label.setOpaque(true);
            box1.setOpaque(true);
            box2.setOpaque(true);

            panel.add(label,null);
            panel.add(box1,null);
            panel.add(box2,null);

          }

          public Component getListCellRendererComponent(JList list, Object value, int index,boolean isSelected, boolean cellHasFocus){
              if (value == null){
                  label.setText("");
              }
              else{
                    Parameter p = new Parameter();
                    p = (Parameter) value;
                    label.setText(p.getName());
                    box1.setSelected(p.getLn().booleanValue());
                    box2.setSelected(p.getSocial().booleanValue());
              }// else
              label.setBackground(isSelected?SystemColor.textHighlight:SystemColor.text);
              label.setForeground(isSelected?SystemColor.textHighlightText:SystemColor.textText);
              box2.setBackground(isSelected?SystemColor.textHighlight:SystemColor.text);
              box2.setForeground(isSelected?SystemColor.textHighlightText:SystemColor.textText);
              return panel;
          }

      }// End of class



  }// END of Step2Frame




   /****************************************************************************
   *                              STEP 3
   ****************************************************************************/

  private class Step3Frame extends JInternalFrame{


	private static final long serialVersionUID = 8381154358245864832L;

	// Constructor
      Step3Frame(){ mainPanel.add(this,layer);}

      private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(400, 350));
              this.setTitle("STEP 3/6 - Scenario Design Wizard");
      }

      //*******************************************************
      // INPUT PANEL

      private JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,10,10));
      {
        inputPanel.setBorder(BorderFactory.createEtchedBorder());
        inputPanel.setPreferredSize(new Dimension(0,80));
        contentPane.add(inputPanel,  BorderLayout.NORTH);
      }

      //*******************************************************

      private JLabel label = new JLabel("Consumer Type Name :");
            {
              label.setFont(new java.awt.Font("Dialog", 1, 12));
              label.setBorder(BorderFactory.createEtchedBorder());
              label.setHorizontalAlignment(SwingConstants.CENTER);
              label.setHorizontalTextPosition(SwingConstants.CENTER);
              inputPanel.add(label,null);
            }
      private JTextField textField = new JTextField(15);
            {
              textField.setBorder(BorderFactory.createLoweredBevelBorder());
              inputPanel.add(textField,null);
            }
      private JLabel label1 = new JLabel("Percentage :");
            {
              label1.setFont(new java.awt.Font("Dialog", 1, 12));
              label1.setBorder(BorderFactory.createEtchedBorder());
              label1.setHorizontalAlignment(SwingConstants.CENTER);
              label1.setHorizontalTextPosition(SwingConstants.CENTER);
              inputPanel.add(label1,null);
            }
      private JTextField textField1 = new JTextField(5);
            {
              textField1.setBorder(BorderFactory.createLoweredBevelBorder());
              inputPanel.add(textField1,null);
            }

//***************************END of input panel*********************************


      //*******************************************************
      // Control PANEL

      private JPanel controlPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,5,30));
      {
        controlPanel.setBorder(BorderFactory.createEtchedBorder());
        controlPanel.setPreferredSize(new Dimension(120,0));
        contentPane.add(controlPanel,  BorderLayout.EAST);
      }

      //*******************************************************

      private JButton newButton = new JButton("     New...     ");
      {
        newButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(newButton,null);
        newButton.addActionListener(new ActionListener(){
              @SuppressWarnings("unchecked")
			public void actionPerformed(ActionEvent ev){
                try{
                    if(!textField.getText().equals("")){
                      float f = (new Float(textField1.getText())).floatValue();
                      if( f<=100 && f>0 ){
                        // update model
                        ConsumerType ct = new ConsumerType(textField.getText(),new Float(textField1.getText()));
                        model.addElement(ct);
                        consumerTypes.addElement(ct);
                        step3.setVisible(false);

                        // step 3.1
                        JInternalFrame step3_1 = new Step3_1Frame(ct.getName());
                        step3_1.setLocation(50,50);
                        step3_1.setVisible(true);
                        textField.setText("");
                        textField1.setText("");
                      }
                      else{
                        JOptionPane.showMessageDialog(Step3Frame.this,"Percentage MUST be between 0 and 100 !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
                      }
                    }
                }
                catch (NumberFormatException nfe){
                  JOptionPane.showMessageDialog(Step3Frame.this,"FILL in Percentage field with a FLOAT NUMBER !!!","Error",
                                                                                JOptionPane.ERROR_MESSAGE);
                }
              } // actionPerformed
        });
      } // END addButton

      private JButton editButton = new JButton("     Edit...     ");
      {
        editButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(editButton);
        editButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
               JOptionPane.showMessageDialog(Step3Frame.this,"Under Construction","Info",JOptionPane.NO_OPTION);

               // TEST                                    <--------------------------------------
                for(int i = 0; i<demandCurveParameters.length ; i++){
                    Parameter p = demandCurveParameters[i];
                    log.info(p.getName()+ " " + p.getLn() + " " + p.getSocial());
                }

                log.info(" Consumer Types : ");
                int blockStart = 0;
                for(int j = 0; j<consumerTypes.size() ; j++){
                  ConsumerType ct = (ConsumerType) consumerTypes.elementAt(j);
                  log.info(ct.getName() + " : " + ct.getPercentage());
                  for(int i=0; i<demandCurveParameters.length;i++){
                     ParameterAttributes pa = (ParameterAttributes) consumerTypeParameters.elementAt(blockStart+i);
                     log.info(pa.getName()+ " " + pa.getLn() + "  " + pa.isSocial() + "  " +
                                           "  " + pa.getElasticity() + "  "
                                           + pa.getDemandCurveFunction().getFunctionRepresentation()+ "  ");
                     Iterator it = pa.getDemandCurveFunction().getFunctionConstants();
                     while(it.hasNext()){
                          Function.FunctionConstant fc = (Function.FunctionConstant) it.next();
                          log.info(fc.getConstantName() + " - " + fc.getConstantFValue());
                     }
                     if(pa.isSocial()){
                        it = pa.getSocialFunction().getFunctionConstants();
                        log.info("Social : " + pa.getSocialFunction().getFunctionRepresentation());
                        while(it.hasNext()){
                           Function.FunctionConstant fc = (Function.FunctionConstant) it.next();
                           log.info(fc.getConstantName() + " - " + fc.getConstantFValue());
                        }// while
                     }// if

                  } // i
                  blockStart += demandCurveParameters.length;
                }// j

            }
        });
      } // END editButton

      private JButton removeButton = new JButton("   Remove   ");
      {
        removeButton.setBorder(BorderFactory.createRaisedBevelBorder());
        controlPanel.add(removeButton);
        removeButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                int index = list.getSelectedIndex();
                if( index != -1){
                  // remove from model
                  model.removeElementAt(index);
                  // remove from list
                  consumerTypes.removeElementAt(index);
                  // remove its parameters
                  for(int i=0; i<demandCurveParameters.length ; i++)
                      consumerTypeParameters.removeElementAt(
                                      (index * demandCurveParameters.length) + i);
                }

            }
        });
      } // END remove Button

      //***************************END of Control Panel**********************






      //*******************************************************
      // LIST PANEL

      private JPanel listPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,20,20));
      {
        listPanel.setBorder(BorderFactory.createEtchedBorder());

        contentPane.add(listPanel,  BorderLayout.CENTER);
      }

      //*******************************************************

      private DefaultListModel model = new DefaultListModel();

      private JList list = new JList(model);
      {
        list.setCellRenderer(new ListRenderer());
      }
      private JScrollPane scroll = new JScrollPane(list);
      {
        scroll.setPreferredSize(new Dimension(150,150));
        listPanel.add(scroll,null);
      }

      //***************************END of List Panel**********************


      //*******************************************************
      // NAVIGATION PANEL

      private JPanel navigationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,30,10));
      {
        navigationPanel.setBorder(BorderFactory.createEtchedBorder());
        navigationPanel.setPreferredSize(new Dimension(0,40));
        contentPane.add(navigationPanel,  BorderLayout.SOUTH);
      }

      //*******************************************************

      private JButton cancelButton = new JButton("     Cancel    ");
      {
        cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(cancelButton,null);
        cancelButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){
                 try{Step3Frame.this.setClosed(true);}
                 catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
               if (JOptionPane.showConfirmDialog(Step3Frame.this,
                                 "ALL consumer types defined so far, will be deleted if ParametersList change!!","Info",
                                                JOptionPane.OK_CANCEL_OPTION) == JOptionPane.OK_OPTION){

                      step3.setVisible(false);
                      step2.setVisible(true);
               }

            }
        });
      } // END previousButton

      private JButton nextButton = new JButton("    Next >>    ");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);
        nextButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                // inputs already saved
                String error="", warning="";
                boolean ok = true;

                switch (checkPercentages()){
                   case 0 :  break;
                   case 1 :  error = "No Consumer Types defined !!";
                             break;
                   case 2 :  error = "Percentages exceed 100% !!";
                             break;
                   case 3 :  warning = "Percentages rounded !!\nContinue ?";
                             break;
                }

                if(!error.equals("")){
                  JOptionPane.showMessageDialog(Step3Frame.this,error,"Error",JOptionPane.ERROR_MESSAGE);
                  ok = false;
                }
                else{
                     String str = "";
                     for(int i = 0 ; i<consumerTypes.size() ; i++){
                          ConsumerType ct = (ConsumerType) consumerTypes.elementAt(i);
                          str += ("[ " + ct.getName() + " ]  :  "  + ct.getMembers()
                                                                          + " / "+ simulationParameters[2].intValue() + "\n");
                     }
                     if(!warning.equals("")){
                         if(JOptionPane.showConfirmDialog(Step3Frame.this,(str+warning),"Warning",JOptionPane.YES_NO_OPTION) == JOptionPane.NO_OPTION)
                               ok = false;
                     }
                     else
                        JOptionPane.showMessageDialog(Step3Frame.this,str,"Info",JOptionPane.INFORMATION_MESSAGE);
                }

                if (ok) {
                      step3.setVisible(false);
                      step4 = new Step4Frame();
                }

            }
        });
      } // END nextButton

      //***************************END of Navigation Panel**********************

      // RENDER
      class ListRenderer implements ListCellRenderer{
          @SuppressWarnings("unused")
		private boolean focused = false;
          private JPanel panel;
          private JLabel typeName;
          private JLabel percentage;

          public ListRenderer(){
            panel = new JPanel(new GridLayout(1,2,0,0));
            typeName = new JLabel();
            percentage = new JLabel("",SwingConstants.CENTER);
            panel.setOpaque(true);
            typeName.setOpaque(true);
            percentage.setOpaque(true);
            panel.add(typeName,null);
            panel.add(percentage,null);

          }

          public Component getListCellRendererComponent(JList list, Object value, int index,boolean isSelected, boolean cellHasFocus){
              if (value == null){
                  typeName.setText("");
                  percentage.setText("");
              }
              else{
                  ConsumerType ct = (ConsumerType) value;
                  typeName.setText(ct.getName());
                  percentage.setText(ct.getPercentage().toString()+ "%");
              }

              typeName.setBackground(isSelected?SystemColor.textHighlight:SystemColor.text);
              typeName.setForeground(isSelected?SystemColor.textHighlightText:SystemColor.textText);
              percentage.setBackground(isSelected?SystemColor.textHighlight:SystemColor.text);
              percentage.setForeground(isSelected?SystemColor.textHighlightText:SystemColor.textText);
              return panel;
          }

      }// End of class

      private int checkPercentages(){

          float sum = 0;
          int counter = 0 , population = simulationParameters[2].intValue() ;

          // Calculate consumers number for each type from percentages
          // model & consumerTypes --> identical

          if ( model.size() == 0 ) return 1;

          for(int i = 0 ; i < consumerTypes.size() ; i++){
             ConsumerType ct = (ConsumerType)consumerTypes.elementAt(i);
             ct.setMembers( Math.round(
                                (ct.getPercentage().floatValue() / 100) * population)
                          );
             sum += ct.getPercentage().floatValue();
             counter += ct.getMembers();
          }

          if (sum>101) return 2;
          // check rounding
          ConsumerType ct = (ConsumerType)consumerTypes.lastElement();
          if (counter != population){
              ct.setMembers( (population - counter) + ct.getMembers()  );
              return 3;
          }

          return 0;
      }


  }// END of Step3Frame


   /****************************************************************************
   *                              STEP 3.1
   ****************************************************************************/

  private class Step3_1Frame extends JInternalFrame{

	private static final long serialVersionUID = -7956322878889418413L;

	private int index = 0;    // Count the parameters

      private boolean flagFunctionSelected = false;
      private boolean flagSocialSelected = false;

      private String consumerTypeName;

      private String[] availableFunctionsNames = new String[availableFunctions.length];
      {
        for(int i=0 ; i<availableFunctions.length;i++)
          availableFunctionsNames[i] = availableFunctions[i].getFunctionName();
      }

      private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(650,400));

      }

      //*******************************************************
      // TITLE PANEL

      private JPanel titlePanel = new JPanel(new GridLayout(2,1,5,5));
      {
        titlePanel.setBorder(BorderFactory.createEtchedBorder());
        titlePanel.setPreferredSize(new Dimension(0,150));
      }

      //*******************************************************

      private JPanel subTitlePanel = new JPanel(new FlowLayout(FlowLayout.CENTER,5,5));
      {
        titlePanel.add(subTitlePanel,null);
      }

      private JLabel titleLabel1 = new JLabel();
            {
              titleLabel1.setFont(new java.awt.Font("Dialog", 1, 12));
              titleLabel1.setBorder(BorderFactory.createRaisedBevelBorder());
              titleLabel1.setHorizontalAlignment(SwingConstants.CENTER);
              titleLabel1.setHorizontalTextPosition(SwingConstants.CENTER);
              subTitlePanel.add(titleLabel1,null);
            }
      private JLabel titleLabel2 = new JLabel();
            {
              titleLabel2.setFont(new java.awt.Font("Dialog", 1, 12));
              titleLabel2.setHorizontalAlignment(SwingConstants.CENTER);
              titleLabel2.setHorizontalTextPosition(SwingConstants.CENTER);
              titleLabel2.setForeground(SystemColor.textText);
              titlePanel.add(titleLabel2,null);
            }

//***************************END of title panel*********************************


      //*******************************************************
      // Center PANEL

      private JPanel centerPanel = new JPanel(new GridLayout(3,1,0,0));
      {
        centerPanel.setBorder(BorderFactory.createEtchedBorder());
      }


      //*******************************************************
      // INPUT PANEL

      private JPanel inputPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,15,20));
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
              inputPanel.add(inputLabelElasticity,null);
            }

      private JTextField textFieldElasticity = new JTextField(7);
            {
              textFieldElasticity.setBorder(BorderFactory.createLoweredBevelBorder());
              inputPanel.add(textFieldElasticity,null);
            }



      private JLabel inputLabelFunction = new JLabel("Function");
            {
              inputLabelFunction.setFont(new java.awt.Font("Dialog", 1, 12));
              inputLabelFunction.setHorizontalAlignment(SwingConstants.CENTER);
              inputLabelFunction.setHorizontalTextPosition(SwingConstants.CENTER);
              inputPanel.add(inputLabelFunction,null);
            }

      private JComboBox functionCombo = new JComboBox(availableFunctionsNames);
            {
                inputPanel.add(functionCombo,null);
                functionCombo.addActionListener(new ActionListener(){
                  public void actionPerformed(ActionEvent e){
                        if ("comboBoxChanged".equals(e.getActionCommand())){

                             functionPanel.removeAll();

                             functionPanel.validate();
                             flagFunctionSelected = true;
                             if(functionCombo.getSelectedItem().toString().equals("MetDATA") ||
                                   functionCombo.getSelectedItem().toString().equals("PRICE") ){
                                  // to pass the ok test and will be changed
                                  flagSocialSelected = true;
                                  socialCombo.setEnabled(false);
                                  socialPanel.removeAll();
                                  socialPanel.setBorder(BorderFactory.createEmptyBorder());
                                  socialPanel.validate();
                             }
                             else if (demandCurveParameters[index].getSocial().booleanValue()){
                                  socialCombo.setEnabled(true);
                             }

                             createParametersPanel(functionPanel,
                                                 availableFunctions[functionCombo.getSelectedIndex()]);

                        }
                  }
                });
            }


      private JLabel inputLabelSocial = new JLabel("Social Function");
            {
              inputLabelSocial.setFont(new java.awt.Font("Dialog", 1, 12));
              inputLabelSocial.setHorizontalAlignment(SwingConstants.CENTER);
              inputLabelSocial.setHorizontalTextPosition(SwingConstants.CENTER);
              inputPanel.add(inputLabelSocial,null);
            }


      private JComboBox socialCombo = new JComboBox(availableFunctionsNames);
            {
              socialCombo.removeItem("MetDATA");
              socialCombo.removeItem("PRICE");

              socialCombo.setEnabled(false);
              inputPanel.add(socialCombo,null);
              socialCombo.addActionListener(new ActionListener(){
                 public void actionPerformed(ActionEvent e){
                      if ("comboBoxChanged".equals(e.getActionCommand())){
                           socialPanel.removeAll();
                           socialPanel.validate();
                           flagSocialSelected = true;
                           createParametersPanel(socialPanel,
                                                        availableFunctions[socialCombo.getSelectedIndex()]);

                      }
                }
              });
            }

      //***************************END of Input Panel**********************






      //*******************************************************
      // Function PANEL

      private JPanel functionPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,5,5));
      {
        functionPanel.setName("FUNCTION");
      }


      //*******************************************************
      // Social PANEL

      private JPanel socialPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,5,5));
      {
        socialPanel.setName("SOCIAL");
      }


      //*******************************************************
      // End PANEL

      private JPanel endPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,10,10));
      {
        endPanel.setBorder(BorderFactory.createEtchedBorder());
        titlePanel.setPreferredSize(new Dimension(0,60));
      }

      //*******************************************************

      private JButton okButton = new JButton("   OK   ");
      {
        okButton.setBorder(BorderFactory.createRaisedBevelBorder());
        endPanel.add(okButton,null);
        okButton.addActionListener(new ActionListener(){
           @SuppressWarnings({"unchecked","unchecked"})
		public void actionPerformed(ActionEvent ev){
            if(flagFunctionSelected &&
                        (demandCurveParameters[index].getSocial().booleanValue()?flagSocialSelected:true)){
             try{

                int i=0;
                boolean ok = true;

                // Saving this consumer type parameters

                ParameterAttributes pa = new ParameterAttributes();
                pa.setName(demandCurveParameters[index].getName());
                pa.setElasticity(new Float(textFieldElasticity.getText()).floatValue());
                pa.setLn(demandCurveParameters[index].getLn().booleanValue());
                pa.setDemandCurveFunction((Function)
                                  availableFunctions[functionCombo.getSelectedIndex()].getClass().newInstance());

                //********************************
                if (functionCombo.getSelectedItem().equals("PRICE"))          // 6
                    pa.getDemandCurveFunction().setFunctionName("PRICE");
                if (functionCombo.getSelectedItem().equals("RANDOM-INT"))
                    pa.getDemandCurveFunction().setFunctionName("RANDOM-INT");
                if (functionCombo.getSelectedItem().equals("RANDOM-FL"))
                    pa.getDemandCurveFunction().setFunctionName("RANDOM-FL");
                //********************************

                Vector v = new Vector(0);
                Iterator it = pa.getDemandCurveFunction().getFunctionConstants();

                while (it.hasNext()){
                   Function.FunctionConstant fc = (Function.FunctionConstant) it.next();

                   if (fc.asFloat())
                       fc.setConstantValue(new Float(simpleTextFields[0][i].getText()).floatValue());
                   else
                       ok = fc.setConstantValue(simpleTextFields[0][i].getText());

                   if (!ok) new Float("zong!!");

                   v.addElement(fc);

                   i++;

                }
                pa.getDemandCurveFunction().setFunctionConstants(v);

                // if it is social PARAMETER
                if(pa.getDemandCurveFunction().getFunctionName().equals("MetDATA") ||
                      pa.getDemandCurveFunction().getFunctionName().equals("PRICE"))
                    demandCurveParameters[index].setSocial(Boolean.FALSE);

                else if(demandCurveParameters[index].getSocial().booleanValue()){
                   pa.setSocial(true);
                   pa.setSocialFunction((Function)
                                  availableFunctions[socialCombo.getSelectedIndex()].getClass().newInstance());

                   //********************************
                   if (socialCombo.getSelectedItem().equals("RANDOM-INT"))
                      pa.getSocialFunction().setFunctionName("RANDOM-INT");
                   if (socialCombo.getSelectedItem().equals("RANDOM-FL"))
                      pa.getSocialFunction().setFunctionName("RANDOM-FL");
                   //********************************

                   i=0;
                   Vector v2 = new Vector(0);
                   it = pa.getSocialFunction().getFunctionConstants();

                   while (it.hasNext()){
                     Function.FunctionConstant fc = (Function.FunctionConstant) it.next();
                     if (fc.asFloat())
                        fc.setConstantValue(new Float(simpleTextFields[1][i].getText()).floatValue());
                     else
                        ok = fc.setConstantValue(simpleTextFields[1][i].getText());

                     if (!ok) new Float("zong!!");

                     v2.addElement(fc);

                     i++;
                   }

                   pa.getSocialFunction().setFunctionConstants(v2);

                }

                consumerTypeParameters.addElement(pa);

                // *****************************End of Saving********************************



                if(index >= demandCurveParameters.length-1){
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

                } // ELSE-if
             }
             catch (NumberFormatException nfe){
               JOptionPane.showMessageDialog(Step3_1Frame.this,"Invalid INPUTS !!!",
                                                                    "Error",JOptionPane.ERROR_MESSAGE);
             }
             catch (IllegalAccessException iae){
                iae.printStackTrace();
             }
             catch (InstantiationException ie){
                ie.printStackTrace();
             }

            }// IF  for Flags
            else { // functions are not selected
              JOptionPane.showMessageDialog(Step3_1Frame.this,"Select Functions !!!",
                                                                           "Error",JOptionPane.ERROR_MESSAGE);
            }
           }// Action performed
        });
      } // END okButton


      //***************************END of End Panel**********************


      private int maxConstants = 0;
      {
        for(int i =0; i<availableFunctions.length; i++)
          if (availableFunctions[i].constantsNumber()>maxConstants)
             maxConstants = availableFunctions[i].constantsNumber();
      }

      private JLabel[][] simpleLabels = new JLabel[2][maxConstants];
      {
        for(int j=0 ; j<2 ; j++)
            for(int i=0 ; i<maxConstants ; i++){
               simpleLabels[j][i] = new JLabel();
                   simpleLabels[j][i].setFont(new java.awt.Font("Dialog", 1, 12));
                   //simpleLabels[j][i].setHorizontalAlignment(SwingConstants.CENTER);
                   simpleLabels[j][i].setHorizontalTextPosition(SwingConstants.CENTER);
                   simpleLabels[j][i].setSize(new Dimension(20,15));
            }

      }

      private JTextField[][] simpleTextFields = new JTextField[2][maxConstants];
      {
        for(int j=0 ; j<2 ; j++)
            for(int i=0 ; i<maxConstants ; i++){
               simpleTextFields[j][i] = new JTextField(4);
                  simpleTextFields[j][i].setBorder(BorderFactory.createLoweredBevelBorder());
            }

      }

      private void createParametersPanel(JPanel panel, Function function){
          int j = ( (panel.getName()=="FUNCTION") ? 0 : 1);
          String title = ( (panel.getName()=="FUNCTION") ? "Function  :" : "Social Function  :");

          panel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createTitledBorder(BorderFactory.createLineBorder(SystemColor.BLACK),
                                 title + "   "  + function.getFunctionName().toLowerCase()  + "    " +
                                 function.getFunctionRepresentation()),
                BorderFactory.createEmptyBorder(5,5,5,5)));

          int i=0;
          Iterator it = function.getFunctionConstants();
          while(it.hasNext()){
             Function.FunctionConstant fc = (Function.FunctionConstant) it.next();
             simpleLabels[j][i].setText(fc.getConstantName() + " : ");
             panel.add(simpleLabels[j][i],null);
             simpleTextFields[j][i].setText(function.getFunctionName().equals("MetDATA")?"1":"");
             panel.add(simpleTextFields[j][i],null);
             i++;
          }
          panel.validate();

      } // End createParametersPanel


      // Constructor
      Step3_1Frame(String consumerTypeName){

        this.consumerTypeName = consumerTypeName;

        this.setTitle("STEP 3 - 1/" + demandCurveParameters.length);
        titleLabel1.setText(this.consumerTypeName + " Consumer Type");
        titleLabel2.setText("Demand Curve Parameter : " + demandCurveParameters[0].getName());

        contentPane.add(titlePanel,BorderLayout.NORTH);
        contentPane.add(centerPanel,BorderLayout.CENTER);
          centerPanel.add(inputPanel);
          centerPanel.add(functionPanel);
          centerPanel.add(socialPanel);
        contentPane.add(endPanel,BorderLayout.SOUTH);


        if(demandCurveParameters[0].getName().equals("TEMPERATURE") ||
                                          demandCurveParameters[0].getName().equals("RAINFALL")){
             functionCombo.setEnabled(false);
             flagFunctionSelected=true;
             functionCombo.setSelectedItem("MetDATA");

        } // if
        else if (demandCurveParameters[0].getSocial().booleanValue())
            socialCombo.setEnabled(true);

        mainPanel.add(this,layer);

      }// END od constructor



  }// END of Step3_1Frame



   /****************************************************************************
   *                              STEP 4
   ****************************************************************************/

  private class Step4Frame extends JInternalFrame{

	private static final long serialVersionUID = -5384578159639835523L;


	// Constructor
      Step4Frame(){ showStep4(); }


      private void showStep4(){

        boolean fileChosen = false;
        int i = 0;
        while ( i < demandCurveParameters.length && !launchMOA.booleanValue() ){
           if (demandCurveParameters[i].getName().equals("TEMPERATURE") ||
                  demandCurveParameters[i].getName().equals("RAINFALL") )
                    launchMOA = Boolean.valueOf(true);

           i++;
        }
        String msg = "";
        if (launchMOA.booleanValue()){
            JOptionPane.showMessageDialog(mainPanel,"MetOffice Agent will be launched !!\nSelect file with meteorological data",
                                               "Step 4",
                                               JOptionPane.INFORMATION_MESSAGE);
            // instantiate file chooser
            JFileChooser chooser = new JFileChooser(System.getProperty("user.dir"));

            // file chooser properties
            chooser.setControlButtonsAreShown(true);
            chooser.setDialogType(JFileChooser.CUSTOM_DIALOG);
            chooser.setAcceptAllFileFilterUsed(true);
            chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
            chooser.setMultiSelectionEnabled(false);
            chooser.setSelectedFile(null);
            chooser.setDialogTitle("Scenario Design Wizard - Step 4");
            chooser.setLocation(50,50);

            int returnValue = chooser.showDialog(mainPanel,"Load");
	    if (returnValue == JFileChooser.APPROVE_OPTION) {
	         ScenarioDesignWizard.this.metDataFile = chooser.getSelectedFile();
		    if (ScenarioDesignWizard.this.metDataFile != null) {
		        msg = "You chose this file: " + ScenarioDesignWizard.this.metDataFile.getPath();
                        fileChosen = true;
	            }
	    } else if (returnValue == JFileChooser.CANCEL_OPTION) {
	         msg = "User cancelled operation. No file was chosen.";
	    } else if (returnValue == JFileChooser.ERROR_OPTION) {
	         msg = "An error occured. No file was chosen.";
	    } else {
	         msg =  "Unknown operation occured.";
	    }
        }
        else{
             msg = "MetOffice Agent WON'T be launched !!";
             fileChosen = true;
        }

        JOptionPane.showMessageDialog(mainPanel,msg,"Step 4",JOptionPane.INFORMATION_MESSAGE);
        if(fileChosen){
            step5 = new Step5Frame();
            step5.setLocation(50,50);
            step5.setVisible(true);
        }
        else
            step3.setVisible(true);

      }// END of showStep4


  }// END of Step4Frame



   /****************************************************************************
   *                              STEP 5
   ****************************************************************************/

  private class Step5Frame extends JInternalFrame{

	private static final long serialVersionUID = 1560906109955756274L;

	int chosenScenario=0;
      Integer reviewPeriod;
      Float CPI;
      Float CPIpercentage;
      Vector scenarioVariables = new Vector(0,1);

      // Constructor
      Step5Frame(){ mainPanel.add(this,layer);}

      private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(500, 430));
              this.setTitle("STEP 5/6 - Pricing Policy");
      }

      //*******************************************************
      // INPUT PANEL

      private JPanel inputPanel = new JPanel(new GridLayout(3,1,0,0));
      {
        inputPanel.setBorder(BorderFactory.createEtchedBorder());
        //inputPanel.setPreferredSize(new Dimension(0,100));
        contentPane.add(inputPanel,BorderLayout.NORTH);
      }

      //*******************************************************

       // Scenarios

      private JPanel panel1 = new JPanel(new GridLayout(2,1));
      {
        inputPanel.add(panel1, null);
      }
      private JPanel panel1_a = new JPanel(new FlowLayout(FlowLayout.CENTER));
      {
        panel1.add(panel1_a,null);
      }
      private JComboBox scenarioCombo = new JComboBox(availablePricingScenarios);
      {
        //panel1.setSize(0,40);
        panel1_a.add(scenarioCombo,null);
        scenarioCombo.addActionListener(new ActionListener(){
                  public void actionPerformed(ActionEvent e){
                     chosenScenario = scenarioCombo.getSelectedIndex();
                  }
        });
      }

      private JPanel panel1_b = new JPanel(new FlowLayout(FlowLayout.CENTER));
      {
        panel1.add(panel1_b,null);
      }
      private JLabel labelReview = new JLabel("Policy reviewing every :");
            {
              labelReview.setFont(new java.awt.Font("Dialog", 1, 12));
              labelReview.setHorizontalAlignment(SwingConstants.CENTER);
              labelReview.setHorizontalTextPosition(SwingConstants.CENTER);
              panel1_b.add(labelReview,null);
            }
            private JTextField textReview = new JTextField(5);
            {
              textReview.setBorder(BorderFactory.createLoweredBevelBorder());
              panel1_b.add(textReview,null);
            }
            private JLabel labelStepsReview = new JLabel(" simulation step(s)");
            {
              labelStepsReview.setFont(new java.awt.Font("Dialog", 1, 12));
              labelStepsReview.setHorizontalAlignment(SwingConstants.CENTER);
              labelStepsReview.setHorizontalTextPosition(SwingConstants.CENTER);
              panel1_b.add(labelStepsReview,null);
            }

      // CPI
      private JPanel panel2 = new JPanel(new FlowLayout(FlowLayout.CENTER,0,0));
      private JPanel panel2a = new JPanel(new GridLayout(2,2));
      {
        panel2.setBorder(BorderFactory.createEtchedBorder());
        panel2.add(panel2a,null);
        inputPanel.add(panel2, null);
      }
      private JLabel labelCPI = new JLabel("Consumer Price Index (CPI) :");
      {
        labelCPI.setFont(new java.awt.Font("Dialog", 1, 12));
        panel2a.add(labelCPI, null);
      }
      private JPanel panel_a = new JPanel(new FlowLayout(FlowLayout.LEFT));
      private JTextField textCPI = new JTextField(10);
      {
        textCPI.setBorder(BorderFactory.createLoweredBevelBorder());
        panel2a.add(panel_a, null);
        panel_a.add(textCPI,null);
      }
      private JLabel labelPercentage = new JLabel("Increasing Percentage :");
      {
        labelPercentage.setFont(new java.awt.Font("Dialog", 1, 12));
        panel2a.add(labelPercentage, null);
      }
      private JPanel panel_b = new JPanel(new FlowLayout(FlowLayout.LEADING));
      private JTextField textPercentage = new JTextField(10);
      {
        textPercentage.setBorder(BorderFactory.createLoweredBevelBorder());
        panel2a.add(panel_b, null);
        panel_b.add(textPercentage,null);
      }
      // Price Variables
      private JPanel panel3 = new JPanel(new FlowLayout(FlowLayout.CENTER,0,0));
      private JPanel panel3a = new JPanel(new GridLayout(2,1));
      private JRadioButton[] buttons = new JRadioButton[2];
      private ButtonGroup group = new ButtonGroup();
      {
        buttons[0] = new JRadioButton("Average Price (AP)");
        buttons[1] = new JRadioButton("Marginal Price (MP)");
        group.add(buttons[0]);
        group.add(buttons[1]);
        buttons[0].setSelected(true);
        panel3a.add(buttons[0],null);
        panel3a.add(buttons[1],null);
        panel3a.setBorder(BorderFactory.createEmptyBorder(5,0,5,0));
        panel3.add(panel3a,null);
        inputPanel.add(panel3,null);
      }


//***************************END of input panel*********************************



      //*******************************************************
      // TABLE PANEL

      private JPanel tablePanel = new JPanel(new FlowLayout(FlowLayout.CENTER));
      {
        tablePanel.setBorder(BorderFactory.createEtchedBorder());
        contentPane.add(tablePanel,  BorderLayout.CENTER);
      }

      //*******************************************************

      private TableModel model = new AbstractTableModel(){

		private static final long serialVersionUID = 4616524774096974641L;
		private String[] columnsNames = {"Block No","Limit Down", "Limit Up" , "Price"};
          private Object[][] data = new Object[10][4];

          {
             // Initialize price table
             for(int i=0 ; i<10 ;i++)
               data[i][0]= String.valueOf(i+1);
             data[0][1] = "0";
          }

          public int getColumnCount() { return columnsNames.length; }
          public int getRowCount() { return data.length;}
          public String getColumnName(int col) { return columnsNames[col];}
          public Object getValueAt(int row, int col) {
             return data[row][col];
          }

          public void setValueAt(Object value, int row, int col){
                data[row][col] = value;
                if(col == 2)
                   data[row+1][col-1] = value;
                fireTableCellUpdated (row, col);
          }

          public boolean isCellEditable(int row, int column) {
                  // 1st & 2nd columns is read-only (limit Down)
                  return ((column != 0) && (column !=1))  ;
          }

      };



      private JTable table = new JTable(model);

      private JScrollPane scroll = new JScrollPane(table);
      {
        scroll.setBorder(BorderFactory.createRaisedBevelBorder());
        scroll.setPreferredSize(new Dimension(300,100));
        tablePanel.add(scroll,null);
      }

      //***************************END of List Panel**********************


      //*******************************************************
      // NAVIGATION PANEL

      private JPanel navigationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,30,10));
      {
        navigationPanel.setBorder(BorderFactory.createEtchedBorder());
        navigationPanel.setPreferredSize(new Dimension(0,40));
        contentPane.add(navigationPanel,  BorderLayout.SOUTH);
      }

      //*******************************************************

      private JButton cancelButton = new JButton("    Cancel    ");
      {

        cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(cancelButton,null);
        cancelButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){
                    try{Step5Frame.this.setClosed(true);}
                    catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                step5.setVisible(false);
                step4 = new Step4Frame();
            }
        });
      } // END previousButton

      private JButton nextButton = new JButton(" Next  >> ");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);

        nextButton.addActionListener(new ActionListener(){
            @SuppressWarnings("unchecked")
			public void actionPerformed(ActionEvent ev){

                int countBlocks = 1;
                while ( countBlocks<10 && model.getValueAt(countBlocks,3)!=null && !model.getValueAt(countBlocks,3).equals((String)""))
                   countBlocks++;

                // Set last block's limit up to infinity
                model.setValueAt("100000000",countBlocks-1,2);

                boolean check = true;

                try{
                   reviewPeriod = new Integer(textReview.getText());
                   CPI =  new Float(textCPI.getText());
                   CPIpercentage = new Float(textPercentage.getText());
                }
                catch(NumberFormatException nfee){
                  JOptionPane.showMessageDialog(Step5Frame.this," Invalid input!! CPI's attributes must be a float and review period an integer"
                                                                ,"Error",JOptionPane.ERROR_MESSAGE);

                  check = false;
                }

                if (check && checkTable(countBlocks)){
                  //  JOptionPane.showMessageDialog(Step5Frame.this,"Scenario is ready!!","Information",
                  //                                                        JOptionPane.INFORMATION_MESSAGE);
                    priceData.addElement(new Integer(chosenScenario));
                    priceData.addElement(Step5Frame.this.scenarioVariables);
                    priceData.addElement(reviewPeriod);
                    priceData.addElement(CPI);
                    priceData.addElement(CPIpercentage);
                    if (buttons[0].isSelected())
                      priceData.addElement(new String("AP"));
                    else
                      priceData.addElement(new String("MP"));
                    priceData.addElement(new Integer(countBlocks));
                    for(int i = 0; i<countBlocks;i++){
                        priceData.addElement(new Integer(model.getValueAt(i,1).toString()));
                        priceData.addElement(new Integer(model.getValueAt(i,2).toString()));
                        priceData.addElement(new Float(model.getValueAt(i,3).toString()));
                    }

                    step5.setVisible(false);
                    step6 = new Step6Frame();
                    step6.setLocation(50,50);
                    step6.setVisible(true);

                }
            }
        });
      } // END nextButton

      private boolean checkTable(int blocks){
        try{
           for(int i=0;i<blocks;i++){
                new Integer((String)model.getValueAt(i,2));
                new Float((String)model.getValueAt(i,3));
           }
        }
        catch(NumberFormatException nfe){
               JOptionPane.showMessageDialog(Step5Frame.this,
                        " Invalid input !! Limit down must be an integer and price must be a float",
                                                                       "Error",JOptionPane.ERROR_MESSAGE);
               return false;
        }
        catch(NullPointerException npe){
               JOptionPane.showMessageDialog(Step5Frame.this,
                        " Price table is not properly filled in!!","Error",JOptionPane.ERROR_MESSAGE);
               return false;
        }
        return true;
      }
      //***************************END of Navigation Panel**********************

  }// END of Step5Frame


  /****************************************************************************
   *                              STEP 6
   ****************************************************************************/

  private class Step6Frame extends JInternalFrame{

	private static final long serialVersionUID = -1969313893449647589L;

	Float meanValue;
    Float deviationValue;

    // Constructor
    Step6Frame(){ mainPanel.add(this,layer);}

    private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(500,250));
              this.setTitle("STEP 6/6 - Scenario Design Wizard");
      }

    //*******************************************************
      // DATA PANEL

      private JPanel dataPanel = new JPanel(new GridLayout(3,1));
      {
        dataPanel.setBorder(BorderFactory.createEtchedBorder());
        contentPane.add(dataPanel,  BorderLayout.CENTER);
      }
    //*******************************************************

    private JPanel panel1 = new JPanel(new FlowLayout(FlowLayout.CENTER,10,0));
      {
        dataPanel.add(panel1,null);
      }
      private JLabel labelInfo = new JLabel(
            "Define the Gaussian distribution which community's initial consumptions follow");
            {
              labelInfo.setFont(new java.awt.Font("Dialog", 1, 12));
              labelInfo.setBorder(BorderFactory.createCompoundBorder(BorderFactory.createLoweredBevelBorder(),
                                                                  BorderFactory.createEmptyBorder(10,10,10,10)));
              labelInfo.setHorizontalAlignment(SwingConstants.CENTER);
              labelInfo.setHorizontalTextPosition(SwingConstants.CENTER);
              panel1.add(labelInfo,null);
            }
    private JPanel panel2 = new JPanel(new FlowLayout(FlowLayout.CENTER));
      {
        dataPanel.add(panel2,null);
      }

    private JLabel labelMean = new JLabel("Mean value (ì) - (m3):");
            {
              labelMean.setFont(new java.awt.Font("Dialog", 1, 12));
              labelMean.setHorizontalAlignment(SwingConstants.CENTER);
              labelMean.setHorizontalTextPosition(SwingConstants.CENTER);
              panel2.add(labelMean,null);
            }
    private JTextField textMean = new JTextField(5);
            {
              textMean.setBorder(BorderFactory.createLoweredBevelBorder());
              panel2.add(textMean,null);
            }

     private JPanel panel3 = new JPanel(new FlowLayout(FlowLayout.CENTER));
      {
        dataPanel.add(panel3,null);
      }

    private JLabel labelDev = new JLabel("Deviation (ó^2) :");
            {
              labelDev.setFont(new java.awt.Font("Dialog", 1, 12));
              labelDev.setHorizontalAlignment(SwingConstants.CENTER);
              labelDev.setHorizontalTextPosition(SwingConstants.CENTER);
              panel3.add(labelDev,null);
            }
    private JTextField textDev = new JTextField(5);
            {
              textDev.setBorder(BorderFactory.createLoweredBevelBorder());
              panel3.add(textDev,null);
            }


    //*******************************************************
      // NAVIGATION PANEL

      private JPanel navigationPanel = new JPanel(new FlowLayout(FlowLayout.CENTER,30,10));
      {
        navigationPanel.setBorder(BorderFactory.createEtchedBorder());
        navigationPanel.setPreferredSize(new Dimension(0,40));
        contentPane.add(navigationPanel,  BorderLayout.SOUTH);
      }

      //*******************************************************

      private JButton cancelButton = new JButton("     Cancel    ");
      {
        cancelButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(cancelButton,null);
        cancelButton.addActionListener(new ActionListener(){
              public void actionPerformed(ActionEvent ev){
                  try{Step6Frame.this.setClosed(true);}
                  catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                step6.setVisible(false);
                step5.setVisible(true);
            }
        });
      } // END previousButton

      private JButton nextButton = new JButton("End Wizard");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);

        //Inform SuiteGUI to read inputs
        nextButton.addActionListener(suite);

        nextButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if (checkInputs()) {
                    saveInputs();
                    step6.setVisible(false);

                }
            }
        });
      } // END nextButton

      //***************************END of Navigation Panel**********************

      private boolean checkInputs(){
          boolean t =true;

          try{
            meanValue = new Float(textMean.getText());
            deviationValue = new Float(textDev.getText());
            t =true;
          }
          catch (NumberFormatException nfe){
            JOptionPane.showMessageDialog(this,"Fill in the fields with floats !!!","Error",
                                                                               JOptionPane.ERROR_MESSAGE);
            t=false;
          }

          return t;
      }

      @SuppressWarnings("unchecked")
	private void saveInputs(){
            distributionData.addElement(meanValue);
            distributionData.addElement(deviationValue);
      }

  }// END of Step6Frame




  //*******************************************************************************************

  public Object[] packedInputs(){

    Object[] allInputs = new Object[12];

    // add parameters
    for(int i=0; i<5;i++)
        allInputs[i] = simulationParameters[i];

    allInputs[5] = consumerTypes;

    allInputs[6] = this.consumptionLn;

    allInputs[7] = new Integer(demandCurveParameters.length);

    allInputs[8] = consumerTypeParameters;

    allInputs[9] = this.metDataFile;

    allInputs[10] = priceData;

    allInputs[11] = distributionData;

    return allInputs;

  }



  //*******************************************************************************************

  public class Parameter{
          private String name;
          private Boolean ln,social;

          public Parameter(){}
          public Parameter(String n,Boolean log, Boolean soc){
            this.name = n;
            this.ln = log;
            this.social = soc;
          }

          public String getName(){ return this.name;}
          public Boolean getLn(){ return this.ln;}
          public Boolean getSocial(){return this.social;}

          public void setName(String n){ this.name = n;}
          public void setLn(Boolean n){ this.ln = n;}
          public void setSocial(Boolean n){ this.social = n;}

  }// end of parameter Class




}// END of ScenarioDesignWizard