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

    StackedBarChartRenderer.java
    Created on 26. September 2002
*/

package de.progra.charting.render;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.awt.font.LineMetrics;
import java.awt.font.FontRenderContext;
import java.text.DecimalFormat;
import de.progra.charting.PointToPixelTranslator;
import de.progra.charting.CoordSystem;
import de.progra.charting.model.AbstractChartDataModel;
import de.progra.charting.model.ChartDataModel;
import de.progra.charting.model.ChartDataModelConstraints;
import de.progra.charting.model.StackedChartDataModelConstraints;

/**
 * This renderer creates a stacked BarChart. This will only work on a ChartDataModel
 * with non-numeric x-axis values, because I couldn't make any sense out of
 * a bar chart with a numeric x-axis like in a line chart.
 * @author  mueller
 * @version 1.0
 */
public class StackedBarChartRenderer extends AbstractChartRenderer {
    
    protected float boxWidth = 1.0f;
    
    /** Creates new StackedBarChartRenderer
     * @param cs the CoordSystem used to translate into pixel space
     * @param model the DataModel that should be rendered
     */
    public StackedBarChartRenderer(CoordSystem cs, AbstractChartDataModel model) {
        super(cs, model);
    }

    /** Creates new StackedBarChartRenderer
     * @param cs the CoordSystem used to translate into pixel space
     * @param model the DataModel that should be rendered
     * @param boxWidth a value between 0.0 and 1.0 representing how much of the 
     * alloted space each box should consume.  If 1.0 is passed, then each box will 
     * completely fill it's allotted space, alternately I suggest you don't pass 0.0
     */
    public StackedBarChartRenderer(CoordSystem cs, AbstractChartDataModel model, 
                                   float boxWidth) {
        this(cs, model);
        this.boxWidth = boxWidth;
    }


    /** Finally renders the Object in the Graphics object.
     * @param g the Graphics2D object in which to render
     */
    public void renderChart(Graphics2D g) {
        ChartDataModel m = getChartDataModel();
        ChartDataModelConstraints con = m.getChartDataModelConstraints(CoordSystem.FIRST_YAXIS);
        
        System.out.println("** Maximum: "+con.getMaximumValue()+" Minimum: "+con.getMinimumValue());
        
        if(m.isColumnNumeric())
            return;
        
        RowColorModel rcm = getRowColorModel();
        AffineTransform yaxis1 = getTransform(CoordSystem.FIRST_YAXIS);
        
        int datasetcount = m.getDataSetNumber();
        
        int maximumDataSetLength = Integer.MIN_VALUE;
        
        for(int i = 0; i < model.getDataSetNumber(); i++) {
            maximumDataSetLength = Math.max(maximumDataSetLength, model.getDataSetLength(i));
        } 
        
        Point2D pointzero;
        if(con.getMinimumValue().floatValue() > 0)
           pointzero = yaxis1.transform(new Point2D.Float((float)con.getMinimumColumnValue(),
                                                         con.getMinimumValue().floatValue()),
                                        null);
        else if(con.getMaximumValue().floatValue() < 0)
           pointzero = yaxis1.transform(new Point2D.Float((float)con.getMinimumColumnValue(),
                                                         con.getMaximumValue().floatValue()),
                                        null);
        else
           pointzero = yaxis1.transform(new Point2D.Float((float)con.getMinimumColumnValue(),
                                                         0f),
                                        null);
        
        Point2D point1 = yaxis1.transform(new Point2D.Float((float)con.getMinimumColumnValue(), 
                                                           con.getMaximumValue().floatValue()),
                                          null);
        Point2D point2 = yaxis1.transform(new Point2D.Float((float)con.getMaximumColumnValue(), 
                                                             con.getMaximumValue().floatValue()),
                                          null);
        Point2D value = point1;
        
        int dataunitwidth = (int)((point2.getX() - point1.getX()) / con.getMaximumColumnValue());
        int boxwidth = (int)(dataunitwidth * boxWidth);
        float margin = (float)(dataunitwidth * ((1.0 - boxWidth)/2f));
        
        /* We paint the values starting at x-value "0".
         * As we only render BarCharts for ChartDataModels with
         * non-numeric x-axis values we don't have to read those
         * values from the data model. You can look in 
         * ObjectChartDataModel to see, how the x-axis bounds
         * are defined: the minimum value is always 0, the maximum
         * value is the amount of non-numeric x-axis values.
         */
        double currentvalue = 0.0;
        Rectangle2D box = null;
        Point2D oldmaxvalue;
        Point2D oldminvalue;
        
        for(int j = 0; j < maximumDataSetLength; j++) {
            double minvalue = 0.0;
            double maxvalue = 0.0;
            
            oldmaxvalue = pointzero;
            oldminvalue = pointzero;
            
            for(int i = 0; i < m.getDataSetNumber(); i++) {
                
                if(j < m.getDataSetLength(i))
                    currentvalue = m.getValueAt(i, j).doubleValue();
                else
                    currentvalue = 0.0;
                
                if(currentvalue < 0.0) {
                    minvalue += currentvalue;
                    yaxis1.transform(new Point2D.Float((float)j, (float)minvalue),
                                     value);
                   
                    box = 
                        new Rectangle2D.Float((float)(value.getX()),
                                              (float)Math.min(value.getY(), oldminvalue.getY()),
                                              (float)boxwidth,
                                              (float)Math.abs(oldminvalue.getY() - value.getY()));
                    oldminvalue = (Point2D)value.clone();
                 }
                else {
                    maxvalue += currentvalue;
                    yaxis1.transform(new Point2D.Float((float)j, (float)maxvalue),
                                     value);
                    
                    box = 
                        new Rectangle2D.Float((float)(value.getX()),
                                              (float)Math.min(value.getY(), oldmaxvalue.getY()),
                                              (float)boxwidth,
                                              (float)Math.abs(oldmaxvalue.getY() - value.getY()));
                    
                    oldmaxvalue = (Point2D)value.clone();
                }
                    
                g.setColor(rcm.getColor(i));
                g.fill(box);
                g.setColor(Color.black);
                g.draw(box);
            }
        } 
   }//end render method    

}

