// ===========================================================================
// CONTENT  : CLASS FileWalker
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.2 - 04/07/2003
// HISTORY  :
//  21/01/2000  duma  CREATED
//	14/02/2003	duma	added		->	Support for patterns with wildcards for digits
//	04/07/2003	duma	bugfix	->	NullPointerException in walkThrough for protected directories
//
// Copyright (c) 2000-2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.File;
import java.io.FilenameFilter;

import org.pf.text.StringUtil;

/**
 * This class provides services to navigate through a file directory and
 * handle files that match a name filter.
 *
 * @author Manfred Duchrow
 * @version 1.2
 */
public class FileWalker
{ 
  // =========================================================================
  // CONSTANTS
  // =========================================================================
  /**
   * The character to be used to separate filename patterns (';').
   */
  public static final char PATTERN_SEPARATOR_CHAR		= ';' ;

  /**
   * The character to be used to separate filename patterns (';') as String.
   */
  public static final String PATTERN_SEPARATOR		  = ";" ;
  
  // =========================================================================
  // INSTANCE VARIABLES
  // =========================================================================
  private FileHandler fileHandler = null ;
  protected FileHandler getFileHandler() { return fileHandler ; }  
  protected void setFileHandler( FileHandler newValue ) { fileHandler = newValue ; }  

  private boolean goOn = true ;
  protected boolean getGoOn() { return goOn ; }  
  protected void setGoOn( boolean newValue ) { goOn = newValue ; }  
	
  private Character digitWildcard = null ;
  protected Character getDigitWildcard() { return digitWildcard ; }
  protected void setDigitWildcard( Character newValue ) { digitWildcard = newValue ; }	
  // =========================================================================
  // CLASS METHODS
  // =========================================================================
  
  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================
  /**
   * Initialize the new instance with default values.
   */
  public FileWalker( FileHandler handler )
  {
  	this.setFileHandler( handler ) ;
  } // FileWalker()  

	// -------------------------------------------------------------------------

  /**
   * Initialize the new instance with a file handler and a wildcard character
   * for digits.
   * 
   * @param handler The file handler that gets all found files
   * @param digitWildcard A character that is used as wildcard for digits in filname patterns
   */
  public FileWalker( FileHandler handler, char digitWildcard )
  {
  	this( handler ) ;
		this.setDigitWildcardChar( digitWildcard ) ;  	
  } // FileWalker()  

	// -------------------------------------------------------------------------

  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================
  
  /**
   * This method starts in the given directory to search for all files
   * matching the given pattern(s).   <br>
   * There can be more than one pattern in the pattern parameter. They have 
   * to be separated by the PATTERN_SEPARATOR (';').   <p>
   * If recursive is <b>true</b> it goes down to each subdirectory and doing
   * the same there.<br>
   * For each matching file (non-directory) the defined <i>FileHandler.handle()</i>
   * is called.
   *
   * @param dir The directory where to start
   * @param pattern The file name pattern(s) for filtering out the correct files ( wildcards '*' and '?' )
   * @param recursive If set to true, the file selection is going down to all subdirectories
   * @return the number of found files, that have matched the given pattern.
   */
	public long walkThrough( String dir, String pattern, boolean recursive )
	{
		ExtendedFileFilter filter		= null ;
		String[] patterns						= null ;
		String strPattern ;
		
		this.setGoOn( true ) ;
		filter = new ExtendedFileFilter() ;
		
		patterns = this.extractPatterns( pattern ) ;
		for (int i = 0; i < patterns.length; i++)
		{
			strPattern = patterns[i] ;
			if ( this.hasDigitWildcard() )
			{
				filter.addPattern( strPattern, true, this.getDigitWildcardChar() ) ;
			}
			else
			{
				filter.addPattern( strPattern, true ) ;
			}
		}
		
		if ( recursive )
			filter.alwaysIncludeDirectories() ;
		else
			filter.alwaysExcludeDirectories() ;

		return this.walkThrough( dir, filter, recursive ) ;	
	} // walkThrough()

	// -------------------------------------------------------------------------
	
	/**
	 * Sets the given character as a wildcard character to match
	 * digits ('0'-'9') only.   <br>
	 * 
	 * @param digitWildcard The placeholder character for digits
	 */
	public void setDigitWildcardChar( char digitWildcard )
	{
		if ( digitWildcard <= 0 )
		{
			this.setDigitWildcard( null ) ;
		}
		else
		{
			this.setDigitWildcard( new Character( digitWildcard ) ) ;
		}
	} // setDigitWildcardChar()

	// -------------------------------------------------------------------------

  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================

	protected long walkThrough( String dir, FilenameFilter filter, boolean recursive )
	{
		long counter			= 0 ;
		File directory		= null ;
		File file					= null ;
		File[] files			= null ;
		int index					= 0 ;
		
		directory = new File( dir ) ;
		files = directory.listFiles( filter ) ;
		if ( files == null )  // BUGFIX suggested by Kyle Gossman
			return counter ;
			
		this.setGoOn( this.getFileHandler().directoryStart( directory, files.length ) ) ;
		if ( ! this.getGoOn() )
			return counter ;
		
		for ( index = 0 ; index < files.length ; index++ )
		{
			file = files[index] ;
			
			if ( file.isDirectory() )
			{
				if ( recursive )
				{
					counter += this.walkThrough( file.getPath(), filter, recursive ) ;
				}
			}
			else
			{
				this.setGoOn( this.getFileHandler().handleFile( file ) ) ;
				counter++ ;
			}
			if ( ! this.getGoOn() )
				break ;
		} // for
		this.setGoOn( this.getFileHandler().directoryEnd( directory ) ) ;
				
		return counter ;
	} // walkThrough()

  // -------------------------------------------------------------------------

	protected String[] extractPatterns( String pattern )
	{
		return StringUtil.current().parts( pattern, PATTERN_SEPARATOR ) ;
	} // extractPatterns()

  // -------------------------------------------------------------------------

	protected char getDigitWildcardChar()
	{
		if ( this.hasDigitWildcard() )
			return this.getDigitWildcard().charValue() ;
		else
			return '\0' ;
	} // getDigitWildcardChar()

	// -------------------------------------------------------------------------
	
	protected boolean hasDigitWildcard()
	{
		return this.getDigitWildcard() != null ;
	} // hasDigitWildcard()

	// -------------------------------------------------------------------------   
	
} // class FileWalker