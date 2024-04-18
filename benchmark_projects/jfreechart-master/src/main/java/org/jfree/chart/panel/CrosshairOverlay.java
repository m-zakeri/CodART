/* ===========================================================
 * JFreeChart : a free chart library for the Java(tm) platform
 * ===========================================================
 *
 * (C) Copyright 2000-2020, by Object Refinery Limited and Contributors.
 *
 * Project Info:  http://www.jfree.org/jfreechart/index.html
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
 * License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
 * USA.
 *
 * [Oracle and Java are registered trademarks of Oracle and/or its affiliates.
 * Other names may be trademarks of their respective owners.]
 *
 * ---------------------
 * CrosshairOverlay.java
 * ---------------------
 * (C) Copyright 2011-2020, by Object Refinery Limited.
 *
 * Original Author:  David Gilbert (for Object Refinery Limited);
 * Contributor(s):   John Matthews;
 *
 */

package org.jfree.chart.panel;

import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.event.OverlayChangeEvent;
import org.jfree.chart.plot.Crosshair;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.ui.RectangleEdge;
import org.jfree.chart.util.Args;
import org.jfree.chart.util.CloneUtils;
import org.jfree.chart.util.PublicCloneable;

import java.awt.*;
import java.awt.geom.Rectangle2D;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * An overlay for a {@link ChartPanel} that draws crosshairs on a chart.  If
 * you are using the JavaFX extensions for JFreeChart, then you should use
 * the {@code CrosshairOverlayFX} class.
 *
 * @since 1.0.13
 */
public class CrosshairOverlay extends AbstractOverlay implements Overlay,
        PropertyChangeListener, PublicCloneable, Cloneable, Serializable {
    private transient CrosshairOverlayHelper crosshairOverlayHelper = new CrosshairOverlayHelper();

    private void readObject(ObjectInputStream stream) throws IOException, ClassNotFoundException {
        this.crosshairOverlayHelper = (CrosshairOverlayHelper) stream.readObject();
        stream.defaultReadObject();
    }

    /**
     * Storage for the crosshairs along the x-axis.
     */
    protected List<Crosshair> xCrosshairs;

    /**
     * Storage for the crosshairs along the y-axis.
     */
    protected List<Crosshair> yCrosshairs;

    /**
     * Creates a new overlay that initially contains no crosshairs.
     */
    public CrosshairOverlay() {
        super();
        this.xCrosshairs = new ArrayList<>();
        this.yCrosshairs = new ArrayList<>();
    }

    /**
     * Adds a crosshair against the domain axis (x-axis) and sends an
     * {@link OverlayChangeEvent} to all registered listeners.
     *
     * @param crosshair the crosshair ({@code null} not permitted).
     * @see #removeDomainCrosshair(Crosshair)
     * @see #addRangeCrosshair(Crosshair)
     */
    public void addDomainCrosshair(Crosshair crosshair) {
        Args.nullNotPermitted(crosshair, "crosshair");
        this.xCrosshairs.add(crosshair);
        crosshair.addPropertyChangeListener(this);
        fireOverlayChanged();
    }

    /**
     * Removes a domain axis crosshair and sends an {@link OverlayChangeEvent}
     * to all registered listeners.
     *
     * @param crosshair the crosshair ({@code null} not permitted).
     * @see #addDomainCrosshair(Crosshair)
     */
    public void removeDomainCrosshair(Crosshair crosshair) {
        Args.nullNotPermitted(crosshair, "crosshair");
        if (this.xCrosshairs.remove(crosshair)) {
            crosshair.removePropertyChangeListener(this);
            fireOverlayChanged();
        }
    }

    /**
     * Clears all the domain crosshairs from the overlay and sends an
     * {@link OverlayChangeEvent} to all registered listeners.
     */
    public void clearDomainCrosshairs() {
        if (this.xCrosshairs.isEmpty()) {
            return;  // nothing to do
        }
        for (Crosshair c : getDomainCrosshairs()) {
            this.xCrosshairs.remove(c);
            c.removePropertyChangeListener(this);
        }
        fireOverlayChanged();
    }

    /**
     * Returns a new list containing the domain crosshairs for this overlay.
     *
     * @return A list of crosshairs.
     */
    public List<Crosshair> getDomainCrosshairs() {
        return new ArrayList<>(this.xCrosshairs);
    }

    /**
     * Adds a crosshair against the range axis and sends an
     * {@link OverlayChangeEvent} to all registered listeners.
     *
     * @param crosshair the crosshair ({@code null} not permitted).
     */
    public void addRangeCrosshair(Crosshair crosshair) {
        Args.nullNotPermitted(crosshair, "crosshair");
        this.yCrosshairs.add(crosshair);
        crosshair.addPropertyChangeListener(this);
        fireOverlayChanged();
    }

    /**
     * Removes a range axis crosshair and sends an {@link OverlayChangeEvent}
     * to all registered listeners.
     *
     * @param crosshair the crosshair ({@code null} not permitted).
     * @see #addRangeCrosshair(Crosshair)
     */
    public void removeRangeCrosshair(Crosshair crosshair) {
        Args.nullNotPermitted(crosshair, "crosshair");
        if (this.yCrosshairs.remove(crosshair)) {
            crosshair.removePropertyChangeListener(this);
            fireOverlayChanged();
        }
    }

    /**
     * Returns a new list containing the range crosshairs for this overlay.
     *
     * @return A list of crosshairs.
     */
    public List<Crosshair> getRangeCrosshairs() {
        return new ArrayList<>(this.yCrosshairs);
    }

    /**
     * Receives a property change event (typically a change in one of the
     * crosshairs).
     *
     * @param e the event.
     */
    @Override
    public void propertyChange(PropertyChangeEvent e) {
        fireOverlayChanged();
    }

    /**
     * Renders the crosshairs in the overlay on top of the chart that has just
     * been rendered in the specified {@code chartPanel}.  This method is
     * called by the JFreeChart framework, you won't normally call it from
     * user code.
     *
     * @param g2         the graphics target.
     * @param chartPanel the chart panel.
     */
    @Override
    public void paintOverlay(Graphics2D g2, ChartPanel chartPanel) {
        Shape savedClip = g2.getClip();
        Rectangle2D dataArea = chartPanel.getScreenDataArea();
        g2.clip(dataArea);
        JFreeChart chart = chartPanel.getChart();
        XYPlot plot = (XYPlot) chart.getPlot();
        ValueAxis xAxis = plot.getDomainAxis();
        RectangleEdge xAxisEdge = plot.getDomainAxisEdge();
        for (Crosshair ch : getDomainCrosshairs()) {
            if (ch.isVisible()) {
                double x = ch.getValue();
                double xx = xAxis.valueToJava2D(x, dataArea, xAxisEdge);
                if (plot.getOrientation() == PlotOrientation.VERTICAL) {
                    crosshairOverlayHelper.drawVerticalCrosshair(g2, dataArea, xx, ch);
                } else {
                    crosshairOverlayHelper.drawHorizontalCrosshair(g2, dataArea, xx, ch);
                }
            }
        }
        ValueAxis yAxis = plot.getRangeAxis();
        RectangleEdge yAxisEdge = plot.getRangeAxisEdge();
        for (Crosshair ch : getRangeCrosshairs()) {
            if (ch.isVisible()) {
                double y = ch.getValue();
                double yy = yAxis.valueToJava2D(y, dataArea, yAxisEdge);
                if (plot.getOrientation() == PlotOrientation.VERTICAL) {
                    crosshairOverlayHelper.drawHorizontalCrosshair(g2, dataArea, yy, ch);
                } else {
                    crosshairOverlayHelper.drawVerticalCrosshair(g2, dataArea, yy, ch);
                }
            }
        }
        g2.setClip(savedClip);
    }

    /**
     * Draws a crosshair horizontally across the plot.
     *
     * @param g2        the graphics target.
     * @param dataArea  the data area.
     * @param y         the y-value in Java2D space.
     * @param crosshair the crosshair.
     */
    protected void drawHorizontalCrosshair(Graphics2D g2, Rectangle2D dataArea,
                                           double y, Crosshair crosshair) {
        crosshairOverlayHelper.drawHorizontalCrosshair(g2, dataArea, y, crosshair);
    }

    /**
     * Draws a crosshair vertically on the plot.
     *
     * @param g2        the graphics target.
     * @param dataArea  the data area.
     * @param x         the x-value in Java2D space.
     * @param crosshair the crosshair.
     */
    protected void drawVerticalCrosshair(Graphics2D g2, Rectangle2D dataArea,
                                         double x, Crosshair crosshair) {
        crosshairOverlayHelper.drawVerticalCrosshair(g2, dataArea, x, crosshair);
    }

    /**
     * Tests this overlay for equality with an arbitrary object.
     *
     * @param obj the object ({@code null} permitted).
     * @return A boolean.
     */
    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof CrosshairOverlay)) {
            return false;
        }
        CrosshairOverlay that = (CrosshairOverlay) obj;
        if (!this.xCrosshairs.equals(that.xCrosshairs)) {
            return false;
        }
        return this.yCrosshairs.equals(that.yCrosshairs);
    }

    /**
     * Returns a clone of this instance.
     *
     * @return A clone of this instance.
     * @throws CloneNotSupportedException if there is some problem
     *                                              with the cloning.
     */
    @Override
    public Object clone() throws CloneNotSupportedException {
        CrosshairOverlay clone = (CrosshairOverlay) super.clone();
        clone.xCrosshairs = (List) CloneUtils.cloneList(this.xCrosshairs);
        clone.yCrosshairs = (List) CloneUtils.cloneList(this.yCrosshairs);
        return clone;
    }

    private void writeObject(ObjectOutputStream stream) throws IOException {
        stream.defaultWriteObject();
        PsiMethodCallExpression:
        stream.writeObject(this.crosshairOverlayHelper);
    }
}
