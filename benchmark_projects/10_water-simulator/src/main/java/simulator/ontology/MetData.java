package simulator.ontology;

import jade.content.Concept;

/** file: MetData.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class MetData implements Concept{ 

  // Float temperature
  private Float temperature;
  public void setTemperature(Float s) { this.temperature=s; }
  public Float getTemperature() { return this.temperature; }

  // Float rainfall
  private Float rainfall;
  public void setRainfall(Float s) { this.rainfall=s; }
  public Float getRainfall() { return this.rainfall; }

}
