package net.sourceforge.ganttproject.task.dependency;

import net.sourceforge.ganttproject.task.Task;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public interface MutableTaskDependencyCollection {
    void clear();

    TaskDependency createDependency(Task dependant, Task dependee) throws TaskDependencyException;
    void deleteDependency(TaskDependency dependency);
}
