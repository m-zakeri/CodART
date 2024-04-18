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

    EditableChartDataModel.java
    Created on 9. June 2002, 15:46
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
 * Implements an editable ChartModel. It uses a vector of DataSets and the columns
 * are numeric.
 * @author  mueller
 * @version 1.0
 */
public class EditableChartDataModel extends DefaultChartDataModel {

    /** Creates a new empty EditableChartDataModel. 
     */
    public EditableChartDataModel() {
        super();
    }
    
    /** Creates new EditableChartDataModel with the default axis binding.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and the columns should
     * be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public EditableChartDataModel(Number[][] data, 
                                 double[] columns, 
                                 String[] rows) {
        this();
        
        columnSet.addAll(Arrays.asList(ChartUtilities.transformArray(columns)));
        
        TreeSet set = (TreeSet)valuesbyaxis.get(new Integer(CoordSystem.FIRST_YAXIS));
                
        ChartUtilities.addDataToSet(set, data);
        trimSet(set);
        
        for(int i = 0; i < data.length; i++) {
            this.data.add(new EditableDataSet(data[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));            
        }
    }

    /** Creates new EditableChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public EditableChartDataModel(int[][] data, 
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
            this.data.add(new EditableDataSet(numdata[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));
        }
    }
    
    /** Creates new EditableChartDataModel.
     * @param data the array of values. The first index specifies the
     * datasets, the last one is the value index.
     * @param columns the array of x-axis values. The length of the
     * datasets and the length of the column should be equal and
     * the columns should be ordered.
     * @param rows the array of DataSet titles. It has to have the same
     * length as the number of DataSets.
     */
    public EditableChartDataModel(double[][] data, 
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
            this.data.add(new EditableDataSet(numdata[i], 
                                              ChartUtilities.transformArray(columns), 
                                              CoordSystem.FIRST_YAXIS,
                                              rows[i]));
        }
    }
    
    /** Creates a new EditableChartDataModel using the
     * given array of EditableDataSets, effectively enabling the creation
     * of DataModels with differently sized DataSets.
     * @param ds the array of DataSets to be used.
     */
    public EditableChartDataModel(EditableDataSet[] ds) {
        super(ds);
    }
	
	/** Sets the axis binding for a given DataSet.
     * @param set the DataSet
     * @param axis the Axis binding
     */
    public void setAxisBinding(int set, int axis) {
    }
	
    /** Sets the value in a given DataSet.
     * @param set the DataSet in which the value should be set
     * @param index the index in the DataSet where the value should be stored
     * @param value the value object
     */
    public void setValueAt(int set, int index, Object value) {
    }
	
    /** Inserts a value together with its column value at the right position. The
	 * right index is determined by performing a binary search on the columns in the
	 * DataSet. Fires a ChartDataModelChangedEvent.
     * @param set the DataSet in which the value should be set
     * @param value the value object
	 * @param column the column value object
     */
    public void insertValue(int set, Object value, Object column) {
		((EditableDataSet)data.get(set)).insertValue(value, column);
		columnSet.add(column);
        TreeSet treeset = (TreeSet)valuesbyaxis.get(new Integer(getAxisBinding(set)));
		treeset.add(value);
        trimSet(treeset);
		
		fireChartDataModelChangedEvent(this);
    }
	
	/** Removes the value in a given DataSet.
     * @param set the DataSet in which the value should be set
     * @param index the index in the DataSet where the value should be stored
     */
    public void removeValueAt(int set, int index) {
    }
	
	public void removeDataSet(int set) {}
	
	public void addDataSet(EditableDataSet ds) {}
}
