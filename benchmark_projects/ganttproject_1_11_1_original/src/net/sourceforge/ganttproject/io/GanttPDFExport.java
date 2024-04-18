/***************************************************************************
                           GanttPDFExport.java  -  description
                             -------------------
    begin                : sep 2003
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

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.io.StringReader;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Locale;

import javax.swing.tree.DefaultMutableTreeNode;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.sax.SAXResult;
import javax.xml.transform.sax.SAXTransformerFactory;
import javax.xml.transform.sax.TransformerHandler;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import net.sourceforge.ganttproject.GanttExportSettings;
import net.sourceforge.ganttproject.GanttGraphicArea;
import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.IGanttProject;
import net.sourceforge.ganttproject.PrjInfos;
import net.sourceforge.ganttproject.ResourceLoadGraphicArea;
import net.sourceforge.ganttproject.export.FontRecord;
import net.sourceforge.ganttproject.export.FontTriplet;
import net.sourceforge.ganttproject.export.JDKFontLocator;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;

import org.apache.avalon.framework.logger.ConsoleLogger;
import org.apache.avalon.framework.logger.Logger;
import org.apache.fop.apps.Driver;
import org.apache.fop.apps.FOPException;
import org.apache.fop.apps.Options;
import org.apache.fop.image.FopImageFactory;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.AttributesImpl;

public class GanttPDFExport {

	private static GanttLanguage language = GanttLanguage.getInstance();
    private static SAXTransformerFactory ourTransformerFactory;

    private static String getHexaColor(java.awt.Color color) {
		StringBuffer out = new StringBuffer();
	    out.append("#");
        if (color.getRed() <= 15) {
          out.append("0");
        }
        out.append(Integer.toHexString(color.getRed()));
        if (color.getGreen() <= 15) {
          out.append("0");
        }
        out.append(Integer.toHexString(color.getGreen()));
        if (color.getBlue() <= 15) {
          out.append("0");
        }
        out.append(Integer.toHexString(color.getBlue()));
        
		return out.toString();
	}
	
	
	/** Write the tasks */
	private static String writeTasks(GanttTree tree) {	
		StringBuffer out = new StringBuffer();
		ArrayList lot=tree.getAllTasks();
		for(int i=0, k=lot.size(); i < k; i++) {
			Task t = (Task) ((DefaultMutableTreeNode)lot.get(i)).getUserObject();
			if(t!=t.getManager().getRootTask()) {
				out.append("\t\t<ganttproject:task>\n");
				out.append("\t\t\t<name>" + correct(t.toString())  + "</name>\n");
				out.append("\t\t\t<begin>" + t.getStart()  + "</begin>\n");
				out.append("\t\t\t<end>" + t.getEnd()  + "</end>\n");
				out.append("\t\t\t<milestone>" + (t.isMilestone() ? "true" : "false")  + "</milestone>\n");
				out.append("\t\t\t<progress>" + t.getCompletionPercentage()  + "</progress>\n");
				// list all assigned users				
                StringBuffer usersS = new StringBuffer();
                ResourceAssignment[] assignments = t.getAssignments();
				if (assignments.length>0) {
                    for(int j=0;j<assignments.length;j++) {
                        usersS.append(assignments[j].getResource().getName() + "\n");
                    }
                }
                else {
                    usersS.append("&#160;");
                }
				out.append("\t\t\t<assigned-to>" + usersS.toString()  + "</assigned-to>\n");
				out.append("\t\t\t<notes><![CDATA[" + ((t.getNotes() == null || t.getNotes().length() == 0) ? " " : t.getNotes())  + "]]></notes>\n");
				out.append("\t\t\t<color>"+getHexaColor(t.getColor())+"</color>\n");
				out.append("\t\t</ganttproject:task>\n");				    
			}
		}
		return out.toString();
	}
	
	/** Write the resources */
	private static String writeResources(HumanResourceManager resMan)
	{
		StringBuffer out = new StringBuffer();				
		
        ArrayList lor=resMan.getResources();
		
//		String []function=RoleManager.Access.getInstance().getRoleNames();
		for(int i=0, j=lor.size(); i < j; i++) {
			HumanResource p = (HumanResource)lor.get(i);
			out.append("\t\t<ganttproject:resource>\n");
			out.append("\t\t\t<name>" + correct(p.toString()) + "</name>\n");
			out.append("\t\t\t<role>" + correct(p.getRole().getName()) + "</role>\n");
			out.append("\t\t\t<mail>" + (p.getMail()==null || p.getMail().length() == 0 ? " " : correct(p.getMail())) + "</mail>\n");
			out.append("\t\t\t<phone>" + (p.getPhone()==null || p.getPhone().length() == 0 ? " " : correct(p.getPhone())) + "</phone>\n");
			out.append("\t\t</ganttproject:resource>\n");
		}
		return out.toString();
	}
	
	
	/**Save the project in HTML 
	 * @throws TransformerException
	 * @throws IOException*/
	public static void save(File pdffile,
			IGanttProject ganttProject,
		HumanResourceManager resourceManager, GanttTree tree, GanttGraphicArea area, ResourceLoadGraphicArea rarea,
		GanttExportSettings bool, String xslfo)	throws IOException, TransformerException {
			        
			String path=new File(xslfo).getParent();	
			
			DateFormat df =java.text.DateFormat.getDateTimeInstance(DateFormat.MEDIUM, DateFormat.MEDIUM,Locale.getDefault() );
			
			//write the image of the calendar
			//area.fitWholeProject(true);
			area.export(new File(System.getProperty("java.io.tmpdir")+"/"+"ganttchart.jpg"), bool,"jpg");
			//rarea.fitWholeProject(true);
			rarea.export(new File(System.getProperty("java.io.tmpdir")+"/"+"resourceschart.jpg"), "jpg", bool);
			
			
			//create XML for xslt
			StringBuffer ganttXML = new StringBuffer();
			ganttXML.append("<?xml version=\"1.0\" encoding=\"utf-8\"?> \n");
			ganttXML.append("<xsl:stylesheet\n\txmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\"\n\txmlns:ganttproject=\"http://ganttproject.sf.net/\"\n\tversion=\"1.0\">\n\n");
			ganttXML.append("<ganttproject:report xslfo-path=\""+path+"\">\n\n");
			
			//Project Informations 
			ganttXML.append("\t<ganttproject:project xslfo-path=\""+path+"\"\n");
			ganttXML.append("\t\ttitle=\""+language.getText("ganttReport")+"\"\n");
		    ganttXML.append("\t\tname=\""+GanttProject.correctLabel(language.getText("project"))+"\"\n");
			ganttXML.append("\t\tnameValue=\""+ ((ganttProject.getProjectName().length()==0)?" ":correct(ganttProject.getProjectName())) +"\"\n");
			ganttXML.append("\t\torganisation=\""+GanttProject.correctLabel(language.getText("organization"))+"\"\n");
			ganttXML.append("\t\torganisationValue=\""+ ((ganttProject.getOrganization().length()==0)?" ":correct(ganttProject.getOrganization())) +"\"\n");
			ganttXML.append("\t\twebLink=\""+GanttProject.correctLabel(language.getText("webLink"))+"\"\n");
			ganttXML.append("\t\twebLinkValue=\""+ ((ganttProject.getWebLink().length()==0)?" ":correct(ganttProject.getWebLink())) +"\"\n");
			ganttXML.append("\t\tcurrentDateTimeValue=\"" +df.format( new java.util.Date() ) +"\"\n");
			ganttXML.append("\t\tdescription=\""+GanttProject.correctLabel(language.getText("shortDescription"))+"\">\n");
			ganttXML.append("\t\t<desctiptionValue><![CDATA[\n");
			ganttXML.append("\t\t\t"+ ((ganttProject.getDescription().length()==0)?" ":correct(ganttProject.getDescription())) +"\n");
			ganttXML.append("\t\t]]></desctiptionValue>\n");
			ganttXML.append("\t</ganttproject:project>\n\n");

			//Gantt chart
			ganttXML.append("\t<ganttproject:ganttchart xslfo-path=\""+path+"\" title=\""+language.getText("ganttChart")+"\" src=\""+System.getProperty("java.io.tmpdir")+"/"+"ganttchart.jpg"+"\">\n");
			ganttXML.append("\t</ganttproject:ganttchart>\n\n");

			//Resources chart
			ganttXML.append("\t<ganttproject:resourceschart xslfo-path=\""+path+"\" title=\""+language.getText("resourcesChart")+"\" src=\""+System.getProperty("java.io.tmpdir")+"/"+"resourceschart.jpg"+"\">\n");
			ganttXML.append("\t</ganttproject:resourceschart>\n\n");

			//List of tasks
			ganttXML.append("\t<ganttproject:tasks xslfo-path=\""+path+"\" title=\""+language.getText("tasksList")+"\"\n");
			ganttXML.append("\t\tname=\""+language.getText("name")+"\"\n");
			ganttXML.append("\t\tbegin=\""+language.getText("start")+"\"\n");
			ganttXML.append("\t\tend=\""+language.getText("end")+"\"\n");
			ganttXML.append("\t\tmilestone=\""+language.getText("meetingPoint")+"\"\n");
			ganttXML.append("\t\tprogress=\"%\"\n");
			ganttXML.append("\t\tassigned-to=\"Res.\"\n");
			ganttXML.append("\t\tnotes=\""+language.getText("notes")+"\">\n\n");
			ganttXML.append(writeTasks(tree));
			ganttXML.append("\n\t</ganttproject:tasks>\n\n");
			
			//list of resources
			ganttXML.append("\t<ganttproject:resources xslfo-path=\""+path+"\" title=\""+language.getText("resourcesList")+"\"\n");
			ganttXML.append("\t\tname=\""+language.getText("colName")+"\"\n");
			ganttXML.append("\t\trole=\""+language.getText("colRole")+"\"\n"); 
			ganttXML.append("\t\tmail=\""+language.getText("colMail")+"\"\n");
			ganttXML.append("\t\tphone=\""+language.getText("colPhone")+"\">\n\n");
			ganttXML.append(writeResources(resourceManager));
			ganttXML.append("\t</ganttproject:resources>\n\n");

			ganttXML.append("</ganttproject:report>\n\n");
			ganttXML.append("</xsl:stylesheet>\n");
			
//	==================================================================================================================
			//Uncomment this line to write the temporary xml file on the console
			//System.out.println(ganttXML);
//	==================================================================================================================

			System.out.println("PDF Creation...");
			convert2PDF(ganttXML, pdffile, xslfo);			
			System.out.println("Success!\n");			

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
	

	public static void convert2PDF(StringBuffer ganttXML, File pdf, String xslfo) 
                throws IOException, /*FOPException,*/ TransformerException {
	   
	   
	    System.out.println("XSL : "+xslfo);
		System.out.println("PDF : "+pdf);
        //System.out.println("text:\n"+ganttXML.toString());

	    //Construct driver
        Driver driver = new Driver();
        
        //Setup logger
        Logger logger = new ConsoleLogger(ConsoleLogger.LEVEL_INFO);
       // driver.setLogger(logger);
        //MessageHandler.setScreenLogger(logger);

        //Setup Renderer (output format)        
        driver.setRenderer(Driver.RENDER_PDF);
        
        //Setup output
        OutputStream out = new java.io.FileOutputStream(pdf);

        try {
            FopImageFactory.resetCache();
            Options o = createOptions();
            driver.setOutputStream(out);
            //Setup XSLT
            TransformerFactory factory = TransformerFactory.newInstance();
            Transformer transformer = factory.newTransformer(new StreamSource(xslfo));
        
            //Setup input for XSLT transformation
            Source src = new StreamSource(new StringReader(ganttXML.toString()));
        
            //Resulting SAX events (the generated FO) must be piped through to FOP
            Result res = new SAXResult(driver.getContentHandler());
            //Result res = new StreamResult(new File("report.fo"));

            //Start XSLT transformation and FOP processing
            transformer.transform(src, res);
        }
        catch (FOPException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        catch (TransformerException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        finally {
            out.close();
        }
    }

    private static Options createOptions() throws FOPException {
        JDKFontLocator locator = new JDKFontLocator();
        FontRecord[] fontRecords = locator.getFontRecords();
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        StreamResult output = new StreamResult(outputStream);
        try {
            TransformerHandler handler = getTransformerFactory().newTransformerHandler();
            handler.setResult(output);
            //just for nifty debugging :)
            //handler.getTransformer().setOutputProperty(OutputKeys.INDENT, "yes");
            createConfiguration(handler, fontRecords);
        }
        catch (TransformerConfigurationException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        catch (SAXException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        Options result = new Options(new ByteArrayInputStream(outputStream.toByteArray()));

        //return result;
        System.err.println(outputStream.toString());
        return result;
    }

    private static void createConfiguration(TransformerHandler handler, FontRecord[] fontRecords) throws SAXException {
        AttributesImpl attrs = new AttributesImpl();
        handler.startDocument();
        handler.startElement("", "configuration", "configuration", attrs);
        handler.startElement("", "fonts", "fonts", attrs);

        for (int i=0; i<fontRecords.length; i++) {
            FontRecord nextRecord = fontRecords[i];
            attrs.clear();
            attrs.addAttribute("", "metrics-file", "metrics-file", "CDATA", nextRecord.getMetricsLocation().toString());
            attrs.addAttribute("", "kerning", "kerning", "CDATA", "yes");
            attrs.addAttribute("", "embed-file", "embed-file", "CDATA", nextRecord.getFontLocation().getPath());
            handler.startElement("", "font", "font", attrs);
            writeTriplets(handler, nextRecord.getFontTriplets());
            handler.endElement("", "font", "font");
        }
        handler.endElement("", "fonts", "fonts");
        handler.endElement("", "configuration", "configuration");
        handler.endDocument();
    }

    private static void writeTriplets(TransformerHandler handler, FontTriplet[] fontTriplets) throws SAXException {
        AttributesImpl attrs = new AttributesImpl();
        for (int i=0; i<fontTriplets.length; i++) {
            FontTriplet next = fontTriplets[i];
            attrs.clear();
            attrs.addAttribute("", "name", "name", "CDATA", next.getName());
            attrs.addAttribute("", "style", "style", "CDATA", next.isItalic() ? "italic" : "normal");
            attrs.addAttribute("", "weight", "weight", "CDATA", next.isBold() ? "bold" : "normal");
            handler.startElement("", "font-triplet", "font-triplet", attrs);
            handler.endElement("", "font-triplet", "font-triplet");
        }
    }

    private static SAXTransformerFactory getTransformerFactory() {
        if (ourTransformerFactory==null) {
            ourTransformerFactory = (SAXTransformerFactory)SAXTransformerFactory.newInstance();
        }
        return ourTransformerFactory;
    }

}
