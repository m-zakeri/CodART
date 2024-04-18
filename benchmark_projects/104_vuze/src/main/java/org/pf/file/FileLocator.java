// ===========================================================================
// CONTENT  : CLASS FileLocator
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.3 - 14/03/2003
// HISTORY  :
//  17/05/2002  duma  CREATED
//	24/05/2002	duma	added		->	toURL(), isFile(), isDirectory(), getAbsolutePath()
//	21/06/2002	duma	added		->	realFile()
//	14/03/2003	duma	added		->	getStandardizedPath(), getStandardizedAbsolutePath()
//
// Copyright (c) 2002-2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file ;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import org.pf.text.StringUtil; 

/**
 * This class mainly supports access to files which can be in the normal
 * file directory structure or inside zip archives.
 * The main purpose is to provide methods that transparently treat files 
 * the same way whether they are in the normal directory structure or
 * inside archives.
 * The syntax is simply to allow archive names in a path name at any place
 * where a sub-directory name can be. <br>
 * Examples: <br>
 * <ul>
 *   <li>d:\temp\archive.zip\config\nls.properties</li>
 *	 <li>/usr/java/jdk1.3/src.jar/java/io/File.java</li>
 * </ul>
 * @author Manfred Duchrow
 * @version 1.3
 */
public class FileLocator
{
  // =========================================================================
  // CONSTANTS
  // =========================================================================
	private static final boolean DEBUG = false ;
	private static final String FILE_PROTOCOL_INDICATOR = "file:" + File.separator ;
	private static final String ARCHIVE_INDICATOR				= "!" + File.separator ;

  // =========================================================================
  // INSTANCE VARIABLES
  // =========================================================================
  private FileLocator parent = null ;
  protected FileLocator getParent() { return parent ; }
  protected void setParent( FileLocator newValue ) { parent = newValue ; }

  private File file = null ;
  protected File getFile() { return file ; }
  protected void setFile( File newValue ) { file = newValue ; }
  
  private ZipFile zipFile = null ;
  protected ZipFile getZipFile() { return zipFile ; }
  protected void setZipFile( ZipFile newValue ) { zipFile = newValue ; }  
   
  private boolean exists = true ;
  protected boolean getExists() { return exists ; }
  protected void setExists( boolean newValue ) { exists = newValue ; }
      
  private Exception exception = null ;
  protected Exception getException() { return exception ; }
  protected void setException( Exception newValue ) { exception = newValue ; }
      
  // =========================================================================
  // CLASS METHODS
  // =========================================================================
  /**
   * Create a file locator that corresponds to the given file name.
   */
  public static FileLocator create( File file )
  {
  	FileLocator locator = new FileLocator() ;
		
		return locator.createFrom( file ) ;
  } // create()

  // -------------------------------------------------------------------------

  /**
   * Create a file locator that corresponds to the given file name.
   */
  public static FileLocator create( String filename )
  {
		return create( new File( filename ) ) ;
  } // create()

  // -------------------------------------------------------------------------

  private static FileLocator newWith( FileLocator aParent, String[] pathElements )
		throws Exception
  {
  	FileLocator locator = new FileLocator() ;
		
		return locator.createFrom( aParent, pathElements ) ;
  } // newWith()

  // -------------------------------------------------------------------------

  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================
  /**
   * Initialize the new instance with default values.
   */
  private FileLocator()
  {
    super() ;
  } // FileLocator()

  // -------------------------------------------------------------------------

  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================

	/**
	 * Returns the file that contains the data the locator points to.
	 * If the locator points to a normal file in a directory, than
	 * this file will be returned.
	 * If the locator points to a file inside an archive, the file
	 * will be unzipped into the <i><b>temp</i></b> directory and this
	 * temp file will be returned.
	 * If the locator points to a none existing file, this method 
	 * returns false.
	 */
	public File realFile()
	{
		File aFile ;
		try
		{
			aFile = this.fileRef() ;
		}
		catch (Exception e)
		{
			aFile = null ;
		}
		return aFile ;
	} // realFile()

  // -------------------------------------------------------------------------

	/**
	 * Returns whether or not the file specified by this locator exists.
	 */
	public boolean exists()
	{
		return this.getExists() ;
	} // exists()

  // -------------------------------------------------------------------------

	/**
	 * Returns whether or not the name specified by this locator 
	 * points to a file.
	 */
	public boolean isFile()
	{
		try 
		{
			if ( this.exists() )
				return this.isFileElement( this.getFile() ) ;
			else
				return false ;
		} 
		catch(Exception e) 
		{
			return false ;
		}
	} // isFile()

  // -------------------------------------------------------------------------

	/**
	 * Returns whether or not the name specified by this locator 
	 * points to a directory.
	 */
	public boolean isDirectory()
	{
		try 
		{
			if ( this.exists() )
				return ! this.isFileElement( this.getFile() ) ;
			else
				return false ;
		} 
		catch(Exception e) 
		{
			return false ;
		}
	} // isDirectory()

  // -------------------------------------------------------------------------

	/**
	 * Returns the size of the file or 0 if it does not exist.
	 */
	public long size()
	{
		ZipEntry entry ;
		
		try 
		{
			if ( this.isInArchive() )
			{
				entry = this.archiveEntry() ;
				// if ( DEBUG ) com.mdcs.joi.Inspector.inspectWait( entry ) ;
				return entry.getSize() ;
			}
			else
			{
				return this.getFile().length() ;
			} 
		}
		catch(Exception ex) 
		{
			if ( DEBUG ) ex.printStackTrace() ;
			return 0L ;
		} 
	} // size()

  // -------------------------------------------------------------------------

	/**
	 * Returns the timestamp of when the file was last modified 
	 * or 0 in any case of error.
	 */
	public long lastModified()
	{
		ZipEntry entry ;
		
		try 
		{
			if ( this.isInArchive() )
			{
				entry = this.archiveEntry() ;
				return entry.getTime() ;
			}
			else
			{
				return this.getFile().lastModified() ;
			} 
		}
		catch(Exception ex) 
		{
			if ( DEBUG ) ex.printStackTrace() ;
			return 0L ;
		} 
	} // lastModified()

  // -------------------------------------------------------------------------

	/**
	 * Returns an opened input stream on the file defined by this locator.
	 */
	public InputStream getInputStream()
		throws Exception
	{
		ZipEntry entry ;
		
		if ( this.isInArchive() )
		{
			entry = this.archiveEntry() ;
			return this.container().getInputStream( entry ) ;
		}
		else
		{
			return new FileInputStream( this.getFile() ) ;
		} 
	} // getInputStream()

  // -------------------------------------------------------------------------

	/**
	 * Returns whether or not the file specified by this locator 
	 * is inside an archive.
	 */
	public boolean isInArchive()
	{
		return this.getParent() != null ;
	} // isInArchive()

  // -------------------------------------------------------------------------

	/**
	 * Returns the full pathname.
	 */
	public String getPath()
	{
		return this.fullFilePath( false ).getPath() ;
	} // getPath()

  // -------------------------------------------------------------------------

	/**
	 * Returns the full absolute pathname.
	 */
	public String getAbsolutePath()
	{
		return this.fullFilePath( true ).getPath() ;
	} // getAbsolutePath()

  // -------------------------------------------------------------------------

	/**
	 * Returns the full pathname in a standardized for.
	 * That is all ".." and "." elements are removed and forward slashes are 
	 * used as separators of the remaining elements.
	 */
	public String getStandardizedPath()
	{
		return this.fileUtil().standardize( this.getPath() ) ;
	} // getStandardizedPath()

  // -------------------------------------------------------------------------

	/**
	 * Returns the full absolute pathname in a standardized form.
	 * That is all ".." and "." elements are removed and forward slashes are 
	 * used as separators of the remaining elements.
	 */
	public String getStandardizedAbsolutePath()
	{
		return this.fileUtil().standardize( this.getAbsolutePath() ) ;
	} // getStandardizedAbsolutePath()

  // -------------------------------------------------------------------------

	/**
	 * Returns the last exception that occured while using this locator
	 * or null, if no exception was thrown at all.
	 */
	public Exception exception()
	{
		return this.getException() ;
	} // exception()

  // -------------------------------------------------------------------------

	/**
	 * Returns the name of the file as an URL.
	 */
	public URL toURL()
		throws MalformedURLException
	{
		StringBuffer buffer = new StringBuffer( 128 ) ;
		
		this.urlPath( buffer ) ;
		return new URL( buffer.toString() ) ;
	} // toURL()

  // -------------------------------------------------------------------------

  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================

	protected FileLocator createFrom( File filePath )
	{
		FileLocator locator	= null ;
		String[] parts 			= null ;
		File path						= filePath ;
		
		if ( path.getPath().startsWith( FILE_PROTOCOL_INDICATOR ) )
			path = this.convertFromURLSyntax( path ) ;
			
		parts = str().parts( path.getPath(), File.separator ) ;
		try
		{
		 	locator = this.initFromPath( parts, path.getPath().startsWith( File.separator ) ) ;
		}
		catch ( Exception ex )
		{
			this.setException( ex ) ;
			this.doesNotExist( path ) ;
			locator = this ;
		}
		return locator ;
	} // createFrom()

  // -------------------------------------------------------------------------

  private FileLocator createFrom( FileLocator aParent, String[] pathElements )
		throws Exception
  {
  	this.setParent( aParent ) ;
  	return this.initFromPath( pathElements, false ) ;
  } // createFrom()

  // -------------------------------------------------------------------------

	protected FileLocator initFromPath( String[] parts, boolean startsFromRoot )
		throws Exception
	{
		FileLocator locator			= this ;
		File pathElement 				= null ;
		String[] rest						= null ;
		boolean elementExists		= false ;
		
		if ( startsFromRoot )
			pathElement = new File( File.separator ) ;
		
		for ( int i = 0 ; i < parts.length ; i++ )
		{
			if ( pathElement == null )
				pathElement = new File( parts[i] ) ;
			else
				pathElement = new File( pathElement, parts[i] ) ;

			elementExists = this.doesElementExist( pathElement ) ;
			
			if ( elementExists )
			{	
				this.setFile( pathElement ) ;
				if ( this.isFileElement( pathElement ) )
				{
					if ( DEBUG ) System.out.println( "Locator(" + pathElement + ")" ) ;
					if ( i < ( parts.length - 1 ) )  // Is not last element ? 
					{
						rest = str().copyFrom( parts, i + 1 ) ;
						// if (DEBUG) com.mdcs.joi.Inspector.inspect( "SubLocator", rest ) ;
						locator = FileLocator.newWith( this, rest ) ;
					}
					break ;
				}
			}
			else
			{
				if ( this.isInArchive() )
				{
					if ( i < ( parts.length - 1 ) )  // Is not last element ? 
					{
						// Directories are not always identifiable individually in zip archives.
						// Therefore it must be accepted that they are not found.
						// So in such case no exception will be thrown.
					}
					else
					{
						throw new Exception( "\"" + pathElement.getPath() + "\" does not exist" );
					}
				}
				else
				{
					throw new Exception( "\"" + pathElement.getPath() + "\" does not exist" );
				}
			}
		}
		return locator ;
	} // initFromPath()

  // -------------------------------------------------------------------------

	protected boolean doesElementExist( File element )
		throws Exception
	{
		if ( this.isInArchive() )
		{
			return doesElementExistInArchive( element.getPath() ) ;			
		}
		else
		{
			return element.exists() ;
		}
	} // doesElementExist()

  // -------------------------------------------------------------------------

	protected boolean isFileElement( File element )
		throws Exception
	{
		if ( this.isInArchive() )
		{
			return isFileInArchive( element.getPath() ) ;			
		}
		else
		{
			return element.isFile() ;
		}
	} // isFileElement()

  // -------------------------------------------------------------------------

	protected boolean doesElementExistInArchive( String elementName )
		throws Exception
	{
		ZipEntry entry ;

		entry = this.entryFromArchive( elementName ) ;
				
		return ( entry != null ) ;
	} // doesElementExistInArchive()

  // -------------------------------------------------------------------------

	protected boolean isFileInArchive( String elementName )
		throws Exception
	{
		ZipEntry entry ;
		entry = this.entryFromArchive( elementName ) ;
		
		// Unfortunately entry.isDirectory() returns false even for
		// pure directory entries inside a zip archive, so it can't be used here.
		// The trick below is problematic, because apart from 
		// directories it will also not recognize files with size 0.
		
		return ( entry != null ) && ( entry.getSize() > 0 ) ;
	} // isFileInArchive()

  // -------------------------------------------------------------------------

	protected ZipEntry entryFromArchive( String elementName )
		throws Exception
	{
		ZipEntry entry ;
		ZipFile archive ;
		String name ;
		
		name = str().replaceAll( elementName, "\\", "/" ) ;
		archive = this.container() ;
		entry = archive.getEntry( name ) ;

		if (DEBUG)
		{
			// if ( entry == null ) com.mdcs.joi.Inspector.inspect( name ) ;
			System.out.print( archive.getName() + "::" + name + " --- "
								+ ( entry != null ) ) ; 
			if ( entry == null )
			{
				System.out.println() ;				
			}
			else
			{
				System.out.print( " (" + entry.getSize()  + ")" ) ;
				System.out.print( " (T:" + entry.getTime()  + ")" ) ;
				System.out.println( " (" + ( entry.isDirectory() ? "Dir" : "File" ) + ")" ) ;
			}
		}
		
		return entry ;
	} // entryFromArchive()

  // -------------------------------------------------------------------------

	protected ZipEntry archiveEntry()
		throws Exception
	{
		return this.entryFromArchive( this.getFile().getPath() ) ;
	} // archiveEntry()

  // -------------------------------------------------------------------------

	protected void doesNotExist( File file )
	{
		this.setExists( false ) ;
		this.setFile( file ) ;
	} // doesNoTExist()

  // -------------------------------------------------------------------------

	protected File fullFilePath( boolean absolute )
	{
		File full ;
		
		if ( this.isInArchive() )
		{
			full = new File( 	this.getParent().fullFilePath( absolute ), 
												this.getFile().getPath() ) ;
		}
		else
		{
			if ( absolute )
				full = this.getFile().getAbsoluteFile() ;
			else
				full = this.getFile() ;
		}
		
		return full ;
	} // fullFilePath()

  // -------------------------------------------------------------------------

	protected void urlPath( StringBuffer buffer )
	{
		if ( this.isInArchive() )
		{
			this.getParent().urlPath( buffer ) ; 
			buffer.append( ARCHIVE_INDICATOR ) ;
		}
		else
		{
			buffer.append( FILE_PROTOCOL_INDICATOR ) ;
		}		
		buffer.append( this.getFile().getPath() ) ;
	} // urlPath()

  // -------------------------------------------------------------------------

	protected File fileRef()
		throws Exception
	{
		InputStream archiveStream ;
		FileOutputStream fileStream ;
		ZipEntry entry ;
		File tempFile ;
		
		if ( this.isInArchive() )
		{
			entry = this.archiveEntry() ;
			archiveStream = this.container().getInputStream( entry ) ;
			tempFile = File.createTempFile( "FLOC_", ".xtr" ) ;
			tempFile.deleteOnExit() ;
			fileStream = new FileOutputStream( tempFile ) ;
			fileUtil().copyStream( archiveStream, fileStream ) ;
			return tempFile ;
		}
		else
		{
			return this.getFile() ;
		}
	} // fileRef()

  // -------------------------------------------------------------------------

	/**
	 * Returns the file this locator presents as opened zip file or
	 * null in any case of error.
	 */
	protected ZipFile archive()
		throws Exception
	{
		if ( this.getZipFile() == null )
		{
			this.setZipFile( new ZipFile( this.fileRef() ) ) ;
		}
		return this.getZipFile() ;
	} // archive()

  // -------------------------------------------------------------------------

	/**
	 * Returns the zip file which is presented by the parent container
	 * or null in any case of error.
	 */
	protected ZipFile container()
		throws Exception
	{
		if ( this.isInArchive() )
			return this.getParent().archive() ;
		else
			return null ;
	} // container()

  // -------------------------------------------------------------------------

	protected File convertFromURLSyntax( File file)
	{
		String newStr ;
		
		newStr = file.getPath().substring( FILE_PROTOCOL_INDICATOR.length() ) ;
		newStr = str().replaceAll( newStr, ARCHIVE_INDICATOR, File.separator ) ;
		
		return new File( newStr ) ;
	} // convertFromURLSyntax()
	
  // -------------------------------------------------------------------------

	protected StringUtil str()
	{
		return StringUtil.current() ;
	} // str()
	
  // -------------------------------------------------------------------------

	protected FileUtil fileUtil()
	{
		return FileUtil.current() ;
	} // fileUtil()
	
  // -------------------------------------------------------------------------

} // class FileLocator