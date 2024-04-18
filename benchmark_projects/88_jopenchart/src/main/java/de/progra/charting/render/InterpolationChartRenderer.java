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

    InterpolationRenderer.java
    Created on 24. September 2001, 12:50
*/

package de.progra.charting.render;

import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import java.awt.geom.Area;
import de.progra.charting.CoordSystem;
import java.awt.geom.AffineTransform;
import de.progra.charting.PointToPixelTranslator;
import de.progra.charting.ChartUtilities;
import java.awt.Graphics2D;
import java.awt.Color;
import de.progra.charting.model.ChartDataModel;

/**
 * This renderer creates a InterpolationChart.
 * @author  mueller
 * @version 1.0
 */
public class InterpolationChartRenderer extends AbstractChartRenderer {

    /** Creates new InterpolationChartRenderer
     * @param rcm the RowColorModel needed to determine the right colors
     * @param cs the CoordSystem used to translate values into points
     * @param model the DataModel that should be rendered
     */
    public InterpolationChartRenderer(CoordSystem cs, ChartDataModel model) {
        super(cs, model);
    }
    
    /** Finally renders the Object in the Graphics object.
     * @param g the Graphics2D object in which to render
     */
    public void renderChart(Graphics2D g) {
        ChartDataModel m = getChartDataModel();
        RowColorModel rcm = getRowColorModel();
        AffineTransform yaxis1 = getTransform(CoordSystem.FIRST_YAXIS);
        
        int datasetcount = m.getDataSetNumber();
        Point2D val;
        Point2D paint = null;
        Point2D oldpaint = null;
        if(! m.isColumnNumeric())
            return;
        
        for(int set = 0; set < datasetcount; set++) {
            // Creating Interpolated Function Data
            /*
             "for i in range(AMOUNT) :\n"+
             "   x = lowrange + i * (float(abs(highrange - lowrange)) / AMOUNT)\n"+
             "   columns.append(x)\n"+
             "   model.append("+function+")\n";
            */
            
            double[] x = new double[m.getDataSetLength(set)];
            double[] y = new double[x.length];
            
            for(int i = 0; i < m.getDataSetLength(set);  i++) {
                x[i] = ((Number)m.getColumnValueAt(set, i)).doubleValue();
                
                // Catch x[i] == Not A Number
                if(x[i] != x[i]) x[i] = 0.0;
                
                y[i] = m.getValueAt(set, i).doubleValue();
            }        
                        
            int AMOUNT = 2000;
            double lowrange = m.getChartDataModelConstraints(CoordSystem.FIRST_YAXIS).getMinimumColumnValue();
            double hirange = m.getChartDataModelConstraints(CoordSystem.FIRST_YAXIS).getMaximumColumnValue();

            double xa[] = new double[AMOUNT];
            double ya[] = new double[AMOUNT];
            
            for(int i = 0; i < AMOUNT; i++) {
                xa[i] = lowrange + i * (Math.abs(hirange - lowrange) / (double)AMOUNT);
                ya[i] = ChartUtilities.interpolate(x, y, xa[i]);
            }
            
            // Rendering xa[] and ya[]
            for(int i = 0; i < AMOUNT; i++) {
                
                val = new Point2D.Double(xa[i], ya[i]);
                    
                oldpaint = paint;
                if(yaxis1.transform(val, null) != null)
                    paint = yaxis1.transform(val, paint);
                else
                    continue;
                
                g.setColor(rcm.getColor(set));
                
                
                if(oldpaint != null) {
                    
                    g.drawLine((int)oldpaint.getX(), (int)oldpaint.getY(),
                               (int)paint.getX(), (int)paint.getY());
                }
            }
            oldpaint = null;
            paint = null;
        }
   }    
}
