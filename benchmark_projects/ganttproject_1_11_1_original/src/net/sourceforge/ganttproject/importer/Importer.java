package net.sourceforge.ganttproject.importer;

import java.io.File;

import net.sourceforge.ganttproject.GanttProject;

public interface Importer {

    void run(GanttProject project, File selectedFile);

}
