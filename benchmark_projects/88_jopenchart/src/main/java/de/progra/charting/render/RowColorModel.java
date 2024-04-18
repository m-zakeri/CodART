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

    RowColorModel.java
    Created on 28. August 2001, 20:02
*/

package de.progra.charting.render;

import java.awt.Color;
import de.progra.charting.model.ChartDataModel;
import java.util.HashMap;
import java.awt.geom.RectangularShape;
import java.awt.geom.Ellipse2D;
import java.awt.geom.Rectangle2D;
import de.progra.charting.render.shape.Diamond2D;
import de.progra.charting.render.shape.Triangle2D;

/**
 * This class implements the correspondence between the DataSets and the
 * colors used for rendering the charts and the legend.
 * @author mueller
 * @version 1.0
 */
public class RowColorModel {

    private static RowColorModel instance;
    
    protected ChartDataModel model;
    
    protected final static Color[] predefinedColors = {Color.blue, Color.cyan, Color.red, 
                                                 Color.pink, Color.yellow,
                                                 Color.green, Color.magenta, Color.orange,
                                                 Color.darkGray, Color.gray, Color.lightGray};
    
	public static final Ellipse2D ELLIPSE_SHAPE = new Ellipse2D.Float(0f, 0f, 5f, 5f);
	public static final Rectangle2D SQUARE_SHAPE = new Rectangle2D.Float(0f, 0f, 5f, 5f);
	public static final Diamond2D DIAMOND_SHAPE = new Diamond2D(0f, 0f, 5f, 5f);
	public static final Triangle2D TRIANGLE_SHAPE = new Triangle2D(0f, 0f, 5f, 5f, false);
	public static final Triangle2D TRIANGLEDOWN_SHAPE = new Triangle2D(0f, 0f, 5f, 5f, true);
    
    protected final static RectangularShape[] predefinedShapes = {ELLIPSE_SHAPE,
                                                                  SQUARE_SHAPE, 
                                                                  DIAMOND_SHAPE,
                                                                  TRIANGLE_SHAPE,
                                                                  TRIANGLEDOWN_SHAPE};
                                                                  
    protected int predefinedColorsIdx = 0;
                          
    protected HashMap customColors = new HashMap();
    
    protected HashMap customShapes = new HashMap();
    
    /** Creates new RowColorModel.
     * @param model the ChartDataModel which contains the information about all the DataSets
     */
    public RowColorModel(ChartDataModel model) {
        this.model = model;
    }
    
    /** Use this method to get an instance of the chart's RowColorModel. 
     * @param model the ChartDataModel whose data sets will be mapped to
     * colors.
     * @return a new instance of RowColorModel if there's no instance 
     * of if the model has changed (esp. useful if you create multiple charts
     * after one another).
     * @deprecated
     */
    public static RowColorModel getInstance(ChartDataModel model) {
        if(instance == null || !model.equals(instance.model))
            instance = new RowColorModel(model);
        
        return instance;
    }
    
    /** Computes the amount of all Legend entries, ie. DataSets.
     * @return the amount of all rows, ie. DataSets.
     */    
    public int getRowCount() {
        return model.getDataSetNumber();
    }
    
    /** Returns the row title of a specific DataSet.
     * @param i the DataSet index
     * @return the String title
     */    
    public String getRow(int i) {
        return model.getDataSetName(i);
    }

    /** Computes the Color for a DataSet. For the first DataSets the stored Colors like <CODE>Color.red</CODE> etc are used. If there are more DataSets than stored colors, random colors are used.
     * @param row the row for which the Color should be returned
     * @return the Color stored for the given row.
     */    
    public Color getColor(int row) {
    	
    	// get the custom color
        Color c = (Color)customColors.get(new Integer(row));
        
        // if no custom color
        if(c == null) 
        {        	
        	// see if there is a predefined color for this row
        	if (predefinedColorsIdx < predefinedColors.length)  {
                c = predefinedColors[predefinedColorsIdx++];
            }
        	else {
                c = new Color((float)Math.random(),
                               (float)Math.random(),
                               (float)Math.random());
            }
          
          	// remember this 
            customColors.put(new Integer(row), c);
        }
        
        // done
        return c;
    }
    
    /** Returns the Shape for a DataSet. By default, the Shapes from
     * the <code>predefinedShapes</code> array are cycled through unless you define
     * your own shape to data binding using 
     * <code>setShape(int row, RectangularShape shape)</code>.
     * @param row the row for which the Shape should be returned
     * @return the Shape stored for the given row.
     */    
    public RectangularShape getShape(int row) {
    	
    	// get the custom color
        RectangularShape c = (RectangularShape)customShapes.get(new Integer(row));
        
        // if no custom color
        if(c == null) 
        {        	
        	// calculate the matching predefined shape by a modulo operation
            c = predefinedShapes[row % predefinedShapes.length];
            
          	// remember this 
            customShapes.put(new Integer(row), c);
        }
        
        // done
        return c;
    }
    
    /** Force a certain color for a row
     * @param row the row for which the Color should be set
     * @param color the color that is associated with the row
     */    
    public void setColor(int row, Color color) {
        customColors.put(new Integer(row), color);
    }
    
    /** Force a certain Shape for a row
     * @param row the row for which the Shape should be set
     * @param shape the RectangularShape that is associated with the row
     */    
    public void setShape(int row, RectangularShape shape) {
        customShapes.put(new Integer(row), shape);
    }
}
