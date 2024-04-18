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

package fi.vtt.noen.testgen.parser;

import fi.vtt.noen.testgen.model.daikon.*;
import fi.vtt.noen.testgen.model.daikon.constraints.*;

import java.util.*;

/**
 * A parser for Daikon log files. Reads the Daikon log file and parses it into blocks, where each
 * block represents a monitored point of execution. Each block is taken to describe a state in the
 * generated state-machine. The invariants for this block are then turned into
 * invariant constraint objects describing when these states can be entered. Block sequences are also
 * considered, and considered to describe transition constraints between two blocks where one
 * follows another. These are then turned into transition invariant constraints for when this
 * transition can occur. 
 *
 * @author Teemu Kanstrén
 */
public class DaikonParser {
  private static final String EOF = "Exiting Daikon.";
//  private static final String ln = System.getProperty("line.separator");
  private String itemSeparator;
  private final String text;
  private int index = 0;

  public DaikonParser(String text) {
    this.text = text;
    trySeparator("\r\n");
    trySeparator("\n");
    trySeparator("\r");
    index = text.indexOf(itemSeparator)+itemSeparator.length();
  }

  private void trySeparator(String lineChange) {
    if (itemSeparator != null) {
      //already found and set
      return;
    }
    String test = "==========================================================================="+lineChange;
    if (text.indexOf(test) > 0) {
      itemSeparator = test;
    }
  }

  public DaikonModel parseAll() {
    String block = nextBlock();
    DaikonModel model = new DaikonModel();
    while (block != null) {
//      System.out.println("block:"+block);
      Collection<String> items = items(block);
      Iterator<String> i = items.iterator();
      String name = parseEventName(i.next());
      DaikonModelElement me = DaikonModelElement.create(name);
      model.add(me);
      while (i.hasNext()) {
        DaikonConstraint daikonConstraint = constraint(i.next());
        if (daikonConstraint != null && daikonConstraint.isEnabled()) {
          //some logs had empty lines which now give null, so add this paranoia..
          me.addConstraint(daikonConstraint);
        }
      }
      block = nextBlock();
    }
    return model;
  }

  public String nextBlock() {
    int endIndex = text.indexOf(itemSeparator, index);
    if (endIndex < 0) {
      endIndex = text.indexOf(EOF, index);
    }
    if (endIndex < 0) {
      return null;
    }
    String result = text.substring(index, endIndex);
    index = endIndex+itemSeparator.length();
    return result;
  }

  public static Collection<String> items(String block) {
    Collection<String> items = new ArrayList<String>();
    int index = 0;
    int endIndex = block.indexOf("\n");
    while (endIndex > 0) {
      String item = block.substring(index, endIndex);
      items.add(item);
      index = endIndex+1;
      endIndex = block.indexOf("\n", index);
    }
    return items;
  }

  public static DaikonConstraint constraint(String item) {
//    System.out.println("item:"+item);
    if (item.trim().length() == 0) {
      //some daikon logs had empty lines so we do this now..
      return null;
    }
    if (item.split("%").length > 1) {
      //some things just are not to be supported..
      return null;
    }
    String[] parts = item.split(" >= ");
    if (parts.length == 2) {
      return new GreaterOrEqualConstraint(parts[0], parts[1]);
    }
    parts = item.split(" > ");
    if (parts.length == 2) {
      return new GreaterConstraint(parts[0], parts[1]);
    }
    parts = item.split(" <= ");
    if (parts.length == 2) {
      return new LesserOrEqualConstraint(parts[0], parts[1]);
    }
    parts = item.split(" < ");
    if (parts.length == 2) {
      return new LesserConstraint(parts[0], parts[1]);
    }
    if (item.startsWith("size(")) {
      parts = item.split(" == ");
      if (parts.length == 2) {
        return new ConstantSizeConstraint(parts[0], parts[1]);
      }
      parts = item.split(" != ");
      if (parts.length == 2) {
        return new NonEqualConstraint(parts[0], parts[1]);
      }
      parts = item.split(" one of \\{");
      return new ConstantSizeConstraint(parts[0], parts[1]);
    }
    parts = item.split("\\[\\] == \\[");
    if (parts.length == 2) {
      return new ArrayContentsConstraint(parts[0]+"[]", parts[1]);
    }
    parts = item.split("\\[\\] elements == ");
    if (parts.length == 2) {
      return new ArrayElementsConstraint(parts[0]+"[]", parts[1]);
    }
    parts = item.split(" == size\\(");
    if (parts.length == 2) {
      return new SizeOfConstraint(parts[0], parts[1]);
    }
    parts = item.split(" == ");
    if (parts.length == 2) {
      return new EqualsConstraint(parts[0], parts[1]);
    }
    parts = item.split(" != ");
    if (parts.length == 2) {
      return new NonEqualConstraint(parts[0], parts[1]);
    }
    // { is a special char in java regep so we must escape it \\{ or we get regexp error
    parts = item.split(" one of \\{");
    if (parts.length == 2) {
      return new OneOfConstraint(parts[0], parts[1]);
    }
    parts = item.split(" in ");
    if (parts.length == 2) {
      return new AlwaysInArrayConstraint(parts[0], parts[1]);
    }
    throw new IllegalArgumentException("Unsupported contraint:"+item);
  }

  public static Object parseValueObject(String obj) {
    //remove any whitespace, line endings etc that will cause failure of startwith and endswith
    obj = obj.trim();
    if (obj.startsWith("[") && obj.endsWith("]")) {
      return parseStringList(obj);
    }
    boolean array = false;
    if (obj.endsWith("[]")) {
      array = true;
      obj = obj.substring(0, obj.length()-2);
    }
    if (obj.length() == 0) {
      throw new IllegalArgumentException("Cannot parseLexical value from empty string");
    }
    if (obj.startsWith("\"") && obj.endsWith("\"")) {
      //in this case it is of form "value" and is a STRING so we remove the surrounding ""
      String value = obj.substring(1, obj.length()-1);
      return value;
    }
    if (obj.equals("true") || obj.equals("false")) {
      //in this case we have a BOOLEAN variable
      boolean value = Boolean.parseBoolean(obj);
      return value;
    }
    try {
      //we try to parseLexical it as a NUMBER, if we succeed we are happy
      double value = Double.parseDouble(obj);
      return value;
    } catch (NumberFormatException e) {
      //if we come here, it was not a number and we ignore this exception
    }
    if (obj.indexOf("?") == -1) {
      //parameter index with ? separator is needed for reference objects, otherwise we consider it a string
      //this can happen for array content values
      return obj;
    }
//    System.out.println("creating reference object for:"+obj);
    //the only possibility left is that it is a REFERENCE TO ANOTHER VARIABLE
    //meaning it has a certain relation with the other variable, such as they are always equal
    return new ReferenceValue(obj, array);
  }

  public static Collection<String> parseStringList(String obj) {
    Collection<String> result = new ArrayList<String>();
    //trim [ from start and ] from end
    obj = obj.substring(1, obj.length()-1);
    String[] values = obj.split(", ");
    if (values[0].length() == 0) {
      //skip empty arrays
      return Collections.EMPTY_LIST;
    }
    result.addAll(Arrays.asList(values));
    return result;
  }

  public static Collection parseObjectList(String value) {
    if (value.length() == 0) {
      return Collections.EMPTY_LIST;
    }
    Collection contents = new ArrayList();
    String[] valueArray = value.split(",");
    for (String s : valueArray) {
      Object obj = DaikonParser.parseValueObject(s);
      contents.add(obj);
    }
    return contents;
  }

  public static String parseEventName(String text) {
    String[] parts = text.split(":::");
    return parts[0];
  }
}
