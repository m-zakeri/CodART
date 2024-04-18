/*
 * Copyright (C) 2009 VTT Technical Research Centre of Finland.
 *
 * This file is part of NOEN framework.
 *
 * NOEN framework is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2.
 *
 * NOEN framework is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

package fi.vtt.noen.testgen.model.daikon.constraints;

import fi.vtt.noen.testgen.model.daikon.constraints.ReferenceValue;

import static fi.vtt.noen.testgen.StringUtils.*;

import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;
import java.util.Map;

/**
 * Base class for all Daikon based invariants.
 *
 * @author Teemu Kanstrén
 */
public abstract class DaikonConstraint {
  public static final String ln = "\n";
  protected ReferenceValue left;
  protected Object right;
  private boolean lexical = false;

  protected boolean parseLexical(String toCheck) {
    String[] parts = toCheck.split(" \\(lexical");
//    System.out.println("check:"+toCheck+" parts:"+parts.length);
    if (parts.length > 1) {
      lexical = true;
    }
    return lexical;
  }

  //lexicals have not been useful at all so far so just ignore them
  //anything where the right side is a reference is pointless as we only use constraints for guards and
  //parameters in isolation
  public boolean isEnabled() {
    return !lexical && !(right instanceof ReferenceValue);
  }

  public void checkEnabled() {
    if (lexical) {
      throw new IllegalArgumentException("lexical constraints are not supported");
    }
  }

  public boolean isGlobal() {
    return left.isGlobal();
  }

  public boolean isReturnValue() {
    return left.isReturnValue();
  }

  public String returnValue() {
    if (!isReturnValue()) {
      throw new IllegalArgumentException("This is not a return value constraint:"+this);
    }
    return valueObjectToString(right);
  }

  public int getIndex() {
    return left.getIndex();
  }

  protected abstract String guardName();

  public String guardMethod() {
    String method = "  public boolean "+guardName()+"() {"+ln;
    method += toJava();
    method += "    return true;"+ln;
    method += "  }"+ln;
    return method;
  }

  public String guardInvocation() {
//NOTE: this is to test guards only for size checks
//    return "    if("+guardName()+"()) return false;"+ln;
    return "";
  }


//  public String toJavaTransitionConstraint(String content) {
//    return toJava(content, false);
//  }

  protected abstract String toJava();

  public double min() {
    return Integer.MAX_VALUE;
  }

  public double max() {
    return Integer.MIN_VALUE;
  }

  public boolean isTrue() {
    return false;
  }

  public boolean isFalse() {
    return false;
  }

  protected String createCondition(String condition) {
    return createCondition(condition, 0);
  }

  protected String createCondition(String condition, int prefixN) {
    String prefix = "    ";
    for (int i = 0 ; i < prefixN ; i++) {
      prefix += "  ";
    }
    String java = prefix+"if ("+condition+") {"+ln;
    java += prefix+"  return false;"+ln;
    java += prefix+"}"+ln;
    return java;
  }
/*
  public Collection<String> getAssertObjectValues() {
    throw new UnsupportedOperationException("Assert generation is not supported for this constraint.");
  }

  public String getAssertObjectName() {
    return left.getReferredVariable();
  }
*/
  public String asAssert(String returnVar) {
    throw new UnsupportedOperationException("Assert generation is not supported for this constraint.");
  }

  /**
   * Gives the list of array names related to this constraint. They are used to create java.util.List objects
   * into the generated model code.
   *
   * @return List of array names.
   */
  public Collection<String> arrayNames() {
    return Collections.EMPTY_SET;
  }

  /**
   * Turns an object list into a string representation.
   * For example [obj1,obj2,obj3] -> "obj1,obj2,obj3".
   *
   * @param items List of objects.
   * @return The string representation for the argument.
   */
  protected String stringFrom(Collection items) {
    String string = "";
    for (Iterator i = items.iterator(); i.hasNext();) {
      string += i.next();
      if (i.hasNext()) {
        string += ",";
      }
    }
    return string;
  }

  protected String valueObjectToString(Object value) {
    if (value instanceof Boolean) {
      return value.toString();
//      Boolean bool = (Boolean) value;
//      return "new Boolean("+bool.booleanValue()+")";
    }
    if (value instanceof Double) {
      return value.toString();
//      Double d = (Double) value;
//      return "new Double("+d.doubleValue()+")";
    }
    if (value instanceof ReferenceValue) {
      ReferenceValue ref = (ReferenceValue) value;
      return ref.getReferredVariable();
    }
    if (value instanceof String) {
      return "\""+value.toString()+"\"";
    }
    throw new IllegalArgumentException("Unsupport Daikon value object:"+value.getClass());
  }

  protected String valueObjectToGuardString(Object value) {
    if (value instanceof Boolean) {
      return value.toString();
//      Boolean bool = (Boolean) value;
//      return "new Boolean("+bool.booleanValue()+")";
    }
    if (value instanceof Number) {
      Number n = (Number) value;
      int iv = n.intValue();
      return ""+iv;
//      Double d = (Double) value;
//      return "new Double("+d.doubleValue()+")";
    }
    if (value instanceof ReferenceValue) {
      ReferenceValue ref = (ReferenceValue) value;
      return ref.getReferredVariable();
    }
    if (value instanceof String) {
      return value.toString();
    }
    throw new IllegalArgumentException("Unsupport Daikon value object:"+value.getClass());
  }

  protected String valueObjectToGuardObject(Object value) {
    if (value instanceof Boolean) {
      return value.toString();
//      Boolean bool = (Boolean) value;
//      return "new Boolean("+bool.booleanValue()+")";
    }
    if (value instanceof Number) {
      Number n = (Number) value;
      int iv = n.intValue();
      return ""+iv;
//      Double d = (Double) value;
//      return "new Double("+d.doubleValue()+")";
    }
    if (value instanceof ReferenceValue) {
      ReferenceValue ref = (ReferenceValue) value;
      return ref.getReferredVariable();
    }
    if (value instanceof String) {
      return "_"+value.toString()+"_";
    }
    throw new IllegalArgumentException("Unsupport Daikon value object:"+value.getClass());
  }

  /**
   * There are some "lexical" termed invariants in Daikon. This whole thing is rather
   * confusing and in the end these are not used anymore.. This was an attempt to make
   * these "lexical" invariants work by comparing elements of two lists together in order.
   * For example, [1,2,3] and [5,6,7] could be compared as 1 < 5, 2 < 6, 3 < 7.
   * This method is for transition guard methods, returning false if any of the
   * comparisons fails.
   *
   * @param left    Name of first list object.
   * @param right   Name of second list object.
   * @param comparator  Used to compare list items to each other.
   * @return The comparison code.
   */
  protected String lexicalJava(String left, String right, String comparator) {
    return
      "    Iterator i1 = "+left+".iterator();"+ln+
      "    Iterator i2 = "+right+".iterator();"+ln+
      "    while (i1.hasNext()) {"+ln+
      "      Object o1 = i1.next();"+ln+
      "      Object o2 = i2.next();"+ln+
      "      if (o1.hashCode() "+comparator+" o2.hashCode()) {"+ln+
      "        return false;"+ln+
      "      }"+ln+
      "    }"+ln;
  }

  /**
   * There are some "lexical" termed invariants in Daikon. This whole thing is rather
   * confusing and in the end these are not used anymore.. This was an attempt to make
   * these "lexical" invariants work by comparing elements of two lists together in order.
   * For example, [1,2,3] and [5,6,7] could be compared as 1 < 5, 2 < 6, 3 < 7.
   * This method is for test oracles, using JUnit assertions for comparisons.
   *
   * @param left    Name of first list object.
   * @param right   Name of second list object.
   * @param comparator  Used to compare list items to each other.
   * @return The comparison code.
   */
  protected String lexicalAssert(String left, String right, String comparator) {
    return
      "    Iterator i1 = "+left+".iterator();"+ln+
      "    Iterator i2 = "+right+".iterator();"+ln+
      "    while (i1.hasNext()) {"+ln+
      "      Number n1 = (Number)i1.next();"+ln+
      "      Number n2 = (Number)i2.next();"+ln+
      "      assertTrue(n1 "+comparator+" n2);"+ln+
      "    }"+ln;
  }

  protected String parseArrayName(String text) {
    String[] parts = text.split("size\\(");
    text = parts[1];
    parts = text.split("\\[");
    text = parts[0];
    return text;
  }

  public String parameterValues(String type) {
    return null;
  }
}
