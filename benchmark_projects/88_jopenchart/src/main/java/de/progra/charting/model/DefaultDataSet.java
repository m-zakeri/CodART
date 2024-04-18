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

    DefaultDataSet.java
    Created on 1. Juli 2001, 21:20
*/

package de.progra.charting.model;

import de.progra.charting.CoordSystem;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * This is a default DataSet implementation.
 * @author mueller
 * @version 1.0
 */
public class DefaultDataSet implements DataSet {

    protected ArrayList data = new ArrayList();
    
    protected ArrayList columns = new ArrayList();
    
    protected int axis = CoordSystem.FIRST_YAXIS;
    
    protected String title = "";
    
    /** Creates a new empty DefaultDataSet with default axis binding. */
    public DefaultDataSet() {
    }
    
    /** Creates a new empty DefaultDataSet with the given
     * Axis binding.
     */
    public DefaultDataSet(int axis) {
        this();
        setYAxis(axis);
    }
    
    /** Creates a new DefaultDataSet with the given data and
     * the Axis binding.
     * @param data the DataSet values
     * @param columns the DataSet columns, the value and the column array should 
     * have the same length. The columns have to be sorted.
     * @param axis the Axis binding
     */
    public DefaultDataSet(Object[] data, Object[] columns, int axis) {
        this(axis);
        this.data.addAll(Arrays.asList(data));
        this.columns.addAll(Arrays.asList(columns));
    }
    
    /** Creates a new DefaultDataSet with the given data and
     * the Axis binding.
     * @param data the DataSet values
     * @param columns the DataSet columns, the value and the column array should 
     * have the same length. The columns have to be sorted.
     * @param axis the Axis binding
     */
    public DefaultDataSet(Object[] data, Object[] columns, int axis, String title) {
        this(data, columns, axis);
        this.title = title;
    }

    /** Returns the length of this data set, ie the minimum of the columns and the
     * data array length.
     * @return the length of the DataSet
     */
    public int getDataSetLength() {
        return Math.min(data.size(), columns.size());
    }
    
    /** Returns the data at the specified index.
     * @param index the data index
     * @return the Object value
     */
    public Object getValueAt(int index) {
        return data.get(index);
    }
    
    /** Returns the Axis binding.
     * @return the axis binding constant
     */
    public int getYAxis() {
        return axis;
    }
    
    /** Sets the given value at the specified index.
     * @param index the value index
     * @param val the Object value
     */
    public void setValueAt(int index, Object val) {
        data.set(index, val);
    }
    
    /** Sets the Axis binding.
     * @param yaxis the axis binding constant
     */
    public void setYAxis(int yaxis) {
		if(yaxis == CoordSystem.FIRST_YAXIS || yaxis == CoordSystem.SECOND_YAXIS)
			axis = yaxis;
    }
    
    /** Returns the column value.
     * @param index the column index
     * @return the column value
     */
    public Object getColumnValueAt(int index) {
        return columns.get(index);
    }
    
    /** Sets a column value.
     * @param index the column index
     * @param col the column value
     */
    public void setColumnValueAt(int index, Object col) {
        columns.set(index, col);
    }
    
    /** Sets the title of this DataSet.
     * @param title the String title
     */
    public void setTitle(String title) {
        this.title = title;
    }
    
    /** Returns the title of this DataSet.
     * @return the String title
     */
    public String getTitle() {
        return title;
    }    
}