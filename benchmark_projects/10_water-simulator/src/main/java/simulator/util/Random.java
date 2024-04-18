package simulator.util;


/**
 * A random number generator implemented as Function type
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */
 

public class Random extends Function{

	private static final long serialVersionUID = 5561984714827868505L;
	private FunctionConstant min = new FunctionConstant("min",true);
    private FunctionConstant max = new FunctionConstant("max",true);

    private boolean fORi = false;

    public Random (){
       super("RANDOM"," min  < Y < max ");
       this.setFunctionConstant(min);
       this.setFunctionConstant(max);
    }
    public Random (float min,float max){
      super("RANDOM"," min  < Y < max ");
       this.min.setConstantValue(min);
       this.setFunctionConstant(this.min);
       this.max.setConstantValue(max);
       this.setFunctionConstant(this.max);
    }

    public float valueFor(int x){

      if(fORi)
         return valueFor((float)1.);

      java.util.Random gen = new java.util.Random();  // number Generator

      boolean out = false;
      int y = 0;
      if (max.getConstantFValue() > min.getConstantFValue()){
          while(!out){
            y = gen.nextInt((int)max.getConstantFValue());
            if ( y > min.getConstantFValue()) out =true;
          }
      }
      return (float)y;
    }

    public float valueFor(float x){

      java.util.Random gen = new java.util.Random();  // number Generator

      boolean out = false;
      float y = 0;
      if (max.getConstantFValue() > min.getConstantFValue()){
          while(!out){
            y = (gen.nextFloat()* max.getConstantFValue() );
            if ( y > min.getConstantFValue()) out =true;
          }
      }

      return y;
    }

    public boolean parseString(String inputs){return true;}

    public void setFloat(){ this.fORi=true; }

}