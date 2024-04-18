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

    LineChartRenderer.java
    Created on 6. September, 19:19
*/

package de.progra.charting.render;

import java.awt.geom.Line2D;
import java.awt.geom.Point2D;
import java.awt.geom.Area;
import de.progra.charting.CoordSystem;
import java.awt.geom.AffineTransform;
import de.progra.charting.PointToPixelTranslator;
import java.awt.Graphics2D;
import java.awt.Color;
import de.progra.charting.model.ChartDataModel;

/**
 * This renderer creates a LineChart.
 * @author  mueller
 * @version 1.0
 */
public class LineChartRenderer extends AbstractChartRenderer {

    /** Creates new LineChartRenderer
     * @param rcm the RowColorModel needed to determine the right colors
     * @param cs the CoordSystem used to translate values into points
     * @param model the DataModel that should be rendered
     */
    public LineChartRenderer(CoordSystem cs, ChartDataModel model) {
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
        boolean numericalcolumns = m.isColumnNumeric();
        float modelVal = 0f;
        //System.out.println("** Render LineChart.-");
        for(int set = 0; set < datasetcount; set++) {
            for(int value = 0; value < m.getDataSetLength(set);  value++) {
                modelVal = m.getValueAt(set, value).floatValue();
                
                if(modelVal != modelVal || modelVal == Float.NEGATIVE_INFINITY || modelVal == Float.POSITIVE_INFINITY) {
                    //System.out.print(".");
                    oldpaint = null;
                    continue;
                }
                
                if(numericalcolumns)
                    val = new Point2D.Float(((Number)m.getColumnValueAt(set, value)).floatValue(),
                                            modelVal);
                else
                    val = new Point2D.Float((float)value,
                                            modelVal);

                //System.out.println("** Rendered "+val);
                oldpaint = paint;
                
                if(yaxis1.transform(val, null) != null) {
                    paint = yaxis1.transform(val, null);
                    //System.out.println("** val = "+val+"  paint = "+paint);
                }
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
