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

    CoordSystem.java
    Created on 26. Juni 2001, 22:49
 */

package de.progra.charting;

import de.progra.charting.render.AbstractRenderer;
import de.progra.charting.render.ChartRenderingHints;
import java.awt.Rectangle;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.awt.geom.Line2D;
import java.awt.geom.AffineTransform;
import java.awt.Graphics2D;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Font;
import java.awt.font.FontRenderContext;
import java.awt.font.TextLayout;
import java.text.DecimalFormat;
import de.progra.charting.model.ChartDataModel;
import de.progra.charting.model.ChartDataModelConstraints;


/** This class defines a coordinate system. The CoordSystem class computes
 * an AffineTransform for each y-axis, which translates the user space
 * coordinates (ie. the data value coordinates) into pixel space coordinates.
 * These AffineTransform classes make the PixelToPointTranslator obsolete,
 * since it provides more flexibility. <code>getDefaultTransform</code> always
 * computes the default transformation, whereas you can set another
 * transformation via <code>setTransform</code>. This will be used to implement
 * zooming and panning in the Swing classes.<p>
 * All classes incl. this one, which render data will use the transformations
 * to translate the coordinates. The transformations are not set up on
 * instantiation of a CoordSystem, instead they're computed when setBounds
 * is called, because they need this information of course. Afterwards you
 * can set your own transformation or even better you can manipulate the
 * existing ones by pre- or postconcatenating another AffineTransform.
 */
public class CoordSystem extends AbstractRenderer {
    
	/** The x-axis caption string. */
    protected String xaxis_unit = "x";
	/** The y-axis caption string. */
    protected String yaxis_unit = "y";
    
	/** The Font used in the CoordSystem. */
    protected Font font = new Font("sans", Font.PLAIN, 9);
    
    /** FontRenderContext used througout the CoordSystem*/
    protected final FontRenderContext frc = new FontRenderContext(null, false, false);
    /** DecimalFormat used throught on the Yaxis of the CoordSystem*/
    protected DecimalFormat dfY;
    /** DecimalFormat used throught on the Xaxis of the CoordSystem*/
    protected DecimalFormat dfX;
    /** if true, the arrows will be drawn at the end of the axi*/
    protected boolean shouldDrawArrows = true;
    /** if true, the increment will be painted at each tick mark*/ 
    protected boolean shouldPaintAltTick = true;
    /** if true only the tick will be painted on the yaxis.  Alternately, if false, a 
     * light grey line will paint across the background of the chart.*/
    protected boolean shouldPaintOnlyTick = true;
    
    /** If true, the labels will be painted. If false, only the ticks will display. */
    protected boolean shouldPaintLabels = true;
    
    /** The left margin */
	protected int leftmargin = 50;
	/** The top margin. */
    protected int topmargin = 20;
	
	/** The right margin. */
    protected int rightmargin = 30;
	/** The bottom margin. */
    protected int bottommargin = 30;
	/** The minimal margin constant. */
    public final int MINIMALMARGIN = 20;
	/** The arrow length constant. */
    public final int ARROWLENGTH = 15;
    
	/** The ChartDataModel constraints of the first y-axis and the x-axis. */
    protected ChartDataModelConstraints constraints;
	/** The ChartDataModel constraints of the second y-axis and the x-axis. */
    protected ChartDataModelConstraints constraints2;
    
	/** The DataModel class. */
    protected ChartDataModel model;
    
	/** The utilities class, which contains all the rendering methods etc. */
    protected CoordSystemUtilities c;
    
	/** The xaxis.*/
    protected Axis xaxis;
    /** The first y-axis. */
	protected Axis yaxis;
	/** The second y-axis. */
    protected Axis yaxis2;
    
	/** The multiplication matrix for the first y-axis and the x-axis. */
    protected AffineTransform y1transform;
	/** The multiplication matrix for the second y-axis and the x-axis. */
    protected AffineTransform y2transform;
    
    /** the axis binding constant for the first y-axis
     */
    public static final int FIRST_YAXIS = 0;
    /** the axis binding constant for the second y-axis
     */
    public static final int SECOND_YAXIS = 1;
    
    /** Creates a new CoordSystem using the given model constraints.
     * Also creates default linear x and y-axis. Note that the length
     * of the axis are set on the first call to
     * setBounds().
     * @param c the ChartDataModel needed to compute the DataConstraints.
     */
    public CoordSystem(ChartDataModel cdm) {
        this.constraints = cdm.getChartDataModelConstraints(FIRST_YAXIS);
        this.constraints2 = cdm.getChartDataModelConstraints(SECOND_YAXIS);
        
        this.model = cdm;
        
        xaxis = new Axis(Axis.HORIZONTAL, constraints);
        yaxis = new Axis(Axis.VERTICAL, constraints);
        
        c = new CoordSystemUtilities(this, constraints, constraints2, model);
		
		dfY = new DecimalFormat();
        dfX = new DecimalFormat();
    }
    
    /** Creates a new CoordSystem using the given model constraints.
     * Also creates default linear x and y-axis. Note that the length
     * of the axis are set on the first call to
     * setBounds().
     * @param c the ChartDataModel needed to compute the DataConstraints.
     * @param xtext the x-axis unit
     * @param ytext the y-axis unit
     */
    public CoordSystem(ChartDataModel c, String xunit, String yunit) {
        this(c);

        setXAxisUnit(xunit);
        setYAxisUnit(yunit);
    }
	
	/**
     * Create a new CoordSystem with alternate painting parameters.
     * @param c the ChartDataModel needed to compute the DataConstraints.
     * @param drawArrows if true the arrows will be drawn at the end of the axis
     * @param paintAltYTick if true the caption will paint on alternate ticks of the 
     * yaxis instead of on every one.
     * @param paintOnlyYTick if true the horizontal lightgray line will <i>not</i>
     * appear behind the chart at each yaxis tick mark.
     */
    public CoordSystem(ChartDataModel c, DecimalFormat yAxisFormat, 
            boolean drawArrows, boolean paintAltYTick, boolean paintOnlyYTick) {
        this(c);
        dfY = yAxisFormat;
        shouldDrawArrows = drawArrows;
        shouldPaintAltTick = paintAltYTick;
        shouldPaintOnlyTick = paintOnlyYTick;
    }

    /** Sets the coordinate transformation for any y-coordinate.
     * @param at the AffineTransform that transforms the coordinates into pixel
     * space
     * @axis defines for which y-axis the transform is computed
     */
    public void setTransform(AffineTransform at, int axis) {
        switch(axis) {
            case(FIRST_YAXIS): y1transform = at; break;
            case(SECOND_YAXIS): y2transform = at; break;
        }
    }
    
    /** Returns the currently defined AffineTransform for any y-axis.
     * @param axis the y-axis to be used.
     */
    public AffineTransform getTransform(int axis) {
        switch(axis) {
            case(FIRST_YAXIS): return y1transform;
            case(SECOND_YAXIS): return y2transform;
        }
        
        return null;
    }
    
    /** This method computes the default transform which transforms the
     * user space coordinates of this coordinate system to the pixel
     * space coordinates used in the Graphics object.
     * All rendering in the CoordinateSystem and the ChartRenderers
     * will rely on this transform.
     * @param axis defines which y-axis to use.
     */
    public AffineTransform getDefaultTransform(int axis) {
        double x_pt2px = 0;
        double y_pt2px = 0;
        double xcoord0 = 0;
        double ycoord0 = 0;
        
        x_pt2px = 1 / getXAxis().getPointToPixelRatio();
        //System.out.println("** x_pt2px = "+getXAxis().getPointToPixelRatio());
        xcoord0 = getBounds().getX() + getLeftMargin() + getXAxis().getPixelForValue(0.0);
        
        switch(axis) {
            case FIRST_YAXIS:
                y_pt2px = 1 / getFirstYAxis().getPointToPixelRatio();
                ycoord0 = getBounds().getY() + getBounds().getHeight() - getBottomMargin() -
                getFirstYAxis().getPixelForValue(0.0);
                break;
            case SECOND_YAXIS:
                y_pt2px = 1 / getSecondYAxis().getPointToPixelRatio();
                ycoord0 = getBounds().getY() + getBounds().getHeight() - getBottomMargin() -
                getSecondYAxis().getPixelForValue(0.0);
                break;
        }
        return new AffineTransform(x_pt2px, 0f, 0f,
        -y_pt2px, xcoord0, ycoord0);
    }
    
    /** Sets the x-axis.
     * @param a the x-axis
     */
    public void setXAxis(Axis a) {
        xaxis = a;
    }
    
    /** Returns the x axis.
     * @return the x-axis
     */
    public Axis getXAxis() {
        return xaxis;
    }

    /** Sets the x-axis unit string.
     * @param xtext the unit string
     */
    public void setXAxisUnit(String xunit) {
        this.xaxis_unit = xunit;
    }
    
    /** Gets the x-axis unit string.
     * @return the label String
     */
    public String getXAxisUnit() {        
        return xaxis_unit;
    }
    
    /** Sets the y-axis unit string.
     * @param ytext the unit string
     */
    public void setYAxisUnit(String yunit) {
        this.yaxis_unit = yunit;
    }
    
    /** Gets the y-axis label.
     * @return the label String
     */
    public String getYAxisUnit() {        
        return yaxis_unit;
    }
    
    /** Sets the font for the axis labels.
     * @param f the Font to be used
     */
    public void setFont(Font f) {
        font = f;
    }
    
    /** Returns the font used for the axis labels.
     * @return the Font object
     */
    public Font getFont() {        
        return font;
    }

    /** Sets the left y-axis and computes the matrix transformation.
     * @param a the left y-axis
     */
    public void setFirstYAxis(Axis a) {
        yaxis = a;
    }
    
    /** Returns the first y-axis.
     * @return the left y-axis
     */
    public Axis getFirstYAxis() {
        return yaxis;
    }
    
    /** Sets the second y-axis and computes the matrix transformation.
     * @param a the right y-axis
     */
    public void setSecondYAxis(Axis a) {
        yaxis2 = a;
    }
    
    /** Returns the second y-axis.
     * @return the right y-axis
     */
    public Axis getSecondYAxis() {
        return yaxis2;
    }
    
    /** Returns the inner margin, ie the bounds minus the margins.
     * @return a Rectangle object defining the inner bounds.
     */
    public Rectangle getInnerBounds() {
        Rectangle b = getBounds();
        Rectangle i = new Rectangle((int)b.getX() + getLeftMargin() - 1,
        (int)b.getY() + getTopMargin() - 1,
        (int)b.getWidth() - (getLeftMargin() + getRightMargin()) + 2,
        (int)b.getHeight() - (getTopMargin() + getBottomMargin()) + 2);
        return i;
    }
    
    /** Computes all margins, initializes the length of the Axis and
     * calls <code>super.setBounds</code>. Additionally, it sets the
     * default AffineTransforms for every y-axis.
     * @param bounds <CODE>Rectangle</CODE> object defining the bounds
     */
    public void setBounds(Rectangle bounds) {
        super.setBounds(bounds);
	
	setRightMargin(c.computeRightMargin());
	setLeftMargin(c.computeLeftMargin());
	
	setTopMargin(c.computeTopMargin());
	setBottomMargin(c.computeBottomMargin());
        
        xaxis.setLength((int)(bounds.getWidth()) - getLeftMargin() - getRightMargin());
        //System.out.println("** xaxis.length = "+xaxis.getLength());
        yaxis.setLength((int)(bounds.getHeight()) - getTopMargin() - getBottomMargin());
        //System.out.println("** yaxis.length = "+yaxis.getLength());
        setTransform(getDefaultTransform(FIRST_YAXIS), FIRST_YAXIS);
        if(yaxis2 != null) {
            yaxis2.setLength((int)(bounds.getHeight()) - getTopMargin() - getBottomMargin());
            setTransform(getDefaultTransform(SECOND_YAXIS), SECOND_YAXIS);
        }
    }
    
    /** Returns the preferred size needed for the renderer.
     * @return a Dimension with the minimum Integer values.
     */
    public Dimension getPreferredSize() {
        return new Dimension(Integer.MIN_VALUE, Integer.MIN_VALUE);
    }
    
    /** Overrides the method to just call <code>paintDefault</code>.
     * @param g the <CODE>Graphics2D</CODE> object to paint in
     */
    public void render(Graphics2D g) {
        paintDefault(g);
    }
    
    /** This method is called by the paint method to do the actual painting.
     * The painting is supposed to start at point (0,0) and the size is
     * always the same as the preferred size. The paint method performs
     * the possible scaling.
     * @param g the <CODE>Graphics2D</CODE> object to paint in
     */
    public void paintDefault(Graphics2D g) {
        g.setColor(Color.black);
        
        Line2D x = c.getXAxisLine2D();
        Line2D y = c.getYAxisLine2D();
        
        g.draw(x);
        g.draw(y);
        
        // draw X-Axis Arrow
		if(shouldDrawArrows) {
			g.drawLine((int)x.getX2(), (int)x.getY2(), (int)x.getX2() + ARROWLENGTH, (int)x.getY2());
			g.fillPolygon(new int[] {(int)(x.getX2() + ARROWLENGTH / 3.0),
						(int)(x.getX2() + ARROWLENGTH / 3.0),
						(int)(x.getX2() + ARROWLENGTH)},
						new int[] {(int)x.getY2() - 3, (int)x.getY2() + 3, (int)x.getY2()},
						3);
		}
        
        // draw X-Axis label right below the Arrow ?!
        g.setColor(Color.black);
        TextLayout layoutX = new TextLayout(getXAxisUnit(), getFont(), 
                                           new FontRenderContext(null, true, false));
		layoutX.draw(g, (float)x.getX2() + (float)ARROWLENGTH / 3,  (float)x.getY2() + (float)layoutX.getBounds().getHeight() + 5);
        
        // draw Y-Axis Arrow
		if(shouldDrawArrows) {
			g.drawLine((int)y.getX1(), (int)y.getY1(), (int)y.getX1(), (int)y.getY1() - ARROWLENGTH);
			g.fillPolygon(new int[] {(int)(y.getX1() - 3),
						(int)(y.getX1() + 3),
						(int)(y.getX1())},
						new int[] {(int)(y.getY1() - ARROWLENGTH / 3.0),
						(int)(y.getY1() - ARROWLENGTH / 3.0),
						(int)y.getY1() - ARROWLENGTH},
						3);
		}

        // draw Y-Axis label right below the Arrow ?!
        g.setColor(Color.black);
        TextLayout layoutY = new TextLayout(getYAxisUnit(), getFont(), 
                                           new FontRenderContext(null, true, false));
        layoutY.draw(g, (float)y.getX1()-6-(float)layoutY.getBounds().getWidth(), 
                        (float)y.getY1() - layoutX.getDescent() - 3);
        
        if(getSecondYAxis() != null) {
            Line2D y2 = c.getSecondYAxisLine2D();
            g.draw(y2);
        }
        
        if(model.isColumnNumeric())
            c.drawNumericalXAxisTicks(g);
        else
            c.drawXAxisTicks(g);
        
        c.drawYAxisTicks(g);
    }
    
    /** Returns a new PointToPixelTranslator for the given axis.
     * Please notice that this method is deprecated since release 0.92.
     * The PointToPixelTranslator interface has been replaced with
     * AffineTransforms.
     * @param y the y-axis identifier used to choose the right Point / Pixel ratio
     * @return a PointToPixelTranslator object or null if the resulting
     * Point is not within the Bounds of the Coordinate System
     * @deprecated
     */
    public PointToPixelTranslator getPointToPixelTranslator(int yaxis) {
        final Axis x = this.getXAxis();
        final Axis y;
        if(yaxis == CoordSystem.FIRST_YAXIS)
            y = this.getFirstYAxis();
        else
            y = this.getSecondYAxis();
        
        return new PointToPixelTranslator() {
            public Point2D getPixelCoord(Point2D pt) {
                double x0 = 0.0;
                double y0 = 0.0;
                
                x0 = getBounds().getX()+getLeftMargin()+
                x.getPixelForValue(pt.getX());
                
                y0 = getBounds().getY()+getBounds().getHeight() - getBottomMargin() -
                y.getPixelForValue(pt.getY());
                Point2D p = new Point2D.Double(x0, y0);
                
                if(getInnerBounds().contains(p))
                    return p;
                else
                    return null;
            }
        };
    }
    
    /** Returns the left margin. */
    protected int getLeftMargin() {
        return leftmargin;
    }
    
    /** Returns the right margin. */
    protected int getRightMargin() {
        return rightmargin;
    }
    
    /** Returns the top margin. */
    protected int getTopMargin() {
        return topmargin;
    }
    
    /** Returns the bottom margin. */
    protected int getBottomMargin() {
        return bottommargin;
    }
    
    /** Sets the left margin.
     * @param margin the new margin value 
     */
    protected void setLeftMargin(int margin) {
        leftmargin = margin;
    }
    
    /** Sets the right margin.
     * @param margin the new margin value 
     */
    protected void setRightMargin(int margin) {
        rightmargin = margin;
    }
    
    /** Sets the top margin.
     * @param margin the new margin value 
     */
    protected void setTopMargin(int margin) {
        topmargin = margin;
    } 
    
    /** Sets the bottom margin.
     * @param margin the new margin value 
     */
    public void setBottomMargin(int margin) {
        bottommargin = margin;
    } 
	
	/** Returns the FontRenderContext used througout the CoordSystem*/
	public FontRenderContext getFontRenderContext() {
		return frc;
	}
	
    /** Returns the DecimalFormat used throught on the Yaxis of the CoordSystem*/
    public DecimalFormat getYDecimalFormat() {
		return dfY;
	}
	
    /** Returns the DecimalFormat used throught on the Xaxis of the CoordSystem*/
	public DecimalFormat getXDecimalFormat() {
		return dfX;
	}
    
    /** if true, the arrows will be drawn at the end of the axis*/
	public boolean isDrawArrows() {
		return shouldDrawArrows;
	}
    
    /** if true, the increment will be painted at each tick mark*/
	public boolean isPaintAltTick() {
		return shouldPaintAltTick;
	}
    
    /** if true only the tick will be painted on the yaxis.  Alternately a 
     * light grey line will paint across the background of the chart.*/
    public boolean isPaintOnlyTick() {
		return shouldPaintOnlyTick;
	}
   
    public boolean isPaintLabels() {
        return shouldPaintLabels;
    }
    
    public void setPaintLabels(boolean label) {
        shouldPaintLabels = label;
    }
    
    /** Returns the used ChartDataModelConstraints. */
    public ChartDataModelConstraints getChartDataModelConstraints(int axis) {
        if(axis == FIRST_YAXIS)
            return constraints;
        else if(axis == SECOND_YAXIS)
            return constraints2;
        else
            return null;
    }
}
