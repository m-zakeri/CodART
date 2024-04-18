// ===========================================================================
// CONTENT  : CLASS ExtendedFileFilter
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.1 - 14/02/2003
// HISTORY  :
//  24/01/2000  duma  CREATED
//	14/02/2003	duma	added		->	Support for digit wildcard characher
//
// Copyright (c) 2000-2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.File;
import java.io.FilenameFilter;
import java.util.Iterator;
import java.util.List;
import java.util.Vector;

import org.pf.text.StringPattern;

/**
 * This filter implements the standard pattern matching on UNIX and Windows
 * platforms. It supports the wildcards '*' and '?' on file names.  <br>
 * It allows to set more than one pattern.
 * Apart from that it allows control over inclusion/exclusion of directories 
 * independently from name patterns.
 *
 * @author Manfred Duchrow
 * @version 1.1
 */
public class ExtendedFileFilter implements FilenameFilter
{ 
  // =========================================================================
  // CONSTANTS
  // =========================================================================
	protected final static int DIR_CHECK_NAME		= 1 ;
	protected final static int DIR_INCLUDE			= 2 ;
	protected final static int DIR_EXCLUDE			= 3 ;
		
  // =========================================================================
  // INSTANCE VARIABLES
  // =========================================================================
  private List stringPatterns = new Vector() ;
  protected List getStringPatterns() { return stringPatterns ; }  
  protected void setStringPatterns( List newValue ) { stringPatterns = newValue ; }  
	
  private int dirHandling = DIR_CHECK_NAME ;
  protected int getDirHandling() { return dirHandling ; }  
  protected void setDirHandling( int newValue ) { dirHandling = newValue ; }  
		
  // =========================================================================
  // CLASS METHODS
  // =========================================================================
  
  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================

  /**
   * Initialize the new instance with default values.
   */
  public ExtendedFileFilter()
  {
  } // ExtendedFileFilter()  

  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================

	/**
	 * Adds a pattern. All filenames match this pattern are acceptable.   <br>
	 * Case sensitivity is switched on !
	 * 
	 * @param pattern The pattern string containing  optional wildcards ( '*', '?' ) 
	 */
	public void addPattern( String pattern )
	{
		StringPattern stringPattern		= null ;
		
		stringPattern = new StringPattern( pattern, false ) ;
		this.getStringPatterns().add( stringPattern ) ;
	} // addPattern()
  
  // -------------------------------------------------------------------------

	/**
	 * Adds a pattern. All filenames match this pattern are acceptable.   <br>
	 * Case sensitivity is switched on !
	 * The second parameter specifies a character that will be recognized in the
	 * pattern as a placeholder for a single digit character.  <p>
	 * A patterb "XX-####.log" with a digitWildcard set to '#' wil match to
	 * "XX-2000.log" and "XX-7376.log" but not to "XX-C363.log" and "XX-dddd.log".
	 * 
	 * @param pattern The pattern string containing  optional wildcards ( '*', '?' ) 
	 * @param digitWildcard The character that will be treated as wildcard for digits ('0'-'9')
	 */
	public void addPattern( String pattern, char digitWildcard )
	{
		StringPattern stringPattern		= null ;
		
		stringPattern = new StringPattern( pattern, false, digitWildcard ) ;
		this.getStringPatterns().add( stringPattern ) ;
	} // addPattern()
  
  // -------------------------------------------------------------------------

	/**
	 * Adds a pattern. All filenames match this pattern are acceptable.
	 * 
	 * @param pattern The pattern string containing  optional wildcards ( '*', '?' ) 
	 * @param ignoreCase If true, all character comparisons are ignoring uppercase/lowercase
	 */
	public void addPattern( String pattern, boolean ignoreCase )
	{
		StringPattern stringPattern		= null ;
		
		stringPattern = new StringPattern( pattern, ignoreCase ) ;
		this.getStringPatterns().add( stringPattern ) ;
	} // addPattern()
  
  // -------------------------------------------------------------------------

	/**
	 * Adds a pattern. All filenames that match this pattern are acceptable.
	 * Additionally to the standard wildcards '*' and '?' a wildcard for single
	 * digit characters ('0' - '9') can be specified here.
	 * 
	 * @param pattern The pattern string containing  optional wildcards ( '*', '?' ) 
	 * @param ignoreCase If true, all character comparisons are ignoring uppercase/lowercase
	 * @param digitWildcard The character that will be treated as wildcard for digits ('0'-'9')
	 */
	public void addPattern( String pattern, boolean ignoreCase, char digitWildcard )
	{
		StringPattern stringPattern		= null ;
		
		stringPattern = new StringPattern( pattern, ignoreCase, digitWildcard ) ;
		this.getStringPatterns().add( stringPattern ) ;
	} // addPattern()
  
  // -------------------------------------------------------------------------

	/**
	 * Sets the filter to only accept directories that match a defined pattern.
	 */
	public void checkNameOfDirectories()
	{
		this.setDirHandling( DIR_CHECK_NAME ) ;
	} // checkNameOfDirectories()
  
  // -------------------------------------------------------------------------

	/**
	 * Sets the filter to always accept directories, even if they don't match
	 * a given pattern.
	 */
	public void alwaysIncludeDirectories()
	{
		this.setDirHandling( DIR_INCLUDE ) ;
	} // alwaysIncludeDirectories()
  
  // -------------------------------------------------------------------------

	/**
	 * Sets the filter to never accept directories.
	 */
	public void alwaysExcludeDirectories()
	{
		this.setDirHandling( DIR_EXCLUDE ) ;
	} // alwaysExcludeDirectories()
  
  // -------------------------------------------------------------------------

  /**
   * Tests if a specified file should be included in a file list.
   *
   * @param dir the directory in which the file was found.
   * @param name the name of the file.
   * @return true if and only if the name should be included in the file list, false otherwise.
   */
	public boolean accept( File dir, String name )
	{		
		File fileOrDir		= null ;
		
		fileOrDir = new File( dir, name ) ;
		if ( fileOrDir.isDirectory() )
		{
			if ( this.mustIncludeDirectories() )
				return true ;
			if ( this.mustExcludeDirectories() )
				return false ;
		}
		
		return ( this.checkAgainstPatterns( name ) ) ;
	} // accept()
		
  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================

	protected boolean checkAgainstPatterns( String name )
	{
		Iterator iterator			= null ;
		StringPattern pattern	= null ;
		
		iterator = this.getStringPatterns().iterator() ;
		while ( iterator.hasNext() )
		{
			pattern = (StringPattern)iterator.next() ;
			if ( pattern.matches( name ) )
				return true ;
		} // while
		
		return false ; // No pattern matched
	} // checkAgainstPatterns

  // -------------------------------------------------------------------------

	/**
	 * Returns true if the filter always accepts directories, even if they don't match
	 * a given pattern.
	 */
	public boolean mustIncludeDirectories()
	{
		return ( this.getDirHandling() == DIR_INCLUDE ) ;
	} // mustIncludeDirectories()
  
  // -------------------------------------------------------------------------

	/**
	 * Returns true if the filter never accepts directories.
	 */
	public boolean mustExcludeDirectories()
	{
		return ( this.getDirHandling() == DIR_EXCLUDE ) ;
	} // mustExcludeDirectories()
  
  // -------------------------------------------------------------------------

// -------------------------------------------------------------------------

} // class ExtendedFileFilter