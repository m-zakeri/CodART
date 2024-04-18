package simulator.SA;

import java.util.Random;

import org.apache.log4j.Logger;

/**
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

class GaussGenerator {
 Logger log = Logger.getLogger(GaussGenerator.class);
  float mean;
  float deviation;


  Random generator = new Random();

  GaussGenerator(float mean,float deviation){
      this.mean = mean;
      // MUST be checked => Y = sqrt(deviation) * X + mean
      this.deviation = (float)Math.sqrt(deviation);
  }

  protected Float getRandomInitialConsumption(){

      float initialConsumption = (((float)generator.nextGaussian())*deviation) + mean;
      //TEST
      log.debug("Initial consumption is: " + initialConsumption);

      return new Float(initialConsumption);
  }
}