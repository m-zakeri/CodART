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

package fi.vtt.noen.testgen.model.fsm;

import org.processmining.models.graphbased.directed.transitionsystem.TransitionSystem;
import org.processmining.models.graphbased.directed.transitionsystem.State;
import org.processmining.models.graphbased.directed.transitionsystem.Transition;

import java.util.*;

/**
 * Describes the FSM model as received from ProM. FSM states and transitions between these states.
 *
 * @author Teemu Kanstrén
 */
public class FSMModel {
  private Map<String, FSMState> states = new TreeMap<String, FSMState>();
  private Map<FSMState, Collection<FSMTransition>> transitions = new HashMap<FSMState, Collection<FSMTransition>>();
  private Set<FSMTransition> allTransitions = new HashSet<FSMTransition>();

  //this is for testing
  public FSMModel(TreeMap<String, FSMState> states, Collection<FSMTransition> transitions) {
    this.states = states;
    for (Iterator<FSMTransition> i = transitions.iterator(); i.hasNext();) {
      FSMTransition transition = i.next();
      FSMState source = transition.getSource();
      addTransition(source,transition);
    }
  }

  private void addTransition(FSMState source, FSMTransition transition) {
    Collection<FSMTransition> transitions = this.transitions.get(source);
    if (transitions == null) {
      transitions = new ArrayList<FSMTransition>();
      this.transitions.put(source, transitions);
    }
    transitions.add(transition);
    allTransitions.add(transition);
  }

  public FSMModel(TransitionSystem ts) {
    Set<State> tsStates = ts.getNodes();
    for (State state : tsStates) {
      String id = removePromPrefixAndPostFix(state.toString());
      if (id.length() == 0) {
        //skip the "INIT" empty state that is added by PROM
        continue;
      }
      FSMState fsmState = new FSMState(id);
      states.put(id, fsmState);
    }

    Set<Transition> tsTransitions = ts.getEdges();
    for (Transition transition : tsTransitions) {
      String sourceId = transition.getSource().toString();
      if (sourceId.length() == 0) {
        //skip the "INIT" empty state that is added by PROM
        continue;
      }
      sourceId = removePromPrefixAndPostFix(sourceId);
      FSMState source = states.get(sourceId);
      String targetId = transition.getTarget().toString();
      targetId = removePromPrefixAndPostFix(targetId);
      FSMState target = states.get(targetId);
      FSMTransition st = new FSMTransition(source, target);
      addTransition(source, st);
    }
  }

  //removes [[ and ]] surroundings from prom state names to match then to daikon states
  private String removePromPrefixAndPostFix(String stateId) {
    if (stateId.equals("[[]]")) {
      return "";
    }
    String[] parts = stateId.split("\\[\\[");
    stateId = parts[1];
    parts = stateId.split("\\]\\]");
    stateId = parts[0];
    return stateId;
  }

  public Map<String, FSMState> getStates() {
    return states;
  }

  public int numberOfStates() {
    return states.size();
  }

  public int numberOfTransitions() {
    return allTransitions.size();
  }

  public Collection<FSMTransition> getTransitionsFor(FSMState state) {
    return transitions.get(state);
  }

  public FSMState getState(String id) {
    return states.get(id);
  }

  public String toString() {
    return "states:"+ states.toString()+"\ntransitions:"+ transitions.toString();
  }
}
