package simulator.util;

import jade.core.AID;

/**
 * A  list of default Agent IDs
 * 
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public interface AIDs {
  /**
   * Simulator Agent AID
   */
  public static final AID SIMULATOR = new AID("simulator",false);
  /**
   * MetOffice Agent AID
   */
  public static final AID MET_OFFICE = new AID("metOffice",false);
  /**
   * WaterSupplier Agent AID
   */
  public static final AID WATER_SUPPLIER = new AID("supplier",false);
  /**
   * MetOffice Agent AID as an element of an AID[] array
   */
  public static final AID[] MOA = {MET_OFFICE};
}