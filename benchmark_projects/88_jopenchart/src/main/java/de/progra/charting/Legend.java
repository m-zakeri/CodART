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

    Legend.java
    Created on 26. Juni 2001, 22:49
 */

package de.progra.charting;

import java.awt.*;
import java.awt.geom.*;
import java.awt.font.*;
import java.awt.image.*;
import de.progra.charting.render.*;

/** This class implements a Chart's Legend. The Strings and the colors 
 * can be set manually or eventually through some kind of data model.
 */
public class Legend extends AbstractRenderer {
        
    protected int inner_margin = 5;
    protected int color_text_spacing = 10;
    protected Font font = new Font("Helvetica", Font.PLAIN, 14);
    protected Rectangle colorbox = new Rectangle(25, 15);
   
    protected RowColorModel rcm;
    
    /** Creates a default Legend. */
    public Legend() {
    }
    
    /** Creates a Legend with the given Strings and Colors.
     * @param rcm the RowColorModel containing the row titles and their colors.
     */
    public Legend(RowColorModel rcm) {
        setRowColorModel(rcm);
    } 
    
    /** Defines the RowColorModel of the DataModel.
     * @param rcm the RowColorModel
     */
    public void setRowColorModel(RowColorModel rcm) {
        this.rcm = rcm;
    }
    
    /** Returns the RowColorModel of the DataModel.
     * @return the RowColorModel
     */
    public RowColorModel getRowColorModel() {
        return rcm;
    }
    
    /** Sets the size of the color boxes.
     * @param r the Rectangle defining the colored box rendered left to every Legend entry.
     */
    public void setColorBox(Rectangle r) {
        colorbox = r;
    }
    
    /** Returns the size of the color boxes.
     * @return the Rectangle defining the colored box left to every Legend entry
     */
    public Rectangle getColorBox() {        
        return colorbox;
    }
    
    /** Sets the Font that is used to render the Legend.
     * @param f the font object
     */
    public void setFont(Font f) {
        font = f;
    }
    
    /** Returns this Legend's Font.
     * @return the font currently in use
     */
    public Font getFont() {        
        return font;
    }
    
    /** Returns the preferred size needed for the renderer.
     * @return a non-null Dimension object
     */
    public Dimension getPreferredSize() {
        RowColorModel rcm = getRowColorModel();
        
        int maxTitleWidth = Integer.MIN_VALUE;
        int titleHeight = Integer.MIN_VALUE;
        
        titleHeight = 
            (int)getFont().getMaxCharBounds(new FontRenderContext(null, true, false)).getHeight();        
        
        for(int i = 0; i < rcm.getRowCount(); i++) {
            TextLayout layout = 
                new TextLayout(rcm.getRow(i), getFont(), 
                               new FontRenderContext(null, true, false));
            
            maxTitleWidth = (int)Math.max((double)maxTitleWidth, 
                                          layout.getBounds().getWidth());
        }
        
        return new Dimension((int)(2*inner_margin + color_text_spacing +
                             getColorBox().getWidth() + maxTitleWidth),
                             Math.max(titleHeight, (int)getColorBox().getHeight()) * rcm.getRowCount() +
                             (rcm.getRowCount() + 1) * inner_margin);
    }
    
    /** This method is called by the paint method to do the actual painting.
     * The painting is supposed to start at point (0,0) and the size is
     * always the same as the preferred size. The paint method performs
     * the possible scaling.
     * @param g the <CODE>Graphics2D</CODE> object to paint in
     */
    public void paintDefault(Graphics2D g) {
        RowColorModel rcm = getRowColorModel();
        
        int height = Integer.MIN_VALUE;
        
        int fontheight = 
            (int)getFont().getMaxCharBounds(g.getFontRenderContext()).getHeight();        
        height = (int)Math.max(fontheight, getColorBox().getHeight());
        
        int startx = inner_margin;
        int starty = inner_margin;
        
        Rectangle colorBox = getColorBox();
        
        /* Rendering the Text and the ColorBoxes. */
        for(int i = 0; i < rcm.getRowCount(); i++) {
            colorBox.setLocation(startx, starty);
            g.setColor(rcm.getColor(i));
            
            g.fill(colorBox);
            
            g.setColor(Color.black);
            
            TextLayout layout = 
                new TextLayout(rcm.getRow(i), getFont(), 
                               new FontRenderContext(null, true, false));
                   
            layout.draw(g, 
                        startx + (int)colorBox.getWidth() + color_text_spacing, 
                        starty+(int)colorBox.getHeight());
            
            starty = starty + height + inner_margin;
        }
    }
}