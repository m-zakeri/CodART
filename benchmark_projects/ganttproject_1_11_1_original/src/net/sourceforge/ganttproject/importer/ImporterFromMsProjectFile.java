package net.sourceforge.ganttproject.importer;

import java.io.File;
import java.io.IOException;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.document.Document;
import net.sourceforge.ganttproject.document.FileDocument;
import net.sourceforge.ganttproject.gui.GanttDialogInfo;

import net.sourceforge.ganttproject.io.GanttMPPOpen;
import net.sourceforge.ganttproject.io.GanttMPXJOpen;
import net.sourceforge.ganttproject.io.GanttMPXOpen;
import net.sourceforge.ganttproject.io.GanttMSPDIOpen;


public class ImporterFromMsProjectFile extends ImporterBase implements Importer 
{

	public void run(GanttProject project, File selectedFile) 
	{
        if (acceptImport(project)) 
				{
            Document document = getDocument(selectedFile);
            openDocument(project, document);
        }

  }

	protected Document getDocument(File selectedFile) 
	{
    	return new FileDocument(selectedFile);
  }


	 protected void openDocument(GanttProject project, Document document) 
	 {
	 		try 
      {
    		GanttMPXJOpen open = null ;
				
				if(document.getPath().toLowerCase().endsWith(".mpp"))
					open = new GanttMPPOpen(project.getTree(), project);
				else /*if(document.getPath().toLowerCase().endsWith(".mpx"))*/
					open = new GanttMPXOpen(project.getTree(), project);
				/*else 
					open = new GanttMSPDIOpen(project.getTree(), project);*/
				

					
				open.load(document.getInputStream());
				
			} catch (IOException e)
        {
            GanttDialogInfo gdi = new GanttDialogInfo(project,
                    GanttDialogInfo.ERROR, GanttDialogInfo.YES_OPTION,
                    project.getLanguage().getText("msg2") + "\n"
                            + document.getDescription(), project.getLanguage()
                            .getText("error"));
            gdi.show();
        }
   }

}
