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

    ChartUtilities.java
    Created on 21. September 2001, 17:42
 */

package de.progra.charting;

import java.util.*;

/**
 * This class offers multiple static methods to perform mathematical
 * operations concerning the Chart, e.g. methods for rounding the minimal and
 * maximal x-values gracefully.
 * @author  mueller
 * @version 1.0
 */
public class ChartUtilities {

    /** This method calculates the optimal rounding for the minimal and
     * maximal ChartModel values. It computes the difference of the
     * minimal and maximal value and rounds the values min and max according
     * to the exponent of the difference.
     * @param min the minimal column value of the ChartDataModel
     * @param max the maximal column value of the ChartDataModel
     * @return a double[] with the rounded minimal value at index 0 and
     * the maximal value at index 1.
     */
    public static double[] performAutoScale(double min, double max) {
        double[] d = new double[2];  // d[0] = min d[1] = max
        
        double diff = max - min;
        
        d[0] = floor(min, exp(diff));
        d[1] = ceil(max, exp(diff));
        
        return d;
    }
    
    /** Calculates the best tick spacing for the rounded minimal and maximal
     * values.
     * @param min the rounded minimal value
     * @param max the rounded maximal value
     * @return the spacing of ticks on the x-axis.
     */
    public static double calculateTickSpacing(double min, double max) {
        double spacing = 1.0;
        
        double diff = max - min;
        
        int exp = exp(diff);
        
	exp--;
        
        spacing = 1.0 * Math.pow(10.0, (double)exp);
	
	// Currently, only every second tick gets a label, so 20 - 40 ticks are fine. 
	// This should be reduced in a loop probably.
	if((diff / spacing) < 20)
            return 0.5 * spacing;
	else if((diff / spacing) > 40)
	    return 2 * spacing;
        else
            return spacing;
    }
    
    /** This function performs a polynomial interpolation using a set of
     * given x and y values. It uses Neville's interpolation algorithm.
     * @param xa the array of known x-values
     * @param ya the array of known y-values
     * @param x the x value for which the y value will be computed
     * @return the corresponding y value
     */
    public static double interpolate(double xa[], double ya[], double x) {
        /*
            Given arrays xa[1..n] and ya[1..n], and given a value x, 
            this routine returns a value y. 
            If P(x) is the polynomial of degree N ? 1 
            such that P(xa[i]) = ya[i]; 
            i = 1...n, then the returned value y = P(x).
         */

        if(xa.length != ya.length || xa.length == 0 || ya.length == 0) {
            System.out.println("** Invalid Parameter");
            return Double.NaN;
        }
        
        int n = xa.length;
        double y = 0.0;
        double dy = 0.0;
        
        int i, m, ns = 1;
        double den, dif, dift, ho, hp, w;
        double[] c = new double[n];
        double[] d = new double[n];
        dif = Math.abs(x - xa[0]);
        
        for (i = 0; i < n; i++) { // Here we find the index ns of the closest table entry,
            if ( (dift = Math.abs(x - xa[i])) < dif) {
                ns = i;
                dif=dift;
            }
            c[i] = ya[i]; // and initialize the tableau of c's and d's.
            d[i] = ya[i];
        }
        
        y = ya[ns--]; // This is the initial approximation to y.
        //System.out.println("** y ~ "+y);
        
        for (m = 0; m < n - 1; m++) { // For each column of the tableau,
            for (i = 0; i < n - m - 1; i++) { // we loop over the current c's and d's and update them. 
                
                //System.out.println("** m = "+m+", i = "+i);
                ho = xa[i] - x;
                hp = xa[i + m + 1] - x;
                w = c[i + 1] - d[i];
                
                if ( (den = ho - hp) == 0.0) {
                    return Double.NaN;
                }
                // This error can occur only if two input xa's are (to within roundof identical.
                
                //System.out.println("** ho = "+ho+", hp = "+hp);
                
                den = w / den;
                d[i] = hp * den; // Here the c's and d's are updated.
                c[i] = ho * den;
                //System.out.println("** c[i] = "+c[i]+", d[i] = "+d[i]);
            }

            y += (dy = (2 * (ns + 1) < (n - m) ? c[ns + 1] : d[ns--]));
            //System.out.println("** dy = "+dy+", y = "+y);

            /*
            After each column in the tableau is completed, we decide which correction, c or d,
            we want to add to our accumulating value of y, i.e., which path to take through the
            tableau forking up or down. We do this in such a way as to take the most "straight
            line" route through the tableau to its apex, updating ns accordingly to keep track of
            where we are. This route keeps the partial approximations centered (insofar as possible)
            on the target x. The last dy added is thus the error indication.
            */
      }

      return y;
    }
    
    /** This method returns the largest double value that is smaller than
     * <code> d = x * 10<sup>exp</sup></code> where x is rounded down to
     * the closest integer.
     * @param d the double value to be rounded
     * @param exp the exponent of 10 to which d should be rounded
     * @return <code> Math.floor(x) * 10<sup>exp</sup></code>
     */
    public static double floor(double d, int exp) {
        double x = 1.0 * Math.pow(10.0, (double)exp);
        
        return Math.floor(d / x) * x;
    }

    /** This method returns the smallest double value that is smaller than
     * <code> d = x * 10<sup>exp</exp></code> where x is rounded up to
     * the closest integer.
     * @param d the double value to be rounded
     * @param exp the exponent of 10 to which d should be rounded
     * @return <code> Math.ceil(x) * 10<sup>exp</sup></code>
     */
    public static double ceil(double d, int exp) {
        double x = 1.0 * Math.pow(10.0, (double)exp);
        
        return Math.ceil(d / x) * x;
    }
    
    /** A double value can be represented like 
     * <code>d = x * 10<sup>exp</sup></code> and this method returns
     * the value of exp for a double d.
     * @param d the double value
     * @return the exponent of 10
     */
    public static int exp(double d) {
        int exp = 0;
        boolean positive = (d <= -1 || d >= 1 );
        
        while((d <= -10) || (d >= 10) || ((d > -1) && (d < 1))) {
            if(positive) {
                d /= 10;
                exp++;
            } else {
                d *= 10;
                exp--;
            }
        }
        
        return exp;
    }
    
            
    /** Transforms a two-dimensional array of primitives
     * to an array of Numbers.
     */
    public static Number[][] transformArray(int[][] data) {
        Number[][] n = new Number[data.length][data[0].length];
        
        for(int i = 0; i < data.length; i++)
            for(int j = 0; j < data[0].length; j++)
                n[i][j] = new Integer(data[i][j]);
                
        return n;
    }
    
    /** Transforms a two-dimensional array of primitives
     * to an array of Numbers.
     */
    public static Number[][] transformArray(double[][] data) {
        Number[][] n = new Number[data.length][data[0].length];
        
        for(int i = 0; i < data.length; i++)
            for(int j = 0; j < data[0].length; j++)
                n[i][j] = new Double(data[i][j]);
                
        return n;
    }
    
    /** Transforms an array of primitives
     * to an array of Numbers.
     */
    public static Number[] transformArray(double[] data) {
        Number[] n = new Number[data.length];
        
        for(int i = 0; i < data.length; i++)
           n[i] = new Double(data[i]);
                
        return n;
    }
    
    /** Transforms an array of primitives
     * to an array of Numbers.
     */
    public static Number[] transformArray(int[] data) {
        Number[] n = new Number[data.length];
        
        for(int i = 0; i < data.length; i++)
           n[i] = new Integer(data[i]);
                
        return n;
    }
    
    /** Adds a two-dimensional array to a TreeSet. */
    public static void addDataToSet(TreeSet set, Number[][] data) {
        for(int i = 0; i < data.length; i++) {
            set.addAll(Arrays.asList(data[i]));
        }
    }
    
    /** A test routine. */
    public static void main(String[] args) {
        double min = -0.00337;
        double max = 0.00745;
        
        double[] d = performAutoScale(min, max);
        
        System.out.println("** AutoScaling: ("+min+", "+max+") -> ("+d[0]+", "+d[1]+")");
        
        double s = calculateTickSpacing(d[0], d[1]);
        
        System.out.print("** Ticks: ");
        for(double i = d[0]; i <= d[1]; i += s)
            System.out.print(" "+i+" ");
        System.out.println();
        
        System.out.println("** Performing interpolation for 4*x^2");
        System.out.println("** Given values [-4, 64], [0, 0], [3, 36]");
        
        double xa[] = {-4.0, 0.0, 3.0};
        double ya[] = {64.0, 0.0, 36.0};
        
        System.out.print("** Calculating values");
        //double f = interpolate(xa, ya, 1.0);
        //System.out.println("** f(1) = "+f);
        
        for(double i = -5.0; i < 6.0; i += 0.5) {
            System.out.print("["+i+", "+interpolate(xa, ya, i)+"]");
        }
        
        System.out.println();
        
        System.out.println("** Performing interpolation for 5 * x^3 - 4 * x^2 + 2 * x - 5");
        System.out.println("** Given values [-5, -740], [0, -5], [1, -2], [5, 530]");
        
        double xb[] = {-5.0, 0.0, 1.0, 5.0};
        double yb[] = {-740.0, -5.0, -2.0, 530.0};
        
        System.out.print("** Calculating values ");
        
        for(double i = -5.0; i < 6.0; i += 0.5) {
            System.out.print("["+i+", "+interpolate(xb, yb, i)+"]");
        }
        
        System.out.println();
         
    }
}
