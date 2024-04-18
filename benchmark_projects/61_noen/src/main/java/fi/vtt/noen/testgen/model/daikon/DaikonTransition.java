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
import fi.vtt.noen.testgen.StringUtils;

import java.util.Iterator;
import java.util.Map;
import java.util.Set;

/**
 * Describes the invariants related to given values when a transition is made from one state to another state.
 * In practice, this means invariants over the relevant variable values at the time when the first state was
 * entered, causing a transition from this input state to output state afterwards. This is not relevant in
 * cases where the originating state is not an input state of course.. unless you do sequences where
 * several output states are in a sequence, which is not really supported right now.. 
 *
 * @author Teemu Kanstrén
 */
public class DaikonTransition extends DaikonModelElement {
  private String source = null;
  private String target = null;
  public static final String ln = "\n";

  public DaikonTransition(String fullName) {
    super(fullName);
    String[] names = fullName.split(",");
    if (names.length != 2) {
      throw new IllegalArgumentException("Transition format must be 'source,target' but it was '"+ fullName +"'");
    }
    this.source = names[0];
    this.target = names[1];
  }

  public String getSource() {
    return source;
  }

  public String getTarget() {
    return target;
  }

  public String guardContentMethods(Set<String> generatedMethods) {
    String guard = "";
    for (DaikonConstraint dc : constraints) {
      if (dc.isGlobal()) {
        //onle generate each method once
        String id = dc.guardInvocation();
        if (generatedMethods.contains(id)) {
          continue;
        }
        generatedMethods.add(id);
        guard += ln+dc.guardMethod();
      }
    }
    return guard;
  }

  public String createAsserts(String returnVar) {
    String assertion = "";
    for (DaikonConstraint dc : constraints) {
      if (dc.isReturnValue()) {
        assertion += dc.asAssert(returnVar);
      }
    }
    return assertion;
  }

  public String createTransitionGuards() {
    String guard = "";
    for (DaikonConstraint dc : constraints) {
      if (dc.isGlobal()) {
        //only global variable constraints are important for guards
        guard += dc.guardInvocation();
      }
    }
    return guard;
  }
}
