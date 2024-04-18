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
import java.util.Collections;

/**
 * An invariant that says the contents of a variable always match a certain value. The
 * matched value may be a constant primitive value or the contents of another variable.
 * For example, if X is the name of the variable which this invariant describes, possibilities
 * include X = 1, where X always has the value of 1, and X = Y, where the contents of X always
 * match the contents of Y. 
 *
 * @author Teemu Kanstrén
 */
public class EqualsConstraint extends DaikonConstraint {
  public EqualsConstraint(String left, String value) {
    this.left = (ReferenceValue) DaikonParser.parseValueObject(left);
    this.right = DaikonParser.parseValueObject(value);
  }

  public double min() {
    if (right instanceof Number) {
      Number n = (Number) right;
      return n.doubleValue();
    }
    return super.min();
  }

  public double max() {
    if (right instanceof Number) {
      Number n = (Number) right;
      return n.doubleValue();
    }
    return super.max();
  }

  public String toString() {
    return left +" == "+right;
  }

  public String asAssert(String returnVar) {
/*    String expected = valueObjectToString(value);
    String assertion = "";
    if (value instanceof ReferenceValue) {
      assertion += "String expected = create"+left.getReferredVariable()+"For("+valueObjectToString(value)+");"+ln;
      expected = "expected";
    }
    assertion += "assertEquals("+expected+", "+returnVar+");"+ln;
    */
    return "assertEquals("+valueObjectToString(right)+", "+returnVar+");"+ln;
  }

/*  public Collection<String> getAssertObjectValues() {
    if (value instanceof ReferenceValue) {
      Collection<String> result = new ArrayList<String>();
      result.add(valueObjectToString(value));
      return result;
    }
    return Collections.EMPTY_LIST;
  }*/

  public String toJava() {
    return createCondition(left.getReferredVariable()+".equals("+valueObjectToString(right)+")");
  }

  protected String guardName() {
    return left.getReferredVariable()+"DoesNotEqual"+valueObjectToGuardObject(right);
  }
}
