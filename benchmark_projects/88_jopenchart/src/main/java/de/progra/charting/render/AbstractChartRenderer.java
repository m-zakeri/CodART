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

    ChartRenderer.java
    Created on 26. Juni 2001, 22:52
*/

package de.progra.charting.render;

import java.awt.Rectangle;
import de.progra.charting.CoordSystem;
import java.awt.geom.AffineTransform;
import java.awt.Shape;
import de.progra.charting.PointToPixelTranslator;
import java.awt.Graphics2D;
import java.awt.Dimension;
import de.progra.charting.model.ChartDataModel;

/**
 * This class is the superclass for all the different ChartRenderer.
 * @author  mueller
 * @version 1.0
 */
public abstract class AbstractChartRenderer implements Renderer {

    protected Rectangle bounds;
    
    protected CoordSystem coord;
    
    protected PointToPixelTranslator p;
    
    protected ChartDataModel model;
  
    protected RowColorModel rcm;
    
    /** Creates new AbstractChartRenderer
     * @param model the DataModel that should be rendered
     */
    protected AbstractChartRenderer(ChartDataModel model) {
        this.model = model;
    }
    
    /** Creates new AbstractChartRenderer
     * @param rcm the RowColorModel that defines the correspondence between row titles and colors
     * @param p the Object used to translate values into points
     * @param model the DataModel that should be rendered
     * @deprecated Use the constructor 
        <code>AbstractChartRenderer(CoordSystem cs, 
                                    ChartDataModel model)</code>
     *  instead.
     */
    public AbstractChartRenderer(PointToPixelTranslator p, ChartDataModel model) {
        this(model);
        this.p = p;
    }
    
    /** Creates new AbstractChartRenderer
     * @param cs the CoordSystem which contains the AffineTransforms to translate
     * into pixel space
     * @param rcm the RowColorModel that defines the correspondence between row titles and colors
     * @param model the DataModel that should be rendered
     */
    public AbstractChartRenderer(CoordSystem cs, 
                                 ChartDataModel model) {
        this(model);
        this.coord = cs;
    }

    /** Gets the bounds for this renderer.
     * @return the bounds of this renderer. If <code>setBounds</code> has not
     * been called before, the bounds computed from
     * <code>getPreferredSize</code> is returned.
     */
    public Rectangle getBounds() {
        return bounds;
    }
    
    /** Returns the preferred size needed for the renderer.
     * @return a non-null Dimension object
     */
    public Dimension getPreferredSize() {
        return new Dimension(Integer.MIN_VALUE, Integer.MIN_VALUE);
    }
    
    /** Calls <code>renderChart(g)</code> and crops the output to the desired
	 * bounds. This way you can manually set small maximum and minimum values 
	 * which automatically gets reflected in the CoordSystem but the ChartRenderer
	 * doesn't need to care.
     * @param g the Graphics2D object in which to render
     */
    public void render(Graphics2D g) {
		Rectangle bounds = getBounds();
		Shape clip = g.getClip();
		g.setClip((int)bounds.getX(), (int)bounds.getY(), (int)bounds.getWidth(), (int)bounds.getHeight());
		renderChart(g);
		g.setClip(clip);
	}
	
	/** Finally renders the chart in the clipped rectangle. */
	public abstract void renderChart(Graphics2D g);
    
    /** Sets the bounds the layout manager has assigned to
     * this renderer. Those, of course, have to be
     * considered in the rendering process.
     * @param bounds the new bounds for the renderer.
     */
    public void setBounds(Rectangle bounds) {
        this.bounds = bounds;
    }
    
    /** Sets the ChartDataModel whose DataSets are rendered.
     * @param model the ChartDataModel
     */
    public void setChartDataModel(ChartDataModel model) {
        this.model = model;
    }
    
    /** Returns the ChartDataModel whose DataSets are rendered.
     * @return a ChartDataModel which contains the Chart's data
     */
    public ChartDataModel getChartDataModel() {
        return model;
    }   
    
    /** Sets the PointToPixelTranslator. 
     * @param p the PointToPixelTranslator
     * @deprecated Has been made obsolete by using AffineTransforms
     */
    public void setPointToPixelTranslator(PointToPixelTranslator p) {
        this.p = p;
    }
    
    /** Returns the PointToPixelTranslator.
     * @return the PointToPixelTranslator currently in use
     * @deprecated Has been made obsolete by using AffineTransforms
     */
    public PointToPixelTranslator getPointToPixelTranslator() {
        return p;
    } 
    
    /** Returns the current CoordSystem. */
    public CoordSystem getCoordSystem() {
        return coord;
    }
    
    /** Sets the CoordSystem which contains the AffineTransforms to
     * translate into pixel space.
     * @param cs the new CoordSystem 
     */
    public void setCoordSystem(CoordSystem cs) {
        coord = cs;
    }    
    
    /** Returns the currently defined AffineTransform for any y-axis.
     * @param axis the y-axis to be used.
     */
    public AffineTransform getTransform(int axis) {
        return getCoordSystem().getTransform(axis);
    }
    
    /** Sets a RowColorModel to define the correlation of row titles and colors used for the Legend.
     * @param rcm the RowColorModel
     */    
    public void setRowColorModel(RowColorModel rcm) {
        this.rcm = rcm;
    }
    
    /** Returns the RowColorModel currently in use.
     * @return a RowColorModel
     */    
    public RowColorModel getRowColorModel() {
        return rcm;
    }
}
