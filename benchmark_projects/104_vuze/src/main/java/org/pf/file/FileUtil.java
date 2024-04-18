// ===========================================================================
// CONTENT  : CLASS FileUtil
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.1 - 14/03/2003
// HISTORY  :
//  17/05/2002  duma  CREATED
//	14/03/2003	duma	added		->	standardize(), javaFilename()
//
// Copyright (c) 2002-2003, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.file ;

// ===========================================================================
// IMPORTS
// ===========================================================================
import java.io.* ;

import org.pf.text.StringUtil;

/**
 * This class provides helper methods for file and stream handling.
 * It's an add-on to the java.io package.
 * The service is implemented as a singleton, so use the
 * <b>FileUtil.current()</b> method to get the sole instance.
 *
 * @author Manfred Duchrow
 * @version 1.1
 */
public class FileUtil
{
  // =========================================================================
  // CONSTANTS
  // =========================================================================
  /** The lines.separator from the system properties as a constant */
	public static final String LINE_SEPARATOR	= System.getProperty( "line.separator" ) ;
	protected static final int DEFAULT_BUFFER_SIZE	= 1024 ;

  // =========================================================================
  // CLASS VARIABLES
  // =========================================================================
	private static FileUtil current = new FileUtil() ;

  // =========================================================================
  // CLASS METHODS
  // =========================================================================

  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================
  /**
   * Initialize the new instance with default values.
   */
  private FileUtil()
  {
    super() ;
  } // FileUtil()
 
  // =========================================================================
  // PUBLIC CLASS METHODS
  // =========================================================================
	public static FileUtil current()
	{
		return current ;
	} // current()
 
  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================

	/**
	 * Copies all data from the iniput stream to the output stream using
	 * a buffer with the default size (1024 bytes).
	 * After all data is copied both streams will be closed !
	 */
	public void copyStream( InputStream inStream, OutputStream outStream )
			throws IOException
	{
		this.copyStream( inStream, outStream, DEFAULT_BUFFER_SIZE ) ;
	} // copyStream()
 
  // -------------------------------------------------------------------------

	/**
	 * Copies all data from the iniput stream to the output stream using
	 * a buffer of the given size in bytes.
	 * After all data is copied both streams will be closed !
	 */
	public void copyStream( InputStream inStream, OutputStream outStream, 
													int bufSize )
			throws IOException
	{
		byte[] buffer = new byte[bufSize] ;
		int count ;
		
		try
		{
			count = inStream.read(buffer) ;
			while ( count > -1 )
			{
				outStream.write( buffer, 0, count ) ;
				count = inStream.read(buffer) ;
			}
		}
		finally
		{
			this.close(inStream) ;
			this.close(outStream) ;
		}
	} // copyStream()
 
  // -------------------------------------------------------------------------

	/**
	 * Reads the whole content of the given input stream and returns 
	 * it as a string.
	 * The stream will be closed after calling this method. Even if an exception
	 * occured!
	 * 
	 * @param inStream The input stream to read
	 * @return The text content of the given stream
	 */
	public String readTextFrom( InputStream inStream )
		throws IOException
	{
		StringWriter writer ;
		
		writer = new StringWriter( 1024 ) ;
		this.copyText( inStream, writer ) ;
		return writer.toString() ;
	} // readTextFrom()
 
	// -------------------------------------------------------------------------

	/**
	 * Reads the whole content of the file with the given name and returns 
	 * it as a string.
	 * 
	 * @param filename The name of the text containing file
	 */
	public String readTextFrom( String filename )
		throws IOException
	{
		FileInputStream inStream ;

		inStream = new FileInputStream( filename ) ;		
		return this.readTextFrom( inStream ) ;
	} // readTextFrom()
 
	// -------------------------------------------------------------------------

	/**
	 * Reads the whole content of the specified file and returns 
	 * it as a string.
	 */
	public String readTextFrom( File file )
		throws IOException
	{
		FileInputStream inStream ;

		inStream = new FileInputStream( file ) ;		
		return this.readTextFrom( inStream ) ;
	} // readTextFrom()
 
	// -------------------------------------------------------------------------

	/**
	 * Copies all text lines from the specified reader to the given writer.
	 * After that the reader will be closed. Even if an exception occurs.
	 * 
	 * @param reader The reader which provides the text to copy
	 * @param writer The writer to which the text will be copied
	 */
	public void copyText( Reader reader, final StringWriter writer )
		throws IOException
	{
		BufferedReader bufReader ;
		String line ;
		LineProcessor processor ;
		
		bufReader = new BufferedReader( reader ) ;
		try
		{
			processor = new LineProcessor()
				{
					public boolean processLine( String line, int lineNo )
					{
						if ( lineNo > 1 )
							writer.write( LINE_SEPARATOR ) ;				
				
						writer.write( line ) ;
						return true ;
					}
				} ;
			this.processTextLines( bufReader, processor ) ;
		}
		finally
		{ 
			bufReader.close() ;
		}
	} // copyText()
 
	// ------------------------------------------------------------------------

	/**
	 * Reads all text lines from the file with the specified name and passes them 
	 * one by one to the given line processor.
	 * The processing will be terminated, if the end of the text is reached or
	 * if the processor returns <b>false</b>.<br>
	 * 
	 * @param filename The name of the text file to read
	 * @param processor The processor that receives the lines from the text
	 */
	public void processTextLines( String filename, LineProcessor processor )
		throws IOException
	{
		FileInputStream inStream ;
		
		if ( filename == null )
			throw new IllegalArgumentException( "filename must not be null" ) ;
		
		inStream = new FileInputStream( filename ) ;
		this.processTextLines( inStream, processor ) ; 
	} // processTextLines()
	
	// -------------------------------------------------------------------------
	
	/**
	 * Reads all text lines from the specified input stream and passes them 
	 * one by one to the given line processor.
	 * The processing will be terminated, if the end of the text is reached or
	 * if the processor returns <b>false</b>.<br>
	 * The given input stream will be closed after the execution of this method.
	 * Even if an exception occured.
	 * 
	 * @param inStream The input stream that contains the text
	 * @param processor The processor that receives the lines from the text
	 */
	public void processTextLines( InputStream inStream, LineProcessor processor )
		throws IOException
	{
		InputStreamReader reader ;

		if ( inStream == null )
			throw new IllegalArgumentException( "inStream must not be null" ) ;
		
		reader = new InputStreamReader( inStream ) ;
		this.processTextLines( reader, processor ) ; 
	} // processTextLines()
	
	// -------------------------------------------------------------------------
	
	/**
	 * Reads all text lines from the specified reader and passes them one by one
	 * to the given line processor.
	 * The processing will be terminated, if the end of the text is reached or
	 * if the processor returns <b>false</b>.
	 * 
	 * @param reader The reader that contains a text stream
	 * @param processor The processor that receives the lines from the text
	 */
	public void processTextLines( Reader reader, LineProcessor processor )
		throws IOException
	{
		BufferedReader bufReader ;
		String line ;
		int counter = 0 ;
		boolean continue_reading = true ;
		
		if ( reader == null )
			throw new IllegalArgumentException( "reader must not be null" ) ;

		if ( processor == null )
			throw new IllegalArgumentException( "processor must not be null" ) ;
				
		bufReader = new BufferedReader( reader ) ;
		while ( continue_reading && bufReader.ready() )
		{
			line = bufReader.readLine() ;
			if ( line == null )
				break ;

			counter++ ;
			continue_reading = processor.processLine( line, counter ) ;
		} 
	} // processTextLines()
 
	// ------------------------------------------------------------------------

	/**
	 * Close the given stream ignoring any exception.
	 * Returns true, if the stream was closed successfully, false otherwise
	 */
	public boolean close( InputStream stream )
	{
		if ( stream == null )
		{
			return false ;
		}
		try
		{
			stream.close() ;
			return true ;
		}
		catch (IOException e)
		{
			return false ;
		}
	} // close()
 
	// -------------------------------------------------------------------------

	/**
	 * Close the given stream ignoring any exception.
	 * Returns true, if the stream was closed successfully, false otherwise
	 */
	public boolean close( OutputStream stream )
	{
		if ( stream == null )
		{
			return false ;
		}
		try
		{
			stream.close() ;
			return true ;
		}
		catch (IOException e)
		{
			return false ;
		}
	} // close()
 
	// -------------------------------------------------------------------------

	/**
	 * Convert the filename to a canonical (see java.io.File.getCanonicalPath())
	 * format and replace any backslashes '\' by slashes ('/').
	 * If possible all "." and ".." elements in the path are eliminated.
	 * 
	 * @param filename The filename which has to be standardized
	 * @return An absolute filename that uses slashes to separate its elements
	 */
	public String standardize( String filename )
	{
		if ( filename == null )
			return null ;

		return this.standardizeFilename( filename ) ;
	} // standardize()
 	
	// -------------------------------------------------------------------------

	/**
	 * Returns the given filename in the platform independent way that Java 
	 * understands. That is all elements are separated by a forward slash rather
	 * than back slashes as on Windows systems.
	 * 
	 * @param filename The name to be modified
	 */
	public String javaFilename( String filename )
	{
		if ( filename == null )
			return null ;
			
		return filename.replace( '\\', '/' ) ;
	} // javaFilename()
 
	// -------------------------------------------------------------------------

  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================
	protected void copyText( InputStream inStream, StringWriter writer )
		throws IOException
	{
		this.copyText( new InputStreamReader( inStream ), writer ) ;
	} // copyText()
 
	// ------------------------------------------------------------------------

	protected String standardizeFilename( String filename )
	{
		String[] nameElements ;
		boolean hasDriveLetter ;
		boolean startedFromRoot ;
		boolean isAbsolute ;
		int index ;
		
		filename = this.javaFilename(filename) ;
		startedFromRoot = filename.startsWith( "/" ) ;
		nameElements = this.str().parts( filename, "/" ) ;
		if ( nameElements.length > 0 )
		{
			hasDriveLetter = nameElements[0].endsWith( ":" ) ;
			if ( hasDriveLetter )
			{
				nameElements[0] = nameElements[0].toUpperCase() ;
			}
			else
			{
				if ( startedFromRoot )
				{
					nameElements = this.str().append( new String[] { "" }, nameElements );
				}
			}
			isAbsolute = hasDriveLetter || startedFromRoot ;
			for (int i = 0; i < nameElements.length; i++)
			{
				if ( ".".equals( nameElements[i] ) )
				{
					nameElements[i] = null ;
				}
				else
				{
					if ( "..".equals( nameElements[i] ) )
					{
						index = this.indexOfPreceedingNotNullElement( nameElements, i-1 ) ;
						if ( index >= 0 )
						{
							if ( ( index > 0 ) || ( ! isAbsolute ) )
							{
								nameElements[i] = null ;
								nameElements[index] = null ;
							}
						}
					}
				}	
			}
			nameElements = this.str().removeNull( nameElements ) ;
			return this.str().asString( nameElements, "/" ) ;
		}
		else
		{
			return "" ;
		}
	} // standardizeFilename()
 
	// -------------------------------------------------------------------------

	protected int indexOfPreceedingNotNullElement( String[] elements, int start )
	{
		for (int i = start; i >= 0 ; i--)
		{
			if ( elements[i] != null )
			{
				if ( "..".equals( elements[i] ) ) // This is not a valid not null element
				{
					return -1 ;
				}
				else
				{
					return i ;				
				}
			}
		}
		return -1 ;
	} // indexOfPreceedingNotNullElement()
 
	// -------------------------------------------------------------------------

	protected StringUtil str()
	{
		return StringUtil.current() ;
	} // str()
 
	// -------------------------------------------------------------------------

} // class FileUtil