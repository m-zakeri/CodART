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

import java.util.Collection;

/**
 * An event attribute is the value of a variable at the time of the event. This is the base class for
 * this type of value objects. These are used in invariant inference.
 *
 * @author Teemu Kanstrén
 */
public class EventAttribute {
  protected String name;
  protected String type;
  protected String value;

  public static final String TYPE_STRING = "java.lang.String";

  public EventAttribute() {
  }

  public EventAttribute(String name, Object obj) {
    init(name, obj);
  }

  private void init(String name, Object obj) {
    this.name = name;
    this.value = ""+obj;
    if (obj instanceof Integer) {
      this.type = "int";
      return;
    }
    if (obj instanceof Double) {
      this.type = "double";
      return;
    }
    if (obj instanceof Boolean) {
      this.type = "boolean";
      boolean value = (Boolean) obj;
      if (value) {
        this.value = "1";
      } else {
        this.value = "0";
      }
      return;
    }
    if (obj instanceof Collection) {
      throw new IllegalArgumentException("Collections need to be created with ArrayAttribute");
    }
    this.type = "java.lang.String";
  }


  public String getName() {
    return name;
  }

  public String getValue() {
    return value;
  }

  public String getType() {
    return type;
  }
}
