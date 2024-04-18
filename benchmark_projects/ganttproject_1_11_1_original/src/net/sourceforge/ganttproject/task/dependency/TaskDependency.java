package net.sourceforge.ganttproject.task.dependency;

import java.util.Date;

import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 * Date: 14.02.2004
 * Time: 2:32:17
 * To change this template use File | Settings | File Templates.
 */
public interface TaskDependency {
    Task getDependant();
    Task getDependee();
    void setConstraint(TaskDependencyConstraint constraint);
    TaskDependencyConstraint getConstraint();
    ActivityBinding getActivityBinding();
    void delete();    
    
    interface ActivityBinding {
    	TaskActivity getDependantActivity();
    	TaskActivity getDependeeActivity();
    	Date[] getAlignedBounds();
    }
}
