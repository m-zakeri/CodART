package net.sourceforge.ganttproject.task.dependency.constraint;

import java.util.Date;

import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.dependency.TaskDependency.ActivityBinding;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.task.TaskMutator;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.GanttCalendar;
//import net.sourceforge.ganttproject.time.GregorianTimeUnitStack;
import net.sourceforge.ganttproject.language.GanttLanguage;

/**
 * Dependant task finishes not earlier than dependee finishes
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class FinishFinishConstraintImpl extends ConstraintImpl implements TaskDependencyConstraint {
    public FinishFinishConstraintImpl() {
        super(GanttTaskRelationship.FF, GanttLanguage.getInstance().getText("finishfinish"));
    }

    public TaskDependencyConstraint.Collision getCollision() {
        TaskDependencyConstraint.Collision result = null;
        Task dependee = getDependency().getDependee();
        Task dependant = getDependency().getDependant();
        GanttCalendar dependeeEnd = dependee.getEnd();
        GanttCalendar dependantEnd = dependant.getEnd();
        //
        boolean isActive = dependant.isStartFixed() ? dependantEnd.compareTo(dependeeEnd)<0 : dependantEnd.compareTo(dependeeEnd)!=0;

        GanttCalendar acceptableStart = dependant.getStart();
        if (isActive) {
            Task clone = dependee.unpluggedClone();
            TaskMutator mutator = clone.createMutator();
            mutator.shift(-dependant.getDuration().getLength());
            acceptableStart = clone.getEnd();
        }
        
        result = new TaskDependencyConstraint.DefaultCollision(acceptableStart, TaskDependencyConstraint.Collision.START_LATER_VARIATION, isActive);
        return result;
    }

	public ActivityBinding getActivityBinding() {
		TaskActivity[] dependantActivities = getDependency().getDependant().getActivities();
		TaskActivity[] dependeeActivities = getDependency().getDependee().getActivities();
		TaskActivity theDependant = dependantActivities[dependantActivities.length-1];
		TaskActivity theDependee = dependeeActivities[dependeeActivities.length-1];
		return new DependencyActivityBindingImpl(theDependant, theDependee, new Date[] {theDependant.getEnd(), theDependee.getEnd()});
	}
    
    
}
