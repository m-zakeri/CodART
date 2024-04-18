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
 * A base class for any invariant constraints that describes the size of an object with the
 * possibility that it is formed as a sum of more than one. For example, size is always 1 or
 * size is always x+1, or x-1.
 *
 * @author Teemu Kanstrén
 */
public abstract class ConstraintWithAddition extends DaikonConstraint {
  protected int leftAddition = 0;
  protected int rightAddition = 0;

  protected String parseAddition(String value, boolean left) {
    value = value.trim();
    int index = value.indexOf('+');
    if (index == -1) {
      index = value.indexOf('-');
    } else {
      //Integer.parseInt does not like to see the '+' sign there so we increment by 1 to pass it
      index++;
    }
    if (index == -1) {
      return value;
    }
    String addPart = value.substring(index, value.length());
    int addition = Integer.parseInt(addPart);
    if (addition > 0) {
      //we must return index to before + sign to also trim that off
      index--;
    }
    if (left) {
      leftAddition = addition;
    } else {
      rightAddition = addition;
    }
    return value.substring(0, index);
  }

  protected String additionToString(boolean left) {
    String addPart = "";
    int addition = 0;
    if (left) {
      addition = leftAddition;
    } else {
      addition = rightAddition;
    }
    if (addition > 0) {
      addPart = "+"+addition;
    }
    if (addition < 0) {
      //negative values get - sign automatically
      addPart = ""+addition;
    }
    return addPart;
  }
}
