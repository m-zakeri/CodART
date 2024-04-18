package net.sourceforge.ganttproject.task.dependency;

import net.sourceforge.ganttproject.task.Task;

public class TaskDependencySliceImpl implements TaskDependencySlice {
    private final Task myTask;
    private final TaskDependencyCollection myDependencyCollection;

    public TaskDependencySliceImpl(Task task, TaskDependencyCollection dependencyCollection) {
        myTask = task;
        myDependencyCollection = dependencyCollection;
    }

    public TaskDependency[] toArray() {
        return myDependencyCollection.getDependencies(myTask);
    }

    public void clear() {
        TaskDependency[] deps = toArray();
        for (int i=0; i<deps.length; i++) {
            deps[i].delete();
        }
    }

    protected Task getTask() {
        return myTask;
    }

    protected TaskDependencyCollection getDependencyCollection() {
        return myDependencyCollection;
    }
}
