package net.sourceforge.ganttproject.export;

import net.sourceforge.ganttproject.GanttExportSettings;
import net.sourceforge.ganttproject.GanttGraphicArea;
import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.GanttTree;
import net.sourceforge.ganttproject.PrjInfos;
import net.sourceforge.ganttproject.ResourceLoadGraphicArea;

/**
 * @deprecated This class is just a value object which is used for passing 
 * export parameters to export routines. It should be thrown away after 
 * export subsystem refactoring
 * 
 * @author bard
 * @created 13.09.2004
 */
public class DeprecatedProjectExportData {
    final String myFilename;
    final GanttProject myProject;
    final GanttTree myTree;
    final GanttGraphicArea myGanttChart;
    final ResourceLoadGraphicArea myResourceChart;
    final GanttExportSettings myExportOptions;
    final String myXslFoScript;
    
    
    public DeprecatedProjectExportData(final String myFilename,
            final GanttProject myProject, final GanttTree myTree,
            final GanttGraphicArea myGanttChart,
            final ResourceLoadGraphicArea myResourceChart,
            final GanttExportSettings myExportOptions,
            final String myXslFoScript) {
        super();
        this.myFilename = myFilename;
        this.myProject = myProject;
        this.myTree = myTree;
        this.myGanttChart = myGanttChart;
        this.myResourceChart = myResourceChart;
        this.myExportOptions = myExportOptions;
        this.myXslFoScript = myXslFoScript;
    }
}
