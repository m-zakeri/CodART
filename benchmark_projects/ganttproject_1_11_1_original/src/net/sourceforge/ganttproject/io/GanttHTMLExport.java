/***************************************************************************
                           GanttHTMLExport.java  -  description
                             -------------------
    begin                : feb 2003
    copyright            : (C) 2003 by Thomas Alexandre
    email                : alexthomas(at)ganttproject.org
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
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.io.StringReader;
import java.util.ArrayList;
import java.net.URL;
import java.net.URLConnection;

import javax.imageio.ImageIO;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeNode;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttExportSettings;
import net.sourceforge.ganttproject.GanttGraphicArea;
import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.PrjInfos;
import net.sourceforge.ganttproject.ResourceLoadGraphicArea;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;

/** 
  * Class able to export the project in HTML
  * @author Pawel Lipinski (90%)
  */
public class GanttHTMLExport {	
	private static GanttLanguage language = GanttLanguage.getInstance();				
	
	/** Write the tasks */
	private static String writeTasks(GanttTree tree) {	
		StringBuffer out = new StringBuffer();
		ArrayList lot=tree.getAllTasks();
		for(int i=0, k=lot.size(); i < k; i++) {
      DefaultMutableTreeNode node = (DefaultMutableTreeNode)lot.get(i);
			Task t = (Task) (node).getUserObject();
            
      int depth = 0;
      TreeNode up = node;
       while ((up = up.getParent()) != null && up != tree.getRoot()) {
          depth += 1;
       }

			if(t!=t.getManager().getRootTask()) {
				out.append("\t\t<task depth=\""+depth+"\">\n");
				out.append("\t\t\t<name>" + correct(t.getName())  + "</name>\n");
				out.append("\t\t\t<begin>" + t.getStart()  + "</begin>\n");
				out.append("\t\t\t<end>" + t.getEnd()  + "</end>\n");
				out.append("\t\t\t<milestone>" + (t.isMilestone() ? "true" : "false")  + "</milestone>\n");
				out.append("\t\t\t<progress>" + t.getCompletionPercentage()  + "</progress>\n");
				// list all assigned users
                StringBuffer usersS = new StringBuffer();
                ResourceAssignment[] assignments = t.getAssignments();
				if (assignments.length>0) {
				    usersS.append(assignments[0].getResource().getName());
                }
				for(int j=1;j<assignments.length;j++) {
					usersS.append(", " + assignments[j].getResource().getName());
                }
				out.append("\t\t\t<assigned-to>" + correct(usersS.toString())  + "</assigned-to>\n");
				out.append("\t\t\t<notes><![CDATA[" + ((t.getNotes() == null || t.getNotes().length() == 0) ? " " : t.getNotes())  + "]]></notes>\n");
				out.append("\t\t</task>\n");				    
			}
		}
		return out.toString();
	}
	
	/** Write the resources */
	private static String writeResources(GanttProject appli)
	{
		StringBuffer out = new StringBuffer();				
		
		HumanResourceManager resMan=(HumanResourceManager) appli.getHumanResourceManager();
        ArrayList lor=resMan.getResources();
		
//		String []_function=RoleManager.Access.getInstance().getRoleNames();
		for(int i=0, j=lor.size(); i < j; i++) {
			HumanResource p = (HumanResource)lor.get(i);
			out.append("\t\t<resource>\n");
			out.append("\t\t\t<name>" + correct(p.toString()) + "</name>\n");
			out.append("\t\t\t<role>" + correct(p.getRole().getName()) + "</role>\n");
			out.append("\t\t\t<mail>" + (p.getMail()==null || p.getMail().length() == 0 ? " " : correct(p.getMail())) + "</mail>\n");
			out.append("\t\t\t<phone>" + (p.getPhone()==null || p.getPhone().length() == 0 ? " " : correct(p.getPhone())) + "</phone>\n");
			out.append("\t\t</resource>\n");
		}
		return out.toString();
	}
	
	
	/**Save the project in HTML */
	public static void save(File file, /*String name, String desc, String orga,*/
			PrjInfos prjInfos,
		GanttProject prj, GanttTree tree, GanttGraphicArea area, ResourceLoadGraphicArea rarea,
		GanttExportSettings bool)	{
		try {											
			String path=file.getParent();			//the directory 
			String absolute = getFileName(file);	//file without the extention								
			
			//write the image of the calendar
			area.export (new File(path+"/"+absolute+".png"), bool,"png");
			rarea.export(new File(path+"/"+absolute+"-res.png"), "png", bool);
			
			//create XML for xslt
			StringBuffer ganttXML = new StringBuffer();
			ganttXML.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n");
			ganttXML.append("<ganttproject>\n");
			ganttXML.append("\t<title>" + "GanttProject - " + absolute + "</title>\n");
			ganttXML.append("\t<links prefix=\"" + absolute + "\">\n");
			ganttXML.append("\t\t<home>" + language.getText("home") + "</home>\n");
			ganttXML.append("\t\t<chart>" + language.getText("gantt") + "</chart>\n");
			ganttXML.append("\t\t<tasks>" + GanttProject.correctLabel(language.getText("task")) + "</tasks>\n");
			ganttXML.append("\t\t<resources>" + GanttProject.correctLabel(language.getText("human")) + "</resources>\n");
			ganttXML.append("\t</links>\n");
			ganttXML.append("\t<project>\n");
			ganttXML.append("\t\t<name title=\"" + GanttProject.correctLabel(language.getText("project"))  + "\">" + ((prjInfos.getName().length()==0)?" ":correct(prjInfos.getName())) + "</name>\n");
			ganttXML.append("\t\t<organization title=\"" + GanttProject.correctLabel(language.getText("organization"))  + "\">" + ((prjInfos.getOrganization().length()==0)?" ":correct(prjInfos.getOrganization())) + "</organization>\n");
			ganttXML.append("\t\t<webLink title=\"" + GanttProject.correctLabel(language.getText("webLink"))  + "\">" + ((prjInfos.getWebLink().length()==0)?" ":correct(prjInfos.getWebLink())) + "</webLink>\n");
			ganttXML.append("\t\t<description title=\"" + GanttProject.correctLabel(language.getText("shortDescription") ) + "\">" + ((prjInfos.getDescription().length()==0)?" ":correct(prjInfos.getDescription())) + "</description>\n");
			ganttXML.append("\t</project>\n");
			ganttXML.append("\t<chart>" + absolute + ".png</chart>\n");
			ganttXML.append("\t<resources name=\"" + language.getText("colName") + "\" role=\"" + language.getText("colRole") + "\" mail=\"" + 
					language.getText("colMail") + "\" phone=\"" + language.getText("colPhone") + "\">\n");
			ganttXML.append(writeResources(prj));
			ganttXML.append("\t\t<chart path=\"" + absolute + "-res.png" +"\"/>\n");
			ganttXML.append("\t</resources>\n");
			ganttXML.append("\t<tasks name=\"" + language.getText("name") + "\" begin=\"" + language.getText("start") + "\" end=\"" + 
					language.getText("end") + "\" milestone=\"" + language.getText("meetingPoint") + "\" progress=\"" + 
					language.getText("advancement") + "\" assigned-to=\"" + language.getText("assignTo") + "\" notes=\"" + language.getText("notesTask") + "\">\n");
			ganttXML.append(writeTasks(tree));
			ganttXML.append("\t</tasks>\n");
			ganttXML.append("\t<footer version=\"Ganttproject ("+GanttProject.version+")\" date=\""+GanttCalendar.getDateAndTime()+"\"/>\n");
			ganttXML.append("</ganttproject>\n");
			
//	==================================================================================================================
			//Uncomment this line to write the temporary xml file on the standard output
			//System.out.println(ganttXML);
//	==================================================================================================================			
						
			// produce htmls from xml/xsl
			TransformerFactory tFactory = TransformerFactory.newInstance();
			Transformer transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt.xsl"));
			transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(new FileOutputStream(file)));
			
			transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-chart.xsl"));
			transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(new FileOutputStream(path+"/"+absolute+"-chart.html")));
			
			transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-resources.xsl"));
			transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(new FileOutputStream(path+"/"+absolute+"-resources.html")));
			
			transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-tasks.xsl"));
			transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(new FileOutputStream(path+"/"+absolute+"-tasks.html")));			
		
		
			//If there is some images copy their to the path od the html pages
			File imageDirectory=new File(prj.getXslDir()+File.separator+"images"+File.separator);
			if (imageDirectory.exists() && imageDirectory.isDirectory()){
				File [] lof = imageDirectory.listFiles();
				if(lof.length!=0) {
					//Create the directory images
					File newImgDir= new File(path+File.separator+"images"+File.separator);
					if(newImgDir.mkdir()) {
				
						for(int i=0;i<lof.length;i++){
							String ext=getExtention(lof[i]);
							ImageIO.write(ImageIO.read(new FileInputStream(lof[i])),ext,new File(path+File.separator+"images"+File.separator+lof[i].getName()));
						}
					}
						
				}
			}
		
		}catch(NullPointerException e)	{
			System.out.println(e.getMessage());
			e.printStackTrace();
		
		}catch(TransformerException e)	{
			System.out.println(e.getMessageAndLocation());
		
		}catch(Exception e)	{
			System.out.println(e);
			
		}
	}

    /**
     * Publish the HTML-Pages to a Webserver
     * @param urlString
     * @param prjInfos
     * @param prj
     * @param tree
     * @param area
     * @param rarea
     * @param bool
     */
    public static void publish(String urlString,
    PrjInfos prjInfos,
        GanttProject prj,
        GanttTree tree,
        GanttGraphicArea area,
        ResourceLoadGraphicArea rarea,
        GanttExportSettings bool) throws IOException {
        URL url;
        try {
            url = new URL(urlString + "gantt.png");
            URLConnection urlc = url.openConnection();
            OutputStream os = urlc.getOutputStream();
            //write the image of the calendar
            area.export(os, bool, "png");
            os.flush();
            os.close();
            url = new URL(urlString + "resources.png");
            urlc = url.openConnection();
            os = urlc.getOutputStream();
            rarea.export(os, "png", bool);
            os.flush();
            os.close();

            //create XML for xslt
            StringBuffer ganttXML = new StringBuffer();
            ganttXML.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n");
            ganttXML.append("<ganttproject>\n");
            ganttXML.append("\t<title>" + "GanttProject</title>\n");
            ganttXML.append("\t<links prefix=\"gantt\">\n");
            ganttXML.append("\t\t<home>" + language.getText("home") + "</home>\n");
            ganttXML.append("\t\t<chart>" + language.getText("gantt") + "</chart>\n");
            ganttXML.append("\t\t<tasks>" + GanttProject.correctLabel(language.getText("task")) + "</tasks>\n");
            ganttXML.append("\t\t<resources>" + GanttProject.correctLabel(language.getText("human")) + "</resources>\n");
            ganttXML.append("\t</links>\n");
            ganttXML.append("\t<project>\n");
            ganttXML.append(
                "\t\t<name title=\""
                    + GanttProject.correctLabel(language.getText("project"))
                    + "\">"
                    + ((prjInfos.getName().length() == 0) ? " " : correct(prjInfos.getName()))
                    + "</name>\n");
            ganttXML.append(
                "\t\t<organization title=\""
                    + GanttProject.correctLabel(language.getText("organization"))
                    + "\">"
                    + ((prjInfos.getOrganization().length() == 0) ? " " : correct(prjInfos.getOrganization()))
                    + "</organization>\n");
            ganttXML.append(
                "\t\t<webLink title=\""
                    + GanttProject.correctLabel(language.getText("webLink"))
                    + "\">"
                    + ((prjInfos.getWebLink().length() == 0) ? " " : correct(prjInfos.getWebLink()))
                    + "</webLink>\n");
            ganttXML.append(
                "\t\t<description title=\""
                    + GanttProject.correctLabel(language.getText("shortDescription"))
                    + "\">"
                    + ((prjInfos.getDescription().length() == 0) ? " " : correct(prjInfos.getDescription()))
                    + "</description>\n");
            ganttXML.append("\t</project>\n");
            ganttXML.append("\t<chart>gantt.png</chart>\n");
            ganttXML.append(
                "\t<resources name=\""
                    + language.getText("colName")
                    + "\" role=\""
                    + language.getText("colRole")
                    + "\" mail=\""
                    + language.getText("colMail")
                    + "\" phone=\""
                    + language.getText("colPhone")
                    + "\">\n");
            ganttXML.append(writeResources(prj));
            ganttXML.append("\t\t<chart path=\"resources.png" + "\"/>\n");
            ganttXML.append("\t</resources>\n");
            ganttXML.append(
                "\t<tasks name=\""
                    + language.getText("name")
                    + "\" begin=\""
                    + language.getText("start")
                    + "\" end=\""
                    + language.getText("end")
                    + "\" milestone=\""
                    + language.getText("meetingPoint")
                    + "\" progress=\""
                    + language.getText("advancement")
                    + "\" assigned-to=\""
                    + language.getText("assignTo")
                    + "\" notes=\""
                    + language.getText("notesTask")
                    + "\">\n");
            ganttXML.append(writeTasks(tree));
            ganttXML.append("\t</tasks>\n");
            ganttXML.append(
                "\t<footer version=\"Ganttproject ("
                    + GanttProject.version
                    + ")\" date=\""
                    + GanttCalendar.getDateAndTime()
                    + "\"/>\n");
            ganttXML.append("</ganttproject>\n");

            // produce htmls from xml/xsl
            TransformerFactory tFactory = TransformerFactory.newInstance();
            Transformer transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt.xsl"));

            url = new URL(urlString + "gantt.html");
            urlc = url.openConnection();
            os = urlc.getOutputStream();

            transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(os));
            os.flush();
            os.close();
            //----------------------
            url = new URL(urlString + "gantt-chart.html");
            urlc = url.openConnection();
            os = urlc.getOutputStream();

            transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-chart.xsl"));
            transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(os));
            os.flush();
            os.close();

            //-----------------------
            url = new URL(urlString + "gantt-resources.html");
            urlc = url.openConnection();
            os = urlc.getOutputStream();

            transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-resources.xsl"));
            transformer.transform(new StreamSource(new StringReader(ganttXML.toString())), new StreamResult(os));
            os.flush();
            os.close();
            //-----------------------------
			
			url = new URL(urlString + "gantt-tasks.html");
			urlc = url.openConnection();
			os = urlc.getOutputStream();
			
            transformer = tFactory.newTransformer(new StreamSource(prj.getXslDir() + "/gantt-tasks.xsl"));
            transformer.transform(
                new StreamSource(new StringReader(ganttXML.toString())),
                new StreamResult(os));
            os.flush();   
            os.close();

        } catch (NullPointerException e) {
            System.out.println(e.getMessage());
            e.printStackTrace();

        } catch (TransformerException e) {
            System.out.println(e.getMessageAndLocation());

        } catch (Exception e) {
            throw new IOException(GanttLanguage.getInstance().getText("errorFTPConnection"));
        }
    }
	
	
  /** Correct the charcters to be compatible with xml format */
  public static String correct(String s) {
    String res;
    res = s.replaceAll("&", "&#38;");
    res = res.replaceAll("<", "&#60;");
    res = res.replaceAll(">", "&#62;");
    res = res.replaceAll("/", "&#47;"); 
    res = res.replaceAll("\"", "&#34;");  
    return res;
  }


    /** the name of the files */	
    public static String getFileName(File f) {
        String ext = null;
        String s = f.getName();
        int i = s.lastIndexOf('.');

        if (i > 0 &&  i < s.length() - 1) {
           //ext = s.substring(0,i).toLowerCase();
        	 ext = s.substring(0,i);
        }
        System.out.println(ext+"  "+s);
        return ext;
    }
	
	/**Return the extention for the file*/
	public static String getExtention(File f){
		String ext = null;
        String s = f.getName();
        int i = s.lastIndexOf('.');

        if (i > 0 &&  i < s.length() - 1) {
            ext = s.substring(i+1,s.length()).toLowerCase();
        }
        return ext;	
	}
}
