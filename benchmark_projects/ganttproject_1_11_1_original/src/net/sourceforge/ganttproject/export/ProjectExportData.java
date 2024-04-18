/*
LICENSE:
                                                                 
   This program is free software; you can redistribute it and/or modify  
   it under the terms of the GNU General Public License as published by  
   the Free Software Foundation; either version 2 of the License, or     
   (at your option) any later version.                                   
                                                                         
   Copyright (C) 2004, GanttProject Development Team
 */
package net.sourceforge.ganttproject.export;

import net.sourceforge.ganttproject.GanttExportSettings;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.resource.HumanResourceManager;

import java.io.File;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 */
public class ProjectExportData {
    final GanttExportSettings myExportSettings;
    final File myOutputFile;
    final String myProjectName;
    final String myProjectDescription;
    final String myOrganization;
    final HumanResourceManager myResourceManager;
    final TaskContainmentHierarchyFacade myTaskHierarchyFacade;
    final GanttChartExportProcessor myGanttChartExportProcessor;
    final ResourceChartExportProcessor myResourceChartExportProcessor;
    final GanttTree myGanttTree;
    
    public ProjectExportData(GanttExportSettings myExportSettings, File myOutputFile, String myProjectName, String myProjectDescription, String myOrganization, HumanResourceManager myResourceManager, TaskContainmentHierarchyFacade myTaskHierarchyFacade, GanttChartExportProcessor myGanttChartExportProcessor, ResourceChartExportProcessor myResourceChartExportProcessor, GanttTree ganttTree) {
        this.myExportSettings = myExportSettings;
        this.myOutputFile = myOutputFile;
        this.myProjectName = myProjectName;
        this.myProjectDescription = myProjectDescription;
        this.myOrganization = myOrganization;
        this.myResourceManager = myResourceManager;
        this.myTaskHierarchyFacade = myTaskHierarchyFacade;
        this.myGanttChartExportProcessor = myGanttChartExportProcessor;
        this.myResourceChartExportProcessor = myResourceChartExportProcessor;
        this.myGanttTree = ganttTree;
    }
}
