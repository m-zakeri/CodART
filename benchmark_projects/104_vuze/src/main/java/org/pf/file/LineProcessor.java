// ===========================================================================
// CONTENT  : INTERFACE LineProcessor
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.0 - 02/07/2003
// HISTORY  :
//  02/07/2003  mdu  CREATED
//
// Copyright (c) 2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file ;

// ===========================================================================
// IMPORTS
// ===========================================================================

/**
 * A simple interface that allows processing a longer text line by line.
 * Usually used together with FileUtil.processTextLines().
 *
 * @author Manfred Duchrow
 * @version 1.0
 */
public interface LineProcessor
{
  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================

	/**
	 * Processes the given line and returns true if the caller should continue.
	 * If false is returned, the caller should stop.
	 * 
	 * @param line The line to process (must not be null)
	 * @param lineNo	The linen number (starting with 1)
	 */
	public boolean processLine( String line, int lineNo ) ;

	// -------------------------------------------------------------------------
	
} // interface LineProcessor
