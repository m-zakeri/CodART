package net.sourceforge.ganttproject.importer;

import java.io.File;
import java.io.IOException;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.document.Document;
import net.sourceforge.ganttproject.document.FileDocument;
import net.sourceforge.ganttproject.gui.GanttDialogInfo;
import net.sourceforge.ganttproject.io.GanttXMLOpen;
import net.sourceforge.ganttproject.parser.AllocationTagHandler;
import net.sourceforge.ganttproject.parser.DependencyTagHandler;
import net.sourceforge.ganttproject.parser.ResourceTagHandler;
import net.sourceforge.ganttproject.parser.RoleTagHandler;
import net.sourceforge.ganttproject.parser.TaskTagHandler;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.roles.RoleManager;
import net.sourceforge.ganttproject.roles.RoleManagerImpl;
import net.sourceforge.ganttproject.task.TaskManager;

public class ImporterFromGanttFile extends ImporterBase implements Importer {

    public void run(GanttProject project, File selectedFile) {
        if (acceptImport(project)) {
            Document document = getDocument(selectedFile);
            openDocument(project, document);
        }
    }

    public void run(GanttProject project, Document document) {
        openDocument(project, document);
    }
    
    protected Document getDocument(File selectedFile) {
    	return new FileDocument(selectedFile);
    }
    
    protected void openDocument(GanttProject project, Document document) {
        try 
        {
            TaskManager taskManager = project.getTaskManager().emptyClone();
            //ResourceManager resourceManager = project.getHumanResourceManager();
            ResourceManager resourceManager = new HumanResourceManager(project.getRoleManager().getDefaultRole());
            RoleManager roleManager = new RoleManagerImpl();
            GanttXMLOpen opener = new GanttXMLOpen(project.getTree(), project,
                project.getResourcePanel(), project.getArea(), taskManager,true);
            opener.addTagHandler(opener.getDefaultTagHandler());
            TaskTagHandler taskHandler = new TaskTagHandler(taskManager, opener.getContext());
            opener.addTagHandler(taskHandler);
            ResourceTagHandler resourceHandler = new ResourceTagHandler(resourceManager, roleManager);
            opener.addTagHandler(resourceHandler);
            DependencyTagHandler dependencyHandler = new DependencyTagHandler(opener.getContext(), taskManager);
            opener.addTagHandler(dependencyHandler);
            RoleTagHandler roleHandler = new RoleTagHandler(roleManager);
            opener.addTagHandler(roleHandler);
            opener.addParsingListener(dependencyHandler);
            opener.addParsingListener(resourceHandler);
            AllocationTagHandler allocationHandler = new AllocationTagHandler(resourceManager, taskManager);
            opener.addTagHandler(allocationHandler);
            //
            opener.load(document.getInputStream());
            project.getRoleManager().importData(roleManager);
            project.getHumanResourceManager().importData(resourceManager);
            project.getTaskManager().importData(taskManager);
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
