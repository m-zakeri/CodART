package net.sourceforge.ganttproject.task.dependency.constraint;

import java.util.Date;

import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.dependency.TaskDependency.ActivityBinding;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.language.GanttLanguage;

/**
 * Dependant task starts not earlier than dependee starts
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class StartStartConstraintImpl extends ConstraintImpl implements TaskDependencyConstraint {
    public StartStartConstraintImpl() {
        super(GanttTaskRelationship.SS, GanttLanguage.getInstance().getText("startstart"));
    }

    public TaskDependencyConstraint.Collision getCollision() {
        TaskDependencyConstraint.Collision result = null;
        Task dependee = getDependency().getDependee();
        Task dependant = getDependency().getDependant();
        GanttCalendar dependeeStart = dependee.getStart();
        GanttCalendar dependantStart = dependant.getStart();
        //
        boolean isActive = dependant.isStartFixed() ?
                dependantStart.compareTo(dependeeStart)<0 :
                dependantStart.compareTo(dependeeStart)!=0;
        GanttCalendar acceptableStart = dependee.getStart();
        result = new TaskDependencyConstraint.DefaultCollision(acceptableStart, TaskDependencyConstraint.Collision.START_LATER_VARIATION, isActive);
        return result;
    }

	public ActivityBinding getActivityBinding() {
		TaskActivity[] dependantActivities = getDependency().getDependant().getActivities();
		TaskActivity[] dependeeActivities = getDependency().getDependee().getActivities();
		TaskActivity theDependant = dependantActivities[0];
		TaskActivity theDependee = dependeeActivities[0];
		return new DependencyActivityBindingImpl(theDependant, theDependee, new Date[] {theDependant.getStart(), theDependee.getStart()});
	}
    

}
