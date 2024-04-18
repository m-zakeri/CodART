package net.sourceforge.ganttproject.task.dependency.constraint;

import net.sourceforge.ganttproject.task.dependency.TaskDependency;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class ConstraintImpl {
    private final int myID;
    private final String myName;
    private TaskDependency myDependency;

    public ConstraintImpl(int myID, String myName) {
        this.myID = myID;
        this.myName = myName;
    }

    protected TaskDependency getDependency() {
        return myDependency;
    }

    public void setTaskDependency(TaskDependency dependency) {
        myDependency = dependency;
    }

    public String getName() {
        return myName;
    }

    public int getID() {
        return myID;
    }

    public String toString() {
        return getName();
    }
}
