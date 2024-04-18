package simulator.util;

import jade.core.AID;

/**
 * A class that holds some basic properties for a consumer Agent. 
 * Agent Name, AID, x,y positions on grid and its consumer type
 *
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ConsumerAttributes {

  private String agentName;
  private AID aid;
  private int x;
  private int y;
  private String consumerType;


  /**
   * Constructor
   */
  public ConsumerAttributes(){}
  /**
   * Constructor
   * @param name Consumer agent's local name (in Jade Platform)
   * @param x x position on grid
   * @param y y position on grid
   */
  public ConsumerAttributes(String name, int x, int y){ agentName = name;
                                                     this.x = x;
                                                     this.y = y; }
  /**
   *
   * @return
   */
  public String getName(){ return agentName; }
  /**
   *
   * @param name
   */
  public void setName(String name) { agentName = name;}
  /**
   *
   * @return
   */
  public AID getAID(){ return aid; }
  /**
   *
   * @param aid
   */
  public void setAID(AID aid) { this.aid = aid;}
  /**
   *
   * @return
   */
  public int getX(){ return x; }
  /**
   *
   * @param x
   */
  public void setX(int x) { this.x=x; }
  /**
   *
   * @return
   */
  public int getY(){ return y; }
  /**
   *
   * @param y
   */
  public void setY(int y) { this.y=y; }
  /**
   *
   * @return
   */
  public String getConsumerType(){ return consumerType; }
  /**
   *
   * @param consumerType
   */
  public void setConsumerType(String consumerType) { this.consumerType = consumerType;}

  //public String print(){ return /*System.out.println*/(agentName + " [ " + consumerType + " ] ");}

}