package simulator.ontology;

import jade.content.Concept;

/** file: Parameter.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class Parameter implements Concept{ 

  // String name
  private String name;
  public void setName(String s) { this.name=s; }
  public String getName() { return this.name; }

  // Float weight
  private Float weight;
  public void setWeight(Float s) { this.weight=s; }
  public Float getWeight() { return this.weight; }

}
