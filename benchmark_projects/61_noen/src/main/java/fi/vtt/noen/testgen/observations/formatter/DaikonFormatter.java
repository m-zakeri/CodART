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

package fi.vtt.noen.testgen.observations.formatter;

import fi.vtt.noen.testgen.observations.data.*;
import fi.vtt.noen.testgen.model.Const;
import fi.vtt.noen.testgen.Main;
import fi.vtt.noen.testgen.parser.InterfaceParser;

import java.util.Iterator;
import java.util.Set;
import java.util.HashSet;
import java.util.Collection;
import java.util.Properties;
import java.util.ArrayList;
import java.io.IOException;
import java.io.OutputStream;
import java.io.FileInputStream;

/**
 * Produces a log file in Daikon format. Uses as input the events and attributes captured from
 * monitoring program execution.
 *
 * @author Teemu Kanstrén
 */
public class DaikonFormatter extends BasicFormatter {
  private Set<String> declarations = new HashSet<String>();
  private boolean simple = false;
  private final Collection<String> inputs;
  //private final Collection<Class> inputs;
  //private final Collection<Class> outputs;

  public DaikonFormatter(String fileName, boolean simple) throws IOException {
    super(fileName);
    this.simple = simple;
    if (simple) {
      inputs = null;
      return;
    }
    try {
      inputs = InterfaceParser.methodNames(inputs());
      System.out.println("inputs:"+inputs);
    } catch (Exception e) {
      e.printStackTrace();
      throw new RuntimeException("failed to load input and output interface definitions for daikon formatter", e);
    }
  }

  public DaikonFormatter(String fileName, Collection<String> inputs) throws IOException {
    super(fileName);
    this.inputs = inputs;
    System.out.println("inputs:"+inputs);
  }

  private static Class classForProperty(String property) throws Exception {
    Properties configuration = new Properties();
    configuration.load(new FileInputStream("testgen.properties"));
    String className = configuration.getProperty(property);
    if (className == null) {
      return null;
    }
    System.out.println("creating class for:"+className);
    return Class.forName(className);
  }

  private static Collection<Class> classesForMultipleProperties(String prefix) throws Exception {
    Collection<Class> classes = new ArrayList<Class>();
    int index = 1;
    while (true) {
      Class clazz = classForProperty(prefix + index);
      index++;
      if (clazz == null) {
        break;
      }
      classes.add(clazz);
    }
    return classes;
  }

  public static Collection<Class> inputs() throws Exception {
    return classesForMultipleProperties("InputInterface");
  }

  public static Collection<Class> outputs() throws Exception {
    return classesForMultipleProperties("OutputInterface");
  }

  public String header() {
    OutputBuffer out = new OutputBuffer();
    out.append("decl-version 2.0");
    out.append("var-comparability implicit");
    return out.toString();
  }

  public String footer() {
    return "";
  }

  public String fileNameExtension() {
    return "dtrace";
  }

  public String observations(ProgramRun run) {
    OutputBuffer out = new OutputBuffer();
    Event previousEvent = null;
    Event event = Const.INITIAL_STATE;

    for (Iterator<Event> ei = run.iterator(); ei.hasNext();) {
      previousEvent = event;
      event = ei.next();
      if (simple) {
        simplePoint(event, "10", out);
        continue;
      }
      if ((inputs.contains(previousEvent.getName()) && inputs.contains(event.getName()))
          || (!previousEvent.isExit() && event.isExit() && (previousEvent.getName()+"_EXIT").equals(event.getName()))) {
        point(previousEvent.getName(), previousEvent, "11", out);
      }
      if (previousEvent.isExit()) {
        //this is needed for return value assertion
        point(previousEvent.getName(), previousEvent, "22", out);
      } else {
        //this is needed for transition conditions
        if (inputs.contains(previousEvent.getName()) && !inputs.contains(event.getName())
            && !previousEvent.isExit() && !event.isExit()) {
          String name = previousEvent.getName()+","+event.getName();
          point(name, previousEvent, "22", out);
        }
      }
//      if (inputs.contains(event.getName())) {
//        point(event.getName(), event, "11", out);
//      }
    }
//    System.out.println("last event:"+event.getName());
    //this is here since up above only previous events are logged, this can lead to losing the last event
    if (!simple) {
      if (inputs.contains(event.getName()) || event.isExit()) {
        point(event.getName(), event, "11", out);
      }
    }
    return out.toString();
  }

  private void simplePoint(Event event, String comparability, OutputBuffer out) {
    String name = event.getName();
    name = name.replace(' ', '_');
    if (!event.isExit()) {
      name += ":::ENTER";
    } else {
      //for some reason daikon seems to insist on having the line numbers here.. otherwise you get a complaint about combined points?
      name += ":::EXIT1";
    }
    declarations(event, name, out, comparability);
    out.append("");
    out.append(name);
    attributes(event, out);
  }

  private void point(String name, Event event, String comparability, OutputBuffer out) {
    name = name.replace(' ', '_');
    name += ":::ENTER";
    declarations(event, name, out, comparability);
    out.append("");
    out.append(name);
    attributes(event, out);
  }

  private void declarations(Event event, String eventName, OutputBuffer out, String comparability) {
    if (declarations.contains(eventName)) {
      return;
    }
    declarations.add(eventName);
    out.append("");
    out.append("ppt "+eventName);
    if (event.isExit()) {
      out.append("ppt-type exit");
    } else {
      out.append("ppt-type enter");
    }
    for (Iterator<EventAttribute> ai = event.attributes(); ai.hasNext();) {
      EventAttribute attribute = ai.next();
      if (attribute instanceof ArrayAttribute) {
        out.append("  variable "+attribute.getName()+"[]");
        out.append("    var-kind array");
      } else {
        out.append("  variable "+attribute.getName());
        out.append("    var-kind variable");
      }
      out.append("    dec-type "+attribute.getType());
      out.append("    rep-type "+attribute.getType());
      out.append("    comparability "+comparability);
    }
  }

  private void attributes(Event event, OutputBuffer out) {
    for (Iterator<EventAttribute> ai = event.attributes(); ai.hasNext();) {
      EventAttribute attribute = ai.next();
      if (attribute instanceof ArrayAttribute) {
        out.append(attribute.getName()+"[]");
      } else {
        out.append(attribute.getName());
      }
      if (attribute.getType().equals(EventAttribute.TYPE_STRING)) {
        //daikon log requires surrounding string values with double quotes
        out.append('"'+attribute.getValue()+'"');
      } else {
        out.append(attribute.getValue());
      }
      out.append("1");
    }
  }
}
