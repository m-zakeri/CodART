package simulator.ontology;

import jade.content.Predicate;
import jade.util.leap.ArrayList;
import jade.util.leap.Iterator;
import jade.util.leap.List;

/** file: StepTotalConsumption.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class StepTotalConsumption implements Predicate{ 

  // WaterConsumption stepConsumption
  private WaterConsumption stepConsumption;
  public void setStepConsumption(WaterConsumption s) { this.stepConsumption=s; }
  public WaterConsumption getStepConsumption() { return this.stepConsumption; }

  // StepAttr step4
  private StepAttr step4;
  public void setStep4(StepAttr s) { this.step4=s; }
  public StepAttr getStep4() { return this.step4; }

  //  Collection  waterPrice
  private List waterPrice = new ArrayList();
  public void addWaterPrice(PriceBlock o) { waterPrice.add(o); }
  public boolean removeWaterPrice(PriceBlock o) {return waterPrice.remove(o); }
  public void clearAllWaterPrice() {waterPrice.clear(); }
  public Iterator getAllWaterPrice() {return waterPrice.iterator(); }
  public List getWaterPrice() {return waterPrice; }
  public void setWaterPrice(List l) {waterPrice = l; }

}
