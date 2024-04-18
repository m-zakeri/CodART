package simulator.ontology;

import jade.content.Predicate;
import jade.util.leap.ArrayList;
import jade.util.leap.Iterator;
import jade.util.leap.List;

/** file: AskWeightsFor.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class AskWeightsFor implements Predicate{ 

  //  Collection  parameters
  private List parameters = new ArrayList();
  public void addParameters(Parameter o) { parameters.add(o); }
  public boolean removeParameters(Parameter o) {return parameters.remove(o); }
  public void clearAllParameters() {parameters.clear(); }
  public Iterator getAllParameters() {return parameters.iterator(); }
  public List getParameters() {return parameters; }
  public void setParameters(List l) {parameters = l; }

  // StepAttr step3
  private StepAttr step3;
  public void setStep3(StepAttr s) { this.step3=s; }
  public StepAttr getStep3() { return this.step3; }

}
