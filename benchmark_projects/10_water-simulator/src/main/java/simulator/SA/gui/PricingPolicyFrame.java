package simulator.SA.gui;

import jade.gui.GuiEvent;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.TableModel;

import simulator.SA.SimulationAgent;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class PricingPolicyFrame extends JInternalFrame {
	private static final long serialVersionUID = -3332140195203607928L;
	private SimulationAgent myAgent;
      private int chosenScenario=0;
      private Integer reviewPeriod;
      private Float CPI;
      private Float CPIpercentage;
      private Vector scenarioVariables = new Vector(0,1);
      private Vector priceData = new Vector(0,1);
      private String[] availablePricingScenarios;

      // Constructor
      public PricingPolicyFrame(SimulationAgent a, String[] availablePricingScenarios, Vector priceData){
          this.myAgent = a;
          this.availablePricingScenarios = availablePricingScenarios;
          this.priceData = priceData;
          setDataToFields();
      }

      private JPanel contentPane = (JPanel) this.getContentPane();
      {
              contentPane.setLayout(new BorderLayout());
              this.setClosable(true);
              this.setDefaultCloseOperation(JInternalFrame.HIDE_ON_CLOSE);
              this.setResizable(false);
              this.setSize(new Dimension(500, 430));
              this.setTitle("Pricing Policy");
      }

      //*******************************************************
      // INPUT PANEL

      private JPanel inputPanel = new JPanel(new GridLayout(3,1,0,0));
      {
        inputPanel.setBorder(BorderFactory.createEtchedBorder());
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
      private JComboBox scenarioCombo = new JComboBox(/*availablePricingScenarios*/);
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
		private static final long serialVersionUID = 8205637828692708450L;
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
                    try{PricingPolicyFrame.this.setClosed(true);}
                    catch(java.beans.PropertyVetoException ex){}
              }
        });
      } // END cancelButton

      /*private JButton previousButton = new JButton("  << Previous  ");
      {
        previousButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(previousButton);
        previousButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent ev){
                step5.setVisible(false);
                step4 = new Step4Frame();
            }
        });
      } // END previousButton*/

      private JButton okButton = new JButton("  OK  ");
      {
        okButton.setBorder(BorderFactory.createRaisedBevelBorder());
        navigationPanel.add(okButton);

        okButton.addActionListener(new ActionListener(){
            @SuppressWarnings("unchecked")
			public void actionPerformed(ActionEvent ev){

                int countBlocks = 1;
                while ( countBlocks<10 && model.getValueAt(countBlocks,3)!=null && !model.getValueAt(countBlocks,3).equals((String)""))
                   countBlocks++;

                // Set last block's limit up to infinity
                model.setValueAt("1000000",countBlocks-1,2);

                boolean check = true;

                try{
                   reviewPeriod = new Integer(textReview.getText());
                   CPI =  new Float(textCPI.getText());
                   CPIpercentage = new Float(textPercentage.getText());
                }
                catch(NumberFormatException nfee){
                  JOptionPane.showMessageDialog(PricingPolicyFrame.this," Invalid input!! CPI's attributes must be a float and review period an integer"
                                                                ,"Error",JOptionPane.ERROR_MESSAGE);

                  check = false;
                }

                if (check && checkTable(countBlocks)){
                    priceData.removeAllElements();
                    priceData.addElement(new Integer(chosenScenario));
                    priceData.addElement(PricingPolicyFrame.this.scenarioVariables);
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

                    GuiEvent ge = new GuiEvent((Object) this, SimulationAgent.PRICING_POLICY_INPUT);
                    ge.addParameter(priceData);
                    myAgent.postGuiEvent(ge);

                    PricingPolicyFrame.this.setVisible(false);

                }
            }
        });
      } // END okButton

      private boolean checkTable(int blocks){
        try{
           for(int i=0;i<blocks;i++){
                new Integer((String)model.getValueAt(i,2));
                new Float((String)model.getValueAt(i,3));
           }
        }
        catch(NumberFormatException nfe){
               JOptionPane.showMessageDialog(PricingPolicyFrame.this,
                        " Invalid input !! Limit down must be an integer and price must be a float",
                                                                       "Error",JOptionPane.ERROR_MESSAGE);
               return false;
        }
        catch(NullPointerException npe){
               JOptionPane.showMessageDialog(PricingPolicyFrame.this,
                        " Price table is not properly filled in!!","Error",JOptionPane.ERROR_MESSAGE);
               return false;
        }
        return true;
      }
      //***************************END of Navigation Panel**********************

      private void setDataToFields(){
          for(int i=0; i < this.availablePricingScenarios.length ; i++)
               this.scenarioCombo.addItem(this.availablePricingScenarios[i]);

          this.scenarioCombo.setSelectedIndex(((Integer)priceData.elementAt(0)).intValue());
          // not used yet
          //this.scenarioVariables = (Vector) priceData.elementAt(1);
          this.textReview.setText(((Integer)priceData.elementAt(2)).toString());
          this.textCPI.setText(((Float)priceData.elementAt(3)).toString());
          this.textPercentage.setText(((Float)priceData.elementAt(4)).toString());
          if ( ((String)priceData.elementAt(5)).equals("AP"))
              this.buttons[0].setSelected(true);
          else
              this.buttons[1].setSelected(true);

          int j = 7;
          for(int i = 0; i < ((Integer)priceData.elementAt(6)).intValue() ;i++){
              model.setValueAt(priceData.elementAt(j).toString(),i,1);
              j++;
              model.setValueAt(priceData.elementAt(j).toString(),i,2);
              j++;
              model.setValueAt(priceData.elementAt(j).toString(),i,3);
              j++;
          }
      }


}// END of Pricing Policy Frame