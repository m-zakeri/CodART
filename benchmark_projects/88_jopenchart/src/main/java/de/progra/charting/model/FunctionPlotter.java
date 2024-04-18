/*
    JOpenChart Java Charting Library and Toolkit
    Copyright (C) 2001  Sebastian Müller
    http://jopenchart.sourceforge.net

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

    FunctionPlotter.java
    Created on 7. September 2001, 17:14
*/

package de.progra.charting.model;

import org.nfunk.jep.JEP;

/**
 * This class can be used to create a ChartDataModel from a mathematical 
 * function. A Python interpreter implemented in Java is called to calculate
 * the function values. Therefore, I didn't need to implement a parsing
 * algorithm. Of course, you need to know the Python syntax for mathematical
 * functions. The quadratical function <code>5x<sup>2</sup>-3x+4</code> e.g. 
 * would be written as <code>5*x**2-3*x+4</code>. Please note, that it takes
 * approx. 1 s to plot a quadratical function like this computing 2000 single
 * values.
 * @author  mueller
 * @version 1.0
 */
public class FunctionPlotter {

    /** Creates new FunctionPlot */
    private FunctionPlotter() {}
    
    /** This method creates a new ChartDataModel from the computed
     * function data. In order to compute the needed values, a Python script is
     * created using the provided parameters and is executed afterwards:<p>
       <pre><code>
        String pyfile = "" +
        "AMOUNT = "+amount+"\n"+
        "columns = []\n"+
        "model = []\n"+
        "lowrange = "+lowrange+"\n"+
        "highrange = "+highrange+"\n"+
        "for i in range(AMOUNT) :\n"+
        "   x = lowrange + i * (float(abs(highrange - lowrange)) / AMOUNT)\n"+
        "   columns.append(x)\n"+
        "   model.append("+function+")\n";
                
        interp.exec(pyfile);
       </code></pre>
       Finally the values are extracted via the PythonInterpreter:<p>
       <pre><code>
       pymodel[0] = (double[])interp.get("model", double[].class);
       pycolumns = (double[])interp.get("columns", double[].class);
       </code></pre>
     * @param lowrange the lower x-value to begin from
     * @param highrange the highest x-value to reach
     * @param amount the amount of values that should be computed (2000 is
     * a good value for smooth curves)
     * @param function the mathematical function in Python notation
     * @param rows the array with the DataSet title
     * @throws IllegalArgumentException if the function contains more than 
     * one variable.
     */
    
    public static DefaultChartDataModel createChartDataModelInstance(double lowrange,
                                                              double highrange,
                                                              int amount,
                                                              String function,
                                                              String[] rows) {
        double x = 0.0;
        JEP jep = new JEP();
        jep.addStandardConstants();
        jep.addStandardFunctions();
        
        jep.parseExpression(function);
        
        String[] vars = jep.getVariables();
        String var = "x";
            
        if(vars.length > 1)
            throw new IllegalArgumentException("The supplied function contains more than one variable.");
        
        if(vars.length == 1)
            var = vars[0];
        
        double[][] model = new double[1][amount];
        double[] columns = new double[amount];
                        
        for(int i = 1; i <= amount; i++) {
            x = lowrange + i * ((double)Math.abs(highrange - lowrange) / amount);
            columns[i-1] = x;
            jep.addVariable(var, x);
            model[0][i-1] = jep.getValue();            
            //System.out.println("** Calc("+columns[i-1]+") = "+model[0][i-1]);
        }
                
        return new DefaultChartDataModel(model, columns, rows);
    }
    
    /** This method creates a new ChartDataModel from the computed
     * function data. This implementation automatically uses the function
     * as DataSet title.
     * @param lowrange the lower x-value to begin from
     * @param hirange the highest x-value to reach
     * @param amount the amount of values that should be computed (2000 is
     * a good value for smooth curves)
     * @param function the mathematical function in Python notation
     */
    
    public static DefaultChartDataModel createChartDataModelInstance(double lowrange,
                                                              double hirange,
                                                              int amount,
                                                              String function) {
            return createChartDataModelInstance(lowrange, hirange, 
                                                amount, function,
                                                new String[] {function});
    }
    
}
