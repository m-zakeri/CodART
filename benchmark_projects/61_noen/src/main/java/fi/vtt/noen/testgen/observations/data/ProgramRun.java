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

import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

/**
 * Describes one execution of the analysed program, that is used as a basis for invariant inference
 * and FSM generation.
 *
 * @author Teemu Kanstrén
 */
public class ProgramRun {
  private final long startTime;
  private final String name;
  private final List<Event> events = new ArrayList<Event>();

  public ProgramRun(String name) {
    this.startTime = System.currentTimeMillis();
    this.name = name;
  }

  public void add(Event event) {
    events.add(event);
  }

  public Iterator<Event> iterator() {
    return events.iterator();
  }

  public String getName() {
    return name;
  }
}
