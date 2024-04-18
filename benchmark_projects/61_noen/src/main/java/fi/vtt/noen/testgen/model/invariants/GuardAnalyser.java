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
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;

/**
 * @author Teemu Kanstrén
 */
public class GuardAnalyser {
  private final Map<String, Map<InvariantType, Collection<Invariant>>> validInvariants = new HashMap<String, Map<InvariantType, Collection<Invariant>>>();
  private Event previousEvent = null;
//  private final Map<String, Collection<Invariant>> invalidatedInvariants = new HashMap<String, Collection<Invariant>>();

  public void process(Event event) {
    Map<InvariantType, Collection<Invariant>> eventInvariants = validInvariants.get(event.getName());
    boolean first = false;
    if (eventInvariants == null) {
      eventInvariants = new HashMap<InvariantType, Collection<Invariant>>();
      validInvariants.put(event.getName(), eventInvariants);
//      invalidatedInvariants.put(event.getName(), new ArrayList<Invariant>());
      first = true;
    }
    checkForAlwaysIn(event, first);
    checkForLargerThan(event, first);
    checkForValueRange(event, first);
    checkForStateUpdates(event, first);
    if (!event.isExit()) {
      previousEvent = event;
    }
  }

  private void checkForStateUpdates(Event event, boolean first) {
    //TODO this is not implemented as it is left out of scope for now to create new Daikon replacement..
    if (event.isExit()) {
      Collection<CollectionAttribute> collectionAttributes = event.getCollectionAttributes();
      for (CollectionAttribute ca : collectionAttributes) {
        CollectionAttribute pca = previousEvent.getCollectionAttribute(ca.getName());
        if (pca == null) {
          //TODO: remove any invariant related to this array
          continue;
        }
        Collection<String> previousValues = new ArrayList<String>(pca.getValues());
        Collection<String> values = new ArrayList<String>(ca.getValues());
        values.removeAll(previousValues);
        for (String value : values) {
          Collection<StringAttribute> stringAttributes = previousEvent.getStringAttributes();
          for (StringAttribute sa : stringAttributes) {
            if (sa.getValue().equals(value)) {
              //TODO:create new invariant
            }
          }
        }
      }
    }
  }

  private void checkForValueRange(Event event, boolean first) {
    Collection<StringAttribute> stringAttributes = event.getStringAttributes();
    Map<InvariantType, Collection<Invariant>> eventInvariants = validInvariants.get(event.getName());
    Collection<Invariant> valueRanges = eventInvariants.get(InvariantType.VALUE_RANGE);
    if (valueRanges == null) {
      valueRanges = new ArrayList<Invariant>();
      eventInvariants.put(InvariantType.VALUE_RANGE, valueRanges);
    }
    for (StringAttribute strAttr : stringAttributes) {
      String name = strAttr.getName();
      InvariantValueRange valueRange = null;
      for (Invariant invariant : valueRanges) {
        if (invariant.name().equals(name)) {
          valueRange = (InvariantValueRange) invariant;
          break;
        }
      }
      int value = 0;
      try {
        value = Integer.parseInt(strAttr.getValue());
      } catch (NumberFormatException e) {
        //TODO:for complete behaviour, this should remove the invariant but this requires
        //building a list of invalid invariants so it is not re-created later
        continue;
      }
      if (valueRange == null) {
        valueRange = new InvariantValueRange(name);
        valueRanges.add(valueRange);
      }
      if (value > valueRange.getMax()) {
        valueRange.setMax(value);
      }
      if (value < valueRange.getMin()) {
        valueRange.setMin(value);
      }
    }
  }

  private void checkForLargerThan(Event event, boolean first) {
    Collection<CollectionAttribute> collectionAttributes = event.getCollectionAttributes();
    if (first) {
      Map<InvariantType, Collection<Invariant>> eventInvariants = validInvariants.get(event.getName());
      if (eventInvariants == null) {
        eventInvariants = new HashMap<InvariantType, Collection<Invariant>>();
        validInvariants.put(event.getName(), eventInvariants);
      }
//      System.out.println("ca:"+collectionAttributes);
      for (CollectionAttribute ca : collectionAttributes) {
        int size = ca.getValues().size();
        ArrayList<Invariant> invariants = new ArrayList<Invariant>();
        eventInvariants.put(InvariantType.LARGER_THAN, invariants);
        InvariantLargerThan invariant = new InvariantLargerThan(ca.getName(), size);
        invariants.add(invariant);
      }
    } else {
      Map<InvariantType, Collection<Invariant>> eventInvariants = validInvariants.get(event.getName());
      Collection<Invariant> invariants = eventInvariants.get(InvariantType.LARGER_THAN);
      if (invariants == null) {
        //this happens for events without any arrays
        return;
      }
      for (Iterator i = invariants.iterator() ; i.hasNext() ; ) {
        InvariantLargerThan lt = (InvariantLargerThan) i.next();
        int limit = lt.getLimit();
        CollectionAttribute attribute = event.getCollectionAttribute(lt.name());
        if (attribute.getValues().size() < limit) {
          limit = attribute.getValues().size();
        }
        lt.setLimit(limit);
        if (limit == 0) {
          i.remove();
        }
      }
    }
  }

  private void checkForAlwaysIn(Event event, boolean first) {
    if (first) {
      collectAlwaysIn(event);
    } else {
      checkAlwaysIn(event);
    }
    //kaikki taulukkojen nimet talteen ensimmäisellä kertaa
    //sen jälkeen vain tarkistus onko se taulukko aina matkassa, jos ei niin invariantti pois
    //samoin se parametri joka pitäisi aina olla siellä
    //ja sitte katotaan onko parametri siinä taulukossa, jos ei niin invariantti pois
  }

  private void checkAlwaysIn(Event event) {
    Map<InvariantType, Collection<Invariant>> eventInvariants = validInvariants.get(event.getName());
    Collection<Invariant> invariants = eventInvariants.get(InvariantType.ALWAYS_IN);
    for (Invariant i : invariants) {
      InvariantAlwaysIn ai = (InvariantAlwaysIn) i;
      String array = ai.name();
      Collection<String> variables = ai.getVariables();
      CollectionAttribute ca = event.getCollectionAttribute(array);
//      System.out.println("array:"+array+" variables:"+variables);
      for (Iterator<String> vi = variables.iterator() ; vi.hasNext() ; ) {
        String variable = vi.next();
//        System.out.println("var:"+variable);
        StringAttribute str = event.getStringAttribute(variable);
//        System.out.println("str:"+str.getValue());
        if (str == null || !ca.getValues().contains(str.getValue())) {
          vi.remove();
        }
      }
//      System.out.println("array:"+array+" variables:"+variables);
      if (ai.isEmpty()) {
        invariants.remove(ai);
      }
    }
  }

  private void collectAlwaysIn(Event event) {
    //this is first time this event is analysed so store all suitable invariants
    Collection<CollectionAttribute> collectionAttributes = event.getCollectionAttributes();
    Map<InvariantType, Collection<Invariant>> eventInvariants = new HashMap<InvariantType, Collection<Invariant>>();
    validInvariants.put(event.getName(), eventInvariants);
    HashSet<Invariant> alwaysInList = new HashSet<Invariant>();
    eventInvariants.put(InvariantType.ALWAYS_IN, alwaysInList);
    for (CollectionAttribute ca : collectionAttributes) {
      Collection<String> values = ca.getValues();
      Collection<StringAttribute> stringAttributes = event.getStringAttributes();
      for (StringAttribute sa : stringAttributes) {
        if (values.contains(sa.getValue())) {
          InvariantAlwaysIn alwaysIn = null;
          for (Iterator i = alwaysInList.iterator() ; i.hasNext() ; ) {
            InvariantAlwaysIn ai = (InvariantAlwaysIn) i.next();
            if (ai.name().equals(ca.getName())) {
              alwaysIn = ai;
              break;
            }
          }
          if (alwaysIn == null) {
            alwaysIn = new InvariantAlwaysIn(ca.getName());
            alwaysInList.add(alwaysIn);
          }
          alwaysIn.add(sa.getName());
        }
      }
    }
  }

  public Map<InvariantType, Collection<Invariant>> getValidInvariants(String eventName) {
    return validInvariants.get(eventName);
  }
}
