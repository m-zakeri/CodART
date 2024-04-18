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
 * An invariant that says the contents of a variable are never equal to a certain value. The
 * matched value may be a constant primitive value or the contents of another variable.
 * For example, if X is the name of the variable which this invariant describes, possibilities
 * include X != 1, where X is always different from 1, and X != Y, where the value of X always
 * is from from that of Y. 
 *
 * @author Teemu Kanstrén
 */public class NonEqualConstraint extends ConstraintWithAddition {
  private boolean rightArray = false;
  private boolean leftArray = false;

  public NonEqualConstraint(String left, String value) {
    if (value.startsWith("size")) {
      rightArray = true;
      parseAddition(value, false);
      value = parseArrayName(value);
    }
    if (left.startsWith("size")) {
      leftArray = true;
      parseAddition(left, true);
      left = parseArrayName(left);
    }
    this.left = (ReferenceValue) DaikonParser.parseValueObject(left);
    this.right = DaikonParser.parseValueObject(value);
  }

  public String asAssert(String returnVar) {
    String value = valueObjectToString(right);
    if (rightArray) {
      value += ".size()"+additionToString(false);
    }
    if (leftArray) {
      returnVar += ".size()"+additionToString(true);
    }
    return "assertTrue("+returnVar+" != "+value+");"+ln;
  }

  public String toString() {
    String lstr = left.toString();
    String rstr = right.toString();
    if (rightArray) {
      rstr = "sizeof("+rstr+")";
    }
    if (leftArray) {
      lstr = "sizeof("+lstr+")";
    }
    lstr += additionToString(true);
    rstr += additionToString(false);
    return lstr +" != "+rstr;
  }

  public String toJava() {
    String lstr = left.getReferredVariable();
    String rstr = valueObjectToString(right);
    if (rightArray) {
      rstr += ".size()";
    }
    if (leftArray) {
      lstr += ".size()";
    }
    lstr += additionToString(true);
    rstr += additionToString(false);
    return createCondition(lstr+" != "+rstr);
  }

  protected String guardName() {
    return left.getReferredVariable()+"Equals"+valueObjectToGuardObject(right);
  }
}
