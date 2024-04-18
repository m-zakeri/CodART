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

package fi.vtt.noen.testgen.model.daikon;

import fi.vtt.noen.testgen.model.daikon.constraints.DaikonConstraint;

import java.util.*;

/**
 * Describes invariants related to a single state (method call). These are manifested in the
 * generated model code as input method states without transitions. 
 *
 * @author Teemu Kanstrén
 */
public class DaikonState extends DaikonModelElement {
  private double min = Integer.MAX_VALUE;
  private double max = Integer.MIN_VALUE;

  public DaikonState(String fullName) {
    super(fullName);
  }

  public String parameterValues(String type) {
    for (DaikonConstraint dc : constraints) {
      if (dc.parameterValues(type) != null) {
        return dc.parameterValues(type);
      }
    }
    return null;
  }

  public String createGuardInvocations() {
    String guard = "";
    for (DaikonConstraint dc : constraints) {
      if (dc.isGlobal()) {
        guard += dc.guardInvocation();
      }
    }
    return guard;
  }

  public String guardContentMethods(Set<String> generatedMethods) {
    //NOTE: this is to test better guards with only size checks
    if (true) return "";

    String guard = "";
    for (DaikonConstraint dc : constraints) {
      if (dc.isGlobal()) {
        //onle generate each method once
        String id = dc.guardInvocation();
        if (generatedMethods.contains(id)) {
          continue;
        }
        generatedMethods.add(id);
        guard += dc.guardMethod();
      }
    }
    return guard;
  }

  //TODO here is a BUG, we need to map min-max to parameters now all parameter for a state share the same min-max
  private void calculateMinMax(int parameterIndex) {
    if (min < Integer.MAX_VALUE || max > Integer.MIN_VALUE) {
      return;
    }
    for (DaikonConstraint dc : constraints) {
      if (dc.getIndex() != parameterIndex) {
        continue;
      }
      double dcmin = dc.min();
      if (dcmin < min) {
        min = dcmin;
      }
      double dcmax = dc.max();
      if (dcmax > max) {
        max = dcmax;
      }
    }
    if (min == Integer.MAX_VALUE) {
      min = Integer.MIN_VALUE;
    }
    if (max == Integer.MIN_VALUE) {
      max = Integer.MAX_VALUE;
    }
  }

  public double min(int parameterIndex) {
    calculateMinMax(parameterIndex);
    return min;
  }

  public double max(int parameterIndex) {
    calculateMinMax(parameterIndex);
    return max;
  }

  public boolean booleanTrue(int parameterIndex) {
    for (DaikonConstraint dc : constraints) {
      if (dc.getIndex() != parameterIndex) {
        continue;
      }
      if (dc.isTrue()) {
        return true;
      }
    }
    return false;
  }

  public boolean booleanFalse(int parameterIndex) {
    for (DaikonConstraint dc : constraints) {
      if (dc.getIndex() != parameterIndex) {
        continue;
      }
      if (dc.isFalse()) {
        return true;
      }
    }
    return false;
  }
}