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

import java.util.*;

/**
 * Describes constraints related to the states and transitions of the EFSM.
 * Each transition from a state is related to a set of invariants to describe when
 * a transition from a state is allowed to happen. Transitions also describe the
 * invariants related to when a transition is made from one state to another. This
 * is used in the geneted model to generate guards for input_output states.
 *
 * @author Teemu Kanstrén
 */
public class DaikonModel {
  private Map<String, DaikonState> states = new HashMap<String, DaikonState>();
  private Map<String, Collection<DaikonTransition>> transitions = new HashMap<String, Collection<DaikonTransition>>();

  public void add(DaikonModelElement element) {
    if (element instanceof DaikonState) {
      add((DaikonState) element);
      return;
    }
    add((DaikonTransition) element);
  }

  public void add(DaikonState state) {
    String name = state.getFullName();
    states.put(name, state);
  }

  public void add(DaikonTransition transition) {
    String source = transition.getSource();
    Collection<DaikonTransition> transitions = this.transitions.get(source);
    if (transitions == null) {
      transitions = new ArrayList<DaikonTransition>();
      this.transitions.put(source, transitions);
    }
    transitions.add(transition);
  }

  public DaikonState getState(String id) {
    return states.get(id);
  }

  public void printStates() {
    System.out.println("states:"+states);
  }

  public Collection<DaikonTransition> getTransitions(String id) {
    return transitions.get(id);
  }

  public DaikonTransition getTransition(String source, String target) {
    Collection<DaikonTransition> transitions = this.transitions.get(source);
    for (Iterator<DaikonTransition> i = transitions.iterator(); i.hasNext();) {
      DaikonTransition transition = i.next();
      if (target.equals(transition.getTarget())) {
        return transition;
      }
    }
    return null;
  }

  public int numberOfStates() {
    return states.size();
  }

  public int numberOfTransitions() {
    int size = 0;
    for (Iterator<String> i = transitions.keySet().iterator(); i.hasNext();) {
      String id = i.next();
      Collection<DaikonTransition> transitions = this.transitions.get(id);
      size += transitions.size();
    }
    return size;
  }
}
