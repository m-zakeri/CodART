package simulator.ontology;

import jade.content.Predicate;
import jade.util.leap.ArrayList;
import jade.util.leap.Iterator;
import jade.util.leap.List;

/** file: Consumes.java
 * @author ontology bean generator
 * @version 2003/08/12
 */


public class Consumes implements Predicate{ 

  // StepAttr step2
  private StepAttr step2;
  public void setStep2(StepAttr s) { this.step2=s; }
  public StepAttr getStep2() { return this.step2; }

  // MetData meteoData
  private MetData meteoData;
  public void setMeteoData(MetData s) { this.meteoData=s; }
  public MetData getMeteoData() { return this.meteoData; }

  // WaterConsumption personalConsumption
  private WaterConsumption personalConsumption;
  public void setPersonalConsumption(WaterConsumption s) { this.personalConsumption=s; }
  public WaterConsumption getPersonalConsumption() { return this.personalConsumption; }

  //  Collection  pricingScale
  private List pricingScale = new ArrayList();
  public void addPricingScale(PriceBlock o) { pricingScale.add(o); }
  public boolean removePricingScale(PriceBlock o) {return pricingScale.remove(o); }
  public void clearAllPricingScale() {pricingScale.clear(); }
  public Iterator getAllPricingScale() {return pricingScale.iterator(); }
  public List getPricingScale() {return pricingScale; }
  public void setPricingScale(List l) {pricingScale = l; }

}
