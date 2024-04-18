package net.sourceforge.ganttproject.importer;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.gui.GanttDialogInfo;

public class ImporterBase {
    protected boolean acceptImport(GanttProject ganttProject) {
        boolean bMerge = true;

        if(ganttProject.projectDocument!=null || ganttProject.askForSave==true)
        {
            GanttDialogInfo gdi = new GanttDialogInfo(
                    ganttProject, GanttDialogInfo.QUESTION,
                    GanttDialogInfo.YES_NO_OPTION, ganttProject.getLanguage().getText("msg17"),
                    ganttProject.getLanguage().getText("question"));
            gdi.show();
            bMerge = (gdi.res == GanttDialogInfo.YES);
        }   
        
        if (!bMerge) {
            if (ganttProject.checkCurrentProject()) {
                ganttProject.closeProject();
                bMerge = true;
            }
        }
        
        return bMerge;        
    }
}
