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
 * This invariant says that the size of an array variable is always constant, while its contents may change.
 * For example, Clients size is always 1 or Clients size is always x+1, where x may be any other variable
 * at that point of execution. This invariant cal also say that the size is one of several constant values.
 *
 * @author Teemu Kanstrén
 */
public class ConstantSizeConstraint extends ConstraintWithAddition {
  public ConstantSizeConstraint(String left, String right) {
    left = parseAddition(left, true);
    right = right.trim();
    //Remove "size(" from start and ")" from end
    left = left.substring(5, left.length()-1);
    //this is an array
    this.left = (ReferenceValue)DaikonParser.parseValueObject(left);
    if (right.startsWith("size(")) {
      right = parseAddition(right, false);
      //this is an array
      right = right.substring(5, right.length()-1);
      this.right = DaikonParser.parseValueObject(right);
    } else if (right.endsWith("}")) {
      //remove } from the end
      right = right.substring(0, right.length()-1);
      this.right = DaikonParser.parseObjectList(right);
    } else {
      this.right = DaikonParser.parseValueObject(right);
    }
  }

  public Collection<String> arrayNames() {
    Collection<String> names = new HashSet<String>();
    names.add(left.getReferredVariable());
    if (right instanceof ReferenceValue) {
      ReferenceValue reference = (ReferenceValue) right;
      if (reference.isArray()) {
        names.add(reference.getReferredVariable());
      }
    }
    return names;
  }

  public String toString() {
    if (right instanceof Collection) {
      String list = stringFrom((Collection)right);
      return "sizeof("+left+") one of {"+list+"}";
    }
    if (!(right instanceof ReferenceValue)) {
      return "sizeof("+ left +") == "+right;
    }
    ReferenceValue reference = (ReferenceValue) right;
    if (reference.isArray()) {
      return "sizeof("+ left +")"+additionToString(true)+" == sizeof("+right+")"+additionToString(false);
    }
    return "sizeof("+ left +")"+additionToString(true)+" == "+right;
  }

  protected String toJava() {
    if (right instanceof Collection) {
      return collectionJava();
    }
    String lstr = left.getReferredVariable() + ".size()";
    String rstr = valueObjectToString(right);
    if (right instanceof ReferenceValue) {
      ReferenceValue reference = (ReferenceValue) right;
      if (reference.isArray()) {
        rstr = reference.getReferredVariable() + ".size()";
      } else {
        rstr = reference.getReferredVariable();
      }
    }
    lstr += additionToString(true);
    rstr += additionToString(false);
    return createCondition(lstr+" == "+rstr);
  }

  public String asAssert(String returnVar) {
    if (right instanceof Collection) {
      Collection values = (Collection) right;
      String assertion = "Collection validSizes = new HashSet();"+ln;
      for (Object o : values) {
        assertion += "validSizes.add("+valueObjectToString(o)+");"+ln;
      }
      assertion += "assertTrue(validSizes.contains(new Double("+returnVar+".size()"+additionToString(false)+")));"+ln;
      return assertion;
    }
    return "assertEquals("+valueObjectToString(right)+", "+returnVar+".size()"+additionToString(false)+");"+ln;
  }

  private String collectionJava() {
    String java = "    Collection validSizes = new HashSet();"+ln;
    Collection values = (Collection) right;
    for (Object o : values) {
      java += "    validSizes.add("+valueObjectToString(o)+");"+ln;
    }
    String condition = "validSizes.contains(new Double(" + left.getReferredVariable() + ".size()" + additionToString(false) + "))";
    String check = createCondition(condition);
    return java + check;
  }

  protected String guardName() {
    if (right instanceof Collection) {
      String result = left.getReferredVariable()+"SizeDoesNotEquals";
      Collection stuff = (Collection) right;
      for (Object o : stuff) {
        result += "_"+valueObjectToGuardObject(o);
      }
      return result;
    }
    return left.getReferredVariable()+"SizeDoesNotEqual"+valueObjectToGuardObject(right);
  }

  public String guardInvocation() {
//    if (!(right instanceof Collection) && !(right instanceof Number)) {
//      return "";
//    }
    if (right instanceof Number) {
      Number n = (Number) right;
      if (n.intValue() == 0) {
        return "";
      }
    } else if (right instanceof Collection) {
      Collection values = (Collection) right;
      for (Object o : values) {
        if (o instanceof Number) {
          if (((Number)o).intValue() == 0) {
//            System.out.println("c1");
            return "";
          }
        } else {
//          System.out.println("c2");
          return "";
        }
      }
    } else {
      return "";
    }
    return "    if("+left.getReferredVariable()+".isEmpty()) return false;"+ln;
  }
}
