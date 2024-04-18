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

package fi.vtt.noen.testgen.observations.data;

import fi.vtt.noen.testgen.model.Const;

import java.util.*;

/**
 * An event in the execution of a program, such as a message passed through its external interface.
 * So like in practice it could be a method call to input or output interface. Or anything else, but
 * thats what it is so far.
 *
 * @author Teemu Kanstrén
 */
public class Event {
  private final String name;
  private final long timestamp;
  private final boolean exit;
  private final Collection<EventAttribute> attributes = new ArrayList<EventAttribute>();

  public Event(String name) {
    this.name = name;
    this.timestamp = System.currentTimeMillis();
    exit = false;
  }

  public Event(String name, long timestamp) {
    this.name = name;
    this.timestamp = timestamp;
    exit = false;
  }

  public Event(String name, boolean exit) {
    this.name = name;
    this.timestamp = System.currentTimeMillis();
    this.exit = exit;
  }

  public boolean isExit() {
    return exit;
  }

  public Date getTime() {
    return new Date(timestamp);
  }

  public String getName() {
//    if (exit) {
//      return name+"_EXIT";
//    }
    return name;
  }

  public void addAttribute(String name, Object obj) {
    attributes.add(new EventAttribute(name, obj));
  }

  public void addAttribute(String name, Collection values) {
    attributes.add(new ArrayAttribute(name, values));
  }

  public Iterator<EventAttribute> attributes() {
    return attributes.iterator();
  }
}
