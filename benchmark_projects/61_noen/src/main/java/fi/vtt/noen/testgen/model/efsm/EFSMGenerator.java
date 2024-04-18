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

import static fi.vtt.noen.testgen.model.efsm.MockGenerator.mockNameFor;
import static fi.vtt.noen.testgen.model.efsm.MockGenerator.mockInit;
import static fi.vtt.noen.testgen.StringUtils.*;

import fi.vtt.noen.testgen.model.fsm.FSMModel;
import fi.vtt.noen.testgen.model.fsm.FSMState;
import fi.vtt.noen.testgen.model.daikon.DaikonState;
import fi.vtt.noen.testgen.model.daikon.DaikonModel;
import fi.vtt.noen.testgen.model.daikon.DaikonTransition;
import fi.vtt.noen.testgen.model.daikon.constraints.DaikonConstraint;
import fi.vtt.noen.testgen.parser.DaikonParser;
import fi.vtt.noen.testgen.parser.PromParser;
import fi.vtt.noen.testgen.parser.InterfaceParser;
import fi.vtt.noen.testgen.StringUtils;

import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.util.*;
import java.lang.reflect.Method;

/**
 * Parses together the PROM model as well as the Daikon model to create EFSM.
 *
 * @author Teemu Kanstrén
 */
public class EFSMGenerator {
  //used as line separator all around, should be moved to common class
  private final String ln = "\n";
  //this is the PROM model, describing states and transitions
  private final FSMModel fsm;
  //describes the invariants over the transitions.
  private final DaikonModel dm;
  //names of array variables in the model, used in code generation
  private final Collection<String> arrayNames = new HashSet<String>();
  //names of all input interface(s) methods
  private final Collection<String> inputs = new ArrayList<String>();
//  private final Collection<String> outputs = new ArrayList<String>();
  //classes to import for the model, used for code generation
  private final Collection<Class> imports = new TreeSet<Class>(new ImportClassComparator());
  //classes for which mock objects have been made
  private final Collection<Class> mocks = new HashSet<Class>();
  //map of methods and return values to create parameters for method calls into SUT. key = method name, value = return type
  private final Map<String, Class> valueMethods = new TreeMap<String, Class>();
  //list of output interfaces
  private Collection<Class> outputInterfaces = null;
  //the object that is the target of testing (SUT)
  private final Class objectUnderTest;
  //index for generated return value object names (rv1, rv2, rv3, ...)
  private int rvIndex = 1;

  /**
   * Only for testing.
   *
   * @param objectUnderTest
   * @param fsm
   * @param dm
   */
  public EFSMGenerator(Class objectUnderTest, FSMModel fsm, DaikonModel dm) {
    this.fsm = fsm;
    this.dm = dm;
    this.objectUnderTest = objectUnderTest;
    imports.add(objectUnderTest);
  }

  /**
   * Only for testing.
   *
   * @param objectUnderTest
   * @param fsm
   * @param dm
   * @param inputInterfaces
   * @param outputInterfaces
   */
  public EFSMGenerator(Class objectUnderTest, FSMModel fsm, DaikonModel dm, Collection<Class> inputInterfaces, Collection<Class> outputInterfaces) {
    this.fsm = fsm;
    this.dm = dm;
    this.objectUnderTest = objectUnderTest;
    imports.add(objectUnderTest);
    parseInterfaces(inputInterfaces, outputInterfaces);
  }

  /**
   *
   * @param objectUnderTest
   * @param daikonOutput
   * @param promOutput
   * @param inputInterfaces
   * @param outputInterfaces
   */
  public EFSMGenerator(Class objectUnderTest, String daikonOutput, String promOutput, Collection<Class> inputInterfaces, Collection<Class> outputInterfaces) {
    DaikonParser daikon = new DaikonParser(daikonOutput);
    InputStream in = new ByteArrayInputStream(promOutput.getBytes());
    PromParser prom = new PromParser();
    FSMModel fsm = prom.parse(in);
    DaikonModel dm = daikon.parseAll();
    //since we only deal with the method names, we parseLexical those from input/output interfaces to match against fsm states.
    //method name should equal stateid in fsm/daikon. later these are used differentiate states as output or input
    this.fsm = fsm;
    this.dm = dm;
    this.objectUnderTest = objectUnderTest;
    imports.add(objectUnderTest);
    parseInterfaces(inputInterfaces, outputInterfaces);
  }

  //
  private void parseInterfaces(Collection<Class> inputInterfaces, Collection<Class> outputInterfaces) {
    this.outputInterfaces = outputInterfaces;
    Collection<String> inputs = InterfaceParser.methodNames(inputInterfaces);
    this.inputs.addAll(inputs);
    mocks.addAll(outputInterfaces);
//    Collection<String> outputs = InterfaceParser.methodNames(outputInterfaces);
//    this.outputs.addAll(outputs);
    imports.addAll(inputInterfaces);
    imports.addAll(outputInterfaces);
  }

  /**
   * Generates the actual EFSM
   *
   * @return EFSM as Java code for ModelJUnit.
   */
  public String generateEFSM(String packageName, String className) {
    Map<String, FSMState> fsmStates = fsm.getStates();
    StringBuffer body = new StringBuffer();
    for (String stateId : fsmStates.keySet()) {
      if (inputs.contains(stateId)) {
        body.append(ln);
        body.append(actionFor(stateId));
        body.append(ln);
        body.append(guardFor(stateId));
      }
//      body.append(ln);
      body.append(transitionActionsFor(stateId));
    }
    body.append(ln);
    body.append(valueMethods());

    StringBuffer efsm = new StringBuffer();
    efsm.append(header(packageName, className));
    efsm.append(variables());
    efsm.append(testMethod(className));
    efsm.append(resetMethod(arrayNames, mocks));
    //efsm.append(constructor(className));
    efsm.append(stateMethod());
    efsm.append(body);
    efsm.append(helperMethods());
    efsm.append(guardCheckMethods());
    efsm.append(footer());
    return efsm.toString();
  }

  /**
   *
   * @return
   */
  public String variables() {
    String variables = arrays();
    variables += "  private String state = \"\";"+ln;
    String sutClass = objectUnderTest.getSimpleName();
    String sutObject = lowerCaseFirstLetter(sutClass);
    variables += "  private "+sutClass+" "+sutObject+";"+ln;
    for (Class clazz : mocks) {
      String className = clazz.getSimpleName();
      variables += "  private "+ className +" "+mockNameFor(className)+";"+ln+ln;
    }
    return variables;
  }

  /**
   *
   * @param className
   * @return
   */
  public String constructor(String className) {
    String parameter = objectUnderTest.getSimpleName();
    String objectName = lowerCaseFirstLetter(parameter);
    parameter += " "+objectName;
    String constructor =
        "  public "+className+"("+parameter+") {"+ln+
        "    this."+objectName+" = "+objectName+";"+ln+
        "  }"+ln+ln;
    return constructor; 
  }

  /**
   * Generates the Java code to define a Collection/ArrayList for all the arrays present in the traces.
   *
   * @return Java code to define all used arrays in EFSM model.
   */
  public String arrays() {
    String arrays = "";
    for (Iterator<String> i = arrayNames.iterator(); i.hasNext();) {
      String name = i.next();
      arrays += "  private List "+name+" = new ArrayList();"+ln;
    }
    return arrays;
  }

  /**
   * Old code to create state enumeration. Not used anymore, just kept around for experimentation.
   *
   * @param states  The states of the model.
   * @return  Java code to define the state variable and related enumeration.
   */
  public String stateEnumFor(Collection<FSMState> states) {

    String stateEnum = "  private enum States {"+ln;
    stateEnum += "    Init";
    for (FSMState state : states) {
      String id = capitalizeFirstLetter(state.id());
      stateEnum += ","+ln+"    "+ id;
    }
    stateEnum += ln+"  }"+ln+ln;
    stateEnum += "  public Object getState() {"+ln;
    stateEnum += "    return state;"+ln;
    stateEnum += "  }"+ln;
    return stateEnum;
  }

  /**
   * Generates the state definition method for EFSM.
   *
   * @return  Java code to define the state access method.
   */
  public String stateMethod() {
    String state = "  public Object getState() {"+ln;
    state += "    return state;"+ln;
    state += "  }"+ln;
    return state;
  }

  private String asState(String id) {
    return capitalizeFirstLetter(id);
  }

  /**
   * Generates the @Action part of the EFSM model for modeljunit.
   *
   * @param stateId
   * @return
   */
  public String actionFor(String stateId) {
    if (!inputs.contains(stateId)) {
      //only generate for input states (or methods as they are)
      return "";
    }
    String action = "  @Action"+ln;
    action += "  public void "+stateId+"() throws Exception {"+ln;
    action += "    this.state = \""+ asState(stateId) +"\";"+ln;
    action += "    System.out.println(\""+stateId.toUpperCase()+"\");"+ln;
    action += sutCallWithNoOutputMethods(stateId);
//    action += prefixWith(sutCall(stateId), "    ");
    action += "  }"+ln;
//    action += transitionMethods;
    return action;
  }

  private String sutCallWithNoOutputMethods(String stateId) {
    String call = "";
    for (Class clazz : mocks) {
      MockGenerator mocker = new MockGenerator(clazz);
      call += mocker.replay();
    }
    call += sutCall(stateId);
    for (Class clazz : mocks) {
      MockGenerator mocker = new MockGenerator(clazz);
      call += mocker.verify();
    }
    return prefixWith(call, "    ");
  }

  public String transitionActionsFor(String stateId) {
    if (!inputs.contains(stateId)) {
      return "";
    }
    System.out.println("state:"+stateId);
    Collection<DaikonTransition> transitions = getTransitionsFrom(stateId);
    String actions = "";
    for (DaikonTransition transition : transitions) {
      String target = transition.getTarget();
      System.out.println("target:"+target);
      if (inputs.contains(target)) {
        //skip inputs here, they are to be their own action methods with guards
        continue;
      }
      arrayNames.addAll(transition.arrayNamesForConstraints());
      Method outputMethod = getOutputInterfaceMethodByName(target);
      Class outputInterface = getMockClassFor(target);
      MockGenerator mocker = new MockGenerator(outputInterface);
      actions += ln;
      actions += "  @Action"+ln;
      actions += "  public void "+ stateId +"_"+target+"() throws Exception {"+ln;
      String contents = "";
      contents += "this.state = \""+asState(stateId)+"->"+asState(target)+"\";"+ln;
      contents += "System.out.println(\""+stateId.toUpperCase()+"->"+target.toUpperCase()+"\");"+ln;

      DaikonState state = dm.getState(target +"_EXIT");
//      System.out.println("states:");
//      dm.printStates();
 //     System.out.println("state:"+target+"_EXIT");
      String returnValue = "";
      if (state != null) {
        for (DaikonConstraint constraint : state.getConstraints()) {
          returnValue += constraint.returnValue();
        }
      }

      contents += mocker.callFor(outputMethod, returnValue);
      contents += mocker.replay();
      contents += sutCall(stateId);
      contents += mocker.verify();
      contents = StringUtils.prefixWith(contents, "    ");
      actions += contents;
      actions += "  }"+ln+ln;
      actions += "  public boolean "+stateId+"_"+target+"Guard() {"+ln;
      actions += transition.createTransitionGuards();
      actions += "    return true;"+ln;
      actions += "  }"+ln;
    }
    return actions;
  }

  /**
   *
   * @param stateId
   * @return
   */
  public Collection<DaikonTransition> getTransitionsFrom(String stateId) {
    Collection<DaikonTransition> transitions = dm.getTransitions(stateId);
    if (transitions == null) {
      return Collections.emptyList();
    }
    return transitions;
  }

  /**
  public String transitionMethodCallsFor(String stateId) {
    transitionMethods = "";
    String result = "";
    Collection<DaikonTransition> transitions = getTransitionsFrom(stateId);
    for (DaikonTransition transition : transitions) {
      String target = transition.getTarget();
      if (inputs.contains(target)) {
        //skip inputs here, they are to be their own action methods with guards
        continue;
      }
      arrayNames.addAll(transition.arrayNamesForConstraints());
      Method outputMethod = getOutputInterfaceMethodByName(target);
      Class outputInterface = outputMethod.getDeclaringClass();
      MockGenerator mocker = new MockGenerator(outputInterface);
      String contents = "this.state += \"->"+asState(outputMethod.getName())+"\";"+ln;
      contents += mocker.callFor(outputMethod);
      contents += mocker.replay();
      mocks.add(outputInterface);
      contents += sutCall(stateId);
      contents += mocker.verify();
      contents += "return true;"+ln;
      contents = StringUtils.prefixWith(contents, "    ");
      String transitionMethodName = stateId + "_" + target + "_Transition";
      String methodContent = "  public boolean "+transitionMethodName+"() {"+ln;
      methodContent += transition.createTransitionGuards();
      methodContent += ln+contents;
      methodContent += "  }"+ln;
      transitionMethods += ln+methodContent;
      result += "    if("+transitionMethodName+"()) return;"+ln;
    }
    return result;
  }
*/
  public String assertFor(Method method, String returnVar) {
//    System.out.println("getting exit state:"+method.getName()+"_EXIT");
    DaikonState state = dm.getState(method.getName()+"_EXIT");
    String assertion = "";
    for (DaikonConstraint constraint : state.getConstraints()) {
      assertion += constraint.asAssert(returnVar);
      //TODO to make this work, parseLexical object type from left and if not string/primitive then make the call

/*      Collection<String> valuesToAdd = constraint.getAssertObjectValues();
      if (valuesToAdd.size() == 0) {
        //avoid generating unnecessary methods
        continue;
      }
      String name = constraint.getAssertObjectName();
      Collection<String> values = assertObjects.get(name);
      if (values == null) {
        values = new HashSet<String>();
        assertObjects.put(name, values);
      }
      values.addAll(valuesToAdd);*/
    }
    return assertion;
  }
/*
  public String returnValueBuilders() {
    String result = "";
    for (String name : assertObjects.keySet()) {
      Collection<String> values = assertObjects.get(name);
      result += "public "+name+" create"+name+"For(String str) {"+ln;
      for (String str : values) {
        result += "  if(str.equals("+str+")) {"+ln;
        result += "    return null;"+ln;
        result += "  }"+ln;
      }
      result += "}"+ln;
    }
    return result;
  }*/

  /**
   *
   * @param methodName
   * @return
   */
  public String sutCall(String methodName) {
    Method method = getSUTMethod(methodName);
    String className = objectUnderTest.getSimpleName();
    String objectName = lowerCaseFirstLetter(className);
    Class[] parameterTypes = method.getParameterTypes();
    String parameters = "";
    for (int i = 0; i < parameterTypes.length; i++) {
      Class type = parameterTypes[i];
      imports.add(type);
      String parameterMethodName = methodName+"_p" + i + "()";
      parameters += parameterMethodName;
      if (i < parameterTypes.length-1) {
        parameters += ", ";
      }
      valueMethods.put(parameterMethodName, type);
    }
    Class returnType = method.getReturnType();
    String sutCall = objectName+"."+methodName+"("+parameters+");"+ln;
    if (returnType.equals(void.class)) {
      return sutCall;
    }
    String assertion = assertFor(method, "rv"+rvIndex);
    imports.add(returnType);
    String returnTypeName = returnType.getSimpleName();
    String prefix = returnTypeName +" rv"+rvIndex+" = ";
    rvIndex++;
    return prefix+sutCall+assertion;
  }

  /**
   *
   * @param methodName
   * @return
   */
  private Method getSUTMethod(String methodName) {
    Method[] methods = objectUnderTest.getMethods();
    for (Method method : methods) {
      if (method.getName().equals(methodName)) {
        return method;
      }
    }
    throw new IllegalArgumentException("No method '"+methodName+"' found in "+objectUnderTest+".");
  }

  /**
   *
   * @return
   */
  public String valueMethods() {
    String result = "  //---------- TODO IMPLEMENT METHODS IN THIS SECTION TO GENERATE OBJECTS ------------"+ln;
    String sutName = objectUnderTest.getSimpleName();
    result += "  private "+ sutName + " create"+sutName+"(";
    for (Class mockType : mocks) {
      imports.add(mockType);
      String typeName = mockType.getSimpleName();
      result += typeName;
      result += " mock"+typeName;
    }
    result += ") throws Exception {"+ln;
    result += "    return null;"+ln;
    result += "  }"+ln+ln;
    for (Iterator<String> i = valueMethods.keySet().iterator(); i.hasNext();) {
      String parameterMethodName = i.next();
      Class type = valueMethods.get(parameterMethodName);
      //the states are stored with actual method names, we must get the original from the valuemethod name to access it
      String[] parts = parameterMethodName.split("_p");
      String methodName = parts[0];
      String indexStr = parts[1].split("\\(")[0];
      int index = Integer.parseInt(indexStr);
      DaikonState state = dm.getState(methodName);

      //TODO remove debug
//      System.out.println("state for:"+methodName+" = "+state);
/*      if (state.getFullName().equals("Cunsubscribe")) {
        System.out.println("pindex:"+index);
        if (index == 2) {
          System.out.println("type:"+type.isPrimitive());
        }
      }*/

      result += "  private "+type.getSimpleName()+" "+parameterMethodName+" {"+ln;
      if (type.equals(boolean.class)) {
        result += booleanJavaReturn(state, index);
      } else if (type.isPrimitive()) {
        result += minMaxJavaReturn(state, index, type);
      } else {
        String param = state.parameterValues(type.getSimpleName());
        if (param != null) {
          result += param;
        } else {
          result += "    return null;"+ln;
        }
      }
      result += "  }"+ln;
      if (i.hasNext()) {
        result += ln;
      }
    }
    return result;
  }

  public String booleanJavaReturn(DaikonState state, int parameterIndex) {
    boolean returnTrue = state.booleanTrue(parameterIndex);
    boolean returnFalse = state.booleanFalse(parameterIndex);
    if (returnTrue) {
      if (returnFalse) {
        String java = "    double rnd = Math.random();"+ln;
        java += "    if (rnd >= 0.5) {"+ln;
        java += "      return false;"+ln;
        java += "    }"+ln;
        java += "    return true;"+ln;
        return java;
      }
      return "    return true;"+ln;
    }
    return "    return false;"+ln;
  }

  public String minMaxJavaReturn(DaikonState state, int parameterIndex, Class type) {
    //TODO:state is is the method in general, not tied to transition in which it is
    //executed. this could be narrowed.. or in spirit of some publications
    //it could also be extended to test with new values.. so its an open option
    //may be useful to try with different styles

    double min = state.min(parameterIndex);
    double max = state.max(parameterIndex);
    double diff = max - min;
    if (diff == 0) {
      String typecast = "";
      if (type.equals(int.class)) {
        typecast = "(int)";
      } else if (type.equals(char.class)) {
        typecast = "(char)";
      } else if (type.equals(byte.class)) {
        typecast = "(byte)";
      } else if (type.equals(long.class)) {
        typecast = "(long)";
      } else if (type.equals(float.class)) {
        typecast = "(float)";
      } else if (type.equals(double.class)) {
        typecast = "(double)";
      }
      //it has a constant value
      return "    return "+typecast+min+";"+ln;
    }
    if (diff < 0) {
      throw new IllegalStateException("Invariant max is smaller than min for:"+state.getFullName());
    }
    String value = "    return 0";
    if (type.equals(int.class)) {
      value = "    return cInt((int)"+min+", (int)"+max+");";
    } else if (type.equals(char.class)) {
      value = "    return cChar((char)"+min+", (char)"+max+");";
    } else if (type.equals(byte.class)) {
      value = "    return cByte((byte)"+min+", (byte)"+max+");";
    } else if (type.equals(long.class)) {
      value = "    return cLong((long)"+min+", (long)"+max+");";
    } else if (type.equals(float.class)) {
      value = "    return cFloat((float)"+min+", (float)"+max+");";
    } else if (type.equals(double.class)) {
      value = "    return cDouble((double)"+min+", (double)"+max+");";
    }
    return value+ln;
  }

  public Method getOutputInterfaceMethodByName(String methodName) {
    for (Class clazz : outputInterfaces) {
      Method[] methods = clazz.getMethods();
      for (Method method : methods) {
        if (method.getName().equals(methodName)) {
          return method;
        }
      }
    }
    throw new IllegalArgumentException("No method '"+methodName+"' found in any available output interface:"+outputInterfaces);
  }

  public Class getMockClassFor(String methodName) {
    for (Class clazz : outputInterfaces) {
      Method[] methods = clazz.getMethods();
      for (Method method : methods) {
        if (method.getName().equals(methodName)) {
          return clazz;
        }
      }
    }
    throw new IllegalArgumentException("No method '"+methodName+"' found in any available output interface:"+outputInterfaces);
  }

  public String guardFor(String stateId) {
    if (!inputs.contains(stateId)) {
      //only generate for input states (or methods as they are)
      return "";
    }
    DaikonState state = dm.getState(stateId);
    String guard = "  public boolean "+ stateId +"Guard() {"+ln;
    if (state != null) {
      guard += state.createGuardInvocations();
      arrayNames.addAll(state.arrayNamesForConstraints());
    }
    guard += "    return true;"+ln;
    guard += "  }"+ln;
    return guard;
  }

  public String guardCheckMethods() {
    //these are disabled now since no longer needed
    if (true) return "";
    String methods = "//----------------------- GENERATED GUARD CHECK METHODS -----------------------------"+ln;
    Map<String, FSMState> fsmStates = fsm.getStates();
    Set<String> generatedMethods = new HashSet<String>();
    for (String stateId : fsmStates.keySet()) {
      DaikonState state = dm.getState(stateId);
      methods += state.guardContentMethods(generatedMethods);
      Collection<DaikonTransition> transitions = getTransitionsFrom(stateId);
      for (DaikonTransition transition : transitions) {
        methods += transition.guardContentMethods(generatedMethods);
      }
    }
    return methods;
  }

  /**
   * Creates the basic Java code for the header part of the modeljunit EFSM code. This includes
   * imports, class definitions, etc. All possibly used classes are always imported regardles,
   * such as collection, arraylist, ...
   *
   * @return The java code for imports and other header stuff.
   */

  public String header(String packageName, String className) {
    String header = "package "+packageName+";"+ln+ln;
    header += "import static org.junit.Assert.*;"+ln;
    header += "import static org.easymock.EasyMock.*;"+ln+ln;
    header += "import org.easymock.EasyMock;"+ln;
    header += "import org.junit.Before;"+ln;
    header += "import org.junit.Test;"+ln;
    header += "import net.sourceforge.czt.modeljunit.Action;"+ln;
    header += "import net.sourceforge.czt.modeljunit.FsmModel;"+ln;
    header += "import net.sourceforge.czt.modeljunit.Tester;"+ln;
    header += "import net.sourceforge.czt.modeljunit.RandomTester;"+ln;
    header += "import net.sourceforge.czt.modeljunit.GraphListener;"+ln;
    header += "import net.sourceforge.czt.modeljunit.coverage.CoverageMetric;"+ln;
    header += "import net.sourceforge.czt.modeljunit.coverage.TransitionCoverage;"+ln+ln;
    header += "import net.sourceforge.czt.modeljunit.Action;"+ln;
    header += "import java.util.Iterator;"+ln;
    header += "import java.util.HashSet;"+ln;
    header += "import java.util.List;"+ln;
    header += "import java.util.Random;"+ln;
    //add imports like this so the sets take care of duplicates
    imports.add(java.util.Collection.class);
    imports.add(java.util.ArrayList.class);
    for (Iterator<Class> i = imports.iterator(); i.hasNext();) {
      Class clazz = i.next();
      if (clazz.isPrimitive() || clazz.getPackage().getName().equals("java.lang")) {
        continue;
      }
      header += "import "+clazz.getName()+";"+ln;
      if (!i.hasNext()) {
        header += ln;
      }
    }
    header += "public class "+className+" implements FsmModel {"+ln;
    header += "  private int testIndex = 1;"+ln;
    return header;
  }

  /**
   * Last part of the EFSM Java code for modeljunit, closes the model class.
   *
   * @return The Java code to close up the model.
   */
  public String footer() {
    return "}"+ln;
  }

  public String resetMethod(Collection<String> arrayNames, Collection<Class> mocks) {
    String reset = "  public void reset(boolean b) {"+ln;
    reset += "    state = \"\";"+ln;
    reset += "    System.out.println(\"------------------- STARTING TEST \"+testIndex+\"--------------------------\");"+ln;
    reset += "    testIndex++;"+ln;
    for (String name : arrayNames) {
      reset += "    "+name+".clear();"+ln;
    }
    for (Class clazz : mocks) {
      reset += "    EasyMock.reset("+mockNameFor(clazz.getSimpleName())+");"+ln;
    }
    reset += sutSetup();
    reset += "  }"+ln+ln;
    return reset;
  }

  private String sutSetup() {
    String setup = "    try {"+ln;
    String objectName = objectUnderTest.getSimpleName();
    String lcObjectName = lowerCaseFirstLetter(objectName);
    setup += "      "+lcObjectName+" = create"+objectName+"(";
    for (Class clazz : mocks) {
      if (!setup.endsWith("(")) {
        setup += ",";
      }
      setup += mockNameFor(clazz.getSimpleName());
    }
    setup += ");"+ln;
    setup += "    } catch (Exception e) {"+ln;
    setup += "      throw new RuntimeException(e);"+ln;
    setup += "    }"+ln;
    return setup;
  }

  private String mockSetup() {
    String setup = "";
    for (Class clazz : mocks) {
      setup += "    "+mockInit(clazz.getSimpleName());
    }
    return setup;
  }

  public String testMethod(String className) {
    String testMethod =
      "  @Test"+ln+
      "  public void modelJUnitTest() throws Exception {"+ln+
      mockSetup()+
      "    Tester tester = new RandomTester(this);"+ln+
      "    GraphListener listener = tester.buildGraph();"+ln+
      "    listener.printGraphDot(\""+className+".dot\");"+ln+
      "    CoverageMetric trCoverage = new TransitionCoverage();"+ln+
      "    tester.addListener(trCoverage);"+ln+
      "    tester.addListener(\"verbose\");"+ln+
      "    tester.generate(20);"+ln+
      "    tester.getModel().printMessage(trCoverage.getName() + \" was \" + trCoverage.toString());"+ln+
      "  }"+ln+ln;
    return testMethod;
  }

  private String helperMethods() {
    return ln+
        "  //---------- HELPER METHODS TO GENERATE PRIMITIVE VALUES -----------------------------------------"+ln+
        numberHelper("int")+ln+numberHelper("float")+ln+
        numberHelper("long")+ln+numberHelper("byte")+ln+numberHelper("char")+ln+
        mainNumberHelpers()+ln+randomCollectionItemHelper();
  }

  private String numberHelper(String type) {
    String methodName = capitalizeFirstLetter(type);
    return
        "  public "+type+" c"+ methodName +"() {"+ln+
        "    return ("+type+") Math.round(cDouble());" +ln+
        "  }"+ln+ln+
      "  public "+type+" c"+methodName+"("+type+" min, "+type+" max) {"+ln+
      "    return ("+type+") Math.round(cDouble(min, max));"+ln+
      "  }"+ln;
  }

  private String mainNumberHelpers() {
    imports.add(Random.class);
    return
        "  public double cDouble() {"+ln+
        "    double min = Integer.MIN_VALUE;" +ln+
        "    double max = Integer.MAX_VALUE;" +ln+
        "    return cDouble(min, max);"+ln+
        "  }"+ln+ln+
        "  Random random = new Random(100);"+ln+ln+
        "  public double cDouble(double min, double max) {"+ln+
        "    double diff = max-min;" +ln+
        "    double rnd = random.nextDouble();" +ln+
        "    rnd *= diff;" +ln+
        "    rnd += min;" +ln+
        "    return rnd;"+ln+
        "  }"+ln;
  }

//TODO miksi on turhia arrayta siellä generoidussa mallissa?
  private String randomCollectionItemHelper() {
    return
        "  public Object randomItemFrom(Collection array) {"+ln+
        "    List list = new ArrayList(array);"+ln+
        "    return list.get(cInt(0, array.size()-1));" +ln+
        "  }"+ln;
  }
}
