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
public class Event {
  private final String name;
  private boolean exit = false;
  private final Collection<CollectionAttribute> collectionAttributes = new ArrayList<CollectionAttribute>();
  private final Collection<StringAttribute> stringAttributes = new ArrayList<StringAttribute>();

  public Event(String name) {
    this(name, false);
  }

  public Event(String name, boolean exit) {
    this.name = name;
    this.exit = exit;
  }
  
  public void add(StringAttribute attribute) {
    stringAttributes.add(attribute);
  }

  public void add(CollectionAttribute attribute) {
    collectionAttributes.add(attribute);
  }

  public boolean isExit() {
    return exit;
  }

  public String getName() {
    return name;
  }

  public Collection<CollectionAttribute> getCollectionAttributes() {
    return collectionAttributes;
  }

  public CollectionAttribute getCollectionAttribute(String name) {
    for (CollectionAttribute ca : collectionAttributes) {
      if (ca.getName().equals(name)) {
        return ca;
      }
    }
    return null;
  }

  public Collection<StringAttribute> getStringAttributes() {
    return stringAttributes;
  }

  public StringAttribute getStringAttribute(String name) {
    for (StringAttribute sa : stringAttributes) {
      if (sa.getName().equals(name)) {
        return sa;
      }
    }
    return null;
  }
}
