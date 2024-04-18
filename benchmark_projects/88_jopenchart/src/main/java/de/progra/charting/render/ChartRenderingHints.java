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

    ChartRenderingHints.java
    Created on 21. Juni 2001, 12:17
*/

package de.progra.charting.render;

import java.awt.*;

/**
 * This class contains the set of rendering options for a renderer.
 * It extends RenderingHints to provide specific rendering options
 * for fonts, colors etc.
 * @author mueller
 * @version 1.0
 */
public class ChartRenderingHints extends java.util.HashMap {

    /** the key constant for the Title String
     */    
    public final static Object TITLE_STRING_KEY = new Integer(1);
    /** the key constant for the Title font
     */    
    public final static Object TITLE_FONT_KEY = new Integer(2);
    /** the key constant for the Legend font
     */    
    public final static Object LEGEND_FONT_KEY = new Integer(3);
    /** the key constant for the Legend's colorbox
     */    
    public final static Object LEGEND_COLORBOX_KEY = new Integer(4);
    /** the key constant for the Legend's RowColorModel
     */    
    public final static Object LEGEND_ROWCOLORS_KEY = new Integer(5);
    
    /** Creates new ChartRenderingHints */
    public ChartRenderingHints() {
        super();
        
        // Default Title Properties
        put(TITLE_STRING_KEY, "Diagramm Titel");
        put(TITLE_FONT_KEY, new Font("Helvetica", Font.PLAIN, 22));
        
        // Default Legend Properties
        put(LEGEND_FONT_KEY, new Font("Helvetica", Font.PLAIN, 14));
        put(LEGEND_COLORBOX_KEY, new Rectangle(25, 15));
    }
}
