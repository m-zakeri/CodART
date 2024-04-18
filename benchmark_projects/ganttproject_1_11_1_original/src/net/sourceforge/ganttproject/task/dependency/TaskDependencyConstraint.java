package net.sourceforge.ganttproject.task.dependency;

import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.GanttCalendar;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 * Date: 14.02.2004
 * Time: 2:35:20
 * To change this template use File | Settings | File Templates.
 */
public interface TaskDependencyConstraint {
    void setTaskDependency(TaskDependency dependency);
//    boolean isFulfilled();
//    void fulfil();
    Collision getCollision();
    String getName();
    int getID();
    TaskDependency.ActivityBinding getActivityBinding();
    interface Collision {
        GanttCalendar getAcceptableStart();
        int getVariation();

        int NO_VARIATION = 0;
        int START_EARLIER_VARIATION = -1;
        int START_LATER_VARIATION = 1;

        boolean isActive();
    }

    class DefaultCollision implements Collision {
        private final GanttCalendar myAcceptableStart;
        private final int myVariation;
        private final boolean isActive;

        public DefaultCollision(GanttCalendar myAcceptableStart, int myVariation, boolean isActive) {
            this.myAcceptableStart = myAcceptableStart;
            this.myVariation = myVariation;
            this.isActive = isActive;
        }

        public GanttCalendar getAcceptableStart() {
            return myAcceptableStart;
        }

        public int getVariation() {
            return myVariation;
        }

        public boolean isActive() {
            return isActive;
        }
    }
}
