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

/**
 * An invariant that says the contents of a variable are always greater than a certain value. The
 * matched value may be a constant primitive value or the contents of another variable.
 * For example, if X is the name of the variable which this invariant describes, possibilities
 * include X > 1, where X always has a value greater than 1, and X > Y, where the value of X always
 * is greater than that of Y. 
 *
 * @author Teemu Kanstrén
 */
public class GreaterConstraint extends ConstraintWithAddition {
  private boolean array = false;

  public GreaterConstraint(String left, String value) {
    if (parseLexical(value)) {
      return;
    }
    if (value.startsWith("size")) {
      array = true;
      parseAddition(value, false);
      value = parseArrayName(value);
    }
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
    return super.max();
  }

  public String asAssert(String returnVar) {
    checkEnabled();
    String rstr = valueObjectToString(right);
    if (array) {
      rstr += ".size()";
    }
    return "assertTrue("+returnVar+additionToString(true)+" > "+rstr+additionToString(false)+");"+ln;
  }

  public String toString() {
    checkEnabled();
    String rstr = right.toString();
    if (array) {
      rstr = "sizeof("+rstr+")";
    }
    return left +additionToString(true)+" > "+rstr+additionToString(false);
  }

  protected String toJava() {
    checkEnabled();
    String rstr = right.toString();
    if (right instanceof ReferenceValue) {
      ReferenceValue value = (ReferenceValue) right;
      rstr = value.getReferredVariable();
    }
    if (array) {
      rstr += ".size()";
    }
    String condition = left.getReferredVariable() + additionToString(true) + " > " + rstr + additionToString(false);
    return createCondition(condition);
  }

  protected String guardName() {
    return left.getReferredVariable()+"IsNotGreaterThan"+valueObjectToGuardObject(right);
  }
}
