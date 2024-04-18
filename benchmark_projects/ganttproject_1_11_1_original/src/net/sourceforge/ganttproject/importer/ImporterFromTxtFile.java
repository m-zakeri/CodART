package net.sourceforge.ganttproject.importer;

import java.io.File;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.io.GanttTXTOpen;

public class ImporterFromTxtFile extends ImporterBase implements Importer {    
    public void run(GanttProject project, File selectedFile) {
        if (acceptImport(project)) {
            GanttTXTOpen opener = new GanttTXTOpen(project.getTree(), project,
                    project.getArea(), project.getTaskManager());
            opener.load(selectedFile);
            project.setAskForSave(true);
            
        }
    }

}
