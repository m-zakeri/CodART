package simulator.util;

/**
 * An exponential function implemented as Function type
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
  */

public class Raise extends Function{


	private static final long serialVersionUID = -7852793195233992557L;
	private FunctionConstant a = new FunctionConstant("a",true);
    private FunctionConstant n = new FunctionConstant("n",true);

    public Raise (){
       super("LN-RAISE"," Y = a [ln(X)]^n ");
       this.setFunctionConstant(a);
       this.setFunctionConstant(n);
    }

    public float valueFor(int x){

      double init = Math.log((double)x);
      double power = init;
      for(int i=1;i<((int)n.getConstantFValue());i++)
          power = power * init;

      return (a.getConstantFValue() * (float)power);
    }

    public float valueFor(float x){

      float init = (float)Math.log((double)x);
      float power = init;
      for(int i=1;i<((int)n.getConstantFValue());i++)
          power = power * init;

      return (a.getConstantFValue() * power);
    }

    public boolean parseString(String inputs){return true;}

}