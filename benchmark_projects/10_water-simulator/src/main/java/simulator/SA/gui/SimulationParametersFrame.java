package simulator.SA.gui;

import jade.gui.GuiEvent;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;

import simulator.SA.SimulationAgent;



/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class SimulationParametersFrame extends JInternalFrame {

	private static final long serialVersionUID = 2004089817101629607L;


private SimulationAgent myAgent;


  private JPanel contentPane = (JPanel) this.getContentPane();
      {  contentPane.setLayout(new BorderLayout());
         this.setClosable(true);
         this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
         this.setResizable(false);
         this.setSize(new Dimension(400, 350));
         this.setTitle("Simulation Parameters");
      }

      //*******************************************************
      // DATA PANEL

      private JPanel dataPanel = new JPanel(new GridLayout(0,1,5,5));
      { contentPane.add(dataPanel,  BorderLayout.CENTER);}

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
                  try{SimulationParametersFrame.this.setClosed(true);}
                  catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      /*private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.setEnabled(false);
      } // END previousButton*/

      private JButton nextButton = new JButton("    OK    ");
      {
        nextButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(nextButton);
        nextButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                if (checkConstraints()) {
                    saveInputs();
                    SimulationParametersFrame.this.setVisible(false);
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
        GuiEvent ge = new GuiEvent((Object) this, SimulationAgent.SIMULATION_PARAMETERS_INPUT);

        ge.addParameter(new Integer(textField3.getText()));
        ge.addParameter(new Integer(textField1.getText()));
        ge.addParameter(new Integer(textField2.getText()));
        ge.addParameter(new Integer( ( (Integer.parseInt(textField4.getText())*12) +
                                                                      Integer.parseInt(textField5.getText()) )
                                              / Integer.parseInt(textField6.getText())
                                              ));
        ge.addParameter(new Integer(Integer.parseInt(textField6.getText())));
        myAgent.postGuiEvent(ge);
      }

      public SimulationParametersFrame(SimulationAgent a, int population,int gridDimension,int sightLimit,
                                                                          int duration,int simulationStep){

         this.myAgent = a;
         this.textField1.setText(Integer.toString(gridDimension));
         this.textField2.setText(Integer.toString(sightLimit));
         this.textField3.setText(Integer.toString(population));
         int totalMonths = (duration * simulationStep);
         int years = totalMonths / 12;
         int months = totalMonths % 12;
         this.textField4.setText(Integer.toString(years));
         this.textField5.setText(Integer.toString(months));
         this.textField6.setText(Integer.toString(simulationStep));

      }

}// END of Step1Frame

