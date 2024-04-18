package net.sourceforge.ganttproject;

import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.roles.RoleManager;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.time.TimeUnitStack;

/**
 * This interface represents a project as a logical business entity, without any UI 
 * (except some configuration options :)
 * @author bard
 *
 */
public interface IGanttProject {
    String getProjectName();
    void setProjectName(String projectName);
    //
    String getDescription();
    void setDescription(String description);
    //
    String getOrganization();    
    void setOrganization(String organization);
    //
    String getWebLink();   
    void setWebLink(String webLink);
    //
    /**
     * Creates a new task and performs all necessary initialization procedures
     * such as changing properties of parent task, adjusting schedule, etc.
     */
    Task newTask();
    //
    GanttLanguage getI18n();
    UIConfiguration getUIConfiguration();
    ResourceManager getHumanResourceManager();
    RoleManager getRoleManager();
    TaskManager getTaskManager();
    TaskContainmentHierarchyFacade getTaskContainment();
	GPCalendar getActiveCalendar();    
    TimeUnitStack getTimeUnitStack();
    void setModified();
    String getDTDVersion();
}