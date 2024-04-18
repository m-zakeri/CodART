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

     EncodingException.java
     Created on 28. Januar 2002, 21:32
 */

package de.progra.charting;

/**
 * This class encapsulates all image encoding exceptions.
 * @author  mueller
 */
public class EncodingException extends java.lang.Exception {

    private Throwable cause;
    
    /**
     * Creates a new instance of <code>EncodingException</code> without detail message.
     */
    public EncodingException() {
    }

    /**
     * Constructs an instance of <code>EncodingException</code> with the specified detail message.
     * @param msg the detail message.
     */
    public EncodingException(String msg) {
        super(msg);
    }
    
    /**
     * Constructs an instance of <code>EncodingException</code> with the specified detail message
     * and the specified cause.
     * @param msg the detail message.
     * @param cause the Throwable that caused this Exception
     */
    public EncodingException(String msg, Throwable cause) {
        super(msg);
        this.cause = cause;
    }    
    
    /** Returns the Throwable that caused the Exception to be thrown. */
    public Throwable getCause() {
        return cause;
    }    
}