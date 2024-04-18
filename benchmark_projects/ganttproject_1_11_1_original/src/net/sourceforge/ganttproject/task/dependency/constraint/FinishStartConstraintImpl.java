package net.sourceforge.ganttproject.task.dependency.constraint;

import java.util.Date;

import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.dependency.TaskDependency.ActivityBinding;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
//import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.language.GanttLanguage;

/**
 * Dependant task starts not earlier than dependee finishes
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class FinishStartConstraintImpl extends ConstraintImpl implements TaskDependencyConstraint {
    public FinishStartConstraintImpl() {
        super(GanttTaskRelationship.FS, GanttLanguage.getInstance().getText("finishstart"));
    }

    public TaskDependencyConstraint.Collision getCollision() {
        TaskDependencyConstraint.Collision result = null;
        Task dependee = getDependency().getDependee();
        Task dependant = getDependency().getDependant();
        GanttCalendar dependeeEnd = dependee.getEnd();
        GanttCalendar dependantStart = dependant.getStart();
        boolean isActive = dependant.isStartFixed() ?
                dependeeEnd.compareTo(dependantStart)>0 :
                dependeeEnd.compareTo(dependantStart)!=0;
        //new Exception("[FinishStartConstraint] isActive="+isActive+" dependdee="+dependee+" end="+dependeeEnd+" start="+dependantStart).printStackTrace();
        result = new TaskDependencyConstraint.DefaultCollision(dependeeEnd, TaskDependencyConstraint.Collision.START_LATER_VARIATION, isActive);
        return result;
    }
    
	public ActivityBinding getActivityBinding() {
		TaskActivity[] dependantActivities = getDependency().getDependant().getActivities();
		TaskActivity[] dependeeActivities = getDependency().getDependee().getActivities();
		TaskActivity theDependant = dependantActivities[0];
		TaskActivity theDependee = dependeeActivities[dependeeActivities.length-1];
		return new DependencyActivityBindingImpl(theDependant, theDependee, new Date[] {theDependant.getStart(),theDependee.getEnd()});
	}
    
}
