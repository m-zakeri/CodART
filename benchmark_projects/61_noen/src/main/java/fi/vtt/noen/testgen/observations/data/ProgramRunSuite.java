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

import fi.vtt.noen.testgen.observations.formatter.PromFormatter;
import fi.vtt.noen.testgen.observations.formatter.BasicFormatter;
import fi.vtt.noen.testgen.observations.formatter.DaikonFormatter;
import fi.vtt.noen.testgen.observations.formatter.NoenFormatter;

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;
import java.io.IOException;

/**
 * Groups together a group of program executions to form a data set for model generation.
 *
 * @author Teemu Kanstrén
 */
public class ProgramRunSuite {
  //for now only support direct write to disk since some of the runs can take huge memory
//  private final List<ProgramRun> tests = new ArrayList<ProgramRun>();
  private final List<BasicFormatter> formatters;
  private ProgramRun previousTest = null;
  private boolean writeImmediately = true;
  private boolean closed = false;

  public ProgramRunSuite(List<BasicFormatter> formatters) {
    this.formatters = formatters;
  }

  public ProgramRunSuite(String fileName, boolean simple) {
    try {
      formatters = new ArrayList<BasicFormatter>();
      formatters.add(new PromFormatter(fileName));
      formatters.add(new DaikonFormatter(fileName, simple));
    } catch (IOException e) {
      throw new RuntimeException("Failed to create formatters for filename:"+fileName, e);
    }
  }

  public void addTest(ProgramRun test) {
    if (writeImmediately == true) {
      fillHeader();
      writePreviousProgramRunToFile();
      previousTest = test;
//    } else {
//      tests.add(test);
    }
  }

//  public Iterator<ProgramRun> iterator() {
//    return tests.iterator();
//  }

  public void close() {
    if (closed) {
      return;
    }
    writePreviousProgramRunToFile();
    writeFooter();
    closed = true;
  }

  private void output(ProgramRun run) {
    for (BasicFormatter formatter : formatters) {
      formatter.observations(run);
    }
  }

  private void writePreviousProgramRunToFile() {
    if (previousTest != null) {
      output(previousTest);
    }
  }

  private void fillHeader() {
    if (previousTest != null) {
      return;
    }
    for (BasicFormatter formatter : formatters) {
      formatter.header();
    }
  }

  private void writeFooter() {
    if (previousTest != null) {
      for (BasicFormatter formatter : formatters) {
        formatter.footer();
      }
    }
  }
}

