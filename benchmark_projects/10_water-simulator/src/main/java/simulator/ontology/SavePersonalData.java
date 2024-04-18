package simulator.ontology;

import jade.content.AgentAction;

/** file: SavePersonalData.java
 * @author ontology bean generator
 * @version 2003/10/26
 */


public class SavePersonalData implements AgentAction{ 

  // SavingPath toDirectory
  private SavingPath toDirectory;
  public void setToDirectory(SavingPath s) { this.toDirectory=s; }
  public SavingPath getToDirectory() { return this.toDirectory; }

}
