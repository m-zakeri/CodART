package simulator.ontology;

import jade.content.Predicate;

/** file: HasMetData.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class HasMetData implements Predicate{ 

  // StepAttr step1
  private StepAttr step1;
  public void setStep1(StepAttr s) { this.step1=s; }
  public StepAttr getStep1() { return this.step1; }

  // MetData data
  private MetData data;
  public void setData(MetData s) { this.data=s; }
  public MetData getData() { return this.data; }

}
