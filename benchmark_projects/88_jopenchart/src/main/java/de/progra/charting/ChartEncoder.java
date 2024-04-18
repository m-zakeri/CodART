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

    ChartEncoder.java
    Created on 11. November 2001, 18:23
 */

package de.progra.charting;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.OutputStream;
import java.io.IOException;
import java.awt.Rectangle;
import java.awt.Graphics2D;

/**
 * The ChartEncoder class provides several static methods to encode
 * charts to an OutputStream. It uses the Java Advanced Imaging Library
 * which is part of the JDK 1.4 release. The list of supported Image Formats
 * may vary depending on the actual release. Quoting from the current
 * webpage as of 28.1.2002: "As of JAI-1.1.1, the latest public version of JAI, 
 * the image formats supported by these ancillary codec classes are: 
 * BMP, GIF (decoder only), FlashPix (decoder only), JPEG, PNG, PNM, and TIFF."
 * For the actual list of supported image formats call 
 * <code>{@link #getSupportedFormats}</code>.
 * @author mueller
 * @version 1.0
 */
public class ChartEncoder {
    
    /** Prints the JPEG encoded image to an output stream.
     * @param os the OutputStream where the image will be printed to.
     * @param chart the Chart which will be printed to the output stream
     * @throws EncodingException if an error occurred accessing the Stream
     */
    public static void createJPEG(OutputStream os, Chart chart) throws EncodingException {
        boolean success = true;
        try {
            Rectangle r = chart.getBounds();
            BufferedImage img = new BufferedImage((int)r.getWidth(), 
                                                  (int)r.getHeight(), 
                                                  BufferedImage.TYPE_INT_RGB);

            Graphics2D grafx = img.createGraphics();
            chart.render(grafx);
            success = ImageIO.write(img, "jpeg", os);
            os.flush();        
        } catch(Throwable t) {
            throw new EncodingException(t.getMessage(), t);
        }
        
        if(!success)
            throw new EncodingException("No ImageWriter for writing JPEGs found.");
    }
    
    /** Prints the GIF encoded image to an output stream.
     * @param os the OutputStream where the image will be printed to.
     * @param chart the Chart which will be printed to the output stream
     * @throws EncodingException if an error occurred accessing the Stream
     * @deprecated GIF encoding is no longer supported, use PNG instead
     */
    public static void createGIF(OutputStream os, Chart chart) throws EncodingException {
    }
    
    /** Prints the PNG encoded image to an output stream.
     * @param os the OutputStream where the image will be printed to.
     * @param chart the Chart which will be printed to the output stream
     * @throws EncodingException if an error occurred accessing the Stream
     */
    public static void createPNG(OutputStream os, Chart chart) throws EncodingException {
        boolean success = true;        
        try {
            Rectangle r = chart.getBounds();
            BufferedImage img = new BufferedImage((int)r.getWidth(), 
                                                  (int)r.getHeight(), 
                                                  BufferedImage.TYPE_INT_RGB);

            Graphics2D grafx = img.createGraphics();
            chart.render(grafx);
            success = ImageIO.write(img, "png", os);
            os.flush();
        } catch(Throwable t) {
            t.printStackTrace();
            throw new EncodingException(t.getMessage(), t);
        }
        
        if(!success)
            throw new EncodingException("No ImageWriter for writing PNGs found.");
    }
    
    /** Prints the encoded image to an output stream.
     * @param os the OutputStream where the image will be printed to.
     * @param chart the Chart which will be printed to the output stream
     * @param format the informal format name 
     * @throws EncodingException if an error occurred accessing the Stream
     */
    public static void createEncodedImage(OutputStream os, Chart chart, String format) throws EncodingException {
        boolean success = true;
        try {
            Rectangle r = chart.getBounds();
            BufferedImage img = new BufferedImage((int)r.getWidth(), 
                                                  (int)r.getHeight(), 
                                                  BufferedImage.TYPE_INT_RGB);

            Graphics2D grafx = img.createGraphics();
            chart.render(grafx);
            success = ImageIO.write(img, format, os);
            os.flush();
        } catch(Throwable t) {
            throw new EncodingException(t.getMessage(), t);
        }
        
        if(!success)
            throw new EncodingException("No ImageWriter for writing "+format+" images found.");
    }
    
    /** Returns a String array containing the informal format names for 
     * all supported image encodings.
     */
    public static String[] getSupportedFormats() {
       return ImageIO.getWriterFormatNames(); 
    }
}
