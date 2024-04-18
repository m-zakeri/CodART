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

    PieChartRenderer.java
    Created on 7. August 2001, 18:14
*/

package de.progra.charting.render;

import java.awt.geom.Ellipse2D;
import java.awt.geom.Arc2D;
import de.progra.charting.CoordSystem;
import java.awt.geom.AffineTransform;
import de.progra.charting.PointToPixelTranslator;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Color;
import de.progra.charting.model.ChartDataModel;

/**
 * This renderer creates a PieChart.
 * @author  mueller
 * @version 1.0
 */
public class PieChartRenderer extends AbstractChartRenderer {
        
    /** Creates new PieChartRenderer
     * @param model the DataModel that should be rendered
     */
    public PieChartRenderer(ChartDataModel model) {
        super(model);
    }
    
    /** Creates new PieChartRenderer
     * @param cs the CoordSystem used to translate values into points
     * @param model the DataModel that should be rendered
     */
    public PieChartRenderer(CoordSystem cs, ChartDataModel model) {
        super(cs, model);
    }

    /** Finally renders the Object in the Graphics object.
     * @param g the Graphics2D object in which to render
     */
    public void renderChart(Graphics2D g) {
        Object rh = g.getRenderingHint(RenderingHints.KEY_ANTIALIASING);
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        ChartDataModel m = getChartDataModel();
        RowColorModel rcm = getRowColorModel();
        
        double height = this.getBounds().getHeight();
        double width = this.getBounds().getWidth();

        int datenreihen = m.getDataSetNumber();
        // determine shortest dataset length
        int min_length = Integer.MAX_VALUE;
        
        for(int i = 0; i < datenreihen; i++)
            min_length = Math.min(min_length, m.getDataSetLength(i));
        
        double center_y = getBounds().getCenterY();
        double center_x = getBounds().getCenterX();
        
        double rad = Math.min(width * 0.9, height * 0.9);
        double modelVal = 0.0;
        for(int reihe = min_length; reihe >= 1; reihe--) {
            
            double kreis = (double)rad / min_length * reihe;
            Ellipse2D.Double circle = new Ellipse2D.Double((double)center_x-kreis/2,
                                                           (double)center_y-kreis/2, 
                                                           kreis, kreis);
                        
            double sum = 0;
            double start = 0.0;
            
            // Paint data
            for(int i = 0; i < datenreihen; i++) {
                modelVal = m.getValueAt(i, reihe - 1).doubleValue();
                
                // Catch modelVal == Not A Number
                if(modelVal != modelVal)
                    continue;
                sum += modelVal;
            }
            
            for(int i = 0; i < datenreihen; i++) {
                double value = m.getValueAt(i, reihe - 1).doubleValue();
                
                // Catch value == Not A Number
                if(value != value) value = 0.0;
                
                Arc2D.Double arc = new Arc2D.Double(circle.getBounds2D(),
                                                  (double)start, 
                                                  360.0 * (double)value/(double)sum, 
                                                  Arc2D.PIE);
                start += 360 * (double)value/(double)sum;
                
                g.setColor(rcm.getColor(i));
                g.fill(arc);                                                  
            }
            g.setColor(Color.black);
            g.draw(circle);
        }
        
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, rh);
    }    
}
