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

/**
 * Represents a value in an invariant that is a reference to another variable. That is, if the invariant
 * is X < 1, then X is a reference value as it refers to a variable, and 1 is a primitive value.
 *
 * @author Teemu Kanstrén
 */
public class ReferenceValue {
  private final String referredVariable;
  private int index = -1;
  private boolean global = false;
  private boolean returnValue = false;
  private final boolean array;
  public static final ReferenceValue EMPTY_ARRAY = new ReferenceValue();

  private ReferenceValue() {
    referredVariable = null;
    array = true;
  }

  public ReferenceValue(String referredVariable, boolean array) {
    String[] parts = referredVariable.split("\\?");
    this.referredVariable = parts[0];
    this.array = array;
    if (parts[1].equals("g")) {
      //it is a global variable. must use char (g) as some constraints search for "-" and "+"
      global = true;
      return;
    }
    if (parts[1].equals("r")) {
      //it is a return value variable. must use char (r) as some constraints search for "-" and "+"
      returnValue = true;
      return;
    }
    int index = Integer.parseInt(parts[1]);
    if (index < 0) {
      throw new IllegalArgumentException("Parameter index should be >= 0, 'g' for globals or 'r' for return values. Was:"+index+".");
    }
    this.index = index;
  }

  public String getReferredVariable() {
    return referredVariable;
  }

  public int getIndex() {
    return index;
  }

  public boolean isArray() {
    return array;
  }

  public boolean isGlobal() {
    return global;
  }

  public boolean isReturnValue() {
    return returnValue;
  }

  public String toString() {
    return "reference:"+referredVariable;
  }
}
