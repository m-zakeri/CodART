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
import fi.vtt.noen.testgen.model.daikon.constraints.ReferenceValue;

import java.util.Collection;
import java.util.ArrayList;
import java.util.HashSet;

/**
 * This invariant says that the contents of an array object are always the same.
 * For example, array Clients always containst "myclient" and nothing else.
 *
 * @author Teemu Kanstrén
 */
public class ArrayContentsConstraint extends DaikonConstraint {
  /** The expected contents of the array. */
  private final Collection<String> values = new ArrayList<String>();

  public ArrayContentsConstraint(String left, String right) {
    //this is an array
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    right = right.trim();
    System.out.println("left:"+left+" right:"+right);
    right = right.substring(0, right.length()-1);
    String[] values = right.split(", ");
    if (values[0].length() == 0) {
      //skip empty arrays
      System.out.println("empty array");
      return;
    }

    for (int i = 0; i < values.length; i++) {
//      this.values.add(GuardAnalyser.parseValueObject(values[i]));
      this.values.add(values[i]);
    }
    System.out.println("non-empty array"+values);
  }

  public Collection<String> arrayNames() {
    Collection<String> names = new HashSet<String>();
    names.add(left.getReferredVariable());
    return names;
  }
  
  public Collection<String> getValues() {
    return values;
  }

  public String toString() {
    return left+" == "+values;
  }

  public String asAssert(String returnVar) {
    String list = createRequiredList("");
    list += "assertEquals("+returnVar+", requiredValues);"+ln;
//    list += "    for (Object o : requiredValues) {"+ln;
//    list += "      assertTrue("+returnVar+".contains(o));"+ln;
//    list += "    };"+ln;
    return list;
  }

  protected String toJava() {
    String prefix = createRequiredList("    ");
    String conditional = left.getReferredVariable()+".equals(requiredValues)";
    String check = createCondition(conditional);
    return prefix+check;
  }

  protected String guardName() {
    String name = left.getReferredVariable() + "IsNot";
    if (values.isEmpty()) {
      return name + "Empty";
    }
    for (Object o : values) {
      name += "_"+o;
    }
    return name;
  }

  private String createRequiredList(String prefix) {
    String java = prefix+"Collection requiredValues = new ArrayList();"+ln;
    for (String value : values) {
      java += prefix+"requiredValues.add(\""+valueObjectToGuardString(value)+"\");"+ln;
    }
    return java;
  }

  public String guardInvocation() {
    System.out.println("left:"+left+" values:"+values);
    if (values.isEmpty() || values.contains(new Integer(0))) {
      return "";
    }
    return "    if("+left.getReferredVariable()+".isEmpty()) return false;"+ln;
  }
}
