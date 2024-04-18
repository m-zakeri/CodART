package simulator.util;

import java.util.Vector;
import java.util.Iterator;
import java.io.Serializable;

/**
 * An abstract class that defines the basic attributes of a function object.
 * Every implementation of a function must extend this class. A Fuction has a name,a representation
 * and a set of constants. The abstract methods are : valueFor(int step), valueFor(float x)
 * and parseString(String inputs) </p>
 *
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


public abstract class Function implements Serializable{

    private String functionName;
    private String functionRepresentation;
    private Vector functionConstants = new Vector();

    /**
     * Constructor
     */
    public Function(){}

    /**
     * Constructor
     * @param name Function name
     * @param representation A string to give a short description of the Function eg Y = aX + b.
     * Used in GUI
     */
    public Function(String name, String representation){
        this.functionName = name;
        this.functionRepresentation = representation;
    }

    /**
     *
     * @param name
     */
    public void setFunctionName(String name){ this.functionName = name;}
    /**
     *
     * @return
     */
    public String getFunctionName(){ return this.functionName;}

    /**
     *
     * @param r
     */
    public void setFunctionRepresentation(String r){ this.functionRepresentation = r;}
    /**
     *
     * @return
     */
    public String getFunctionRepresentation(){ return this.functionRepresentation;}

    /**
     *
     * @param fc
     */
    @SuppressWarnings("unchecked")
	protected void setFunctionConstant(FunctionConstant fc){ this.functionConstants.addElement(fc);}

    /**
     *simulator
     * @param v
     */
    public void setFunctionConstants(Vector v){ this.functionConstants = v;}
    /**
     *
     * @return An iterator of this function's constants
     */
    public Iterator getFunctionConstants(){ return this.functionConstants.iterator();}

    /**
     *
     * @return The number of constants
     */
    public int constantsNumber(){ return functionConstants.size();}

    /**
     * It must be implemented by a child class so as for every input X (int x) to return a value Y.
     * X could be the stepId.
     * @param x
     * @return
     */
    abstract public float valueFor(int x);
    /**
     * It must be implemented by a child class so as for every input X (float x) to return a value Y.
     * X could be weights' sum when this Function used for socialization.
     * @param x
     * @return
     */
    abstract public float valueFor(float x);
    /**
     * It must be implemented by a child class when a Function has to check if the String read from GUI
     * has the appropriate format.
     * @param inputs
     * @return
     */
    abstract public boolean parseString(String inputs);

    /**
     *
     * <p>Title: FunctionConstant</p>
     * <p>Description: A class to hold the basic attributes of a Function Constant:
     * A name, a float value and a string value. </p>
     * <p>Copyright: Copyright (c) 2003</p>
     * <p>Company: </p>
     * @author Vartalas Panagiotis
     * @version 1.0
     */
    public class FunctionConstant implements java.io.Serializable{

		private static final long serialVersionUID = 8666992235285732337L;
		private String constantName;
        private Float constantFValue;
        private String constantSValue;
        private Boolean FSValue;

        /**
         * Constructor
         */
        public FunctionConstant(){}
        /**
         * Constructor
         * @param name Function constant name
         * @param fsvalue A boolean value to define if the constant value is a String or a float.
         * true for float
         */
        protected FunctionConstant(String name, boolean fsvalue){this.constantName = name;
                                                                  this.FSValue = new Boolean(fsvalue);}

        /**
         *
         * @return true if the constant value is a float
         */
        public boolean asFloat(){ return FSValue.booleanValue();}

        /**
         *
         * @param name
         */
        protected  void setConstantName(String name){ this.constantName = name;}
        /**
         *
         * @return
         */
        public String getConstantName(){ return this.constantName;}

        /**
         *
         * @param value
         * @return
         */
        public boolean setConstantValue(float value){ this.constantFValue = new Float(value);
                                                      return true;}

        /**
         *
         * @return
         */
        public float getConstantFValue(){ return this.constantFValue.floatValue();}

        /**
         * For Overriding
         */

        public boolean setConstantValue(String value){ this.constantSValue = value;
                                                       return parseString(value);}
        /**
         *
         * @return
         */
        public String getConstantSValue(){ return this.constantSValue;}
    }
}