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

    Chart.java
    Created on 21. Juni 2001, 12:47
 */

package de.progra.charting;

import de.progra.charting.render.AbstractChartRenderer;
import java.awt.Rectangle;
import de.progra.charting.model.ChartDataModel;
import java.awt.Graphics2D;

/**
 * This class defines the methods to access a chart. It provides methods
 * to set the multiple chart components. You can set multiple ChartRenderer
 * giving them a z-coordinate. The ChartRenderer that is rendered first is
 * the one with the lowest z-coordinate.
 * @author mueller
 * @version 1.0
 */
public interface Chart {
    
    /** Sets the legend for this chart.
     * @param l The Legend this Chart contains.
     */
    public void setLegend(Legend l);
    
    /** Returns this chart's legend.
     * @return the Legend for this Chart. Could be <CODE>null</CODE>.
     */
    public Legend getLegend();
    
    /** Sets the title for this chart.
     * @param t This Chart's Title.
     */
    public void setTitle(Title t);
    
    /** Returns the title for this chart.
     * @return this Chart's Title. Could be <CODE>null</CODE>.
     */
    public Title getTitle();
    
    /** Sets the coordinate system for this chart,
     * which can be null if the ChartRenderer
     * doesn't need a coordinate system, e.g. if it's a
     * PieChart.
     * @param c The Coordinate System for the Chart.
     */
    public void setCoordSystem(CoordSystem c);
    
    /** Returns the coordinate system.
     * @return the Coordinate System for the Chart. Could be <CODE>null</CODE>.
     */
    public CoordSystem getCoordSystem();
    
    /** Sets the Map with all ChartRenderers. The keys
     * have to be the z-coordinates of the ChartRenderers.
     * @param renderer The Map of ChartRenderers.
     */
    public void setChartRenderer(java.util.Map renderer);
    
    /** Returns the Map of all ChartRenderers.
     * @return the Map of Renderers.
     */
    public java.util.Map getChartRenderer();
    
    /** Adds a ChartRenderer with a specific z-coordinate.
     * @param renderer the ChartRenderer
     * @param z its z-coordinate.
     */
    public void addChartRenderer(AbstractChartRenderer renderer, int z);
    
    /** Returns the ChartRenderer with a specific z-coordinate.
     * @param z the z-coordinate of the desired ChartRenderer.
     * @return the ChartRenderer or <CODE>null</CODE> if none has been found.
     */
    public AbstractChartRenderer getChartRenderer(int z);
    
    /** Stores the ChartDataModel for this Chart.
     * @param model the ChartDataModel
     */
    public void setChartDataModel(ChartDataModel model);
    
    /** Returns the ChartDataModel.
     * @return the ChartDataModel
     */
    public ChartDataModel getChartDataModel();
    
    /** Sets the Bounds for this Chart.
     * @param r the <CODE>Rectangle</CODE> object defining the bounds
     */
    public void setBounds(Rectangle r);
    
    /** Returns the Bounds for the Chart.
     * @return the bounds
     */
    public Rectangle getBounds();
    
    /** Does the layout of the title, legend and coordinate system and
     * calls the render method of all those including the ChartRenderers.
     * @param g the <CODE>Graphics2D</CODE> object to paint in.
     */    
    public void render(Graphics2D g);
}

