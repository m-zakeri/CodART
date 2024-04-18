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

package fi.vtt.noen.testgen;

import java.io.InputStream;
import java.io.IOException;
import java.io.ByteArrayOutputStream;

/**
 * Some utilities for handling of strings.
 *
 * @author Teemu Kanstrén
 */
public class StringUtils {
  public static final String ln = "\n";

  public static String prefixWith(String content, String prefix) {
    String[] lines = content.split(ln);
    String result = "";
    for (String line : lines ) {
      result += prefix+line+ln;
    }
    return result;
  }

  /**
   * Capitalizes the first letter of given string.
   *
   * @param text The text to capitalize.
   * @return Same stuff as given in input, but with first letter in uppercase.
   */
  public static String capitalizeFirstLetter(String text) {
    String temp = text.substring(0, 1).toUpperCase();
    text = temp+text.substring(1);
    return text;
  }

  /**
   * Lowercases the first letter of given string.
   *
   * @param text The text to lowercase.
   * @return Same stuff as given in input, but with first letter in lowercase.
   */
  public static String lowerCaseFirstLetter(String text) {
    String temp = text.substring(0, 1).toLowerCase();
    text = temp+text.substring(1);
    return text;
  }

  public static String stringForStream(InputStream in) throws IOException {
    ByteArrayOutputStream out = new ByteArrayOutputStream();
    byte[] bytes = new byte[512];

    int readBytes;
    while ((readBytes = in.read(bytes)) > 0) {
      out.write(bytes, 0, readBytes);
    }
    return new String(out.toByteArray());
  }
}
