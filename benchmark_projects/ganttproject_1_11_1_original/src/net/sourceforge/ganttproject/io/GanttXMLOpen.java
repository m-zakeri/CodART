/***************************************************************************
 * GanttXMLOpen.java  -  description
 * -------------------
 * begin                : feb 2003
 * copyright            : (C) 2002 by Thomas Alexandre
 * email                : alexthomas(at)ganttproject.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

package net.sourceforge.ganttproject.io;

import java.awt.Color;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.regex.Pattern;

import javax.swing.tree.DefaultMutableTreeNode;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttGraphicArea;
import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.GanttResourcePanel;
import net.sourceforge.ganttproject.GanttTask;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.gui.GanttDialogInfo;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.parser.FileFormatException;
import net.sourceforge.ganttproject.parser.ParsingContext;
import net.sourceforge.ganttproject.parser.ParsingListener;
import net.sourceforge.ganttproject.parser.TagHandler;
import net.sourceforge.ganttproject.shape.ShapePaint;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.task.TaskManagerImpl;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

//import sun.rmi.runtime.GetThreadPoolAction;


/**
 * Class allow the programm to load a gantt file from xml format
 * Use Sax parser
 */
public class GanttXMLOpen {

  /** The tree that contains data */
  //GanttTree treePanel;

  /** The main frame */
  GanttProject prj;
  
  /** The ressources */
  GanttResourcePanel peop;

  /**0-->description of project, 1->note for task */
  int typeChar = -1;

  /** The graphic area */
  GanttGraphicArea area;

  /** A stack of all father */
  ArrayList lot = new ArrayList();

  /*List for depends */
  ArrayList lod = new ArrayList();

  /** The id of the current task*/
  //int taskID;

  //GanttDependStructure gds; //By CL

  String indent = "";
  String marge = "    "; //the marge

  /**The language */
  GanttLanguage language = GanttLanguage.getInstance();
  
  boolean bImport = false;
  int maxID = 0;
	
  
  private ArrayList myTagHandlers = new ArrayList();
  private ArrayList myListeners = new ArrayList();
  private ParsingContext myContext;
  private final TaskManager myTaskManager;

    /** Constructor */
  public GanttXMLOpen(GanttTree tree, GanttProject appli,
                      GanttResourcePanel resources, GanttGraphicArea gra, 
					  TaskManager taskManager,
					  boolean bImport) {
    this(taskManager);
    //this.treePanel = tree;
    this.prj = appli;
    prj.prjInfos.version = null;
    this.peop = resources;
    this.area = gra;
	this.bImport = bImport;
    if(bImport)
    	maxID = ((TaskManagerImpl)taskManager).getMaxID();

  }

  public GanttXMLOpen(TaskManager taskManager) {
    myContext = new ParsingContext();
    myTaskManager = taskManager;
  }

  public boolean load(String filename) {
    boolean temp = load(new File(filename));
    //constructRelationship();
    return temp;

  }

  public boolean load(InputStream inStream) throws IOException {

    // Use an instance of ourselves as the SAX event handler
      myTaskManager.getAlgorithmCollection().getAdjustTaskBoundsAlgorithm().setEnabled(false);
      myTaskManager.getAlgorithmCollection().getRecalculateTaskScheduleAlgorithm().setEnabled(false);
    DefaultHandler handler = new GanttXMLParser();

    // Use the default (non-validating) parser
    SAXParserFactory factory = SAXParserFactory.newInstance();
    try {
      	// Parse the input
      	SAXParser saxParser;
		saxParser = factory.newSAXParser();
		saxParser.parse(inStream, handler);
	} catch (ParserConfigurationException e) {
		e.printStackTrace();
	} catch (SAXException e) {
		e.printStackTrace();
		throw new IOException(e.getMessage());
	}
    myTaskManager.getAlgorithmCollection().getRecalculateTaskScheduleAlgorithm().setEnabled(true);
	myTaskManager.getAlgorithmCollection().getAdjustTaskBoundsAlgorithm().setEnabled(true);
    //treePanel.refreshAllId(treePanel.getRoot());
    //treePanel.forwardScheduling();
    
    return true;

  }

  public boolean load(File file) {

    // Use an instance of ourselves as the SAX event handler
    DefaultHandler handler = new GanttXMLParser();

    // Use the default (non-validating) parser
    SAXParserFactory factory = SAXParserFactory.newInstance();
    try {

      // Parse the input
      SAXParser saxParser = factory.newSAXParser();
      saxParser.parse(file, handler);      
    }
    catch (Exception e) {
      e.printStackTrace();
      GanttDialogInfo gdi = new GanttDialogInfo(prj,
                                                GanttDialogInfo.ERROR,
                                                GanttDialogInfo.YES_OPTION,
                                                language.getText("msg2") +
                                                file.getAbsolutePath(),
                                                language.getText("error"));
      gdi.show();
      return false;
    }

//    if(treePanel!=null) {
//    	treePanel.forwardScheduling();//refreshAllId(treePanel.getRoot());
//  	}
    return true;
  }

  public void addTagHandler(TagHandler handler) {
    myTagHandlers.add(handler);
  }

  public void addParsingListener(ParsingListener listener) {
    myListeners.add(listener);
  }

  public ParsingContext getContext() {
    return myContext;
  }

  public TagHandler getDefaultTagHandler() {
    return new DefaultTagHandler();
  }

  private class DefaultTagHandler
      implements TagHandler {
    public void startElement(
        String namespaceURI,
        String sName,
        String qName,
        Attributes attrs) {
      indent += "    ";
      String eName = sName; // element name
      if ("".equals(eName)) {
        eName = qName; // not namespaceAware

      }
      if (eName.equals("description")) {
      	myCharacterBuffer = new StringBuffer();
        typeChar = 0;
      }
      if (eName.equals("notes")) {
      	myCharacterBuffer = new StringBuffer();
        typeChar = 1;
        // barmeier: we know that this tag has only attibutes no nested tags
        // we can do we need here.
      }
      /*
             if (eName.equals("allocation")) {
        String aName;
        int taskId = 0;
        int resourceId = 0;
        int load = 0;
        for (int i = 0; i < attrs.getLength(); i++) {
          aName = attrs.getQName(i);
          if (aName.equals("task-id")) {
            taskId = new Integer(attrs.getValue(i)).intValue();
          }
          else if (aName.equals("resource-id")) {
            resourceId = new Integer(attrs.getValue(i)).intValue();
          }
          else if (aName.equals("load")) {
            load = new Integer(attrs.getValue(i)).intValue();
          }
        }
        // if no load is specified I assume 100% load
        // this should only be the case if old files
        // were loaded.
        if (load == 0) {
          load = 100;
        }
        GanttTask the_task = treePanel.getTask(taskId);
        HumanResource user = peop.getUserByNumber(resourceId - 1);
//                user.setLoad(load+user.getMaximumUnitsPerDay());
        the_task.taskUser(peop.getUserByNumber(resourceId - 1), load);
             }
       */
      int task_id = 0;
      //GanttTask task = new GanttTask(new String(), new GanttCalendar(), 1);
      //GanttTask task = myTaskManager.createTask();
      
      //task.setLength(1);
      if (attrs != null) {
        for (int i = 0; i < attrs.getLength(); i++) {
          String aName = attrs.getLocalName(i); // Attr name
          if ("".equals(aName)) {
            aName = attrs.getQName(i);

            //The project part
          }
          if (eName.equals("project")) {
            if (aName.equals("name")) {
              prj.prjInfos._sProjectName = attrs.getValue(i);
            }
            else if (aName.equals("company")) {
            	prj.prjInfos._sOrganization = attrs.getValue(i);
            }
            else if (aName.equals("webLink")) {
            	prj.prjInfos._sWebLink = attrs.getValue(i);
            }
            else if (aName.equals("view-date")) {
              area.getViewState().setStartDate(GanttCalendar.parseXMLDate(attrs.getValue(i)).getTime());
              peop.area.getViewState().setStartDate(GanttCalendar.parseXMLDate(attrs.getValue(i)).getTime());
            }
            else if (aName.equals("version")) {
                prj.prjInfos.version = attrs.getValue(i);
            }
          }

          else if (eName.equals("tasks")) {
            if (aName.equals("color")) {
              area.setProjectLevelTaskColor(determineColor(attrs.getValue(i)));
            }
          }
        }
      }
    }

    public void endElement(String namespaceURI, String sName, String qName) {
      indent = indent.substring(0, indent.length() - 4);
      if ("description".equals(qName)) {
      	prj.prjInfos._sDescription = getCorrectString(myCharacterBuffer.toString());
      }
      else if ("notes".equals(qName)) {
      	Task currentTask = myTaskManager.getTask(getContext().getTaskID());
      	currentTask.setNotes(getCorrectString(myCharacterBuffer.toString()));      	
      }
    }

    private final Color determineColor(String hexString) {
      if (!Pattern.matches("#[0-9abcdefABCDEF]{6}+", hexString)) {
        return GanttGraphicArea.taskDefaultColor;
      }
      int r, g, b;
      r = Integer.valueOf(hexString.substring(1, 3), 16).intValue();
      g = Integer.valueOf(hexString.substring(3, 5), 16).intValue();
      b = Integer.valueOf(hexString.substring(5, 7), 16).intValue();
      return new Color(r, g, b);
    }

  }

  private String getCorrectString(String s) {
    //return s.replaceAll("\n" + indent, "\n");
    s = s.replaceAll("\n" + indent, "\n");
    s = s.replaceAll(marge, "");
    while (s.startsWith("\n")) {
      s = s.substring(1, s.length());
    }
    while (s.endsWith("\n")) {
      s = s.substring(0, s.length() - 1);
    }
    
    s = s.replaceAll("&#38;","&");
    s = s.replaceAll("&#60;","<");
    s = s.replaceAll("&#62;",">");
    s = s.replaceAll("&#47;","/"); 
    s = s.replaceAll("&#34;","\"");
    return s;
  }

  private StringBuffer myCharacterBuffer = new StringBuffer();
  class GanttXMLParser
      extends DefaultHandler {
    StringBuffer textBuffer;

    //===========================================================
    // SAX DocumentHandler methods
    //===========================================================

    public void endDocument() throws SAXException {
      for (int i = 0; i < myListeners.size(); i++) {
        ParsingListener l = (ParsingListener) myListeners.get(i);
        l.parsingFinished();
      }
    }

    public void startElement(String namespaceURI,
                             String sName, // simple name
                             String qName, // qualified name
                             Attributes attrs) throws SAXException {
      for (Iterator handlers = myTagHandlers.iterator(); handlers.hasNext(); ) {
        TagHandler next = (TagHandler) handlers.next();
          try {
              next.startElement(namespaceURI, sName, qName, attrs);
          } catch (FileFormatException e) {
              System.err.println(e.getMessage());
          }
      }
    }

    public void endElement(String namespaceURI,
                           String sName,
                           String qName
                           ) throws SAXException {
      for (Iterator handlers = myTagHandlers.iterator(); handlers.hasNext(); ) {
        TagHandler next = (TagHandler) handlers.next();
        next.endElement(namespaceURI, sName, qName);
      }
    }

    public void characters(char buf[], int offset, int len) throws SAXException {
      
//      len=0;
//      for(int i=0;i+offset<buf.length && buf[i+offset]!='<';i++,len++);      
      String s = new String(buf, offset, len);
      if (typeChar>=0) {
        if (IGNORABLE_WHITESPACE.matcher(s).matches()) {
        	return;
        }
      	s = s.replaceAll("^\\n\\x20*", "\n");
      	myCharacterBuffer.append(s);
      }
    }
  }
  
  static Pattern IGNORABLE_WHITESPACE = Pattern.compile("^\\s*$"); 
}
