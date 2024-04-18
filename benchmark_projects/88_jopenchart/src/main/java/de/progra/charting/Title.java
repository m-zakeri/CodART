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

    Title.java
    Created on 21. Juni 2001, 23:53
 */

package de.progra.charting;

import de.progra.charting.render.AbstractRenderer;
import de.progra.charting.render.ChartRenderingHints;
import java.awt.font.TextLayout;
import java.awt.font.FontRenderContext;
import java.awt.geom.Rectangle2D;
import java.awt.Graphics2D;
import java.awt.Dimension;
import java.awt.Color;
import java.awt.Font;

/** This class contains the Chart Title. It's also a Renderer
 * object with some extra properties.
 *
 * @author mueller
 * @version 1.0
 */
public class Title extends AbstractRenderer {

    protected String text = "Chart Title";
    protected Font font = new Font("Helvetica", Font.PLAIN, 22);
    
    /** Creates a new Title with the default settings*/
    public Title() {
    }
    
    /** Creates a new Title with the given text.
     * @param text the Title content
     */    
    public Title(String text) {
        setText(text);
    }
    
    /** Creates a new Title with the given text and font.
     * @param text the Title content
     * @param font the Title format
     */    
    public Title(String text, Font font) {
        setText(text);
        setFont(font);
    }
    
    /** Sets this title's text.
     * @param text the new text
     */
    public void setText(String text) {
        this.text = text;
    }
    
    /** Returns this title's text.
     * @return the String object containing the Title's text
     */
    public String getText() {        
        return text;
    }
    
    /** Sets the Font that is used to render the title.
     * @param f Sets the new font.
     */
    public void setFont(Font f) {
        font = f;
    }
    
    /** Returns this title's Font.
     * @return the Title's font
     */
    public Font getFont() {        
        return font;
    }
    
    /** This method is called by the paint method to do the actual painting.
     * The painting is supposed to start at point (0,0) and the size is
     * always the same as the preferred size. The paint method performs
     * the possible scaling.
     * @param g the <CODE>Graphics2D</CODE> object to paint in
     */
    public void paintDefault(Graphics2D g) {
        g.setColor(Color.black);
        TextLayout layout = new TextLayout(getText(), getFont(), 
                                           new FontRenderContext(null, true, false));
        
        layout.draw(g, 0f, (float)getPreferredSize().getHeight() - layout.getDescent());
    }
    
    /** Returns the preferred size needed for the renderer.
     * @return a non-null Dimension object
     */
    public Dimension getPreferredSize() {
        Rectangle2D titleBounds = 
            getFont().getStringBounds(getText(), 
                                      new FontRenderContext(null, true, false));
        
        return new Dimension((int)titleBounds.getWidth(),
                             (int)titleBounds.getHeight());
    }    
}
