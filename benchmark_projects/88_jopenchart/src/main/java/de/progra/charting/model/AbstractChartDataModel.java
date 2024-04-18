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

    AbstractChartDataModel.java
    Created on 28. Juni 2001, 18:58
*/

package de.progra.charting.model;

import de.progra.charting.event.ChartDataModelListener;
import de.progra.charting.event.ChartDataModelEvent;
import javax.swing.event.EventListenerList;
import de.progra.charting.CoordSystem;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.TreeSet;
import java.util.Set;
import java.util.HashMap;

/**
 * This class implements the event-handling methods for a chart model.
 * @author  mueller
 * @version 1.0
 */
public abstract class AbstractChartDataModel implements ChartDataModel {
    
    /** The listener list. */
    protected EventListenerList listener = new EventListenerList();

    /** Flag defining the automatic scaling of max and min values. */
    protected boolean autoscale = false;

    /** Flag defining the manual scaling of max and min values. */
    protected boolean manualscale = false;

    /** Maximum and minimum column values to be displayed. */
    protected double maxcolumn, mincolumn;

    /** Maximum and minimum values to be displayed. */
    protected Number maxvalue, minvalue;
    
    /** Creates new AbstractChartDataModel */
    public AbstractChartDataModel() {
    }

    /** Removes a ChartDataModelListener.
     * @param l the ChartDataListener
     */
    public void removeChartDataModelListener(ChartDataModelListener l) {
        listener.remove(ChartDataModelListener.class, l);
    }
    
    /** Adds a ChartDataModelListener.
     * @param l the ChartDataModelListener
     */
    public void addChartDataModelListener(ChartDataModelListener l) {
        listener.add(ChartDataModelListener.class, l);
    }
    
    /** Determines if the column values are numeric.
     * @return <CODE>false</CODE> per default
     */
    public boolean isColumnNumeric() {
        return false;
    }    
    
    /** Provides an empty implementation for not-editable DataModels.
     * @param set the DataSet in which the value should be set
     * @param index the index in the DataSet where the value should be stored
     * @param value the value object
     */
    public void setValueAt(int set, int index, Object value) {
    }
    
    /** Returns the class of the column values.
     * @return <CODE>Object.class</CODE> per default
     */
    public Class getColumnClass() {
        return Object.class;
    }
    
    /** Promotes a new ChartDataModelEvent.
     * @param src the source object of the event.
     */
    public void fireChartDataModelChangedEvent(Object src) {
        ChartDataModelEvent e = new ChartDataModelEvent(src);
        Object[] ls = listener.getListenerList();
        for (int i = (ls.length - 2); i >= 0; i-=2) {
            if (ls[i] == ChartDataModelListener.class) {
                ((ChartDataModelListener)ls[i + 1]).chartDataChanged(e);
            }
        }
    }
    
    /** Returns the Axis Binding for a specific DataSet, ie the Axis on
     * which the DataSet should be plotted
     * @param set the DataSet whose Axis binding should be determined
     * @return <code>DataSet.FIRST_YAXIS</code> by default.
     */
    public int getAxisBinding(int set) {
        return CoordSystem.FIRST_YAXIS;
    }
    
    /** Provides a default empty implementation.
     * @param set the DataSet
     * @param axis the Axis binding
     */
    public void setAxisBinding(int set, int axis) {
    }    
    
    public void setAutoScale(boolean b) {
        autoscale = b;
    }
    
    public boolean isAutoScale() {
        return autoscale;
    }

    /** Enables the manual axis scaling. Set the desired
     * maximum and minimum values using the setMaximum...Value
     * functions.
     */
    public void setManualScale(boolean b) {
        manualscale = b;
    }

    /** Returns true if the manual axis scaling is enabled. This overrides
     * the enabled automatic axis scaling.
     */
    public boolean isManualScale() {
        return manualscale;
    }

    /** Sets the maximum x-axis value. */
    public void setMaximumColumnValue(double d) {
        maxcolumn = d;
    }

    /** Sets the minimum x-axis value. */
    public void setMinimumColumnValue(double d) {
        mincolumn = d;
    }

    /** Sets the maximum y-axis value. */
    public void setMaximumValue(Number n) {
        maxvalue = n;
    }

    /** Sets the minimum y-axis value. */
    public void setMinimumValue(Number n) {
        minvalue = n;
    }

    public double getManualMaximumColumnValue() {
        return maxcolumn;
    }

	public double getManualMinimumColumnValue() {
        return mincolumn;
    }

    public Number getManualMaximumValue() {
        return maxvalue;
    }

	public Number getManualMinimumValue() {
        return minvalue;
    }
	
    /** Returns the title of the DataSet.
     * @param set the DataSet identifier
     * @return the the number of
     * the DataSet per default.
     */
    public String getDataSetName(int set) {
        return "Dataset "+set;
    }
    
    /** Compares this ChartDataModel with another object. 
     * @param o the object to compare with
     * @return true, if o is an AbstractChartDataModel, the number of
     * DataSets is equal and all DataSet names and column values are equal.
     */
    public boolean equals(Object o) {
        if(o == null)
            return false;
        try {
            AbstractChartDataModel model = (AbstractChartDataModel)o;
            
            if(getDataSetNumber() != model.getDataSetNumber()) {
                return false;
            }
            
            for(int i = 0; i < getDataSetNumber(); i++) {
                if(!getDataSetName(i).equals(model.getDataSetName(i))) {
                    return false;
                }
                
                for(int j = 0; j < getDataSetLength(j); j++) {
                    if(!getColumnValueAt(j).equals(model.getColumnValueAt(j))) {
                        return false;
                    }
                }
            }
        } catch(Exception e) { return false;}
        
        return true;
    }
    
    protected abstract TreeSet getOrderedValues(int axis);
    
    protected abstract double getFirstColumnValue();
    
    protected abstract double getLastColumnValue();
}
