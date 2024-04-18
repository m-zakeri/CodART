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
import java.util.HashSet;

/**
 * This invariant says that the size of an array variable is always constant, while its contents may change.
 * For example, Clients size is always 1 or Clients size is always x+1, where x may be any other variable
 * at that point of execution.
 * TODO: what is the difference with constantsizeconstraint? ->> apparently this is not supported,the other is
 *
 * @author Teemu Kanstrén
 */
public class SizeOfConstraint extends ConstraintWithAddition {
  public SizeOfConstraint(String left, String right) {
//    System.out.println("left:"+left+" right:"+right);
    left = left.trim();
    left = parseAddition(left, true);
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    right = right.trim();
    right = parseAddition(right, false);
    //this is an array
    //remove last )
    right = right.substring(0, right.length()-1);
    this.right = (ReferenceValue)DaikonParser.parseValueObject(right);
  }

  public Collection<String> arrayNames() {
    Collection<String> names = new HashSet<String>();
    names.add(left.getReferredVariable());
    return names;
  }
  
  public String toString() {
    String lstr = left.toString();
    String rstr = "sizeof("+right+")";
    lstr += additionToString(true);
    rstr += additionToString(false);
    return lstr+" == "+rstr;
  }

  public String asAssert(String returnVar) {
    //this throws but we dont currently support this type of assert anyway 
    return super.asAssert(returnVar);
  }

  public String toJava() {
    ReferenceValue value = (ReferenceValue) right;
    String lstr = value.getReferredVariable()+".size()"+additionToString(false);
    String rstr = left.getReferredVariable()+additionToString(true);
    lstr += additionToString(true);
    rstr += additionToString(false);
    return createCondition(lstr+" == "+rstr);
  }

  protected String guardName() {
    ReferenceValue value = (ReferenceValue) right;
    return value.getReferredVariable()+"SizeDoesNotEqual"+left.getReferredVariable();
  }

}
