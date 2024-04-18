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
public class PDFExportData extends ProjectExportData {
    final String myStylesheet;

    public PDFExportData(GanttExportSettings myExportSettings, File myOutputFile, String myProjectName, String myProjectDescription, String myOrganization, HumanResourceManager myResourceManager, TaskContainmentHierarchyFacade myTaskHierarchyFacade, GanttChartExportProcessor myGanttChartExportProcessor, ResourceChartExportProcessor myResourceChartExportProcessor, GanttTree ganttTree, String stylesheet) {
        super(myExportSettings, myOutputFile, myProjectName, myProjectDescription, myOrganization, myResourceManager, myTaskHierarchyFacade, myGanttChartExportProcessor, myResourceChartExportProcessor, ganttTree);
        myStylesheet = stylesheet;
    }
}
