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

    Axis.java
    Created on 30. Juni 2001, 22:27
 */

package de.progra.charting;

import de.progra.charting.model.ChartDataModelConstraints;

/**
 * The CoordSystem contains two or possibly three Axis objects for the x-axis
 * and the at most two y-axis.
 * @author mueller
 * @version 1.0
 */
public class Axis {

    /** Defines a horizontal x-axis. */
    public final static int HORIZONTAL = 1;
    
    /** Defines a vertical y-axis. */
    public final static int VERTICAL = 2;
    
    /** Defines a logarithmic scale. */
    public final static int LOGARITHMIC = 3;
    
    /** Defines a linear scale. */
    public final static int LINEAR = 4;
    
    /** The axis' alignment. */
    private int align = HORIZONTAL;
    
    ChartDataModelConstraints constraints;
    
    int length = Integer.MAX_VALUE;
    
    /** Creates new Axis.
     * @param align the alignment of the axis.
     * @param c the ChartDataModelConstraints 
     */
    public Axis(int align, ChartDataModelConstraints c) {
                    
        if(align == HORIZONTAL || align == VERTICAL)
            this.align = align;
        
        this.constraints = c;
    }
    
    /** Returns the alignment of the axis.
     * @return the alignment constant: <CODE>Axis.VERTICAL</CODE> or <CODE>Axis.HORIZONTAL</CODE>
     */
    public int getAlignment() {
        return align;
    }

    /** Sets the Pixel length of the axis.
     * @param length the length in pixel
     */
    public void setLength(int length) {
        this.length = length;
    }
    
    /** Returns length of the axis in pixels.
     * @return the length in pixels
     */
    public int getLength() {
        return length;
    }
    
    /** Returns the point on the axis for a specific value.
     * If the axis is a x-axis and the column values are not numeric,
     * this isn't needed since then the axis can be divided into
     * equally long parts. This is a relative pixel distance to
     * the starting pixel of the axis.
     * @param value the double value to compute the pixel distance for
     * @return the pixel distance for the given value relative to the start of the axis
     */
    public double getPixelForValue(double value) {
        // if scale == linear
        if(getAlignment() == Axis.VERTICAL) {
            return (value - constraints.getMinimumValue().doubleValue()) / 
                    getPointToPixelRatio();
        } else {
            return (value - constraints.getMinimumColumnValue()) /  
                   getPointToPixelRatio();
        }
    }
    
    /** Returns the ratio between a value unit and the screen pixels.
     * This is only useful for linear scales.
     * @return the ratio points / pixel length for the axis.
     */
    public double getPointToPixelRatio() {
        //System.out.println("** constraints.getMaximumColumnValue() = "+constraints.getMaximumColumnValue());
        if(getAlignment() == Axis.VERTICAL) {
            
            return (constraints.getMaximumValue().doubleValue() - 
                    constraints.getMinimumValue().doubleValue()) / 
                    length;
        }
        else
            return (constraints.getMaximumColumnValue() - 
                    constraints.getMinimumColumnValue()) / 
                    length;
    }
}
