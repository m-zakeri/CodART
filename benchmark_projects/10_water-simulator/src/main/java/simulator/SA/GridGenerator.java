package simulator.SA;


import java.util.Random;
import java.util.Vector;

import simulator.util.ConsumerAttributes;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class GridGenerator {

  private int population;          // agents' population
  private int NxN;          // grid size (one dimension)
  private Vector consumers = new Vector();  // all agents' attributes

  GridGenerator(int gridSize, int population) {

        // Initialize
        this.population = population;
        NxN = gridSize+1;
        consumers.ensureCapacity(population);

        positionAgentsOnGrid();
  }


  /**
   * Get random positions on a grid and name agents after these
   * eg consumer(2,3)
   */

  @SuppressWarnings("unchecked")
private void positionAgentsOnGrid(){

        // help variables
        boolean done = false;
        int x,y;
        String agentName = "consumer_";

        Random gen = new Random();  // number Generator

        while (!done){
            if ( ( ( x = gen.nextInt(NxN) ) != 0) &&
                 ( ( y = gen.nextInt(NxN) ) != 0) ) {

                agentName += x + "," + y;
                ConsumerAttributes a = new ConsumerAttributes(agentName,x,y);
                if (!checkList(a)){
                      consumers.addElement(a);
                      if (consumers.size() == population) { done = true;}
                }
                agentName = "consumer_";
            }
        }
  }

  /**
   * CheckList : check if there is an agent in this position on grid
   * @param checkedAgent : the agent whose position is checked
   * @return TRUE if there is an agent in this position
   *         FALSE if the agent can be putted in this position
   */

  private boolean checkList(ConsumerAttributes checkedAgent){

        String n = checkedAgent.getName();

        for (int i=0; i<consumers.size(); i++){
          if (((ConsumerAttributes)consumers.get(i)).getName().equals(n) ){
                  return true;
          }
        }
        return false;
  }


  /***************************************
   * getConsumers
   * @return : a Vector with all created Consumers
   */

  Vector getConsumers() { return consumers; }


  /****************************************
   *
   * @param a
   * @param sightLimit
   * @return
   */

  @SuppressWarnings("unchecked") 
  Vector getNeighbours(ConsumerAttributes a, int sightLimit){

        int x0,y0;
        int x,y;
        Vector myNeighbours = new Vector();

        x0 = a.getX();
        y0 = a.getY();

        for (int j=0; j <consumers.size(); j++){
            if (! (a.getName().equals(((ConsumerAttributes)consumers.elementAt(j)).getName()))){
                x = ((ConsumerAttributes)consumers.elementAt(j)).getX();
                y = ((ConsumerAttributes)consumers.elementAt(j)).getY();
                if ( (Math.abs(x0-x) <= sightLimit) && (Math.abs(y0-y) <= sightLimit) ){
                    myNeighbours.addElement((ConsumerAttributes)consumers.elementAt(j));
                }
            }
        }

        return myNeighbours;
  }

}// END of class