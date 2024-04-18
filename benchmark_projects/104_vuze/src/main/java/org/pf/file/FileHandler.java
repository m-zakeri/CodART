// ===========================================================================
// CONTENT  : INTERFACE FileHandler
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.0 - 24/01/2000
// HISTORY  :
//  24/01/2000  duma  CREATED
//
// Copyright (c) 2000, by MDCS. All rights reserved.
// ===========================================================================
package org.pf.file;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.File;

/**
 * This interface must be implemented by classes, that want to use the generic
 * services of <b>FileWalker</b>.  <br>
 * It defines callback methods, that are invoked by a FileWalker instance, when
 * it is 'walking' through a directory(-tree).
 *
 * @see FileWalker
 * @author Manfred Duchrow
 * @version 1.0
 */
public interface FileHandler
{ 
  // -------------------------------------------------------------------------
  
  // =========================================================================
  // CONSTANTS
  // =========================================================================
  
  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================

	/**
	 * This method is called for each file, that a FileWalker instance finds.
	 * It must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param The file, currently found by the FileWalker instance
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean handleFile( File file ) ;

  // -------------------------------------------------------------------------

	/**
	 * This method is called for whenever an exception occurs in walking through
	 * the directories.   <br>
	 * The method must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param ex The exception to handle
	 * @param The file, currently found by the FileWalker instance
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean handleException( Exception ex, File file ) ;

  // -------------------------------------------------------------------------
  
	/**
	 * This method is called for each directory, that a FileWalker finished to walk through.
	 * It must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param dir The directory, the FileWalker has finished to walk through
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean directoryEnd( File dir ) ;	
  
  // -------------------------------------------------------------------------
  
  /**
	 * This method is called for each directory, that a FileWalker starts to walk through.
	 * It must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param dir The directory, the FileWalker is starting to walk through
	 * @param count The number of files and directories the FileWalker found in the directory
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean directoryStart( File dir, int count ) ;

  // -------------------------------------------------------------------------
  
} // class FileHandler