package simulator.util;

import java.io.Serializable;

import org.apache.log4j.Logger;

/**
 * A class representing a Parameter in a demand curve function of a Consumer Agent.
 * The properties of such a parameter are : 
 * name, 
 * elasticity, 
 * a boolean indicating if parameter's value  will be the logarithm or not of the function, 
 * a Function for calculating the parameter's value,
 * a Function for calculating the social weight for this parameter, 
 * a boolean indicating if this parameter is social
 * 
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
  */


public class ParameterAttributes implements Serializable{


	private static final long serialVersionUID = 6885432319261152672L;
	private Logger log = Logger.getLogger(ParameterAttributes.class);
//Properties
  private String name;
  private Float elasticity;
  private Boolean ln;
  private Function demandCurveFunction;
  private Function socialFunction;
  private Boolean social= Boolean.FALSE;
  private Float value = new Float(0);

  /**
   * Set parameter name
   * @param name
   */
  public void setName(String name) { this.name = name; }
  /**
   *
   * @return
   */
  public String getName() { return name; }

  /**
   * Set elasticity
   * @param elasticity
   */
  public void setElasticity(float elasticity) { this.elasticity = new Float(elasticity); }
  /**
   *
   * @return
   */
  public float getElasticity() { return elasticity.floatValue(); }

  /**
   * Set true if the value of the parameter is the logarithm of parameter's function
   * @param ln
   */
  public void setLn(boolean ln) { this.ln = new Boolean(ln); }
  /**
   *
   * @return
   */
  public boolean getLn() { return ln.booleanValue(); }

  /**
   * Set the demand curve function for this parameter. The Demand Curve Function gets the stepId
   * as input if the parameter isn't social, otherwise gets the sum of all weights received from
   * its neighbours. It returns parameter's value.
   * @param dCF One of the availabe functions
   */
  public void setDemandCurveFunction(Function dCF) { demandCurveFunction = dCF; }
  /**
   * Set the demand curve function for this parameter
   * @return
   */
  public Function getDemandCurveFunction() { return demandCurveFunction; }

  /**
   * Set the social function for this parameter. The Social Curve Function gets the stepId
   * as input and returns a value (the weight) that the consumer agent will send in socialization
   * stage of simulation in the specified step.
   * @param sF One of the available functions
   */
  public void setSocialFunction(Function sF) { socialFunction = sF; }
  /**
   *
   * @return
   */
  public Function getSocialFunction() { return socialFunction; }

  /**
   * Set this parameter to be social
   */
  public void setSocial(boolean b){ this.social = Boolean.valueOf(b); }
  /**
   *
   * @return
   */
  public boolean isSocial() { return social.booleanValue();}


  /**
   * Calculates parameter's value for the Demand Curve as : elasticity * [ ln ] ( demandCurveFunction(step) )
   * @param step The step for which to calculate parameters value
   * @return Parameter's value that will be summed for calculating total consumer's consumption
   */
  public float valueFor(int step){
	  return valueFor((float)step);
  }

  /**
   * Overrides the previous method if the input is a float number. Mostly used when the parameter is
   * social and the input value is the sum of weights.
   * Calculates parameter's value for the Demand Curve as :
   * elasticity * [ ln ] (demandCurveFunction(weights) )
   * @param x The step for which to calculate parameters value
   * @return Parameter's value that will be summed for calculating total consumer's consumption
   */
  public float valueFor(float x){

      float temp = demandCurveFunction.valueFor(x);

      if (temp >0){

            if (ln.booleanValue()) {
              this.value = new Float(elasticity.floatValue()* ((float)Math.log(temp)));
            }
            else {
              this.value = new Float(elasticity.floatValue() * temp);
            }
      }
      else{
    	  log.error("FATAL ERROR: Parameter was zero");
      }
      return value.floatValue();
  }
  public String toString(){
	  
	return "Parameter" + name + " type: " +  demandCurveFunction.getFunctionName() + 
	"(elasticity: " + elasticity +" log: " + ln + " soc: " + social ;
	  
  }
}