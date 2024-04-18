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

    StackedChartDataModelConstraints.java
    Created on 26. Sept. 2002
*/

package de.progra.charting.model;

import de.progra.charting.ChartUtilities;
import de.progra.charting.CoordSystem;
import java.util.TreeSet;

/**
 * Implementing the ChartDataModelConstraints this class provides an implementation
 * for the data model constraints where the maximum value is the sum of all 
 * positive values and the minimum value is the sum of all negative values.
 * @author  smueller
 */
public class StackedChartDataModelConstraints implements ChartDataModelConstraints {
    
    /** The model for which to calculate the constraints. */ 
    protected AbstractChartDataModel model;
    
    /** The axis to compute the constraints. */
    protected int axis;
    
    /** A flag which determines if column values should be manually scalable. */
    protected boolean allowManualColScale = true;
    
    /** Creates a new instance of DefaultChartDataModelConstraints */
    public StackedChartDataModelConstraints(AbstractChartDataModel model, int axis) {
        this.model = model;
        this.axis = axis;
    }
    
    /** Creates a new instance of DefaultChartDataModelConstraints
     * @param model the AbstractDataModel for which constraints will be computed
     * @param axis the y-axis which will be considered
     * @param allowManualScale a flag which triggers if column values should 
     * be allowed to be scaled manually (default is yes)
     */
    public StackedChartDataModelConstraints(AbstractChartDataModel model, int axis, boolean allowManualColScale) {
        this(model, axis);
        this.allowManualColScale = allowManualColScale;
    }
    
    /** Returns the maximum value of all datasets.  */
    public Number getMaximumValue() {
        int minimumDataSetLength = Integer.MAX_VALUE;
        double maxvalue = 0.0;
        double minvalue = 0.0;
        
        double columnminvalue = Double.MAX_VALUE;
        double columnmaxvalue = Double.MIN_VALUE;
        
        for(int i = 0; i < model.getDataSetNumber(); i++) {
            minimumDataSetLength = Math.min(minimumDataSetLength, model.getDataSetLength(i));
        } 
        
        double value = 0.0;
        
        for(int i = 0; i < minimumDataSetLength; i++) {
            for(int j = 0; j <  model.getDataSetNumber(); j++) {
                value = model.getValueAt(j, i).doubleValue();
                if(value < 0)
                    columnminvalue += value;
                else
                    columnmaxvalue += value;
            }
            minvalue = Math.min(columnminvalue, minvalue);
            columnminvalue = 0.0;
            maxvalue = Math.max(columnmaxvalue, maxvalue);
            columnmaxvalue = 0.0;
        }
        
        if(model.getOrderedValues(CoordSystem.FIRST_YAXIS).size() == 0 
        || (maxvalue == 0.0 && minvalue == 0.0))
            return new Integer(1);
        else if(model.isManualScale()) {
            return new Double(Math.max(model.getManualMaximumValue().doubleValue(), maxvalue));
        }
        else if(model.isAutoScale()) {
            if(minvalue / maxvalue > 0.95) {
                //System.out.println("** ChartUtilities.performAutoScale(min/2, 2 * max)[1]"+ChartUtilities.performAutoScale(min/2, 2 * max)[1]);
                return new Double(ChartUtilities.performAutoScale(minvalue/2, 
                                                                  2 * maxvalue)[1]);
             }
            else {
                //System.out.println("** ChartUtilities.performAutoScale(min, max)[1]"+ChartUtilities.performAutoScale(min, max)[1]);
                return new Double(ChartUtilities.performAutoScale(minvalue, 
                                                              maxvalue)[1]);
             }
        } else
            return new Double(maxvalue);
    }    

    /** Returns the minimum value of all datasets.  */
    public Number getMinimumValue() {
        int minimumDataSetLength = Integer.MAX_VALUE;
        double maxvalue = 0.0;
        double minvalue = 0.0;
        double columnmaxvalue = 0.0;
        double columnminvalue = 0.0;
        
        for(int i = 0; i < model.getDataSetNumber(); i++) {
            minimumDataSetLength = Math.min(minimumDataSetLength, model.getDataSetLength(i));
        } 
        
        double value = 0.0;
        
        for(int i = 0; i < minimumDataSetLength; i++) {
            for(int j = 0; j <  model.getDataSetNumber(); j++) {
                value = model.getValueAt(j, i).doubleValue();
                if(value < 0)
                    columnminvalue += value;
                else
                    columnmaxvalue += value;
            }
            minvalue = Math.min(columnminvalue, minvalue);
            columnminvalue = 0.0;
            maxvalue = Math.max(columnmaxvalue, maxvalue);
            columnmaxvalue = 0.0;
        }

        if(model.getOrderedValues(CoordSystem.FIRST_YAXIS).size() == 0 
        || (maxvalue == 0.0 && minvalue == 0.0))
            return new Integer(0);
        else if(model.isManualScale()) {
            //System.out.println("** model.getManualMinimumValue() = "+model.getManualMinimumValue());
            return new Double(Math.min(model.getManualMinimumValue().doubleValue(), minvalue));
        }
        else if(model.isAutoScale()) {
            //System.out.println("** min = "+min+"  max = "+max);
            
            if(minvalue / maxvalue > 0.95) {
                //System.out.println("** ChartUtilities.performAutoScale(min/2, 2 * max)[0]"+ChartUtilities.performAutoScale(min/2, 2 * max)[0]);
                return new Double(ChartUtilities.performAutoScale(minvalue/2, 
                                                                  2 * maxvalue)[0]);
             }
            else {
                //System.out.println("** ChartUtilities.performAutoScale(min, max)[0]"+ChartUtilities.performAutoScale(min, max)[0]);
                return new Double(ChartUtilities.performAutoScale(minvalue, 
                                                              maxvalue)[0]);
             }
        } else                
           return new Double(minvalue);
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
