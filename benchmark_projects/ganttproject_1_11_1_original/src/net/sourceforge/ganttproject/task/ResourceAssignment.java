package net.sourceforge.ganttproject.task;

import net.sourceforge.ganttproject.resource.ProjectResource;


/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 05.02.2004
 */
public interface ResourceAssignment {
    Task getTask();
    ProjectResource getResource();
    float getLoad();
    void setLoad(float load);
    void delete();
}
