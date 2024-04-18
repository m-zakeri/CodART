package net.sourceforge.ganttproject.task.dependency;

public interface TaskDependencySlice {
    TaskDependency[] toArray();
    void clear();
}
