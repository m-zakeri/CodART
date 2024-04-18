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

package fi.vtt.noen.testgen.model.invariants;

import java.util.Collection;
import java.util.ArrayList;

/**
 * @author Teemu Kanstrén
 */
public class InvariantAlwaysIn extends Invariant {
  private final Collection<String> variables = new ArrayList<String>();

  public InvariantAlwaysIn(String name) {
    super(InvariantType.ALWAYS_IN, name);
  }

  public boolean isEmpty() {
    return variables.isEmpty();
  }

  public void add(String variable) {
    variables.add(variable);
  }

  public Collection<String> getVariables() {
    return variables;
  }

  public boolean equals(Object o) {
    return name.equals(o);
  }

  public int hashCode() {
    return name.hashCode();
  }
}
