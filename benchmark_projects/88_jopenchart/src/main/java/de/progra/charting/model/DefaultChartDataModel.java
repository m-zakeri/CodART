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

    DefaultChartDataModel.java
    Created on 28. Juni 2001, 20:41
*/

package de.progra.charting.model; 

import de.progra.charting.CoordSystem;
import de.progra.charting.ChartUtilities;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.TreeSet;
import java.util.Set;
import java.util.HashMap;

/**
 * Implements a default ChartModel. It uses a DataSet[] and the columns
 * are numeric. It's purely read-only.
 * @author  mueller
 * @version 1.0
 */
public class DefaultChartDataModel extends AbstractChartDataModel {
    
    /** The sorted x-axis values used for calculating the constraints. */
    protected TreeSet columnSet = new TreeSet();
    
    /** The DataSet list.*/
    protected ArrayList data = new ArrayList();
    
    /** A HashMap containing the ordered data used for calculating the constraints. */
    protected HashMap valuesbyaxis = new HashMap();
    
    /** The constraints for the first and second y-axes.*/
    protected ChartDataModelConstraints constraints1, constraints2;
    
    /** Creates a new empty DefaultChartDataModel. 
     */
    public DefaultChartDataModel() {
        TreeSet set1 = new TreeSet();
        valuesbyaxis.put(new Integer(CoordSystem.FIRST_YAXIS), set1);
        TreeSet set2 = new TreeSet();
        valuesbyaxis.put(new Integer(CoordSystem.SECOND_YAXIS), set2);    
        constraints1 = new DefaultChartDataModelConstraints(this, CoordSystem.FIRST_YAXIS);
        constraints2 = new DefaultChartDataModelConstraints(this, CoordSystem.SECOND_YAXIS);
    }
    
    /** Creates new DefaultChartDataModel with the default axis binding.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and the columns should
     * be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public DefaultChartDataModel(Number[][] data, 
                                 double[] columns, 
                                 String[] rows) {
        this();
        
        columnSet.addAll(Arrays.asList(ChartUtilities.transformArray(columns)));
        
        TreeSet set = (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
                
        ChartUtilities.addDataToSet(set, data);
        trimSet(set);
        
        for(int i = 0; i < data.length; i++) {
            this.data.add(new DefaultDataSet(data[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));            
        }
    }
  
    /** Creates new DefaultChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public DefaultChartDataModel(int[][] data, 
                                 double[] columns,
                                 String[] rows) {
        this();
        
        Number[][] numdata = ChartUtilities.transformArray(data);
		
        columnSet.addAll(Arrays.asList(ChartUtilities.transformArray(columns)));
        
        TreeSet set = 
            (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
        
        ChartUtilities.addDataToSet(set, numdata);

        trimSet(set);
        
        for(int i = 0; i < data.length; i++) {
            this.data.add(new DefaultDataSet(numdata[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));
        }
    }
    
    /** Creates new DefaultChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public DefaultChartDataModel(double[][] data, 
                                 double[] columns,
                                 String[] rows) {
        this();
        
        Number[][] numdata = ChartUtilities.transformArray(data);
		
        columnSet.addAll(Arrays.asList(ChartUtilities.transformArray(columns)));
        
        TreeSet set = 
            (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
        
        ChartUtilities.addDataToSet(set, numdata);
        trimSet(set);
        for(int i = 0; i < data.length; i++) {
            this.data.add(new DefaultDataSet(numdata[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));
        }
    }
    
    /** Creates a new DefaultChartDataModel using the
     * given array of DataSets, effectively enabling the creation
     * of DataModels with differently sized DataSets.
     * @param ds the array of DataSets to be used.
     */
    public DefaultChartDataModel(DataSet[] ds) {
        this();
		
        TreeSet set;
        for(int i = 0; i < ds.length; i++) {
			data.add(ds[i]);
            set = (TreeSet)valuesbyaxis.get(new Integer(ds[i].getYAxis()));
            for(int j = 0; j < ds[i].getDataSetLength(); j++) {
                columnSet.add(ds[i].getColumnValueAt(j));                
                set.add(ds[i].getValueAt(j));
                
                trimSet(set);
            }
        }
    }

    /** Returns the length of a certain dataset.
     * @param set the DataSet
     * @return the length of the DataSet
     */
    public int getDataSetLength(int set) {
        return ((DataSet)data.get(set)).getDataSetLength();
    }
    
    /** Returns the total amount of datasets.
     * @return the amount of DataSets
     */
    public int getDataSetNumber() {
        return data.size();
    }
    
    /** Returns the title of the DataSet. This is the number of
     * the DataSet per default.
     * @param set the DataSet index
     * @return the String title
     */
    public String getDataSetName(int set) {
        return ((DataSet)data.get(set)).getTitle();
    }
    
    /** Returns the axis binding for a DataSet
     * @param set the DataSet index
     * @return an axis binding constant
     */
    public int getAxisBinding(int set) {
        return ((DataSet)data.get(set)).getYAxis();
    }
    
    /** Returns true if the columns are numeric.
     * @return <CODE>true</CODE>
     */
    public boolean isColumnNumeric() {
        return true;
    }    
    
    /** Returns the class of the column values.
     * @return <CODE>Double.class</CODE>
     */
    public Class getColumnClass() {
        return Double.class;
    }
    
    /** Returns the Value in a specific dataset at a certain index.      *
     * @param set the DataSet index
     * @param index the value index
     * @return the Number value at the specified position
     */
    public Number getValueAt(int set, int index) {
        return (Number)((DataSet)data.get(set)).getValueAt(index);
    }
    

    /** Use getColumnValue(int set, int col) instead, because DefaultChartDataModel
     * can contain DataSets with different lengths and column values.
     * @return null
     */
    public Object getColumnValueAt(int col) {
        return null;
    }
    
    /** Returns a specific column value.
     * @return the column value or <code>null</code> if the column doesn't exist.
     * @param col the column index
     * @param set the DataSet of which the column value is desired
     */
    public Object getColumnValueAt(int set, int col) {
		// PENDING: Why do we create a new Double here?
        if(col < getDataSetLength(set))
            return new Double(((Number)((DataSet)data.get(set)).getColumnValueAt(col)).doubleValue());
        else
            return null;
    }
    
     
    /** Returns a ChartDataModelConstraints Object for a given axis.
     * This way, there are different constraints for the first and for
     * the second y-axis. If the model is empty, the maximum values are 1 and
     * the minimum values are 0, thus enabling proper rendering.
     * @param axis the axis constant.
     * @return a ChartDataModelConstraints object with the constraints
     * for the specified y-axis.
     */
    public ChartDataModelConstraints getChartDataModelConstraints(final int axis) {
        if(axis == CoordSystem.FIRST_YAXIS)
            return constraints1;
        else
            return constraints2;
    }
    
    /** Sets the ChartDataModelConstraints object for the given
     * axis binding.
     * @param axis the Axis constant
     * @param constraints the ChartDataModelConstraints object
     * @return a ChartDataModelConstraints object.
     */
    public void setChartDataModelConstraints(int axis, ChartDataModelConstraints constraints) {
        if(axis == CoordSystem.FIRST_YAXIS)
            constraints1 = constraints;
        else
            constraints2 = constraints;
    }
    
	/** Removes infinite and NaN values from a TreeSet. Called with the TreeSet
	 * containing all values. If asymptotic functions are plotted, infinite values
	 * are the max / min values, resulting in bogus point-to-pixel rations. Therefore,
	 * these values are omitted from these calculations.
	 */
    protected void trimSet(TreeSet s) {
       while(((Number)s.first()).doubleValue() == Double.NEGATIVE_INFINITY) {
           s.remove(s.first());
       }
       double last = ((Number)s.last()).doubleValue();

       while(last == Double.POSITIVE_INFINITY
            || last != last) {
                s.remove(s.last());
                last = ((Number)s.last()).doubleValue();
       }
    }
    
    /** Returns an ordered set of all data values for the specified axis.
     * This is called by the ChartDataModelConstraints classes.
     */
    protected TreeSet getOrderedValues(int axis) {
        return (TreeSet)valuesbyaxis.get(new Integer(axis));
    }
    
    /** Returns the first ordered column value for use by the ChartDataModelConstraints. */
    protected double getFirstColumnValue() {
        return ((Number)columnSet.first()).doubleValue();
    }
    
    /** Returns the last ordered column value for use by the ChartDataModelConstraints. */
    protected double getLastColumnValue() {
        return ((Number)columnSet.last()).doubleValue();
    }
}
