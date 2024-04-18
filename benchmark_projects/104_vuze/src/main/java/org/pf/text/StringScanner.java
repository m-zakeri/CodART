// ===========================================================================
// CONTENT  : CLASS StringScanner
// AUTHOR   : Manfred Duchrow
// VERSION  : 1.1 - 29/09/2002
// HISTORY  :
//  11/07/2001  duma  CREATED 
//	29/09/2002	duma	added		-> endReached(), endNotReached()
//
// Copyright (c) 2001-2002, by Manfred Duchrow. All rights reserved.
// ===========================================================================
package org.pf.text;

// ===========================================================================
// IMPORTS
// ===========================================================================

/**
 * Simple scanner that allows to navigate over the characters of a string.
 *
 * @author Manfred Duchrow
 * @version 1.1
 */
public class StringScanner
{
  // =========================================================================
  // CONSTANTS
  // =========================================================================
  public static final char END_REACHED    = (char)-1 ;

  // =========================================================================
  // INSTANCE VARIABLES
  // =========================================================================
  protected int length        = 0 ;
  protected int position      = 0 ;
  protected int pos_marker    = 0 ;
  protected char[] buffer     = null ;

  // =========================================================================
  // PUBLIC CLASS METHODS
  // =========================================================================
  /**
   * Returns true, if the given character indicates that the end of the
   * scanned string is reached.
   */
  public boolean endReached( char character )
	{
		return ( character == END_REACHED ) ;
	} // endReached()

  // -------------------------------------------------------------------------
  
  /**
   * Returns true, if the given character does <b>not</b> indicate that the 
   * end of the scanned string si reached.
   */
  public boolean endNotReached( char character )
	{
		return ( ! endReached( character ) ) ;
	} // endNotReached()

  // -------------------------------------------------------------------------
	
  // =========================================================================
  // CONSTRUCTORS
  // =========================================================================
  /**
   * Initialize the new instance with the string that should be scanned.
   */
  public StringScanner( String stringToScan )
  {
    super() ;
    length = stringToScan.length() ;
    buffer = new char[length] ;
    stringToScan.getChars( 0, length, buffer, 0 ) ;
  } // StringScanner()

  // =========================================================================
  // PUBLIC INSTANCE METHODS
  // =========================================================================
  /**
   * Returns the string the scanner was initialized with
   */
  public String toString()
  {
    return new String( buffer ) ;
  } // toString()

  // -------------------------------------------------------------------------

  /**
   * Moves the position pointer count characters.
   * positive values move forwards, negative backwards.
   * The position never becomes negative !
   */
  public void skip( int count )
  {
    position += count ;
    if ( position < 0 )
      position = 0 ;
  } // skip()

  // -------------------------------------------------------------------------

  /**
   * Returns the character at the current position without changing
   * the position, that is subsequent calls to this method return always
   * the same character.
   */
  public char peek()
  {
    return ( position < length() ? buffer[position] : END_REACHED ) ;
  } // skip()

  // -------------------------------------------------------------------------

  /**
   * Returns the character at the current position and increments
   * the position afterwards by 1.
   */
  public char nextChar()
  {
    char next = this.peek() ;
    if ( endNotReached( next ) )
	    this.skip(1);
    return next ;
  } // nextChar()

  // -------------------------------------------------------------------------

	/**
	 * Returns true, if the scanner has reached the end and a further invocation 
	 * of nextChar() would return the END_REACHED character.
	 */
	public boolean atEnd()
	{
		return ( endReached( this.peek() ) ) ;
	} // atEnd()

	// -------------------------------------------------------------------------

	/**
	 * Returns true, if the scanner has not yet reached the end.
	 */
	public boolean hasNext()
	{
		return ! this.atEnd() ;
	} // hasNext()

	// -------------------------------------------------------------------------

  /**
   * Returns the next character that is no whitespace and leaves the
   * position pointer one character after the returned one.
   */
  public char nextNoneWhitespaceChar()
  {
    char next = this.nextChar() ;
    while ( ( endNotReached( next ) ) && ( Character.isWhitespace(next) ) )
    {
      next = this.nextChar() ;
    }
    return next ;
  } // nextNoneWhitespaceChar()

  // -------------------------------------------------------------------------

  /**
   * Returns the current position in the string
   */
  public int getPosition()
  {
    return position ;
  } // getPosition()

  // -------------------------------------------------------------------------

  /**
   * Remembers the current position for later use with restorePosition()
   */
  public void markPosition()
  {
    pos_marker = position ;
  } // markPosition()

  // -------------------------------------------------------------------------

  /**
   * Restores the position to the value of the latest markPosition() call
   */
  public void restorePosition()
  {
    this.setPosition( pos_marker  ) ;
  } // restorePosition()

  // -------------------------------------------------------------------------

  // =========================================================================
  // PROTECTED INSTANCE METHODS
  // =========================================================================
  protected int length()
  {
    return length ;
  } // length()

  // -------------------------------------------------------------------------

	protected void setPosition( int pos )
	{
		if ( ( pos >= 0 ) && ( pos <= this.length() ) )
			position = pos ;
	} // setPosition()

	// -------------------------------------------------------------------------
	
} // class StringScanner