/***************************************************************************
                           GanttSplash.java  -  description
                             -------------------
    begin                : dec 2002
    copyright            : (C) 2002 by Thomas Alexandre
    email                : alexthomas(at)ganttproject.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

package net.sourceforge.ganttproject;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Toolkit;
import java.awt.font.FontRenderContext;
import java.awt.font.TextLayout;
import java.awt.geom.Rectangle2D;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JRootPane;

import net.sourceforge.ganttproject.gui.DialogAligner;
import net.sourceforge.ganttproject.util.TextLengthCalculatorImpl;



/**
 * Class to put a splash before lunch the soft
 */

public class GanttSplash extends JFrame {

    private JLabel mySplashComponent;

    public GanttSplash(){
    	super("GanttProject");
    	
    	ImageIcon splashImage = new ImageIcon(getClass().getResource("/icons/splash.png"));
        mySplashComponent = new JLabel(splashImage) {
        	public void paint (Graphics g) {
        		super.paint(g);
        		Graphics2D g2 = (Graphics2D) g;
        		g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        		Font font = new Font("Arial", Font.BOLD + Font.ITALIC, 22);
        		g2.setFont(font);
        		g2.setColor(Color.black);
                int textLength = TextLengthCalculatorImpl.getTextLength(g, GanttProject.version);
        		g2.drawString(GanttProject.version, (int) (getSize().getWidth() - textLength-5), 236);
        		g2.setColor(Color.white);
        		g2.drawString(GanttProject.version, (int) (getSize().getWidth() - textLength- 6), 235);
        		
        	}
        };                		
    }
        
    public void setVisible(boolean b) {
        if (b) {
            getContentPane().add(mySplashComponent, BorderLayout.CENTER);
            pack();
            DialogAligner.center(this);
        }
        super.setVisible(b);
    }
    
    protected void frameInit() {
        super.frameInit();
        ImageIcon icon = new ImageIcon(getClass().getResource(
        "/icons/ganttproject.png"));
        setIconImage(icon.getImage());  //set the ganttproject icon
        setUndecorated(true);
    }
    
    public void close() {
          setVisible(false);
    	  dispose();
    }

    public JLabel getSplashComponent() {
        return mySplashComponent;
    }
}

