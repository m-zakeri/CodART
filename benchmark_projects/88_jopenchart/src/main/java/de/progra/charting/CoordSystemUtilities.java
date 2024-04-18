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

    CoordSystemUtilities.java 
    Created on 4. April 2002, 22:28
 */

package de.progra.charting;

import java.awt.font.FontRenderContext;
import java.text.DecimalFormat;
import java.awt.geom.AffineTransform;
import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.font.TextLayout;
import de.progra.charting.model.ChartDataModelConstraints;
import de.progra.charting.model.ChartDataModel;

/**
 * This class provides some utility functions for a CoordSystem. They were
 * externalized to make the CoordSystem class clearer.
 * @author  mueller
 * @version 1.0
 */
public class CoordSystemUtilities {

	    /** used for the offset on the y axis for the size of a "tick"*/
    protected final int marginOffset = 6;
	
    protected CoordSystem c;
    protected ChartDataModelConstraints constraints;    
    protected ChartDataModelConstraints constraints2;
    protected ChartDataModel model;
    
    /** Creates a new instance of CoordSystemUtilities */
    public CoordSystemUtilities(CoordSystem coord, 
                                ChartDataModelConstraints constraints, 
                                ChartDataModelConstraints constraints2, 
                                ChartDataModel model) {
        c = coord;
        this.constraints = constraints;
        this.constraints2 = constraints2;
        this.model = model;
    }
    
    /** Computes the left margin. */
    public int computeLeftMargin() {
		double xmin = constraints.getMinimumColumnValue();
        double xmax = constraints.getMaximumColumnValue();
        
        if (xmin <= 0 && xmax > 0) {
		xmin = Math.abs(xmin);
		xmax = Math.abs(xmax);
		
		TextLayout layout = new TextLayout(c.getYAxisUnit(), c.getFont(), 
						   c.getFontRenderContext());
        
		// yaxis label width
		int maxlmargin = computeYAxisLabelWidth() + marginOffset; // + yaxis title width
        
		// unit width
		maxlmargin = Math.max(maxlmargin, (int) layout.getBounds().getWidth() + marginOffset);
        
        
		int margin = (int)(maxlmargin - (xmin / (xmin + xmax)) * (c.getBounds().getWidth() - c.getRightMargin()));
        
		margin += 5; // just for good looking
	
		if(margin < c.MINIMALMARGIN)
		    margin = c.MINIMALMARGIN;
        
		return margin;
	} else {
		return c.MINIMALMARGIN;
	}
    }
    
    /** Computes the right margin. */
    public int computeRightMargin() {
	TextLayout layout = new TextLayout(c.getXAxisUnit(), c.getFont(), 
					  	c.getFontRenderContext());
	return Math.max((int)(layout.getBounds().getWidth() + (double)c.ARROWLENGTH / 3) , c.ARROWLENGTH);
    }
    
    /** Computes the top margin. */
    public int computeTopMargin() {
	TextLayout layout = new TextLayout(c.getYAxisUnit(), c.getFont(), 
					   c.getFontRenderContext());
	return Math.max((int)(layout.getBounds().getHeight() + (double)c.ARROWLENGTH / 3 + layout.getDescent()), c.ARROWLENGTH);
    }
    
    /** Computes the bottom margin. */
    public int computeBottomMargin() {
	double ymin = constraints.getMinimumValue().doubleValue();
        double ymax = constraints.getMaximumValue().doubleValue();
	
        if (ymin <= 0 && ymax > 0) {
		ymin = Math.abs(ymin);
		ymax = Math.abs(ymax);
		
		TextLayout layout = new TextLayout(c.getXAxisUnit(), c.getFont(), 
						    c.getFontRenderContext());
        
		// xaxis label height
		int maxbmargin = computeXAxisLabelHeight() + marginOffset; // + xaxis title height
        
		// unit height
		maxbmargin = Math.max(maxbmargin, (int) layout.getBounds().getHeight() + marginOffset);
        
        
		int margin = (int)(maxbmargin - (ymin / (ymin + ymax)) * (c.getBounds().getHeight() - c.getTopMargin()));
        
		margin += 10; // just for good looking
	
		if(margin < c.MINIMALMARGIN)
		    margin = c.MINIMALMARGIN;
        
		return margin;
	} else {
		return c.MINIMALMARGIN;
	}
    }
    
    /** Computes the maximum height of all x-axis labels. */
    public int computeXAxisLabelHeight() {        
        double min = constraints.getMinimumColumnValue();
        double max = constraints.getMaximumColumnValue();
        double tick = ChartUtilities.calculateTickSpacing(min, max);
        double ypt = 0;
        
        int height = 0;
        
        if(constraints.getMinimumValue().doubleValue() > 0)
            ypt = constraints.getMinimumValue().doubleValue();
        else if(constraints.getMaximumValue().doubleValue() < 0)
            ypt = constraints.getMaximumValue().doubleValue();
        boolean paint = false;
        
        DecimalFormat df = c.getXDecimalFormat();
		FontRenderContext frc = c.getFontRenderContext();
        Font f = c.getFont();
        
        for(double d = min; d <= max; d += tick) {
            if(paint) {
                String sb = df.format(d);
                Rectangle2D r = f.getStringBounds(sb, frc);
                
                height = Math.max(height, (int)r.getHeight());                
            }
            paint = !paint;
        }
        
        return height;
    }
    
    /** Computes the maximum width of all y-axis labels. */
    public int computeYAxisLabelWidth() {
        double min = constraints.getMinimumValue().doubleValue();
        double max = constraints.getMaximumValue().doubleValue();
        double tick = ChartUtilities.calculateTickSpacing(min, max);
        double xpt = 0;
       
        int width = 0;
        
        // shift the y-axis according to the max and min x-values
        if(constraints.getMinimumColumnValue() > 0)
            xpt = constraints.getMinimumColumnValue();
        else if(constraints.getMaximumColumnValue() < 0 && c.getSecondYAxis() != null)
            xpt = constraints.getMaximumColumnValue();
        
        boolean paint = false;
        
        DecimalFormat df = c.getYDecimalFormat();
		FontRenderContext frc = c.getFontRenderContext();
        Font f = c.getFont();
		
        for(double d = min; d <= max; d += tick) {
            if(paint) {
                String sb = df.format(d);
                Rectangle2D r = f.getStringBounds(sb, frc);
                
                width = Math.max((int)r.getWidth(), width);
            }
            paint = !paint;
        }
        
        return width;
    }
    
    /** This method is called by paintDefault to paint the ticks on the
     * x-axis for numerical x-axis values.
     * @param g the Graphics2D context to paint in
     */
    public void drawNumericalXAxisTicks(Graphics2D g) {
        AffineTransform at = c.getTransform(CoordSystem.FIRST_YAXIS);
        
        double min = constraints.getMinimumColumnValue();
        double max = constraints.getMaximumColumnValue();
        double tick = ChartUtilities.calculateTickSpacing(min, max);
        double ypt = 0;
        
        if(constraints.getMinimumValue().doubleValue() > 0)
            ypt = constraints.getMinimumValue().doubleValue();
        else if(constraints.getMaximumValue().doubleValue() < 0)
            ypt = constraints.getMaximumValue().doubleValue();
        
        Point2D p = new Point2D.Double(0.0, 0.0);
        Point2D v;
        Line2D ticks = new Line2D.Double(0.0, 0.0, 0.0, 0.0);
        
		DecimalFormat df = c.getXDecimalFormat();
		FontRenderContext frc = c.getFontRenderContext();
        Font f = c.getFont();
        
		boolean paint = false;
		
        g.setFont(f);
        boolean paintLabels = c.isPaintLabels();
        
        for(double d = min; d <= max; d += tick) {
            p.setLocation(d, ypt);
            v = at.transform(p, null);
            
            ticks.setLine(v.getX(), v.getY() - marginOffset/2, v.getX(), v.getY() + marginOffset/2);
            g.draw(ticks);
            if(paint && paintLabels) {
                String sb = df.format(d);
                Rectangle2D r = f.getStringBounds(sb, frc);
                
                g.drawString(sb, (float)(v.getX() - r.getWidth() / 2),
							(float)(v.getY() + r.getHeight() + marginOffset));
            }
            paint = !paint;
        }
    }
    
    /** This method is called by paintDefault to paint the ticks on the
     * x-axis for non-numerical x-axis values..
     * @param g the Graphics2D context to paint in
     */
    public void drawXAxisTicks(Graphics2D g) {
        AffineTransform at = c.getTransform(CoordSystem.FIRST_YAXIS);
        
        int min = (int)constraints.getMinimumColumnValue();
        int max = (int)constraints.getMaximumColumnValue();
        double tick = 1.0;
        double ypt = 0;
        
        if(constraints.getMinimumValue().doubleValue() > 0)
            ypt = constraints.getMinimumValue().doubleValue();
        else if(constraints.getMaximumValue().doubleValue() < 0)
            ypt = constraints.getMaximumValue().doubleValue();
        
        Point2D p = new Point2D.Double(0.0, 0.0);
        Point2D v = null;
        Point2D oldv = null;
        
        Line2D ticks = new Line2D.Double(0.0, 0.0, 0.0, 0.0);
        
		DecimalFormat df = c.getXDecimalFormat();
		FontRenderContext frc = c.getFontRenderContext();
        Font f = c.getFont();
        
        boolean paint = false;
        boolean paintLabels = c.isPaintLabels();
        g.setFont(f);
        
        for(int i = min - 1; i < max; i++) {
            p.setLocation(i + 1, ypt);
            
            v = at.transform(p, null);
            
            ticks.setLine(v.getX(), v.getY() - marginOffset/2, v.getX(), v.getY() + marginOffset/2);
            
            if(i + 1 < max)
                g.draw(ticks);
            
            // Draw Strings between ticks
            if(oldv != null && paintLabels) {
                String sb = (String)model.getColumnValueAt(i);
                Rectangle2D r = f.getStringBounds(sb, frc);
                
                g.drawString(sb, (float)(oldv.getX()+(v.getX() - oldv.getX()) / 2 - r.getWidth() / 2),
                                (float)(v.getY() + r.getHeight() + marginOffset));
            }
            
            oldv = v;
        }
    }
    
    /** This method is called by paintDefault to paint the ticks on the
     * y-axis.
     * @param g the Graphics2D context in which to draw
     */
    public void drawYAxisTicks(Graphics2D g) {
        AffineTransform at = c.getTransform(CoordSystem.FIRST_YAXIS);
        
        double min = constraints.getMinimumValue().doubleValue();
        double max = constraints.getMaximumValue().doubleValue();
        double tick = ChartUtilities.calculateTickSpacing(min, max);
        double xpt = 0;
       
        // shift the y-axis according to the max and min x-values
        if(constraints.getMinimumColumnValue() > 0)
            xpt = constraints.getMinimumColumnValue();
        else if(constraints.getMaximumColumnValue() < 0 && c.getSecondYAxis() != null)
            xpt = constraints.getMaximumColumnValue();
        
        Point2D p = new Point2D.Double(0.0, 0.0);
        Point2D v;
        Line2D ticks = new Line2D.Double(0.0, 0.0, 0.0, 0.0);
        boolean paint = false;
        
        DecimalFormat df = c.getYDecimalFormat();
		FontRenderContext frc = c.getFontRenderContext();
        Font f = c.getFont();
		
		Color backupColor = g.getColor();
        g.setFont(f);
        boolean paintLabels = c.isPaintLabels();
        
        for(double d = min; d <= max; d += tick) {
            p.setLocation(xpt, d);
            v = at.transform(p, null);
            
            ticks.setLine(v.getX() - marginOffset/2, v.getY(), v.getX() + marginOffset/2, v.getY());
            
			g.draw(ticks);
			
			if (d != min && !c.isPaintOnlyTick()) {
                Line2D xax = getXAxisLine2D();
                ticks.setLine(v.getX() + marginOffset/2, v.getY(), xax.getX2(), v.getY());
                g.setColor(Color.lightGray);
                g.draw(ticks);
                g.setColor(backupColor);
            }
            
            if(paintLabels && (paint || !c.isPaintAltTick())) {
                String sb = df.format(d);
                Rectangle2D r = f.getStringBounds(sb, frc);
                
                g.drawString(sb, (float)(v.getX() - r.getWidth() - marginOffset),
                            (float)(v.getY() + r.getHeight() / 2));
            }
            paint = !paint;
        }
    }
    
    /** Computes the Line2D object of the x-axis using the DataConstraints.*/
    public Line2D getXAxisLine2D() {
        double ypt = 0.0;
        // shift the x-axis according to the max and min y-values
        if(constraints.getMinimumValue().doubleValue() > 0)
            ypt = constraints.getMinimumValue().doubleValue();
        else if(constraints.getMaximumValue().doubleValue() < 0)
            ypt = constraints.getMaximumValue().doubleValue();
        
        AffineTransform at = c.getTransform(CoordSystem.FIRST_YAXIS);
        
        Point2D l = at.transform(new Point2D.Double(constraints.getMinimumColumnValue(), ypt), null);
        Point2D r = at.transform(new Point2D.Double(constraints.getMaximumColumnValue(), ypt), null);
        
        return new Line2D.Double(l, r);
    }
    
    /** Computes the Line2D object of the y-axis using the DataConstraints.*/
    public Line2D getYAxisLine2D() {
        double xpt = 0.0;
        
        // shift the y-axis according to the max and min x-values
        if(constraints.getMinimumColumnValue() > 0)
            xpt = constraints.getMinimumColumnValue();
        else if(constraints.getMaximumColumnValue() < 0 && c.getSecondYAxis() != null)
            xpt = constraints.getMaximumColumnValue();
        
        AffineTransform at = c.getTransform(CoordSystem.FIRST_YAXIS);
        
        Point2D o = at.transform(new Point2D.Double(xpt, constraints.getMaximumValue().doubleValue()), null);
        Point2D u = at.transform(new Point2D.Double(xpt, constraints.getMinimumValue().doubleValue()), null);
        //System.out.println("** Y-Axis ("+o+", "+u+")");
        return new Line2D.Double(o, u);
    }
    
    /** Computes the Line2D object of the second y-axis using the DataConstraints.*/
    public Line2D getSecondYAxisLine2D() {
        double xpt = constraints2.getMaximumColumnValue();
        
        AffineTransform at = c.getTransform(CoordSystem.SECOND_YAXIS);
        
        Point2D o = at.transform(new Point2D.Double(xpt, constraints2.getMaximumValue().doubleValue()), null);
        Point2D u = at.transform(new Point2D.Double(xpt, constraints2.getMinimumValue().doubleValue()), null);
        
        return new Line2D.Double(o, u);
    }

}
