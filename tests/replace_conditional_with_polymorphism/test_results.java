package org.json;

/*
Copyright (c) 2002 JSON.org

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The Software shall be used for Good, not Evil.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
 */

/**
 * This provides static methods to convert comma delimited text into a
 * JSONArray, and to convert a JSONArray into comma delimited text. Comma
 * delimited text is a very popular format for data interchange. It is
 * understood by most database, spreadsheet, and organizer programs.
 * <p>
 * Each row of text represents a row in a table or a data record. Each row
 * ends with a NEWLINE character. Each row contains one or more values.
 * Values are separated by commas. A value can contain any character except
 * for comma, unless is is wrapped in single quotes or double quotes.
 * <p>
 * The first row usually contains the names of the columns.
 * <p>
 * A comma delimited list can be converted into a JSONArray of JSONObjects.
 * The names for the elements in the JSONObjects can be taken from the names
 * in the first row.
 * @author JSON.org
 * @version 2016-05-01
 */
public class CDL {

    /**
     * Get the next value. The value can be wrapped in quotes. The value can
     * be empty.
     * @param x A JSONTokener of the source text.
     * @return The value string, or null if empty.
     * @throws JSONException if the quoted string is badly formed.
     */
    private  String getValue(JSONTokener x) throws JSONException {
        char c;
        char q;
        StringBuilder sb;
        do {
            c = x.next();
        } while (c == ' ' || c == '\t');
        CDL_x.next() chosen = new CDL_x.next()()
		chosen.getValue(this);
		switch ( c )  {
			case0:returnnull ;
		case'"':case'\'':q=c ;
		sb=newStringBuilder (  )  ;
		for (  ;
		 ;
		 )  {
			c=x.next (  )  ;
		if ( c==q )  {
			charnextC=x.next (  )  ;
		if ( nextC!='\"' )  {
			if ( nextC>0 )  {
			x.back (  )  ;
		}
			break ;
		}
			}
			if ( c==0||c=='\n'||c=='\r' )  {
			throwx.syntaxError ( "Missing close quote '"+q+"'." )  ;
		}
			sb.append ( c )  ;
		}
			returnsb.toString (  )  ;
		case',':x.back (  )  ;
		return"" ;
		default:x.back (  )  ;
		returnx.nextTo ( ',' )  ;
		}
			}
			publicstaticJSONArrayrowToJSONArray ( JSONTokenerx ) throwsJSONException {
			JSONArrayja=newJSONArray (  )  ;
		for (  ;
		 ;
		 )  {
			CDLcdl=newCDL (  )  ;
		Stringvalue=cdl.getValue ( x )  ;
		charc=x.next (  )  ;
		if ( value==null|| ( ja.length (  ) ==0&&value.length (  ) ==0&&c!=',' )  )  {
			returnnull ;
		}
			ja.put ( value )  ;
		for (  ;
		 ;
		 )  {
			if ( c==',' )  {
			break ;
		}
			if ( c!=' ' )  {
			if ( c=='\n'||c=='\r'||c==0 )  {
			returnja ;
		}
			throwx.syntaxError ( "Bad character '"+c+"'  ( "+ ( int ) c+" ) ." )  ;
		}
			c=x.next (  )  ;
		}
			}
			}
			publicstaticJSONObjectrowToJSONObject ( JSONArraynames,JSONTokenerx ) throwsJSONException {
			JSONArrayja=rowToJSONArray ( x )  ;
		returnja!=null?ja.toJSONObject ( names ) :null ;
		}
			publicstaticStringrowToString ( JSONArrayja )  {
			StringBuildersb=newStringBuilder (  )  ;
		for ( inti=0 ;
		i<ja.length (  )  ;
		i+=1 )  {
			if ( i>0 )  {
			sb.append ( ',' )  ;
		}
			Objectobject=ja.opt ( i )  ;
		if ( object!=null )  {
			Stringstring=object.toString (  )  ;
		if ( string.length (  ) >0&& ( string.indexOf ( ',' ) >=0||string.indexOf ( '\n' ) >=0||string.indexOf ( '\r' ) >=0||string.indexOf ( 0 ) >=0||string.charAt ( 0 ) =='"' )  )  {
			sb.append ( '"' )  ;
		intlength=string.length (  )  ;
		for ( intj=0 ;
		j<length ;
		j+=1 )  {
			charc=string.charAt ( j )  ;
		if ( c>=' '&&c!='"' )  {
			sb.append ( c )  ;
		}
			}
			sb.append ( '"' )  ;
		}
			else {
			sb.append ( string )  ;
		}
			}
			}
			sb.append ( '\n' )  ;
		returnsb.toString (  )  ;
		}
			publicstaticJSONArraytoJSONArray ( Stringstring ) throwsJSONException {
			returntoJSONArray ( newJSONTokener ( string )  )  ;
		}
			publicstaticJSONArraytoJSONArray ( JSONTokenerx ) throwsJSONException {
			returntoJSONArray ( rowToJSONArray ( x ) ,x )  ;
		}
			publicstaticJSONArraytoJSONArray ( JSONArraynames,Stringstring ) throwsJSONException {
			returntoJSONArray ( names,newJSONTokener ( string )  )  ;
		}
			publicstaticJSONArraytoJSONArray ( JSONArraynames,JSONTokenerx ) throwsJSONException {
			if ( names==null||names.length (  ) ==0 )  {
			returnnull ;
		}
			JSONArrayja=newJSONArray (  )  ;
		for (  ;
		 ;
		 )  {
			JSONObjectjo=rowToJSONObject ( names,x )  ;
		if ( jo==null )  {
			break ;
		}
			ja.put ( jo )  ;
		}
			if ( ja.length (  ) ==0 )  {
			returnnull ;
		}
			returnja ;
		}
			publicstaticStringtoString ( JSONArrayja ) throwsJSONException {
			JSONObjectjo=ja.optJSONObject ( 0 )  ;
		if ( jo!=null )  {
			JSONArraynames=jo.names (  )  ;
		if ( names!=null )  {
			returnrowToString ( names ) +toString ( names,ja )  ;
		}
			}
			returnnull ;
		}
			publicstaticStringtoString ( JSONArraynames,JSONArrayja ) throwsJSONException {
			if ( names==null||names.length (  ) ==0 )  {
			returnnull ;
		}
			StringBuildersb=newStringBuilder (  )  ;
		for ( inti=0 ;
		i<ja.length (  )  ;
		i+=1 )  {
			JSONObjectjo=ja.optJSONObject ( i )  ;
		if ( jo!=null )  {
			sb.append ( rowToString ( jo.toJSONArray ( names )  )  )  ;
		}
			}
			returnsb.toString (  )  ;
	}
}
abstract class parentCDL
{
	public parentCDL(){
	}
	abstract public String getValue(CDL input_class ) ;
}
class CDL_0 extends parentCDL
{
	public CDL_0(){
	}
	public String getValue(CDL input_class ) {
		returnnull ;
	
	}
}
class CDL_'"' extends parentCDL
{
	public CDL_'"'(){
	}
	public String getValue(CDL input_class ) {
		case'\'':q=c ;
		input_class.sb=newStringBuilder (  )  ;
		for (  ;
		 ;
		 )  {
			c=x.next (  )  ;
		if ( c==q )  {
			charnextC=x.next (  )  ;
		if ( nextC!='\"' )  {
			if ( nextC>0 )  {
			x.back (  )  ;
		}
			break ;
		}
			}
			if ( c==0||c=='\n'||c=='\r' )  {
			throwx.syntaxError ( "Missing close quote '"+q+"'." )  ;
		}
			input_class.sb.append ( c )  ;
		}
			returninput_class.sb.toString (  )  ;
	
	}
}
class CDL_',' extends parentCDL
{
	public CDL_','(){
	}
	public String getValue(CDL input_class ) {
		x.back (  )  ;
		return"" ;
	
	}
}
class CDL_default extends parentCDL
{
	public CDL_default(){
	}
	public String getValue(CDL input_class ) {
		x.back (  )  ;
		returnx.nextTo ( ',' )  ;
	
	}
}