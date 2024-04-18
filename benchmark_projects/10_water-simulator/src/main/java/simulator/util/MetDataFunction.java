package simulator.util;

/**
 * A Function implementation that returns the content of the meteorological data
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


public class MetDataFunction extends Function{

	private static final long serialVersionUID = -2320692789743826748L;
	private FunctionConstant a = new FunctionConstant("a",true);

    public MetDataFunction(){
       super("MetDATA"," Y = a * (MetData) ");
       this.setFunctionConstant(a);
       this.a.setConstantValue(1);
    }


    public float valueFor(int x){

      float y = (a.getConstantFValue() * x);
      return y;
    }

    public float valueFor(float x){

      float y = (a.getConstantFValue() * x);
      return y;
    }

    public boolean parseString(String inputs){return true;}

}