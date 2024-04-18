/*
 * Copyright (C) 2010 VTT Technical Research Centre of Finland.
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

package fi.vtt.noen.testgen.observations;

import fi.vtt.noen.testgen.observations.data.Event;
import fi.vtt.noen.testgen.observations.data.ProgramRun;
import fi.vtt.noen.testgen.observations.data.ProgramRunSuite;

/**
 * Facade for producing traces.
 *
 * @author Teemu Kanstren
 */
public class Trace {
  private static ProgramRunSuite suite = null;
  private static ProgramRun run = null;
  //disabled by default in an operational system
  private static boolean disabled = true;

  public static void startTest(String name) {
    if (disabled) {
      suite = new ProgramRunSuite("MFW-trace", true);
      disabled = false;
    }
    run = new ProgramRun(name);
  }

  public static void endTest() {
    if (run == null) {
      throw new NullPointerException("Program Run should be initialized");
    }
    suite.addTest(run);
  }

  public static void close() {
    if (disabled) return;
    suite.close();
  }

  public static void start(String name, Object... args) {
    if (disabled) return;
    event(name, false, args);
  }

  private static void event(String name, boolean exit, Object[] args) {
    Event event = new Event(name, exit);
    String threadId = ""+Thread.currentThread().getId();
    event.addAttribute("threadId", threadId);
    for (int i = 0; i < args.length; i++) {
      Object arg = args[i];
      event.addAttribute("p"+i, arg);
    }
    run.add(event);
  }

  public static void complete(String name, Object... args) {
    if (disabled) return;
    event(name, true, args);
  }
}
