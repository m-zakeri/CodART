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

    Renderer.java
    Created on 5. Juni 2001, 17:13
*/

package de.progra.charting.render;

import java.awt.Graphics2D;
import java.awt.Dimension;
import java.awt.Rectangle;


/** This interface defines the common methods needed for a Renderer class. This
 * contains methods to define specific options, set/get the rendering size and
 * to finally render something.
 */
public interface Renderer {
    
    /** Returns the preferred size needed for the renderer.
     * @return a non-null Dimension object
     */
    public Dimension getPreferredSize();
    
    /** Sets the bounds the layout manager has assigned to
     * this renderer. Those, of course, have to be 
     * considered in the rendering process.
     * @param bounds the new bounds for the renderer.
     */
    public void setBounds(Rectangle bounds);
    
    /** Gets the bounds for this renderer. 
     * @return the bounds of this renderer. If <code>setBounds</code> has not
     * been called before, the bounds computed from 
     * <code>getPreferredSize</code> is returned.
     */
    public Rectangle getBounds();
    
    /** Finally renders the Object in the Graphics object.
     * @param g the Graphics2D object in which to render
     */
    public void render(Graphics2D g);
}

