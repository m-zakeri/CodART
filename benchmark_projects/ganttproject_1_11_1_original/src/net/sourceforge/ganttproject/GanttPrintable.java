/***************************************************************************
                           GanttPrintable.java  -  description
                             -------------------
    begin                : sep 2003
    copyright            : (C) 2003 by Thomas Alexandre
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

import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.print.PageFormat;
import java.awt.print.Printable;



/**
  * Class able to print an image
	*/
public class GanttPrintable 
    implements Printable  {

	/** The image to print */
	private BufferedImage image;
	
	/** Position of the image */
	private int x,y;
	

	/** Constructor */
	public GanttPrintable (BufferedImage image) {
		super();
		this.image = image;
		this.x=this.y=0;
	}

	/** Print the page */
  public int print(Graphics graphics, PageFormat pageFormat, int pageIndex) {

		//search for the best possition of the x, y coordinates
//		int i,j=0;
//		int cpt=0;
//		while(j<image.getHeight()) {
//			i=0;
//			while(i<image.getWidth()) {
//				
//				if(cpt==pageIndex) {
//					x=i;
//					y=j;
//				}
//				i+=(int) pageFormat.getImageableWidth();				
//				cpt++;
//			}
//			j+=(int) pageFormat.getImageableHeight();
//		}
//	
//		if(cpt<=pageIndex) return Printable.NO_SUCH_PAGE;
//		
//		if(x>image.getWidth())x=0;
//		if(y>image.getHeight())return Printable.NO_SUCH_PAGE;
//		
//		
      System.err.println("[GanttPrintable] print(): image: w="+image.getWidth()+" h="+image.getHeight());
      System.err.println("[GanttPrintable] print(): page="+pageIndex);
      int pagesPerRow = (int) (image.getWidth()/pageFormat.getImageableWidth()+1);
      int numRows = (int) (image.getHeight()/pageFormat.getImageableHeight()+1);
      System.err.println("[GanttPrintable] print(): numrows="+numRows+" pagesPerRow="+pagesPerRow);
      int totalPages = pagesPerRow*numRows;
      if (pageIndex>=totalPages) {
          return Printable.NO_SUCH_PAGE;
      }
      //
      int currentRow = pageIndex/pagesPerRow;
      int currentColumn = pageIndex - currentRow*pagesPerRow;
      System.err.println("[GanttPrintable] print(): curentpage="+currentColumn+" current row="+currentRow);
      //
      int leftx = (int) (currentColumn*pageFormat.getImageableWidth());
      int topy = (int) (currentRow*pageFormat.getImageableHeight());
      System.err.println("[GanttPrintable] print(): leftx="+leftx+" topy="+topy);
      //
      int height = (int) (currentRow+1<numRows ? pageFormat.getImageableHeight() : image.getHeight() - (pageFormat.getImageableHeight()*(numRows-1)));
      int width = (int) (currentColumn+1<pagesPerRow ? pageFormat.getImageableWidth() : image.getWidth() - (pageFormat.getImageableWidth()*(pagesPerRow-1)));
      //
      System.err.println("[GanttPrintable] print(): height="+height+" width="+width);
		Graphics2D g2d = (Graphics2D) graphics;
		g2d.translate(pageFormat.getImageableX(), pageFormat.getImageableY());

        Image subimage=image.getSubimage(leftx, topy, width, height);
		g2d.drawImage(subimage, 0, 0, null);
//		int imgw = (int)pageFormat.getImageableWidth();
//		int imgh = (int)pageFormat.getImageableHeight();
//		
//		int width=imgw+x<image.getWidth()?imgw:image.getWidth()-x;
//		int height=imgh+y<image.getHeight()?imgh:image.getHeight()-y;
//		
//		g2d.drawImage(image.getSubimage(x,y,width,height),0,0,null);
//		
//		
//
		return Printable.PAGE_EXISTS;
		
	}
}		
