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

import java.util.Collection;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;

/**
 * Base class for daikon states and transitions, to represent the invariant related to both states and
 * transitions.
 *
 * @author Teemu Kanstrén
 */
public abstract class DaikonModelElement {
  private final String fullName;
  protected final Collection<DaikonConstraint> constraints = new ArrayList<DaikonConstraint>();

  protected DaikonModelElement(String fullName) {
    this.fullName = fullName;
  }

  public static DaikonModelElement create(String fullName) {
    if (fullName.indexOf(",") > 0) {
      return new DaikonTransition(fullName);
    }
    return new DaikonState(fullName);
  }

  public void addConstraint(DaikonConstraint constraint) {
    constraints.add(constraint);
  }

  public String getFullName() {
    return fullName;
  }

  public Collection<String> arrayNamesForConstraints() {
    Collection<String> arrays = new HashSet<String>();
    for (Iterator<DaikonConstraint> i = constraints.iterator(); i.hasNext();) {
      DaikonConstraint dc = i.next();
      arrays.addAll(dc.arrayNames());
    }
    return arrays;
  }

  public Collection<DaikonConstraint> getConstraints() {
    return constraints;
  }

  public String toString() {
    return fullName+"::"+constraints.toString();
  }
}
