/*
 * Created on 05.07.2003
 *
 */
package net.sourceforge.ganttproject.task;

import java.util.Date;

import net.sourceforge.ganttproject.GanttTask;
//import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyCollection;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.algorithm.AlgorithmCollection;
import net.sourceforge.ganttproject.task.event.TaskListener;
import net.sourceforge.ganttproject.time.TimeUnit;

/**
 * @author bard
 *
 */
public interface TaskManager {
    public Task getRootTask();
    public void clear();
    public GanttTask getTask(int taskId);
    public void registerTask(Task task);
    public GanttTask createTask();
    public GanttTask createTask(int taskId);
	public TaskLength createLength(long length);
    TaskLength createLength(TimeUnit unit, float length);
	public TaskLength createLength(TimeUnit timeUnit, Date startDate, Date endDate);

    TaskDependencyCollection getDependencyCollection();
    AlgorithmCollection getAlgorithmCollection();

    TaskDependencyConstraint createConstraint(int constraintID);

    GPCalendar getCalendar();
    TaskContainmentHierarchyFacade getTaskHierarchy();
    void addTaskListener(TaskListener listener);
    
    public class Access {
        public static TaskManager newInstance(TaskContainmentHierarchyFacade.Factory containmentFacadeFactory, TaskManagerConfig config) {
            return new TaskManagerImpl(containmentFacadeFactory, config);
        }
    }

    public TaskLength getProjectLength();
    public int getTaskCount();
    public Date getProjectStart();
	public TaskManager emptyClone();
	public void importData(TaskManager taskManager);


}
