/*
 * Created on 05.07.2003
 *
 */
package net.sourceforge.ganttproject.task;

import java.awt.Color;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.GanttTask;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.task.algorithm.AdjustTaskBoundsAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.AlgorithmCollection;
import net.sourceforge.ganttproject.task.algorithm.FindPossibleDependeesAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.FindPossibleDependeesAlgorithmImpl;
import net.sourceforge.ganttproject.task.algorithm.ProjectBoundsAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.RecalculateTaskCompletionPercentageAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.RecalculateTaskScheduleAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.ProjectBoundsAlgorithm.Result;
import net.sourceforge.ganttproject.task.dependency.EventDispatcher;
import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyCollection;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyCollectionImpl;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyConstraint;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyException;
import net.sourceforge.ganttproject.task.dependency.constraint.FinishFinishConstraintImpl;
import net.sourceforge.ganttproject.task.dependency.constraint.FinishStartConstraintImpl;
import net.sourceforge.ganttproject.task.dependency.constraint.StartFinishConstraintImpl;
import net.sourceforge.ganttproject.task.dependency.constraint.StartStartConstraintImpl;
import net.sourceforge.ganttproject.task.event.TaskDependencyEvent;
import net.sourceforge.ganttproject.task.event.TaskHierarchyEvent;
import net.sourceforge.ganttproject.task.event.TaskListener;
import net.sourceforge.ganttproject.task.event.TaskPropertyEvent;
import net.sourceforge.ganttproject.task.event.TaskScheduleEvent;
import net.sourceforge.ganttproject.task.hierarchy.TaskHierarchyManagerImpl;
import net.sourceforge.ganttproject.time.DateFrameable;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitDateFrameableImpl;
import net.sourceforge.ganttproject.time.gregorian.GregorianCalendar;

/**
 * @author bard
 *
 */
public class TaskManagerImpl implements TaskManager {
    private final TaskHierarchyManagerImpl myHierarchyManager;
    private final TaskDependencyCollectionImpl myDependencyCollection;
    private final AlgorithmCollection myAlgorithmCollection;
    private final List myListeners = new ArrayList();
    private int myMaxID = -1;
    private Map myId2task = new HashMap();
    private Task myRoot;
    private final TaskManagerConfig myConfig;
    private final TaskContainmentHierarchyFacade.Factory myFacadeFactory;
    private TaskContainmentHierarchyFacade myTaskContainment;
    
    TaskManagerImpl(TaskContainmentHierarchyFacade.Factory containmentFacadeFactory, TaskManagerConfig config) {
        myConfig = config;
        myHierarchyManager = new TaskHierarchyManagerImpl();
        EventDispatcher dispatcher = new EventDispatcher() {
            public void fireDependencyAdded(TaskDependency dep) {
                TaskManagerImpl.this.fireDependencyAdded(dep);
            }

            public void fireDependencyRemoved(TaskDependency dep) {
                TaskManagerImpl.this.fireDependencyRemoved(dep);
            }
        };
        myDependencyCollection = new TaskDependencyCollectionImpl(dispatcher) {
            private TaskContainmentHierarchyFacade myTaskHierarchy;
            
            protected TaskContainmentHierarchyFacade getTaskHierarchy() {
                if (myTaskHierarchy==null) {
                    myTaskHierarchy = TaskManagerImpl.this.getTaskHierarchy();
                }
                return myTaskHierarchy;
            }            
        };
        //clear();
        {
            Date today = GregorianCalendar.getInstance().getTime();
            myRoot =  new GanttTask(null, new GanttCalendar(today), 1, this, -1);
            myRoot.setStart(new GanttCalendar(GregorianCalendar.getInstance().getTime()));
            myRoot.setDuration(createLength(getConfig().getTimeUnitStack().getDefaultTimeUnit(), 1));
			myRoot.setExpand(true);
        	
        }
        myFacadeFactory =
                containmentFacadeFactory==null ?
                new FacadeFactoryImpl(myRoot) : containmentFacadeFactory;

        FindPossibleDependeesAlgorithm alg1 = new FindPossibleDependeesAlgorithmImpl() {
            protected TaskContainmentHierarchyFacade createContainmentFacade() {
                return TaskManagerImpl.this.getTaskHierarchy();
            }

        };
        AdjustTaskBoundsAlgorithm alg3 = new AdjustTaskBoundsAlgorithm() {
            protected TaskContainmentHierarchyFacade createContainmentFacade() {
                return TaskManagerImpl.this.getTaskHierarchy();
            }
        };
        RecalculateTaskScheduleAlgorithm alg2 = new RecalculateTaskScheduleAlgorithm(alg3) {
            protected TaskContainmentHierarchyFacade createContainmentFacade() {
                return TaskManagerImpl.this.getTaskHierarchy();
            }
        };
        RecalculateTaskCompletionPercentageAlgorithm alg4 = new RecalculateTaskCompletionPercentageAlgorithm() {
            protected TaskContainmentHierarchyFacade createContainmentFacade() {
                return TaskManagerImpl.this.getTaskHierarchy();
            }
        };
        ProjectBoundsAlgorithm alg5 = new ProjectBoundsAlgorithm();
        myAlgorithmCollection = new AlgorithmCollection(alg1, alg2, alg3, alg4, alg5);
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.task.TaskManager#getTask(int)
     */
    public GanttTask getTask(int taskId) {
        return (GanttTask)myId2task.get(new Integer(taskId));
    }

    public Task getRootTask() {
        if (myRoot==null) {
        }
        return myRoot;
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.task.TaskManager#clear()
     */
    public void clear() {
        myId2task.clear();
		setMaxID(-1);
        myDependencyCollection.clear();
        {
            Date today = GregorianCalendar.getInstance().getTime();
            myRoot =  new GanttTask(null, new GanttCalendar(today), 1, this, -1);
            myRoot.setStart(new GanttCalendar(GregorianCalendar.getInstance().getTime()));
            myRoot.setDuration(createLength(getConfig().getTimeUnitStack().getDefaultTimeUnit(), 1));
			myRoot.setExpand(true);
        	
        }
    }


    public GanttTask createTask() {
    	return createTask(null);
    }
    
    private GanttTask createTask(GanttTask copy) {
        GanttTask result = createTask(-1, copy);
        return result;    	
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.task.TaskManager#createTask(int)
     */
    public GanttTask createTask(int taskID) {
    	return createTask(taskID, null);
    }
    
    private GanttTask createTask(int taskID, GanttTask copy) {
        GanttTask result = new GanttTask("", new GanttCalendar(), 1, this, taskID);
        if (copy!=null) {
        	result.importData(copy);
        }
        if (result.getTaskID()>=getMaxID()) {
        	setMaxID(result.getTaskID()+1);
        }
        //result.setTaskID(taskID);
        //getTaskHierarchy().move(result, getRootTask());
        //result.move(getRootTask());
        fireTaskAdded(result);
		return result;    	
    }
    
    

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.task.TaskManager#registerTask(net.sourceforge.ganttproject.GanttTask)
     */
    public void registerTask(Task task) {
        int taskID = task.getTaskID();
        if (myId2task.get(new Integer(taskID)) == null) { //if the taskID is not in the map
          myId2task.put(new Integer(taskID), task);
          if (getMaxID() < taskID) {
            setMaxID(taskID+1);
          }
        }
        else { //taskID has been in the map. the newTask will not be added
            throw new RuntimeException("There is a task that already has the ID " + taskID);
        }
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.task.TaskManager#setTask(net.sourceforge.ganttproject.GanttTask)
     */
    public void setTask(Task task) {
    	int taskID = task.getTaskID();
		myId2task.put(new Integer(taskID), task);
		if (taskID > getMaxID()) {
		  setMaxID(taskID);
		}
    }

    
    public int getTaskCount() {
        return myId2task.size();
    }
    
    public TaskLength getProjectLength() {
    	if (myId2task.isEmpty()) {
    		return createLength(getConfig().getTimeUnitStack().getDefaultTimeUnit(), 0);
    	}
        Result result = getAlgorithmCollection().getProjectBoundsAlgorithm().getBounds(myId2task.values());
        return createLength(getConfig().getTimeUnitStack().getDefaultTimeUnit(), result.lowerBound, result.upperBound);
    }
    
    public Date getProjectStart() {
    	if (myId2task.isEmpty()) {
    		return myRoot.getStart().getTime();
    	}
        Result result = getAlgorithmCollection().getProjectBoundsAlgorithm().getBounds(myId2task.values());
        return result.lowerBound;
    }
    
    public TaskLength createLength(TimeUnit unit, float length) {
        return new TaskLengthImpl(unit, length);
    }

	public TaskLength createLength(long count) {
		return new TaskLengthImpl(getConfig().getTimeUnitStack().getDefaultTimeUnit(), count);
	}

	public TaskLength createLength(TimeUnit timeUnit, Date startDate, Date endDate) {
        int sign = 1;
        if (endDate.before(startDate)) {
            Date d = endDate;
            endDate = startDate;
            startDate = d;
            sign = -1;
        }
		TaskLength result;
		if (timeUnit instanceof DateFrameable) {
			DateFrameable df = (DateFrameable) timeUnit;
			int unitCount = 0;
			for (;startDate.before(endDate); unitCount++) {
				startDate = df.adjustRight(startDate);
			}
			result = new TaskLengthImpl(timeUnit, sign*unitCount);
		}
		else{
			throw new IllegalArgumentException("Time unit="+timeUnit+" is not date frameable");
		}
		return result;
	}
    
    public TaskDependencyCollection getDependencyCollection() {
        return myDependencyCollection;
    }

    public AlgorithmCollection getAlgorithmCollection() {
        return myAlgorithmCollection;
    }

    public TaskHierarchyManagerImpl getHierarchyManager() {
        return myHierarchyManager;
    }
    public TaskDependencyConstraint createConstraint(final int constraintID) {
        TaskDependencyConstraint result;
        switch (constraintID) {
            case GanttTaskRelationship.FS: {
                result = new FinishStartConstraintImpl();
                break;
            }
            case GanttTaskRelationship.FF: {
                result = new FinishFinishConstraintImpl();
                break;
            }
            case GanttTaskRelationship.SF: {
                result = new StartFinishConstraintImpl();
                break;
            }
            case GanttTaskRelationship.SS: {
                result = new StartStartConstraintImpl();
                break;
            }
            default: {
                throw new IllegalArgumentException("Unknown constraint ID="+constraintID);
            }
        }
        return result;
    }

    public int getMaxID() {
        return myMaxID;
    }

    private void setMaxID(int id) {
        myMaxID = id;
    }

    void increaseMaxID() {
    	myMaxID++;
    }

    public void addTaskListener(TaskListener listener) {
        myListeners.add(listener);
    }

	public GPCalendar getCalendar() {
		return getConfig().getCalendar();
	}

    public void fireTaskProgressChanged(Task changedTask) {
        TaskPropertyEvent e = new TaskPropertyEvent(changedTask);
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.taskProgressChanged(e);
        }        
    }
    
    void fireTaskScheduleChanged(Task changedTask, GanttCalendar oldStartDate, GanttCalendar oldFinishDate) {
        TaskScheduleEvent e = new TaskScheduleEvent(changedTask, oldStartDate, oldFinishDate, changedTask.getStart(), changedTask.getEnd());
        //List copy = new ArrayList(myListeners);
        //myListeners.clear();
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.taskScheduleChanged(e);
        }
    }

    private void fireDependencyAdded(TaskDependency newDependency) {
        TaskDependencyEvent e = new TaskDependencyEvent(getDependencyCollection(), newDependency);
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.dependencyAdded(e);
        }
    }


    private void fireDependencyRemoved(TaskDependency dep) {
        TaskDependencyEvent e = new TaskDependencyEvent(getDependencyCollection(), dep);
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.dependencyRemoved(e);
        }
    }

    private void fireTaskAdded(Task task) {
        TaskHierarchyEvent e = new TaskHierarchyEvent(this, task, null, getTaskHierarchy().getContainer(task));
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.taskAdded(e);
        }
    }

    private void fireTaskRemoved(Task task, Task oldSupertask) {
        TaskHierarchyEvent e = new TaskHierarchyEvent(this, task, oldSupertask, null);
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.taskRemoved(e);
        }
    }

    void fireTaskPropertiesChanged(Task task) {
        TaskPropertyEvent e = new TaskPropertyEvent(task);
        for (int i=0; i<myListeners.size(); i++) {
            TaskListener next = (TaskListener) myListeners.get(i);
            next.taskPropertiesChanged(e);
        }        
    }
    
    public TaskManagerConfig getConfig() {
        return myConfig;
    }

    private static final class FacadeImpl implements TaskContainmentHierarchyFacade {
        private final Task myRoot;
        private List myPathBuffer = new ArrayList();

        public FacadeImpl(Task root) {
            myRoot = root;
        }

        public Task[] getNestedTasks(Task container) {
            return container.getNestedTasks();
        }

        public Task getRoot() {
            return myRoot;
        }

        public Task getContainer(Task nestedTask) {
            return nestedTask.getSupertask();
        }

        public boolean areUnrelated(Task first, Task second) {
            myPathBuffer.clear();
            for (Task container = getContainer(first); container!=null; container=getContainer(container)) {
                myPathBuffer.add(container);
            }
            if (myPathBuffer.contains(second)) {
                return false;
            }
            myPathBuffer.clear();
            for (Task container = getContainer(second); container!=null; container=getContainer(container)) {
                myPathBuffer.add(container);
            }
            if (myPathBuffer.contains(first)) {
                return false;
            }
            return true;
        }

		public void move(Task whatMove, Task whereMove) {
			whatMove.move(whereMove);
		}
    }

    private static class FacadeFactoryImpl implements TaskContainmentHierarchyFacade.Factory {
    	private final Task myRoot;
		FacadeFactoryImpl(Task root) {
			myRoot = root;
		}
        public TaskContainmentHierarchyFacade createFacede() {
            return new FacadeImpl(myRoot);
        }

    }

	public TaskContainmentHierarchyFacade getTaskHierarchy() {
//		if (myTaskContainment==null) {
			return myFacadeFactory.createFacede();
//		}
//		return myTaskContainment;
	}

	public TaskManager emptyClone() {
		return new TaskManagerImpl(null, myConfig);
	}
	
	public void importData(TaskManager taskManager) {
		Task importRoot = taskManager.getRootTask();
		Map original2imported = new HashMap();
		importData(importRoot, getRootTask(), original2imported);
		TaskDependency[] deps = taskManager.getDependencyCollection().getDependencies();
		for (int i=0; i<deps.length; i++) {
			Task nextDependant = deps[i].getDependant();
			Task nextDependee = deps[i].getDependee();
			Task importedDependant = (Task) original2imported.get(nextDependant);
			Task importedDependee = (Task) original2imported.get(nextDependee);
			try {
				TaskDependency dependency = getDependencyCollection().createDependency(importedDependant, importedDependee);
				dependency.setConstraint(deps[i].getConstraint());
			} catch (TaskDependencyException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	private void importData(Task importRoot, Task root, Map original2imported) {
        myId2task.put(new Integer(root.getTaskID()), root);
		Task[] nested = importRoot.getManager().getTaskHierarchy().getNestedTasks(importRoot);
		for (int i=nested.length-1; i>=0; i--) {
			Task nextImported = createTask((GanttTask) nested[i]);
			original2imported.put(nested[i], nextImported);
			//nextImported.move(root);
			getTaskHierarchy().move(nextImported, root);
			importData(nested[i], nextImported, original2imported);
		}
	}

	public Date findClosestWorkingTime(Date time) {
		return getCalendar().findClosestWorkingTime(time);
	}



}
