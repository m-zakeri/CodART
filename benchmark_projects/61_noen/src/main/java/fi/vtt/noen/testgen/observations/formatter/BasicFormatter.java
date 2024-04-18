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

import fi.vtt.noen.testgen.observations.data.ProgramRun;

import java.io.OutputStream;
import java.io.FileOutputStream;
import java.io.IOException;

/**
 * Formatters are objects that turn captured events and attributes into log file of a
 * chosen format. This is the base class for these formatters.
 *
 * @author Teemu Kanstrén
 */
public abstract class BasicFormatter {
  protected final OutputStream out;
  protected final boolean testMode;
  private final String fileName;

  protected BasicFormatter(OutputStream out)  {
    this.out = out;
    this.fileName = "UNKNOWN-USING GIVEN STREAM";
    this.testMode = true;
  }

  protected BasicFormatter(String fileName) throws IOException {
    this.out = new FileOutputStream(fileName+"."+fileNameExtension());
    this.fileName = fileName;
    this.testMode = false;
  }

  public abstract String header();
  public abstract String footer();
  public abstract String observations(ProgramRun test);
  public abstract String fileNameExtension();

  protected class OutputBuffer {
    //private final StringBuffer buf = new StringBuffer();
//    private final String ln = "\n";
    private final byte[] lnb = "\n".getBytes();

    public void append(String text) {
      try {
        out.write(text.getBytes());
        out.write(lnb);
      } catch (IOException e) {
        e.printStackTrace();
        throw new RuntimeException("Error while writing to file named '"+fileName+"'):"+e.getMessage(), e);
      }
    }

   // public String toString() {
   //   return buf.toString();
   // }
  }
}
