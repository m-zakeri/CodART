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
import java.util.HashSet;

/**
 * This invariant says that only the given object is contained in an array at any point of
 * program execution. For example, array Clients is ["myclient"] and this never changes at
 * any of the monitored points of program execution.
 *
 * @author Teemu Kanstrén
 */
public class ArrayElementsConstraint extends DaikonConstraint {
  public ArrayElementsConstraint(String left, String value) {
    //this is an array
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    this.right = DaikonParser.parseValueObject(value);
  }

  public Collection<String> arrayNames() {
    Collection<String> names = new HashSet<String>();
    names.add(left.getReferredVariable());
    return names;
  }

  public String toString() {
    return left +" elements == "+valueObjectToString(right);
  }

  public String asAssert(String returnVar) {
    String java = "for (Object o : "+returnVar+") {"+ln;
    java += "  assertEquals("+valueObjectToString(right)+", o);"+ln;
    java += "}"+ln;
    return java;
  }

  protected String toJava() {
    String java = "    Object expected = "+valueObjectToString(right)+";"+ln;
    java += "    for (Object o : "+left.getReferredVariable()+") {"+ln;
    String check = createCondition("expected.equals(o)", 1);
    java += check;
    java += "    }"+ln;
    return java;
  }

  protected String guardName() {
    return left.getReferredVariable()+"AreDifferentFrom"+valueObjectToGuardObject(right);
  }

}
