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

import fi.vtt.noen.testgen.parser.DaikonParser;
import fi.vtt.noen.testgen.model.daikon.constraints.DaikonConstraint;

import java.util.Collection;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Collections;

/**
 * This invariant says that the contents of a variable are always one of a given set of constant values.
 * For example, it may say that the value of Client is always either "myclient" or "myclient2".
 *
 * @author Teemu Kanstr�n
 */
public class OneOfConstraint extends DaikonConstraint {
  private final Collection values = new ArrayList();
  private boolean elements = false;

  public OneOfConstraint(String left, String value) {
    //always trim since } can have whitespace, linefeeds etc trailing
    left = left.trim();
    if (left.contains("elements")) {
      elements = true;
      left = left.substring(0, left.indexOf("elements")).trim();
    }
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    value = value.trim();
    //we need to remove the } in the end
    value = value.substring(0, value.length()-1);
    //if there is ] then it is a list of lists
    String[] valueArray = value.split("\\],");
    if (valueArray.length > 1) {
      addArrays(valueArray);
    } else {
      values.addAll(DaikonParser.parseObjectList(value));
    }
  }

  private void addArrays(String[] arrays) {
    for (String array : arrays) {
      array = array.trim();
      //remove "[" from start, "]," from end was removed by split earlier
      array = array.substring(1, array.length());
      if (array.endsWith("]")) {
        //for the last item there is no "]," so we need to remove "]" separately
        array = array.substring(0, array.length()-1);
      }
      values.add(DaikonParser.parseObjectList(array));
    }
  }

  public double min() {
    double min = super.min();
    for (Object o : values) {
      if (o instanceof Number) {
        Number n = (Number)o;
        if (n.doubleValue() < min) {
          min = n.doubleValue();
        }
      }
    }
    return min;
  }

  public double max() {
    double max = super.max();
    for (Object o : values) {
      if (o instanceof Number) {
        Number n = (Number)o;
        if (n.doubleValue() > max) {
          max = n.doubleValue();
        }
      }
    }
    return max;
  }

  public String asAssert(String returnVar) {
    String assertion = createValidValuesJava("");
    if (elements) {
      assertion += "for (Object o : "+returnVar+") {"+ln;
      assertion += "  assertTrue(validValues.contains(o));"+ln;
      assertion += "}"+ln;
    } else {
      assertion += "assertTrue(validValues.contains("+returnVar+"));"+ln;
    }
    return assertion;
  }

  public String toString() {
    String values = "{";
    for (Iterator i = this.values.iterator(); i.hasNext();) {
      Object obj = i.next();
      if (obj instanceof Collection) {        
        values += obj;
      } else {
        values += valueObjectToString(obj);
      }
      if (i.hasNext()) {
        values += ",";
      } else {
        values += "}";
      }
    }
    String item = left.toString();
    if (elements) {
      item += " elements";
    }
    return item +" one of "+values;
  }

  protected String toJava() {
    String java = createValidValuesJava("    ");
    if (elements) {
      java += "    for (Object o : "+left.getReferredVariable()+") {"+ln;
      java += createCondition("validValues.contains(o)");
      java += "    }"+ln;
      return java;
    } else {
      String check = createCondition("validValues.contains("+ left.getReferredVariable() +")");
      return java+check;
    }
  }

  private String createValidValuesJava(String prefix) {
    String top = prefix+"HashSet validValues = new HashSet();"+ln;
    String topAdd = "";
    String java = "";
    for (Object value : values) {
      if (value instanceof Collection) {
        topAdd = prefix+"Collection value = new ArrayList();"+ln;
        java += prefix+"value = new ArrayList();"+ln;
        Collection vc = (Collection) value;
        for (Object v : vc) {
          java += prefix+"value.add("+valueObjectToString(v)+");"+ln;
        }
        java += prefix+"validValues.add(value);"+ln;
      } else {
        java += prefix+"validValues.add("+valueObjectToString(value)+");"+ln;
      }
    }
    return top+topAdd+java;
  }

  protected String guardName() {
    String valueStr = "";
    for (Object value : values) {
      if (value instanceof Collection) {
        Collection values2 = (Collection) value;
        for (Object value2 : values2) {
          valueStr += "_"+valueObjectToGuardString(value2)+"_";
        }
        continue;
      }
      valueStr += "_"+valueObjectToGuardString(value)+"_";
    }
    return left.getReferredVariable()+"NotOneOf"+valueStr;
  }
/*
  public String guardInvocation() {
//    System.out.println("values:"+values);
    for (Object o : values) {
      if (o instanceof Number) {
        if (((Number)o).intValue() == 0) {
//          System.out.println("c1");
          return "";
        }
      } else {
//        System.out.println("c2");
        return "";
      }
    }
    return "    if("+left.getReferredVariable()+".isEmpty()) return false;"+ln;
  }*/

  public String guardInvocation() {
    if (elements) {
      return "";
    }
    if (values.isEmpty()) {
      return "";
    }
    for (Object v : values) {
      if (v instanceof Collection && ((Collection) v).isEmpty()) {
        return "";
      }
    }
    return "    if("+left.getReferredVariable()+".isEmpty()) return false;"+ln;
  }
}
