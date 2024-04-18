/***************************************************************************
GanttCSVExport.java
-----------------
begin                : 7 juil. 2004
copyright            : (C) 2004 by Thomas Alexandre
email                : alexthomas@ganttproject.org
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
import java.util.ArrayList;
import java.util.Iterator;

import javax.swing.tree.DefaultMutableTreeNode;

import net.sourceforge.ganttproject.GanttResourcePanel;
import net.sourceforge.ganttproject.GanttTask;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.PrjInfos;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.roles.Role;
import net.sourceforge.ganttproject.task.ResourceAssignment;

/**
 * @author athomas
 *
 * Class to export the project in cvs text format
 */
public class GanttCSVExport 
{
	private GanttTree tree;
	private GanttResourcePanel peop;
	private PrjInfos prjInfos;
	private CSVOptions csvOptions;
	
	ArrayList lot = new ArrayList();
	ArrayList resources = new ArrayList();
	
	int iMaxSize=0;
	
	boolean bFixedSize = false;
	
	/** Constructor. */
	public GanttCSVExport(PrjInfos prjInfos, GanttTree tree,
            GanttResourcePanel peop, CSVOptions csvOptions)
	{
		this.tree = tree;
	    this.peop = peop;
	    this.prjInfos = prjInfos;		
	    this.csvOptions = csvOptions;
	    
	}
	
	/** Save the project as CSV on a stream */
	public void save(OutputStream stream) {
		try {
			OutputStreamWriter out = new OutputStreamWriter(stream);
			beginToSave(out);
			out.close();
		} catch (IOException e) {
			System.out.println("Error in saving the csv file");
		} catch (Exception e) {
			System.out.println(e);
			e.printStackTrace();
		}
	}
	
	/** Start saving the csv document. */
	public void beginToSave(OutputStreamWriter out) throws IOException 
	{
		lot = tree.getAllTasks();
		resources = peop.getPeople();
	    
		
		bFixedSize = csvOptions.bFixedSize;
		
		if(csvOptions.bFixedSize)
			getMaxSize();
		
		/*writeProjectInfos(out);
		out.write("\n");*/
	    
		
		
		writeTasks(out);
	    out.write("\n");
	    writeResources(out);
	    out.write("\n");
	}
	
	/** Write the project information on the file. */
	private void writeProjectInfos(OutputStreamWriter out) throws IOException 
	{
		
	}
	
	/** Write all tasks. */
	private void writeTasks(OutputStreamWriter out) throws IOException 
	{
//		parse all tasks	
	    for(Iterator it=lot.iterator(); it.hasNext();)
		{
			DefaultMutableTreeNode node = (DefaultMutableTreeNode) it.next();
			if(!node.isRoot())
			{
				GanttTask task = (GanttTask)(node.getUserObject());
				
				//ID
				if(csvOptions.bExportTaskID)
					out.write(correctField(""+task.getTaskID())+
							(bFixedSize?"":csvOptions.sSeparatedChar));
					
				//Name
				if(csvOptions.bExportTaskName)
					out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
							correctField(getName(node, task))+
							(bFixedSize?"":csvOptions.sSeparatedTextChar+
							csvOptions.sSeparatedChar));
				
				//Start Date
				if(csvOptions.bExportTaskStartDate)
					out.write(correctField(task.getStart().toString())+
							(bFixedSize?"":csvOptions.sSeparatedChar));
				
				//End Date
				if(csvOptions.bExportTaskEndDate)
					out.write(correctField(task.getEnd().toString())+
							(bFixedSize?"":csvOptions.sSeparatedChar));
				
				//Duration
				if(csvOptions.bExportTaskDuration)
					out.write(correctField(""+task.getLength())+
							(bFixedSize?"":csvOptions.sSeparatedChar));
				
				//Percent complete
				if(csvOptions.bExportTaskPercent)
					out.write(correctField(""+task.getCompletionPercentage())+
							(bFixedSize?"":csvOptions.sSeparatedChar));				

				//Web Link
				if(csvOptions.bExportTaskWebLink)
					out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
							correctField(getWebLink(task))+
							(bFixedSize?"":csvOptions.sSeparatedTextChar+
							csvOptions.sSeparatedChar));				
				
				//associated resources
				if(csvOptions.bExportTaskResources) {
					out.write((bFixedSize?"":csvOptions.sSeparatedTextChar));					
					out.write(correctField(getAssignments(task)));					
					out.write((bFixedSize?"":csvOptions.sSeparatedTextChar+
							csvOptions.sSeparatedChar));
				}
				
				//Notes
				if(csvOptions.bExportTaskNotes)
					out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
							correctField(task.getNotes())+
							(bFixedSize?"":csvOptions.sSeparatedTextChar+
							csvOptions.sSeparatedChar));
				
				out.write("\n");
			}
		}	    
	} //end of write tasks
	 
	/** write the resources. */
	private void writeResources(OutputStreamWriter out) throws IOException 
	{
		//parse all resources
		for (int i = 0; i < resources.size(); i++)
	    {
	    	HumanResource p = (HumanResource) resources.get(i);
	    	
	    	//ID
			if(csvOptions.bExportResourceID)
				out.write(correctField(""+p.getId())+
						(bFixedSize?"":csvOptions.sSeparatedChar));
			//Name
			if(csvOptions.bExportResourceName)
				out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
						correctField(p.getName())+
						(bFixedSize?"":csvOptions.sSeparatedTextChar+
						csvOptions.sSeparatedChar));
			//Mail
			if(csvOptions.bExportResourceMail)
				out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
						correctField(p.getMail())+
						(bFixedSize?"":csvOptions.sSeparatedTextChar+
						csvOptions.sSeparatedChar));
			//Phone
			if(csvOptions.bExportResourcePhone)
				out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
						correctField(p.getPhone())+
						(bFixedSize?"":csvOptions.sSeparatedTextChar+
						csvOptions.sSeparatedChar));
			//Role
			if(csvOptions.bExportResourcePhone) {
				Role role = p.getRole();
		        String sRoleID = "0";
		        if(role != null) sRoleID = role.getPersistentID();
		        
				out.write((bFixedSize?"":csvOptions.sSeparatedTextChar)+
						correctField(sRoleID)+
						(bFixedSize?"":csvOptions.sSeparatedTextChar+
						csvOptions.sSeparatedChar));
			}
			out.write("\n");
	    }
	} //end of write resources
	
	/**set the maximum size for all strings. */
	void getMaxSize()
	{
		iMaxSize = 0;
		for(Iterator it=lot.iterator(); it.hasNext();)
	    {
			DefaultMutableTreeNode node = (DefaultMutableTreeNode) it.next();
			if(!node.isRoot())
			{
				GanttTask task = (GanttTask)(node.getUserObject());

				if(csvOptions.bExportTaskID){
					String s=""+task.getTaskID();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskName){
					String s=""+getName(node, task);
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskStartDate){
					String s=""+task.getStart();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskEndDate){
					String s=""+task.getEnd();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskDuration){
					String s=""+task.getLength();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskPercent){
					String s=""+task.getCompletionPercentage();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskWebLink){
					String s=""+getWebLink(task);
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskResources){
					String s=""+getAssignments(task);
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}
				
				if(csvOptions.bExportTaskNotes){
					String s=""+task.getNotes();
					if(s.length()>iMaxSize)iMaxSize=s.length();
				}	
				
			}
	    }
		
		//parse all resources
		for (int i = 0; i < resources.size(); i++)
		{
		   	HumanResource p = (HumanResource) resources.get(i);
		   	
		   	if(csvOptions.bExportResourceID){
				String s=""+p.getId();
				if(s.length()>iMaxSize)iMaxSize=s.length();
			}
		   	if(csvOptions.bExportResourceName){
				String s=""+p.getName();
				if(s.length()>iMaxSize)iMaxSize=s.length();
			}
		   	if(csvOptions.bExportResourceMail){
				String s=""+p.getMail();
				if(s.length()>iMaxSize)iMaxSize=s.length();
			}
		   	if(csvOptions.bExportResourcePhone){
				String s=""+p.getPhone();
				if(s.length()>iMaxSize)iMaxSize=s.length();
			}
		   	if(csvOptions.bExportResourceRole){
		   		Role role = p.getRole();
		        String sRoleID = "0";
		        if(role != null) sRoleID = role.getPersistentID();
				String s=""+sRoleID;
				if(s.length()>iMaxSize)iMaxSize=s.length();
			}
		}
		
	} //get maxIndentation end
	
	/**@return the name of task with the correct level.*/
	private String getName(DefaultMutableTreeNode node, GanttTask task)
	{
		if(bFixedSize) return task.getName();
		String res="";
		for(int i=0;i<node.getLevel();i++)
			res+="  ";
		return res+task.getName();
	}
	
	/**@return the link of the task. */
	private String getWebLink(GanttTask task)
	{
		return (task.getWebLink().equals("http://")?"":task.getWebLink());
	}
	
	/** @return the list of the assignment for the resources. */
	private String getAssignments(GanttTask task)
	{
		String res = "";
		ResourceAssignment[] assignment = task.getAssignments();
		for(int i=0;i<assignment.length;i++)
			res+=(assignment[i].getResource()+(i==assignment.length-1?"":
					csvOptions.sSeparatedChar.equals(";")?",":";"));
		return res;
	}
	
	private String correctField(String field)
	{
		String res="";
		for(int i=0;i<iMaxSize-field.length();i++)
			res+=" ";
		res+=field;
		return res;
	}
	
}

