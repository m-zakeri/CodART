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
 * This invariant says that the value of a given variable is always one that is at that time contained
 * in another list variable. For example, variable Client is "myclient" and list variable Clients is
 * ["myclient", "myclient2"] and the same applies whatever the value of Client is at some point of
 * program execution.
 *
 * @author Teemu Kanstrén
 */
public class AlwaysInArrayConstraint extends DaikonConstraint {
  public AlwaysInArrayConstraint(String left, String value) {
    //this should always be a reference value, else it makes no sense and exception should be given as is
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    value = value.trim();
    //this is an array
    //this should always be a reference value, else it makes no sense and exception should be given as is
    this.right = (ReferenceValue)DaikonParser.parseValueObject(value);
  }

  public boolean isEnabled() {
    return true;
  }

  public Collection<String> arrayNames() {
    Collection<String> names = new HashSet<String>();
    names.add(left.getReferredVariable());
    return names;
  }

  public String toString() {
    return left+" always in "+right;
  }

  public String asAssert(String returnVar) {
    ReferenceValue value = (ReferenceValue) right;
    String arrayName = value.getReferredVariable();
    return "assertTrue("+arrayName+".contains("+returnVar+"));"+ln;
  }

  protected String toJava() {
    ReferenceValue value = (ReferenceValue) right;
    String arrayName = value.getReferredVariable();
    String itemName = left.getReferredVariable();
    String conditional = arrayName + ".contains(" + itemName + ")";
    return createCondition(conditional);
  }

  public String guardName() {
    return left.getReferredVariable()+"IsNotIn"+valueObjectToGuardString(right);
  }

  public String parameterValues(String type) {
    ReferenceValue value = (ReferenceValue) right;
    String arrayName = value.getReferredVariable();
    return "    return ("+type+") randomItemFrom("+arrayName+");"+ln;
  }
}
