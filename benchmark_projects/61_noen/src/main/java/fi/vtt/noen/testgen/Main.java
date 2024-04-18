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

import static fi.vtt.noen.testgen.StringUtils.*;

import fi.vtt.noen.testgen.model.daikon.DaikonModel;
import fi.vtt.noen.testgen.model.fsm.FSMModel;
import fi.vtt.noen.testgen.model.efsm.EFSMGenerator;
import fi.vtt.noen.testgen.parser.PromParser;
import fi.vtt.noen.testgen.parser.DaikonParser;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.File;
import java.io.FileWriter;
import java.util.Properties;
import java.util.Collection;
import java.util.ArrayList;

/**
 * The starting point of the model generation. Run both Daikon and ProM in the background,
 * processes the results and generates the EFSM code as a result.
 *
 * @author Teemu Kanstrén
 */
public class Main {
  private static String logName = null;
  private static String efsmPackageName = null;
  private static String efsmClassName = null;
  private static PromParser promParser = new PromParser();
  private static Properties configuration = null;

  public static void main(String[] args) throws Exception {
    logName = args[0];
    efsmPackageName = args[1];
    efsmClassName = args[2];

    DaikonModel dm = createDaikonModel();
    System.out.println("Daikon model created.");
    FSMModel fsm = createFSM();
    System.out.println("FSM (PROM) model created.");
    generateEFSM(dm, fsm);
    System.out.println("EFSM created and saved to "+efsmClassName);

//    DaikonModel dmOk = createDaikonModel("ok");
//    FSMModel fsmOk = createFSM("ok");
//    generateEFSM("ok", dmOk, fsmOk);

//    DaikonModel dmError = createDaikonModel("error");
//    FSMModel fsmError = createFSM("error");
//    generateEFSM("error", dmError, fsmError);
  }

  private static void saveToFile(String fileName, String content) throws Exception {
    fileName += ".java";
    File outFile = new File(fileName);
    FileWriter out = new FileWriter(outFile);
    out.write(content);
    out.close();
  }

  public static DaikonModel createDaikonModel() throws Exception {
    String fileName = logName+".dtrace";
    System.out.println("Running daikon for file:"+fileName);
    //comment this line out and the next in to run with pre-processed daikon output 
    String daikonOutput = executeDaikon(fileName);
//    String daikonOutput = fakeDaikon("daikon-test-output.txt");
    System.out.println("Daikon run ended, parsin Daikon model");
//    System.out.println("daikon output:"+daikonOutput);
    DaikonParser parser = new DaikonParser(daikonOutput);
    return parser.parseAll();
  }

  public static FSMModel createFSM() throws Exception {
    String fileName = logName+".mxml";
    System.out.println("Running PROM parser for file:"+fileName);
    InputStream in = new FileInputStream(fileName);
    return promParser.parse(in);
  }

  public static String fakeDaikon(String fileName) throws Exception {
    FileInputStream fin = new FileInputStream(fileName);
    return StringUtils.stringForStream(fin);
  }

  public static String executeDaikon(String fileName) throws Exception {
    Runtime rt = Runtime.getRuntime();
    Process p = rt.exec("java -Xmx512m daikon.Daikon --nohierarchy "+fileName);
    InputStream output = p.getInputStream();
    return stringForStream(output);
  }

  private static void generateEFSM(DaikonModel dm, FSMModel fsm) throws Exception {
    EFSMGenerator generator = new EFSMGenerator(classUnderTest(), fsm, dm, inputs(), outputs());
    System.out.println("Generating EFSM");
    String efsm = generator.generateEFSM(efsmPackageName, efsmClassName);
    saveToFile(efsmClassName, efsm);
  }

  private static Class classUnderTest() throws Exception {
    return classForProperty("ClassUnderTest");
  }

  private static Class classForProperty(String property) throws Exception {
    if (configuration == null) {
      configuration = new Properties();
      configuration.load(new FileInputStream("testgen.properties"));
    }
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
}
