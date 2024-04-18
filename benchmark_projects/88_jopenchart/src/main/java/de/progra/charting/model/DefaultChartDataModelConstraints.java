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

    DefaultChartDataModelConstraints.java
    Created on 16. Sept. 2002
*/

package de.progra.charting.model;

import de.progra.charting.ChartUtilities;
import java.util.TreeSet;

/**
 * Implementing the ChartDataModelConstraints this class provides the default implementation
 * for the data model constraints. Alternative implementations could return the sum of all
 * column values to implement stacked bar charts e.g.
 * @author  smueller
 */
public class DefaultChartDataModelConstraints implements ChartDataModelConstraints {
    
    /** The model for which to calculate the constraints. */ 
    protected AbstractChartDataModel model;
    
    /** The axis to compute the constraints. */
    protected int axis;
    
    /** A flag which determines if column values should be manually scalable. */
    protected boolean allowManualColScale = true;
    
    /** Creates a new instance of DefaultChartDataModelConstraints */
    public DefaultChartDataModelConstraints(AbstractChartDataModel model, int axis) {
        this.model = model;
        this.axis = axis;
    }
    
    /** Creates a new instance of DefaultChartDataModelConstraints
     * @param model the AbstractDataModel for which constraints will be computed
     * @param axis the y-axis which will be considered
     * @param allowManualScale a flag which triggers if column values should 
     * be allowed to be scaled manually (default is yes)
     */
    public DefaultChartDataModelConstraints(AbstractChartDataModel model, int axis, boolean allowManualColScale) {
        this(model, axis);
        this.allowManualColScale = allowManualColScale;
    }
    
    /** Returns the maximum value of all datasets.  */
    public Number getMaximumValue() {
        TreeSet ordered_values = (TreeSet)model.getOrderedValues(axis);
        
        if(ordered_values.size() == 0)
            return new Integer(1);
        else if(model.isManualScale()) {
            //System.out.println("** model.getManualMaximumValue() = "+model.getManualMaximumValue());
            return model.getManualMaximumValue();
        }
        else if(model.isAutoScale()) {
            double min = ((Number)ordered_values.first()).doubleValue();
            double max = ((Number)ordered_values.last()).doubleValue();
            
            //System.out.println("** min = "+min+"  max = "+max);
            
            if(min / max > 0.95) {
                //System.out.println("** ChartUtilities.performAutoScale(min/2, 2 * max)[1]"+ChartUtilities.performAutoScale(min/2, 2 * max)[1]);
                return new Double(ChartUtilities.performAutoScale(min/2, 
                                                                  2 * max)[1]);
             }
            else {
                //System.out.println("** ChartUtilities.performAutoScale(min, max)[1]"+ChartUtilities.performAutoScale(min, max)[1]);
                return new Double(ChartUtilities.performAutoScale(min, 
                                                              max)[1]);
             }
        } else
            return (Number)ordered_values.last();
    }    

    /** Returns the minimum value of all datasets.  */
    public Number getMinimumValue() {
        TreeSet ordered_values = (TreeSet)model.getOrderedValues(axis);

        if(ordered_values.size() == 0)
            return new Integer(0);
        else if(model.isManualScale()) {
            //System.out.println("** model.getManualMinimumValue() = "+model.getManualMinimumValue());
            return model.getManualMinimumValue();
        }
        else if(model.isAutoScale()) {
            double min = ((Number)ordered_values.first()).doubleValue();
            double max = ((Number)ordered_values.last()).doubleValue();

            //System.out.println("** min = "+min+"  max = "+max);
            
            if(min / max > 0.95) {
                //System.out.println("** ChartUtilities.performAutoScale(min/2, 2 * max)[0]"+ChartUtilities.performAutoScale(min/2, 2 * max)[0]);
                return new Double(ChartUtilities.performAutoScale(min/2, 
                                                                  2 * max)[0]);
             }
            else {
                //System.out.println("** ChartUtilities.performAutoScale(min, max)[0]"+ChartUtilities.performAutoScale(min, max)[0]);
                return new Double(ChartUtilities.performAutoScale(min, 
                                                              max)[0]);
             }
        } else                
           return (Number)ordered_values.first();
    }

    /** Returns the minimum column value. 
     * @throws ArrayIndexOutOfBoundsException if the Model is empty
     */
    public double getMinimumColumnValue() {
        if(model.isManualScale() && allowManualColScale) {
            return model.getManualMinimumColumnValue();
        }
        if(model.isAutoScale())
            return ChartUtilities.performAutoScale(model.getFirstColumnValue(),
                                                   model.getLastColumnValue())[0];
        else
            return model.getFirstColumnValue();
    }

    /** Returns the maximum column value. 
     * @throws ArrayIndexOutOfBoundsException if the model is empty
     */
    public double getMaximumColumnValue() {
        if(model.isManualScale() && allowManualColScale) {
            return model.getManualMaximumColumnValue();
        }
        if(model.isAutoScale())
            return ChartUtilities.performAutoScale(model.getFirstColumnValue(),
                                                   model.getLastColumnValue())[1];
        else
            return model.getLastColumnValue();
    }
}