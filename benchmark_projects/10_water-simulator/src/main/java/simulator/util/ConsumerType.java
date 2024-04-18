package simulator.util;

import java.io.Serializable;

/**
 * A class that holds some basic properties for a consumer Type: 
 * Consumer Type Name, its percentage in simulation's population 
 * and the number of agents that finally are of the specified
 * consumer type.
 *
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class ConsumerType implements Serializable {
	
	private static final long serialVersionUID = -2757402347444049686L;
	
	private String name;
	
	private Float percentage;
	
	private Integer members;
	
	/**
	 * Constructor
	 */
	public ConsumerType() {
	}
	
	/**
	 * Constructor
	 * @param name Consumer type name
	 * @param percentage Consumer Type percentage
	 */
	public ConsumerType(String name, Float percentage) {
		this.name = name;
		this.percentage = percentage;
	}
	
	/**
	 *
	 * @return
	 */
	public String getName() {
		return this.name;
	}
	
	/**
	 *
	 * @return
	 */
	public Float getPercentage() {
		return this.percentage;
	}
	
	/**
	 *
	 * @return
	 */
	public int getMembers() {
		return this.members.intValue();
	}
	
	/**
	 *
	 * @param n
	 */
	public void setName(String n) {
		this.name = n;
	}
	
	/**
	 *
	 * @param p
	 */
	public void setPercentage(Float p) {
		this.percentage = p;
	}
	
	/**
	 *
	 * @param m
	 */
	public void setMembers(int m) {
		this.members = new Integer(m);
	}
	
}// end of ConsumerType Class