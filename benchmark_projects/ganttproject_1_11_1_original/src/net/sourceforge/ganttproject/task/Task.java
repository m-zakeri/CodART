package net.sourceforge.ganttproject.task;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttTaskRelationship;
//import net.sourceforge.ganttproject.shape.Shape;
import net.sourceforge.ganttproject.shape.ShapePaint;
//import net.sourceforge.ganttproject.task.dependency.TaskDependencyCollection;
//import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.task.dependency.TaskDependencySlice;
import net.sourceforge.ganttproject.time.TimeUnit;

import java.awt.*;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 27.01.2004
 */
public interface Task extends MutableTask {    
    TaskMutator createMutator();

    // main properties
    int getTaskID();
    String getName();
    boolean isMilestone();
    int getPriority();
    TaskActivity[] getActivities();    
    GanttCalendar getStart();
    GanttCalendar getEnd();
    TaskLength getDuration();
    TaskLength translateDuration(TaskLength duration);
    int getCompletionPercentage();
    boolean isStartFixed();
    ShapePaint getShape();
    Color getColor();
    String getNotes();
	boolean getExpand();
	
    //
    // relationships with other entities
    GanttTaskRelationship[] getPredecessors();
    GanttTaskRelationship[] getSuccessors();
    //HumanResource[] getAssignedHumanResources();
    ResourceAssignment[] getAssignments();
    TaskDependencySlice getDependencies();
    TaskDependencySlice getDependenciesAsDependant();
    TaskDependencySlice getDependenciesAsDependee();
    ResourceAssignmentCollection getAssignmentCollection();

    //
    Task getSupertask();
    Task[] getNestedTasks();
    void move(Task targetSupertask);
    void delete();
    
    TaskManager getManager();

    Task unpluggedClone();
    Color DEFAULT_COLOR = new Color( 140, 182, 206);
}
