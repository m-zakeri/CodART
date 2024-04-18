package simulator.ontology;

import jade.content.AgentAction;

/** file: Start.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class Start implements AgentAction{ 

  // StepAttr simulationStep
  private StepAttr simulationStep;
  public void setSimulationStep(StepAttr s) { this.simulationStep=s; }
  public StepAttr getSimulationStep() { return this.simulationStep; }

}
