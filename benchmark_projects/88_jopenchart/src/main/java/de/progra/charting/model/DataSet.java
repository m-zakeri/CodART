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

    DataSet.java
    Created on 1. Juli 2001, 21:04
*/

package de.progra.charting.model;

/**
 * An interface used to encapsulate the DataSets in a ChartDataModel.
 * It's main objective is to store a DataSet to Axis binding.
 * @author mueller
 * @version 1.0
 */
public interface DataSet {
    
    /** Determines the length of the DataSet
     * @return an int equal to the length
     */    
    public int getDataSetLength();
    
    /** Determines the column value at a specific DataSet index.
     * @param index the column index
     * @return an Object with the column value
     */    
    public Object getColumnValueAt(int index);
    
    /** Sets the column value
     * @param index the column index
     * @param col the column value
     */    
    public void setColumnValueAt(int index, Object col);
    
    /** Returns a value in the DataSet
     * @param index the DataSet index
     * @return an Object with the value.
     */    
    public Object getValueAt(int index);
    
    /** Stores a value in the DataSet.
     * @param index the DataSet index
     * @param val the value to be stored
     */    
    public void setValueAt(int index, Object val);
    
    /** Sets the axis this DataSet is attached to.
     * @param yaxis the axis constant.
     */    
    public void setYAxis(int yaxis);
    
    /** Returns the axis to which this DataSet is attached.
     * @return the axis constant
     */    
    public int getYAxis();
    
    /** Returns the Title of the DataSet.
     * @return a String containing the DataSet's title.
     */    
    public String getTitle();
    
    /** Sets the DataSet's title.
     * @param title the String title for the DataSet
     */    
    public void setTitle(String title);
}
