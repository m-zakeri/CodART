package simulator.util;


/**
 * An implementation of a linear function. 
 * Y = aX + b
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class Linear extends Function{

	private static final long serialVersionUID = -1407554814565153847L;
	private FunctionConstant a = new FunctionConstant("a",true);
    private FunctionConstant b = new FunctionConstant("b",true);

    public Linear (){
       super("LINEAR"," Y = aX + b ");
       this.setFunctionConstant(a);
       this.setFunctionConstant(b);
    }

    public Linear(float a,float b){
       super("LINEAR"," Y = aX + b ");
       this.a.setConstantValue(a);
       this.setFunctionConstant(this.a);
       this.b.setConstantValue(b);
       this.setFunctionConstant(this.b);
    }


    public float valueFor(int x){

      float y = (a.getConstantFValue() * x) + b.getConstantFValue();
      return y;
    }

    public float valueFor(float x){

      float y = (a.getConstantFValue() * x) + b.getConstantFValue();
      return y;
    }

    public boolean parseString(String inputs){return true;}

}