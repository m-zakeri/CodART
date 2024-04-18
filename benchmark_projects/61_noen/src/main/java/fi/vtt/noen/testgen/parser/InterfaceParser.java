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

import java.util.Collection;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.lang.reflect.Method;

/**
 * Parses method names from an interface to be used to identify which methods
 * are part of input and which are part of output.
 *
 * @author Teemu Kanstrén
 */
public class InterfaceParser {
  public static Collection<String> methodNames(Class clazz) {
    Collection<String> names = new ArrayList<String>();
    Method[] methods = clazz.getMethods();
    for (int i = 0; i < methods.length; i++) {
      Method method = methods[i];
      names.add(method.getName());
    }
    return names;
  }

  public static Collection<String> methodNames(Collection<Class> interfaces) {
    Collection<String> methods = new HashSet<String>();
    for (Iterator<Class> i = interfaces.iterator(); i.hasNext();) {
      Class clazz = i.next();
      methods.addAll(methodNames(clazz));
    }
    return methods;
  }
}
