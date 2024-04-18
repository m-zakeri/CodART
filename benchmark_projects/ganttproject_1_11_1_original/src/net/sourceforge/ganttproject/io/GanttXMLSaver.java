/***************************************************************************
 * GanttXMLSaver.java  -  description
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

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Vector;

import javax.swing.tree.DefaultMutableTreeNode;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactoryConfigurationError;
import javax.xml.transform.sax.SAXTransformerFactory;
import javax.xml.transform.sax.TransformerHandler;
import javax.xml.transform.stream.StreamResult;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttGraphicArea;
import net.sourceforge.ganttproject.GanttResourcePanel;
import net.sourceforge.ganttproject.GanttTask;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.IGanttProject;
import net.sourceforge.ganttproject.gui.UIFacade;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.roles.Role;
import net.sourceforge.ganttproject.roles.RoleManager;
import net.sourceforge.ganttproject.roles.RoleSet;
import net.sourceforge.ganttproject.shape.ShapeConstants;
import net.sourceforge.ganttproject.shape.ShapePaint;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.util.ColorConvertion;

//import org.apache.xalan.processor.StopParseException;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.AttributesImpl;

/**
 * Classe for save the project in a XML file
 */
public class GanttXMLSaver {

    private final IGanttProject myProject;
    private final UIFacade myUIFacade;
  private GanttTree tree;
  private GanttResourcePanel peop;
  private GanttGraphicArea area;
  

  private HashMap usersId = new HashMap();

  ArrayList number = new ArrayList();
  //List of tasks
  ArrayList lot = new ArrayList();
  ArrayList lots = new ArrayList();
  

  int cpt;

  String s = "    "; //the marge

  /** The constructor */
  public GanttXMLSaver(IGanttProject project, GanttTree tree,
                       GanttResourcePanel peop, GanttGraphicArea area, UIFacade uiFacade) {
    this.tree = tree;
    this.peop = peop;
    this.area = area;
    myProject = project;
    myUIFacade = uiFacade;
  }

  /** Replace a part of the string by another one */
  public String replaceAll(String notes, String s1, String s2) {

    return notes.replaceAll(s1, s2);
  }

  /** Simple write information of tasks */
  public void writeTask(Writer fout, DefaultMutableTreeNode node, String space) {
    String space2 = s + space;
    try {
      
      GanttTask task = (GanttTask)node.getUserObject();
      
      if(task.getTaskID()==-1) throw new RuntimeException("A task can not has a number equal to -1");
      
      
      int id=task.getTaskID();
      
      /*if (id >= lot.size()) {
        return;
      }*/
      
      
      boolean haschild = false;

      ArrayList child = tree.getAllChildTask(node);
      if (child.size() != 0) {
        haschild = true;

      }

      number.add(new Integer(id));
      cpt++;

//      boolean one = (task.getSuccessorsOld().size() != 0 || (task.getNotes() != null && task.getNotes().length()>=0) ||
//                     haschild);
	
	boolean one = (task.getSuccessorsOld().size()==0 && (task.getNotes() == null || task.getNotes().length()==0) && !haschild);


      //Writes data of task
      fout.write(space + "<task id=\"" + task.getTaskID() + //lots.indexOf(task.toString()) + //By CL
                 "\" ");
      fout.write("name=\"" + correct(task.getName()) + "\" ");

      if (task.colorDefined()) {
        /*fout.write("color=\"#");
        if (task.getColor().getRed() <= 15) {
          fout.write("0");
        }
        fout.write(Integer.toHexString(task.getColor().getRed()));
        if (task.getColor().getGreen() <= 15) {
          fout.write("0");
        }
        fout.write(Integer.toHexString(task.getColor().getGreen()));
        if (task.getColor().getBlue() <= 15) {
          fout.write("0");
        }
        fout.write(Integer.toHexString(task.getColor().getBlue()));
        fout.write("\" ");*/
		fout.write("color=\""+ColorConvertion.getColor(task.getColor())+"\" ");
      }

      if (task.shapeDefined() && 
      		task.getShape() != new ShapePaint(ShapeConstants.BACKSLASH, 
      				task.getColor() , task.getColor())) {
	  fout.write("shape=\"" + task.getShape().getArray()+ "\" ");
      }

      fout.write("meeting=\"" + ( (task.isMilestone()) ? "true" : "false") +
                 "\" ");
      fout.write("start=\"" + task.getStart().toXMLString() + "\" ");
      fout.write("duration=\"" + task.getLength() + "\" ");
      fout.write("complete=\"" + task.getCompletionPercentage() + "\" ");
        fout.write("fixed-start=\"" + (task.isStartFixed() ? "true" : "false") + "\" ");
      fout.write("priority=\"" + task.getPriority() + "\"");
      
      //write the web link of the task
      String sWebLink = task.getWebLink();
      if(sWebLink != null && !sWebLink.equals("") && !sWebLink.equals("http://"))
      	fout.write(" webLink=\"" + sWebLink + "\"");
      
      //write if the task is expand or collapse      
      fout.write(" expand=\"" + task.getExpand() + "\"");
	  	
      if (!one) {
        fout.write(">\n");
      }
      else {
        fout.write("/>\n");
        //fout.writeBytes(">\n");

        //Write notes
      }
      if (task.getNotes() != null && task.getNotes().length()>0) {
        fout.write(space2 + "<notes>");
        fout.write("\n" + space2 + s + correct(replaceAll(task.getNotes(), "\n", "\n" + space2 + s)));
        fout.write("\n" + space2 + "</notes>\n");
      }

      //Write the depends of the task
      /*
      if (task.getDepend().size() != 0) {
        //fout.writeBytes(space2+"<depends>\n");
        for (int i = 0; i < task.getDepend().size(); i++) {
          fout.write(space2 + "<depend id=\"" +
                     tree.getTask( (String) task.getDepend().get(i)).getTaskID() + // changed By CL
                     //lots.indexOf( (String) task.getDepend().get(i)) +
                     "\"/>\n");
          //fout.writeBytes(space2+"</depends>\n");
        }
      }*/

      //use successors to write depends information
      Vector successors = task.getSuccessorsOld();
      for (int i = 0; i < successors.size(); i++) {
        GanttTaskRelationship relationship
            = (GanttTaskRelationship) successors.get(i);
        fout.write(space2 /*+s*/ + "<depend id=\"" +
                   relationship.getSuccessorTaskID()+"\""
                   +" type=\""
                   +relationship.getRelationshipType()
                   +"\"/>\n");
      }

      //Write the child of the task
      if (haschild) {
        for (int i = 0; i < child.size(); i++) {
          Task task2 = (Task) ( (DefaultMutableTreeNode) child.get(i)).
              getUserObject();
          int newid = -1; //lot.lastIndexOf(task2);

          for (int j = 0; j < lot.size(); j++) {
            String a = task2.toString();
            String b = lot.get(j).toString();

            if (a.equals(b)) {
              newid = j;
            }
          }
          writeTask(fout, (DefaultMutableTreeNode)child.get(i), space + s);
        }

      }

      //end of task section
      if (!one) {
        fout.write(space + "</task>\n");
        //fout.writeBytes(space+"</task>\n");

      }
      //      if (tree.getNode(task.toString()).isLeaf() &&
      //          !tree.getFatherNode(task).isRoot()) {
      //        return;
      //      }

      //      if (id == lot.size() - 1) {
      //        return;
      //      }
      //      else {
      //        writeTask(fout, cpt, space);
      //
      //      }

    }
    catch (Exception e) {
      System.out.println(e);
    }
  }

  /** Write the resources on the file */
  public void writeResources(Writer fout) {
    try {
      ArrayList resources = peop.getPeople();
      int cpt_resources = 1;
      for (int i = 0; i < resources.size(); i++, cpt_resources++) {
        HumanResource p = (HumanResource) resources.get(i);
        String string = p.getName();
        byte[] btf8 = string.getBytes("UTF-8");

        fout.write(s + s + "<resource id=\"" + p.getId() + "\" name=\"" +
                   (p.getName()!=null?correct(p.getName()):"") +
                   "\" function=\"" + p.getRole().getPersistentID() + "\" contacts=\"" +
                   (p.getMail()!=null?correct(p.getMail()):"") + "\" phone=\""+ (p.getPhone()!=null?correct(p.getPhone()):"") +"\" />\n");

        usersId.put(p.getName(), new Integer(cpt_resources));
      }
    }
    catch (Exception e) {
      System.out.println(e);
    }
  }

  /** Write the assignement between tasks and users */
  public void writeAllocations(Writer fout) {
      try {

          for (int i = 1; i < lot.size(); i++) {
              Task task = (Task) ((DefaultMutableTreeNode) lot.get(i)).
                      getUserObject();
              //ArrayList users = task.getUsersList();
              ResourceAssignment[] assignments = task.getAssignments();
              for (int j = 0; j < assignments.length; j++) {
                  int task_id = task.getTaskID();//(i-1);
                  ResourceAssignment next = assignments[j];

                  fout.write(s + s + "<allocation task-id=\"" +
                          task_id + "\" resource-id=\"" + next.getResource().getId() +
                          "\" load=\"" + next.getLoad() + "\"/>\n");
              }
          }

      } catch (Exception e) {
          System.out.println(e);
      }
  }
  
  /** Write all roles of the project. */
  public void writeRoles(Writer fout) {
   	try {
//		int id=RoleManager.Access.getInstance().DEFAULT_ROLES_NUMBER;
//		String []roles=RoleManager.Access.getInstance().getRolesShort();
           Role[] projectRoles = RoleManager.Access.getInstance().getProjectLevelRoles();
		for(int i=0;i<projectRoles.length;i++) {
            Role next = projectRoles[i];
			fout.write(s + s + "<role id=\""+(next.getPersistentID())+"\" name=\""+correct(next.getName())+"\"/>\n");
        }

	}catch (Exception e) {
      System.out.println(e);
    }
  }

  /** Correct the charcters to be compatible with xml format */
  public String correct(String s) {
    String res;
    res = s.replaceAll("&", "&#38;");
    res = res.replaceAll("<", "&#60;");
    res = res.replaceAll(">", "&#62;");
    res = res.replaceAll("/", "&#47;"); 
    res = res.replaceAll("\"", "&#34;");  
    return res;
  }

	/** Save the project as XML on a stream (including the XML-prolog) */
	public void save(OutputStream stream, String version) {
		try {
			OutputStreamWriter fout = new OutputStreamWriter(stream, "UTF-8");
			save(fout, version, true);
		} catch (IOException e) {
            e.printStackTrace();
			System.out.println(e);
			//System.out.println("Error in saving the file");
		} catch (TransformerFactoryConfigurationError e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (TransformerException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (SAXException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
	}

    private void startElement(String name, AttributesImpl attrs, TransformerHandler handler) throws SAXException {
        handler.startElement("", name, name, attrs);
        attrs.clear();
    }
    
    private void endElement(String name, TransformerHandler handler) throws SAXException {
        handler.endElement("", name, name);
    }
    
    private void addAttribute(String name, String value, AttributesImpl attrs) {
        attrs.addAttribute("", name, name, "CDATA", value);
    }
    
    private void emptyElement(String name, AttributesImpl attrs, TransformerHandler handler) throws SAXException {
        startElement(name, attrs, handler);
        endElement(name, handler);
        attrs.clear();
    }
    
    private void emptyComment(TransformerHandler handler) throws SAXException {
        handler.comment(new char[] {' '}, 0, 1);
        
    }
	public void save(OutputStreamWriter _fout, String version,boolean includeProlog) 
    throws IOException,TransformerFactoryConfigurationError, TransformerException,SAXException {
        try {
            AttributesImpl attrs = new AttributesImpl();
            StreamResult result = new StreamResult(_fout);
            SAXTransformerFactory factory = (SAXTransformerFactory) SAXTransformerFactory
                    .newInstance();
            TransformerHandler handler = factory.newTransformerHandler();
            Transformer serializer = handler.getTransformer();
            serializer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
            serializer.setOutputProperty(OutputKeys.INDENT, "yes");
            serializer.setOutputProperty(
                    "{http://xml.apache.org/xslt}indent-amount", "4");
            handler.setResult(result);
            handler.startDocument();
            addAttribute("name", getProject().getProjectName(), attrs);
            addAttribute("company", getProject().getOrganization(), attrs);
            addAttribute("webLink", getProject().getWebLink(), attrs);
            addAttribute("view-date", new GanttCalendar(area.getViewState().getStartDate()).toXMLString(), attrs);
            //TODO: 1.11 repair saving zoom state
            //addAttribute("view-zoom", "" + area.getZoom(), attrs);
            addAttribute("version", version, attrs);
            startElement("project", attrs, handler);
            saveViews(handler);
            emptyComment(handler);
            saveCalendar(handler);
            _save(_fout, version, false);

            saveRoles(handler);
            endElement("project", handler);
            handler.endDocument();

            _fout.close();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
       
    private void saveViews(TransformerHandler handler) throws SAXException {
    	new ViewSaver().save(getUIFacade(), handler);
	}

	private void saveCalendar(TransformerHandler handler) throws SAXException {
        new CalendarSaver().save(getProject(), handler);
    }

    private void saveRoles(TransformerHandler handler) throws SAXException {
        AttributesImpl attrs = new AttributesImpl();
        RoleManager roleManager = getProject().getRoleManager();
        RoleSet[] roleSets = roleManager.getRoleSets();
        for (int i=0; i<roleSets.length; i++) {
            RoleSet next = roleSets[i];
            if (next.isEnabled()) {
                addAttribute("roleset-name", next.getName(), attrs);
                emptyElement("roles", attrs, handler);
            }
        }
        //
        RoleSet projectRoleSet = roleManager.getProjectRoleSet();        
        if(!projectRoleSet.isEmpty()){
            startElement("roles", attrs, handler);            
            Role[] projectRoles = projectRoleSet.getRoles();            
            for(int i=0;i<projectRoles.length;i++) {
                Role next = projectRoles[i];
                addAttribute("id", next.getPersistentID(), attrs);
                addAttribute("name", next.getName(), attrs);
                emptyElement("role", attrs, handler);                
            }
            endElement("roles", handler);            
        }
    }

/**
 * Save the project as XML on a writer
 * 
 * @throws TransformerFactoryConfigurationError
 * @throws TransformerFactoryConfigurationError
 * @throws TransformerException
 * @throws SAXException
 */
  public void _save(OutputStreamWriter fout, String version, boolean includeProlog) throws IOException, TransformerFactoryConfigurationError, TransformerException, SAXException {
      //String space="    ";
      number.clear();

      //StringWriter fout = new StringWriter();      
      if (includeProlog) {
        //write header
        //fout.writeBytes("<?xml version=\"1.0\"?>\n");
        fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        //fout.write("<!DOCTYPE project SYSTEM \"http://ganttproject.sourceforge.net/dtd/ganttproject.dtd\">\n\n");
				fout.write("<!DOCTYPE ganttproject.sourceforge.net>\n\n");
	  }

//      fout.write("<project name=\"" + correct(getProject().getProjectName()) + 
//      			 "\" company=\"" + correct(getProject().getOrganization()) +
//      			 "\" webLink=\"" + correct(getProject().getWebLink()) +
//                 "\" view-date=\"" + area.getDate().toXMLString() +
//                 "\" view-zoom=\"" +
//                 area.getZoom() + "\" version=\"" + version + "\">\n");

      fout.write(s + "<description>");
      if (!getProject().getDescription().equals("")) {
        fout.write("\n" + s + s + correct(replaceAll(getProject().getDescription(), "\n", "\n" + s + s)) +
                   "\n");
      }
      fout.write(s + "</description>\n\n");

      lot = tree.getAllTasks();
      lots = tree.getArryListTaskString(null);

	
      //begin of tasks
      //fout.write(s + "<tasks>\n");

      //begin of tasks
      fout.write(s + "<tasks ");
      fout.write("color=\""+ColorConvertion.getColor(area.getTaskColor())+"\"");
      /*fout.write("color=\"#");
      if (area.getTaskColor().getRed() <= 15) {
        fout.write("0");
      }
      fout.write(Integer.toHexString(area.getTaskColor().getRed()));
      if (area.getTaskColor().getGreen() <= 15) {
        fout.write("0");
      }
      fout.write(Integer.toHexString(area.getTaskColor().getGreen()));
      if (area.getTaskColor().getBlue() <= 15) {
        fout.write("0");
      }
      fout.write(Integer.toHexString(area.getTaskColor().getBlue()));
      fout.write("\"");*/

      fout.write(">\n");

      cpt = 1;
      Enumeration children =
          ( (DefaultMutableTreeNode) tree.getJTree().getModel().getRoot()).
          children();
      while (children.hasMoreElements()) {
	DefaultMutableTreeNode element = (DefaultMutableTreeNode) children.nextElement();
    	writeTask(fout, /*lot.indexOf(element)*/element, s + s);
      }

      //end of tasks
      fout.write(s + "</tasks>\n\n");

      //write the resources
      fout.write(s + "<resources>\n");
      writeResources(fout);
      fout.write(s + "</resources>\n\n");

      //write the assign task to user
      fout.write(s + "<allocations>\n");
      writeAllocations(fout);
      fout.write(s + "</allocations>\n\n");
	  
	  //write the assign task to user

      //end of project
//      fout.write("</project>\n");
      
      //fout.close();
      //
            
  }
  
  IGanttProject getProject() {
      return myProject;
  }
  
  UIFacade getUIFacade() {
  	return myUIFacade; 
  }
}
