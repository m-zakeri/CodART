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

    ObjectColumnChartDataModel.java
    Created on 7. August 2001, 17:27
*/

package de.progra.charting.model;

import de.progra.charting.CoordSystem;
import de.progra.charting.ChartUtilities;
import java.util.TreeSet;
import java.util.Set;
import java.util.HashMap;

/**
 * The ObjectChartDataModel implements a ChartDataModel for Charts,
 * which have e.g. String values on the x-axis. This is especially useful
 * for Barcharts and also for Piecharts, although those don't exactly have
 * an x-axis.
 * @author  mueller
 * @version 1.0
 */
public class ObjectChartDataModel extends AbstractChartDataModel {
    
    /** The x-axis values. */
    protected Object[] columns;
        
    /** The data values.*/
    protected DataSet[] data;
    
    /** A HashMap containing the ordered data per axis. */
    protected HashMap valuesbyaxis = new HashMap();
    
    /** The constraints for the first and second y-axes.*/
    protected ChartDataModelConstraints constraints1, constraints2;
    
    /** Creates a new empty DefaultChartDataModel. 
     * Initializes all Objects and Arrays as empty ones.
     */
    public ObjectChartDataModel() {
        data = new DefaultDataSet[0];
        columns = new Object[0];
        
        TreeSet set1 = new TreeSet();
        valuesbyaxis.put(new Integer(CoordSystem.FIRST_YAXIS), set1);
        
        TreeSet set2 = new TreeSet();
        valuesbyaxis.put(new Integer(CoordSystem.SECOND_YAXIS), set2);
        
        constraints1 = new DefaultChartDataModelConstraints(this, CoordSystem.FIRST_YAXIS, false);
        constraints2 = new DefaultChartDataModelConstraints(this, CoordSystem.SECOND_YAXIS, false);
    }
    
    /** Creates new ObjectChartDataModel with the default axis binding.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and the columns should
     * be ordered.
     * @param rows the DataSet titles
     */
    public ObjectChartDataModel(Number[][] data, Object[] columns, String rows[]) {
        this();
        
        this.columns = columns;
        
        this.data = new DefaultDataSet[data.length];
        
        TreeSet set = 
            (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
                
        ChartUtilities.addDataToSet(set, data);
        
        for(int i = 0; i < data.length; i++) {
            this.data[i] = new DefaultDataSet(data[i], 
                                              columns, 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]);            
        }
    }
  
    /** Creates new ObjectChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     * @param rows the DataSet titles
     */
    public ObjectChartDataModel(int[][] data, Object[] columns, String[] rows) {
        this();
        
        Number[][] numdata = ChartUtilities.transformArray(data);
        
        this.columns = columns;
        
        this.data = new DefaultDataSet[data.length];
        
        TreeSet set = 
            (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
        
        ChartUtilities.addDataToSet(set, numdata);
        
        for(int i = 0; i < data.length; i++) {
            this.data[i] = new DefaultDataSet(numdata[i], 
                                              columns, 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]);
        }
    }
    
    
    /** Creates new ObjectChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     *@param rows the DataSet titles
     */
    public ObjectChartDataModel(double[][] data, Object[] columns, String[] rows) {
        this();
        
        Number[][] numdata = ChartUtilities.transformArray(data);
        
        this.columns = columns;
        
        this.data = new DefaultDataSet[data.length];
        
        TreeSet set = 
            (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
        
        ChartUtilities.addDataToSet(set, numdata);
        
        for(int i = 0; i < data.length; i++) {
            this.data[i] = new DefaultDataSet(numdata[i], 
                                              columns, 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]);
        }
    }
    
    /** Creates a new ObjectChartDataModel using the
     * given array of DataSets, effectively enabling the creation
     * of DataModels with differently sized DataSets. Internally, the DataSets
	 * are transformed into equally sized DataSets, where the missing data fields
	 * are filled with Double.NaN.
     * @param ds the array of DataSets to be used.
     * @param columns the array of column values. This needs to be supplied,
     * because using Objects as x-axis values you need to have an ordered 
     * superset of all column values especially if different DataSets only
     * contain some column values
     */
    public ObjectChartDataModel(DataSet[] ds, Object[] columns) {
        this();
        data = ds;
        this.columns = columns;
        
        TreeSet set;
			
        HashMap map = new HashMap();
        
        for(int i = 0; i < ds.length; i++) {
            map.clear();
            Number[] numdata = new Number[columns.length];
            
            for(int j = 0; j < columns.length; j++)
                map.put(columns[j], new Double(Double.NaN));
			
            set = (TreeSet)valuesbyaxis.get(new Integer(ds[i].getYAxis()));
            
            for(int j = 0; j < ds[i].getDataSetLength(); j++) {
                map.put(ds[i].getColumnValueAt(j), ds[i].getValueAt(j));
                set.add(ds[i].getValueAt(j));
            }
					
            for(int j = 0; j < columns.length; j++) {
                numdata[j] = (Number)map.get(columns[j]);
            }
			
            data[i] = new DefaultDataSet(numdata, 
                                         columns, 
                                         CoordSystem.FIRST_YAXIS,
                                         ds[i].getTitle());
        }
    }

    /** Returns the length of a certain dataset.
     * @param set the DataSet index
     * @return the DataSet length
     */
    public int getDataSetLength(int set) {
        return data[set].getDataSetLength();
    }
    
    /** Returns the total amount of datasets.
     * @return the amount of DataSet
     */
    public int getDataSetNumber() {
        return data.length;
    }
    
    
    /** Returns the title of the DataSet. This is the number of
     * the DataSet per default.
     * @param set the DataSet index
     * @return the String title
     */
    public String getDataSetName(int set) {
        return data[set].getTitle();
    }
    
    /** Returns the axis to which a DataSet is attached
     * @param set the DataSet index
     * @return the axis constant
     */
    public int getAxisBinding(int set) {
        return data[set].getYAxis();
    }
    
    /** Returns the Value in a specific dataset at a certain index.
     * @param set the DataSet index
     * @param index the value index
     * @return the Number value
     */
    public Number getValueAt(int set, int index) {
        return (Number)data[set].getValueAt(index);
    }
    
    /** Returns a ChartDataModelConstraints Object for a given axis.
     * This way, there are different constraints for the first and for
     * the second y-axis. If the model is empty, the maximum values are 1 and
     * the minimum values are 0, thus enabling proper rendering.
     * @param axis the axis constant
     * @return the ChartDataModelConstraints for the defined y-axis
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
    public void setChartDataModelConstraints(int axis, ChartDataModelConstraints constraints)  {
        if(axis == CoordSystem.FIRST_YAXIS)
            constraints1 = constraints;
        else
            constraints2 = constraints;
    }

    /** Returns a specific column value.
     * @return the column value or <code>null</code> if the column doesn't exist.
     * @param col the column index
     */
    public Object getColumnValueAt(int col) {
        if(col < columns.length)
            return columns[col];
        else
            return null;
    }    
    
    /** Calls getColumnValueAt(int col).
     * @return the column value or <code>null</code> if the column doesn't exist.
     * @param col the column index
     */
    public Object getColumnValueAt(int set, int col) {        
       return getColumnValueAt(col);
    }   
    
    /** Returns an ordered set of all data values for the specified axis.
     * This is called by the ChartDataModelConstraints classes.
     */
    protected TreeSet getOrderedValues(int axis) {
        return (TreeSet)valuesbyaxis.get(new Integer(axis));
    }
    
    /** Is called by the ChartDataModelConstraints Object to compute the minimum column value.
     * @return Returns 0.0.
     */
    protected double getFirstColumnValue() {
        return 0.0;
    }
    
    /** Is called by the ChartDataModelConstraints Object to compute the maximum column value.
     * @return Returns <code>columns.length</code>.
     */
    protected double getLastColumnValue() {
        return Math.max((double)columns.length, 1.0);
    }
}
