// ===========================================================================
// CONTENT  : CLASS FileFinder
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.2 - 14/02/2003
// HISTORY  :
//  02/12/2001  duma  CREATED
//	23/01/2002	duma	added		-> findFile()
//	14/02/2003	duma	added		-> 3 File[] findFiles() methods
//
// Copyright (c) 2001-2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

/**
 * Helper class with convenient methods to find files.
 *
 * @author Manfred Duchrow
 * @version 1.2
 */
public class FileFinder implements FileHandler
{
  // =========================================================================
  // CONSTANTS
  // =========================================================================

  // =========================================================================
  // INSTANCE VARIABLES
  // =========================================================================
  private List collectedFiles = null ;
  protected List getCollectedFiles() { return collectedFiles ; }
  protected void setCollectedFiles( List newValue ) { collectedFiles = newValue ; }
  
  // =========================================================================
  // CLASS METHODS
  // =========================================================================

  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================
  /**
   * Initialize the new instance with default values.
   */
  protected FileFinder()
  {
  	super() ;
  	this.setCollectedFiles( new ArrayList() ) ;
  } // FileFinder()

  // =========================================================================
  // PUBLIC CLASS METHODS
  // =========================================================================
  
  /**
   * Tries to find the file with the given Name on the classpath.
   * If the file was found and really exists, then it will be returned.
   * In all other cases null will be returned.
   */
  public static File findFileOnClasspath( String filename ) 
  {
    ClassLoader cl 							= null ;
    File file										= null ;
    URL url											= null ;

    try
    {
      cl = FileFinder.class.getClassLoader() ;
      if ( cl == null )
      {
        // System.out.println( "No classloader found !\n<P>" ) ;
        return null ;
      }
      url = cl.getResource( filename ) ;
      if ( url == null )
      {
        // System.out.println( "Settings file '" + filename + "' not found in CLASSPATH !!!" ) ;
      }
      else
      {
        file = new File( url.getFile() ) ;
        // System.out.println( "Settings file '" + file.getAbsolutePath() + "' exists: " + file.exists() ) ;
        if ( ! fileExists( file ) )
          file = null ;
      }
    }
    catch ( Exception ex )
    {
      // ex.printStackTrace() ;
    }
    return file ;
  } // findFileOnClasspath()

  // -------------------------------------------------------------------------

  /**
   * Tries to find the file with the given Name.
   * First it looks if the file exists directly under the given name.
   * If not, it searches the classpath to find it.
   * If the file was found and really exists, then it will be returned.
   * In all other cases null will be returned.
   */
  public static File findFile( String filename ) 
  {
  	File aFile	= null ;
  	
  	aFile = new File( filename ) ;
  	if ( fileExists( aFile ) )
  		return aFile ;
  	
  	aFile = findFileOnClasspath( filename ) ;
  	
  	return aFile ;
  } // findFile()
   
  // -------------------------------------------------------------------------

	/**
	 * Return all files that match the given pattern(s) start searching in the
	 * specified dir. Searches in all sub directories as well.
	 * More than one pattern can be specified in parameter <i>pattern</i>.
	 * They have to be separated by ';'.
	 * 
	 * @param dir The directory to start searching (must not be null)
	 * @param pattern The pattern(s) the filenames must match (must not be null )
	 * @return All file found that matched to at least one of the patterns
	 * @throws IllegalArgumentException If <i>dir</i> or <i>pattern</i> is null
	 */
	public static File[] findFiles( String dir, String pattern )
	{
		return findFiles( dir, pattern, true ) ;
	} // findFiles()

	// -------------------------------------------------------------------------

	/**
	 * Return all files that match the given pattern(s) start searching in the
	 * specified dir. Look into sub directories if <i>recursive</i> is true.
	 * More than one pattern can be specified in parameter <i>pattern</i>.
	 * They have to be separated by ';'.
	 * 
	 * @param dir The directory to start searching (must not be null)
	 * @param pattern The pattern(s) the filenames must match (must not be null )
	 * @param recursive If false, only <i>dir</i> is searched, otherwise all sub directories as well
	 * @return All file found that matched to at least one of the patterns
	 * @throws IllegalArgumentException If <i>dir</i> or <i>pattern</i> is null
	 */
	public static File[] findFiles( String dir, String pattern, boolean recursive )
	{
		return findFiles( dir, pattern, recursive, (char)0 ) ;
	} // findFiles()

	// -------------------------------------------------------------------------

	/**
	 * Return all files that match the given pattern(s) start searching in the
	 * specified dir. Look into sub directories if <i>recursive</i> is true.
	 * Use the given digit wildcard in patterns to match single digits in 
	 * filenames.<br>
	 * More than one pattern can be specified in parameter <i>pattern</i>.
	 * They have to be separated by ';'.
	 * 
	 * @param dir The directory to start searching (must not be null)
	 * @param pattern The pattern(s) the filenames must match (must not be null )
	 * @param recursive If false, only <i>dir</i> is searched, otherwise all sub directories as well
	 * @param digitWildcard The wildcard character for digit representation in the pattern(s)
	 * @return All file found that matched to at least one of the patterns
	 * @throws IllegalArgumentException If <i>dir</i> or <i>pattern</i> is null
	 */
	public static File[] findFiles( String dir, String pattern, boolean recursive,
																	char digitWildcard )
	{
		FileFinder finder ;
		Character digitChar = null ;
		
		if ( dir == null )
			throw new IllegalArgumentException( "FileFinder.findFiles(): dir is null" ) ;

		if ( pattern == null )
			throw new IllegalArgumentException( "FileFinder.findFiles(): pattern is null" ) ;
		
		if ( digitWildcard > 0 )
			digitChar = new Character(digitWildcard) ;
		
		finder = new FileFinder() ;
		return finder.collectFiles( dir, pattern, recursive, digitChar ) ;
	} // findFiles()

	// -------------------------------------------------------------------------

  // =========================================================================
  // PRIVATE CLASS METHODS
  // =========================================================================

	private static boolean fileExists( File file )
	{
		boolean success = false ;
		if ( file != null )
		{
			try
			{
				FileLocator locator = FileLocator.create( file ) ;
				success = locator.exists() ;
			}
			catch ( Exception ex )
			{
				// nothing to do here
			}
		}
		return success ;
	} // fileExists()

  // -------------------------------------------------------------------------

  // =========================================================================
  // INTERFACE FileHandler METHODS
  // =========================================================================
	/**
	 * This method is called for each file, that a FileWalker instance finds.
	 * It must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param The file, currently found by the FileWalker instance
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean handleFile( File file ) 
	{
		this.getCollectedFiles().add( file ) ;			
		return true ;
	} // handleFile() 

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
	public boolean handleException( Exception ex, File file )
	{
		// System.out.println( "Problem with '" + file + "'" ) ;
		// System.out.println( ex ) ;
		return false ;
	} // handleException()

  // -------------------------------------------------------------------------
  
	/**
	 * This method is called for each directory, that a FileWalker finished to walk through.
	 * It must return true, if the FileWalker should continue. To stop the
	 * calling FileWalker it can return false.
	 *
	 * @param dir The directory, the FileWalker has finished to walk through
	 * @return true to continue, false to terminate processing of files
	 */
	public boolean directoryEnd( File dir )
	{
		return true ;
	} // directoryEnd()
  
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
	public boolean directoryStart( File dir, int count )
	{
		return true ;
	} // directoryStart()

  // -------------------------------------------------------------------------

  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================
	protected File[] collectFiles( String dir, String pattern, boolean recursive, 
																	Character digitWildcard )
	{
		FileWalker fileWalker ;
		List list ;
		
		fileWalker = new FileWalker( this ) ;
		if ( digitWildcard != null )
			fileWalker.setDigitWildcardChar( digitWildcard.charValue() ) ;
			
		fileWalker.walkThrough( dir, pattern, recursive ) ;
		list = this.getCollectedFiles() ;
		return (File[])list.toArray( new File[list.size()]) ;
	} // collectFiles()

	// -------------------------------------------------------------------------

} // class FileFinder