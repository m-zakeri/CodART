package net.sourceforge.ganttproject.action;

import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.language.GanttLanguage;

import javax.swing.AbstractAction;
/**
  * Special action for resources
  */
abstract class ResourceAction extends AbstractAction {
    public ResourceAction(ResourceManager hrManager) {
        myManager = hrManager;
    }

    protected ResourceManager getManager() {
        return myManager;
    }
    
    protected GanttLanguage getLanguage() {
        return GanttLanguage.getInstance();
    }

    private ResourceManager myManager;
}	
