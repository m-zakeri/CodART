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

    PointToPixelTranslator.java
    Created on 1. Juli 2001, 01:15
 */

package de.progra.charting;

import java.awt.geom.*;

/**
 * This interface defines the methods necessary to translate data values
 * into pixel coordinates.
 * @author  mueller
 * @version 1.0
 * @deprecated
 */
public interface PointToPixelTranslator {

    /** Transforms a given value into an absolute pixel coordinate.
     * @param pt a <CODE>Point2D</CODE> object containing the value - column pair that should be painted
     * @return a <CODE>Point2D</CODE> object containing the x-y pair which define the absolute pixel-coordinate the values should be painted at.
     * @deprecated
     */
    public Point2D getPixelCoord(Point2D pt);
}

