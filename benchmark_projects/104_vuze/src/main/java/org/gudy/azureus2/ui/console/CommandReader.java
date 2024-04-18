/*
 * CommandReader.java
 *
 * Created on 25. Oktober 2003, 03:03
 */

package org.gudy.azureus2.ui.console;

import java.io.IOException;
import java.io.Reader;
import java.util.List;
import java.util.Vector;

/**
 *
 * @author  tobi
 */
public class CommandReader extends Reader {
  
  private final int ENTER = 0;
  private final int TAB = 1;
  private final int QUOTE = 3;
  private final int ESCAPE = 4;
  private final int NONQUOTEDESCAPE = 5;
  
  private Reader in;
  
  /** Creates a new instance of CommandReader */
  public CommandReader(Reader _in) {
    super();
    in = _in;
  }
  
  private void ensureOpen() throws java.io.IOException {
    if (in == null)
      throw new IOException("Stream closed");
  }
  
  public void close() throws java.io.IOException {
    synchronized(lock) {
      if (in != null) {
        in.close();
        in = null;
      }
    }
  }
  
  public int read() throws java.io.IOException {
    synchronized(lock) {
      ensureOpen();
      return in.read();
    }
  }
  
  public int read(char[] cbuf, int off, int len) throws java.io.IOException {
    synchronized(lock) {
      ensureOpen();
      return in.read(cbuf, off, len);
    }
  }
  
  public String readLine() throws java.io.IOException {
  	synchronized(lock) {
  		ensureOpen();
  		StringBuffer line = new StringBuffer();
  		int ch;
  		while( (char)(ch = in.read()) != '\n' )
  		{
  			if( ch == -1 )
  			{
  				throw new IOException("stream closed");
  			}
  			line.append((char)ch);
  		}
  		return line.toString().trim();
  	}
  }
  public List parseCommandLine( String commandLine )
  {
  	StringBuffer current = new StringBuffer();
  	Vector args = new Vector();
  	boolean allowEmpty = false;
  	boolean bailout = commandLine.length() == 0;
  	int index = 0;
    int state = ENTER;

  	while (!bailout) {
  		
  		int ch = commandLine.charAt(index++);
  		bailout = (index == commandLine.length());
  		char c = (char) ch;
  		
//  		if (c!='\n'){
//  			
//  			line.append( c );
//  		}
//  		
  		switch (state) {
  		/*case SKIP:
  		 switch (c) {
  		 case ' ': case '\t':
  		 break;
  		 case '\"':
  		 mode = QUOTE;
  		 break;
  		 case '&':
  		 background = true;
  		 case ';':
  		 contLine = line.substring(pos +1);
  		 pos = line.length();
  		 break;
  		 default:
  		 mode = READ;
  		 --pos;
  		 }
  		 break;*/
  		
  		case ENTER:
  			switch (c) {
  			case '\"':
  				state = QUOTE;
  				break;
  				/*case ' ': case '\t':
  				 mode = SKIP;
  				 break;*/
  			case  '\\':
  				state = NONQUOTEDESCAPE;
  				break;
//  			case '\n':
//  				bailout = true;
//  				break;
  			case '\r':
  				break;
  			default:
  				current.append(c);
  			}
  			if ((state == ENTER) && ((c==' ') || (bailout))) {
  				String arg = current.toString().trim();
  				if( arg.length() > 0 || allowEmpty )
  				{
  					args.addElement(arg);
  					allowEmpty = false;
  				}
  				current = new StringBuffer();
  			}
  			break;
  			
  		case QUOTE:
  			switch (c) {
  			case '\"':
  				allowEmpty = true;
  				state = ENTER;
  				break;
  			case '\\':
  				state = ESCAPE;
  				break;
  			default:
  				current.append(c);
  			}
  			break;
  			
  		case ESCAPE:
  			switch (c) {
  			case 'n':  c = '\n';  break;
  			case 'r':  c = '\r';  break;
  			case 't':  c = '\t';  break;
  			case 'b':  c = '\b';  break;
  			case 'f':  c = '\f';  break;
  			default: current.append('\\'); break;
  			}
  			state = QUOTE;
  			current.append(c);
  			break;
  		case  NONQUOTEDESCAPE:
  			switch (c) {
  			case  ';':
  				state = ENTER;
  				current.append(c);
  				break;
  			default: // This is not a escaped char.
  				state = ENTER;
  			current.append('\\');
  			current.append(c);
  			break;
  			}
  			break;
  		}
    }
	if ((state == ENTER) && (current.toString().trim().length() > 0 || allowEmpty) )
	{
		String arg = current.toString().trim();
		args.addElement(arg);
	}
  	return args;
  }
}
