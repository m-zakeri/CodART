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

    EditableDataSet.java
    Created on 9. June 2002, 15:40
*/

package de.progra.charting.model;

import java.util.Arrays;

/**
 * This is an editable DataSet implementation.
 * @author mueller
 * @version 1.0
 */
public class EditableDataSet extends DefaultDataSet {
	
	/** Creates a new empty EditableDataSet with default axis binding. */
    public EditableDataSet() {
		super();
    }
    
    /** Creates a new empty EditableDataSet with the given
     * Axis binding.
     */
    public EditableDataSet(int axis) {
        super(axis);
    }
    
    /** Creates a new EditableDataSet with the given data and
     * the Axis binding.
     * @param data the DataSet values
     * @param columns the DataSet columns, the value and the column array should 
     * have the same length. The column array has to be sorted.
     * @param axis the Axis binding
     */
    public EditableDataSet(Object[] data, Object[] columns, int axis) {
        super(data, columns, axis);
    }
    
    /** Creates a new EditableDataSet with the given data and
     * the Axis binding.
     * @param data the DataSet values
     * @param columns the DataSet columns, the value and the column array should 
     * have the same length. The column array has to be sorted!
     * @param axis the Axis binding
     */
    public EditableDataSet(Object[] data, Object[] columns, int axis, String title) {
        super(data, columns, axis, title);
    }
	
	/** Inserts the given column/value pair at the right position, which is
	 * determined through a binary search. If the column is contained in the
	 * column set, setValueAt is called.
	 * @param value the value to be stored
	 * @param column the column value corresponding to value
	 */
	public void insertValue(Object value, Object column) {
		int insertIndex = Arrays.binarySearch(columns.toArray(), column);
		if(insertIndex >= 0) {
			setValueAt(insertIndex, value);
		} else {
			// As the column object wasn't found, the result is -( insertion point) - 1.
			insertIndex++;
			insertIndex *= -1;
			
			data.add(insertIndex, value);
			columns.add(insertIndex, column);
		}
	}
	
	public void removeValue(int index) {
		data.remove(index);
	}
}
