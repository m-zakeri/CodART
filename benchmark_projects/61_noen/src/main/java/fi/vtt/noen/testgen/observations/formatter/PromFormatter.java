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

import fi.vtt.noen.testgen.observations.data.Event;
import fi.vtt.noen.testgen.observations.data.EventAttribute;
import fi.vtt.noen.testgen.observations.data.ProgramRun;

import java.util.Iterator;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Calendar;
import java.io.IOException;
import java.io.OutputStream;

/**
 * Produces a log file in ProM format. Uses as input the events and attributes captured from
 * monitoring program execution.
 *
 * @author Teemu Kanstrén
 */
public class PromFormatter extends BasicFormatter {
  private static int processId = 0;

  public PromFormatter(OutputStream out) {
    super(out);
  }

  public PromFormatter(String fileName) throws IOException {
    super(fileName);
  }

  public String fileNameExtension() {
    return "mxml";
  }

  public String header() {
    OutputBuffer buf = new OutputBuffer();
    buf.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
    buf.append("<WorkflowLog xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" " +
        "xsi:noNamespaceSchemaLocation=\"WorkflowLog.xsd\" description=\"Test data\">");
    buf.append("<Source program=\"Test suite for blaablaa\"/>");
    buf.append("<Process id=\"0\" description=\"test suite name\">");
    return buf.toString();
  }

  public String observations(ProgramRun test) {
    OutputBuffer buf = new OutputBuffer();
    buf.append("<ProcessInstance id=\""+processId+"\" description=\""+test.getName()+"\">");
    processId++;
    for (Iterator<Event> ei = test.iterator(); ei.hasNext();) {
      Event event = ei.next();
      buf.append("<AuditTrailEntry>");
      buf.append("<WorkflowModelElement>"+event.getName()+"</WorkflowModelElement>");
      if (event.isExit()) {
        buf.append("<EventType>complete</EventType>");
      } else {
        buf.append("<EventType>start</EventType>");
      }
//      if (false) { //this is used to disable attributes as PROM hangs on big log files and attributes are not used in PROM right now
      if (event.attributes().hasNext()) {
        buf.append("<Data>");
        for (Iterator<EventAttribute> ai = event.attributes(); ai.hasNext();) {
          EventAttribute attribute = ai.next();
          buf.append("<Attribute name=\""+attribute.getName()+"\">"+attribute.getValue()+"</Attribute>");
        }
        buf.append("</Data>");
      }
      //XPROM modification
      buf.append("<Timestamp>"+formatTime(event)+"</Timestamp>");

//      buf.append("<Timestamp>2008-01-02T12:23:00.000</Timestamp>");
      buf.append("</AuditTrailEntry>");
    }
    buf.append("</ProcessInstance>");
    return buf.toString();
  }

  private String formatTime(Event event) {
    Date time = event.getTime();
    if (testMode) {
      time = new Date(0);
    }
    GregorianCalendar calendar = new GregorianCalendar();
    calendar.setTime(time);
    String format = ""+calendar.get(Calendar.YEAR);
    format += "-"+doubleDigit(calendar.get(Calendar.MONTH)+1);
    format += "-"+doubleDigit(calendar.get(Calendar.DAY_OF_MONTH));
    format += "T"+calendar.get(Calendar.HOUR_OF_DAY);
    format += ":"+calendar.get(Calendar.MINUTE);
    format += ":"+calendar.get(Calendar.SECOND);
    format += "."+calendar.get(Calendar.MILLISECOND);
    return format;
  }

  private String doubleDigit(int digit) {
    String str = ""+digit;
    if (str.length() == 1) {
      str = "0"+str;
    }
    return str;
  }

  public String footer() {
    OutputBuffer buf = new OutputBuffer();
    buf.append("</Process>");
    buf.append("</WorkflowLog>");
    return buf.toString();
  }
/*
  public String format(ProgramRunSuite suite) {
    String result = header();
    for (Iterator<ProgramRun> i = suite.iterator(); i.hasNext();) {
      ProgramRun test = i.next();
      result += observations(test);
    }
    result += footer();
    return result;
  }
*/
  public static void reset() {
    processId = 0;
  }
}
