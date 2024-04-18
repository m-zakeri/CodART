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

package fi.vtt.noen.testgen.model.efsm;

import java.lang.reflect.Method;
import java.lang.reflect.Field;
import java.util.Collection;
import java.util.ArrayList;
import java.util.Iterator;

/**
 * DEPRECATED: Uses MockGenerator now. Generates stub classes for given interface definitions.
 *
 * @author Teemu Kanstrén
 */
public class StubGenerator {
  private String ln = "\n";

  public String stubFor(Class myInterface, String packageName, String className) {
    return header(packageName, className)+variables()+methods(myInterface)+footer();
  }

  public String header(String packageName, String className) {
    return
        "package "+packageName+";"+ln+ln+
        "import java.util.Map;"+ln+
        "import java.util.HashMap;"+ln+ln+
        "public class "+className+" {"+ln;

  }

  public String variables() {
    String result =
        "  private Map<String, Integer> messages = new HashMap<String, Integer>();"+ln+ln+
        "  public void reset() {"+ln+
        "    messages.clear();"+ln+
        "  }"+ln+ln+
        "  private void msgReceived(String msg) {"+ln+
        "    Integer count = messages.get(msg);"+ln+
        "    if (count == null) {"+ln+
        "      count = 0;"+ln+
        "    }"+ln+
        "    count++;"+ln+
        "    messages.put(msg, count);"+ln+
        "  }"+ln+ln+
        "  public int countFor(String msg) {"+ln+
        "    return messages.get(msg);"+ln+
        "  }"+ln;
    return result;
  }

  public String methods(Class myInterface) {
    Method[] methods = myInterface.getMethods();
    String stub = "";
    for (int i = 0; i < methods.length; i++) {
      Method method = methods[i];
      stub += stubFor(method);
    }
    return stub;
  }

  public String stubFor(Method method) {
    String stub = methodNameFor(method);
    stub = methodContentsFor(method, stub);
    return stub;
  }

  private String methodContentsFor(Method method, String stub) {
    stub += " {"+ln;
    Class returnType = method.getReturnType();
    String name = method.getName();
    stub += "    msgReceived(\""+name+"\");"+ln;
    if (!returnType.equals(void.class)) {
      stub += "    return null;"+ln;
    }
    stub += "  }"+ln;
    return stub;
  }

  private String methodNameFor(Method method) {
    String fullName = method.toString();
    String[] parts = fullName.split(" ");
    //interface methods are always shown as "abstract" so remove that (parts[1])
    String methodName = "  "+parts[0]+" "+parts[2]+" "+method.getName();
    //Method.toString also returns fully qualified class names etc so remove those
    parts = fullName.split(method.getName()+"\\(");
    //parts[1] will now contain the parameters and throws statements
    String params = "("+parts[1];
    String stub = methodName+params;
    stub = addParameterNames(method, stub);
    return stub;
  }

  private String addParameterNames(Method method, String stub) {
    if (method.getParameterTypes().length == 0) {
      //it has no parameters
      return stub;
    }
    String[] parts = stub.split(" throws ");
    String exceptions = "";
    if (parts.length > 1) {
      exceptions = " throws "+parts[1];
      stub = parts[0];
    }
    //remove trailing ")" for parameter parsing
    stub = stub.substring(0, stub.length()-1);
    parts = stub.split(",");
    stub = parts[0]+" p1";
    for (int i = 1; i < parts.length; i++) {
      String type = parts[i];
      String name = " p"+(i+1);
      stub += ", "+type+name;
    }
    //put the ")" back there
    return stub+")"+exceptions;
  }

  public String footer() {
    return "}"+ln;
  }
}
