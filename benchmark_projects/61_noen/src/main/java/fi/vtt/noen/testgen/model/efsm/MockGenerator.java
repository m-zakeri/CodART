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

/**
 * Generates source code related to creating mock objects, setting their expectations, and verifying
 * their correctness, etc.
 *
 * @author Teemu Kanstrén
 */
public class MockGenerator {
  //used as line separator all around, should be moved to common class
  private static final String ln = "\n";
  private final String className;


  public MockGenerator(Class clazz) {
    this.className = clazz.getSimpleName();
  }

  public static String mockNameFor(String className) {
    return "mock"+className;
  }

  public static String mockInit(String className) {
    return mockNameFor(className)+" = createMock("+className+".class);"+ln;
  }

  public String replay() {
    return "replay(mock"+className+");"+ln;
  }

  public String verify() {
    return "verify(mock"+className+");"+ln+"EasyMock.reset(mock"+className+");"+ln;
  }

  /**
   *
   * @param methodToCall
   * @return
   */
  public String callFor(Method methodToCall, String returnValue) {
    String methodName = methodToCall.getName();
    Class[] parameterTypes = methodToCall.getParameterTypes();
    String parameters = "";
    for (int i = 0; i < parameterTypes.length; i++) {
      Class type = parameterTypes[i];
      if (type.equals(boolean.class)) {
        parameters += "false";
      } else if (type.isPrimitive()) {
        parameters += 0;
      } else {
        parameters += "("+type.getSimpleName()+")anyObject()";
      }
      if (i < parameterTypes.length-1) {
        parameters += ", ";
      }
    }
    String mockCall = "mock"+className+"."+methodName+"("+parameters+")";
    if (returnValue != null) {
      mockCall = "expect("+mockCall+").andReturn("+returnValue+")";
    }
    mockCall += ";"+ln;
    return mockCall;
  }
}
