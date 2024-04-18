package net.sourceforge.ganttproject.task;


/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 27.01.2004
 */
public interface TaskMutator extends MutableTask {
    void commit();
    void shift(float unitCount);
    int getCompletionPercentage();

    
}
