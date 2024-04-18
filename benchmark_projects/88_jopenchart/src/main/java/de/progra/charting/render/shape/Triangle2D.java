/*
    JOpenChart Java Charting Library and Toolkit
    Copyright (C) 2001  Sebastian MŸller
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

    Triangle2D.java
    Created on 11. September 2002, 22:01
*/

package de.progra.charting.render.shape;

import java.awt.geom.RectangularShape;
import java.awt.geom.Rectangle2D;
import java.awt.geom.PathIterator;
import java.awt.geom.AffineTransform;

/**
 * This class implements a triangular shape.
 * @author  smueller
 */
public class Triangle2D extends RectangularShape {
    
    protected double x = 0.0;
    
    protected double y = 0.0;
    
    protected double width = 0.0;
    
    protected double height = 0.0;
    
    protected boolean upsidedown = false;
    
    /** Creates a new instance of Triangle2D */
    public Triangle2D(double x, double y, double width, double height, boolean upsidedown) {
        setFrame(x, y, width, height);
        this.upsidedown = upsidedown;
    }
    
    public boolean contains(double param, double param1) {
        return false;
    }
    
    public boolean contains(double param, double param1, double param2, double param3) {
        return false;
    }
    
    public boolean intersects(double x, double y, double w, double h) {
        return false;
    }
    
    public Rectangle2D getBounds2D() {
        return new Rectangle2D.Double(x, y, width, height);
    }
    
    public double getHeight() {
        return height;
    }
    
    public PathIterator getPathIterator(AffineTransform affineTransform) {
        return new PathIterator() {
			int state = 0;
			int maxstate = 3;
            
			double[][] dcurrentSegment = {{x + width/2, y},
										  {x, y + height},
										  {x + width, y + height},
										  {0.0, 0.0} };

            
			double[][] ddowncurrentSegment = {{x, y},
                                              {x + width/2, y + height},
                                              {x + width, y},
                                              {0.0, 0.0} };
                                          
			int[] segment = { PathIterator.SEG_MOVETO, PathIterator.SEG_LINETO, PathIterator.SEG_LINETO, PathIterator.SEG_CLOSE};
			
			public int currentSegment(double[] coords) { 
                if(!upsidedown) {
                    coords[0] = dcurrentSegment[state][0];  
                    coords[1] = dcurrentSegment[state][1];
                } else {
                    coords[0] = ddowncurrentSegment[state][0];  
                    coords[1] = ddowncurrentSegment[state][1];
                }
				return segment[state];
			}
			
			public int currentSegment(float[] coords){ 
                if(!upsidedown) {
                    coords[0] = (float)dcurrentSegment[state][0];  
                    coords[1] = (float)dcurrentSegment[state][1];
                } else {
                    coords[0] = (float)ddowncurrentSegment[state][0];  
                    coords[1] = (float)ddowncurrentSegment[state][1];
                }
				return segment[state];
			} 
			
			public int getWindingRule() { return PathIterator.WIND_NON_ZERO; }
			public boolean isDone() { return (state == maxstate); } 
			public void next() { state++ ; } 
		};
    }
    
    public double getWidth() {
        return width;
    }
    
    public double getX() {
        return x;
    }
    
    public double getY() {
        return y;
    }
    
    public boolean isEmpty() {
        return (width<= 0.0 || height <= 0.0);
    }
    
    public void setFrame(double x, double y, double width, double height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
}
