package net.sourceforge.ganttproject.task;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public interface TaskContainmentHierarchyFacade {
    Task[] getNestedTasks(Task container);
    Task getRoot();

    Task getContainer(Task nestedTask);
    void move(Task whatMove, Task whereMove);
    interface Factory {
        TaskContainmentHierarchyFacade createFacede();
    }

    boolean areUnrelated(Task dependant, Task dependee);
}
