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

    AbstractRenderer.java
    Created on 21. Juni 2001, 12:32
*/

package de.progra.charting.render;

import java.awt.image.BufferedImage;
import java.awt.Rectangle;
import java.awt.Image;
import java.awt.Graphics2D;
import java.awt.Dimension;
import java.awt.Color;

/**
 * The AbstractRenderer provides default implementations for the set and
 * get methods of every Renderer. Especially it provides a default mechanism
 * for scaling Renderer instances whose actual bounds are smaller than their
 * preferred size. As a consequence, every Renderer instance only needs
 * to implement paintDefault() which has to render the object from coordinates
 * 0,0 onwards using the preferred size.
 * @author mueller
 * @version 1.0
 */
public abstract class AbstractRenderer implements Renderer {

    Rectangle bounds = new Rectangle(0, 0, 
                                     Integer.MAX_VALUE, 
                                     Integer.MAX_VALUE);
    
    /** Creates new AbstractRenderer */
    public AbstractRenderer() {
    }
    
    /** Sets the bounds the layout manager has assigned to
     * this renderer. Those, of course, have to be
     * considered in the rendering process.
     * @param bounds the new bounds for the renderer.
     */
    public void setBounds(Rectangle bounds) {
        this.bounds = bounds;
    }
    
    /** Gets the bounds for this renderer.
     * @return the bounds of this renderer. If <code>setBounds</code> has not
     * been called before, the bounds computed from
     * <code>getPreferredSize</code> is returned.
     */
    public Rectangle getBounds() {
        return bounds;
    }
    
  
    /** Renders the Object in the Graphics object. Creates a BufferedImage
     * and the corresponding Graphics2D object to paint in. The Image is
     * created using the preferred size. Afterwards <code>paintDefault</code>
     * is called to perform a standard painting in the Graphics object.
     * If the bounds and the preferred size don't match the image is 
     * scaled afterwards.
     * @param g the Graphics2D object in which to render
     */
    public void render(Graphics2D g) {        
        Dimension d = getPreferredSize();
        BufferedImage im = new BufferedImage((int)d.width,
                                             (int)d.height,
                                             BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = im.createGraphics();
        g2.setColor(Color.white);
        g2.fillRect(0, 0, d.width, d.height);
        g2.setColor(Color.black);
        
        paintDefault(g2);
        
        if(d.width > getBounds().getWidth() ||
           d.height > getBounds().getHeight()) {
           // Scale Image
           Image scale = im.getScaledInstance((int)getBounds().getWidth(),
                                              (int)getBounds().getHeight(),
                                              Image.SCALE_SMOOTH);
           
           g.drawImage(scale,
                       (int)getBounds().getX(),
                       (int)getBounds().getY(),
                       null);
        } else             
           g.drawImage(im, (int)getBounds().getX(), 
                       (int)getBounds().getY(), null); 
    }
    
    /** This method is called by the paint method to do the actual painting.
     * The painting is supposed to start at point (0,0) and the size is
     * always the same as the preferred size. The paint method performs
     * the possible scaling.
     * @param g the Graphics2D object to paint in.
     */
    public abstract void paintDefault(Graphics2D g);
}