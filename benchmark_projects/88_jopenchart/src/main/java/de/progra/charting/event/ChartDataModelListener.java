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

    ChartDataModelListener.java
    Created on 28. Juni 2001, 20:31
*/

package de.progra.charting.event;

/**
 * Defines the interface for a ChartDataModelListener
 * @author mueller
 * @version 1.0
 */
public interface ChartDataModelListener extends java.util.EventListener {

    /** This method is called, whenever an event is created.
     * @param evt the event object
     */    
    public void chartDataChanged(ChartDataModelEvent evt);
}

