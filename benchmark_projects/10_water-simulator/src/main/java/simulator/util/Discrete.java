package simulator.util;

/**
 * An implementation of a  discrete function.
 * @author Vartalas Panagiotis
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */


public class Discrete extends Function{


	private static final long serialVersionUID = -169005630854837068L;
	private FunctionConstant period = new FunctionConstant("T",true);
    private FunctionConstant values = new FunctionConstant("Values",false);
    private Float[] v;

    public Discrete(){
       super("DISCRETE"," Y = { Xi } , i å {0,1, ... T} ");
       this.setFunctionConstant(period);
       this.setFunctionConstant(values);
    }

    public float valueFor(int x){
      // x --> stepId (starts from 1)
      int k = (x-1) % ((int)period.getConstantFValue());
      return v[k].floatValue();
    }

    public float valueFor(float x){
      int k = ((int)x) % ((int)period.getConstantFValue());
      return v[k].floatValue();
    }

    public boolean parseString(String inputs){

         v = new Float[(int)period.getConstantFValue()];

         String temp = "";
         char ch;
         int j = 0;
         try{
             for(int i=0 ; i <inputs.length() ; i++){
                  ch = inputs.charAt(i);
                  if (ch == ' ' || ch == ','){
                          if (!temp.equals("")){
                                v[j] = new Float(temp);
                                temp="";
                                j++;
                          }
                  }
                  else
                      temp += ch;
             }
             v[j] = new Float(temp);
         }
         catch(NullPointerException npe){
            return false;
         }

         if (j == (v.length-1) ) return true;
         else    return false;
    }




}