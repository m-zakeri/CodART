/*
LICENSE:
                                                                 
   This program is free software; you can redistribute it and/or modify  
   it under the terms of the GNU General Public License as published by  
   the Free Software Foundation; either version 2 of the License, or     
   (at your option) any later version.                                   
                                                                         
   Copyright (C) 2004, GanttProject Development Team
 */ 
package net.sourceforge.ganttproject.task.algorithm;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.task.TaskLength;

/**
 * @author bard

 */
public abstract class AdjustTaskBoundsAlgorithm extends AlgorithmBase {
	private Set myModifiedTasks = new HashSet();
    public void run(Task task) {
		run(new Task[] {task});
	}
	public void run(Task[] tasks) {
        if (!isEnabled()) {
            return;
        }
		HashSet taskSet = new HashSet(Arrays.asList(tasks));
        myModifiedTasks.addAll(taskSet);
		TaskContainmentHierarchyFacade containmentFacade = createContainmentFacade();
		while (!taskSet.isEmpty()) {
			recalculateSupertaskScheduleBottomUp(taskSet, containmentFacade);
			taskSet.clear();
			for (Iterator modified = myModifiedTasks.iterator(); modified.hasNext();) {
				Task nextTask = (Task)modified.next();
				Task supertask = containmentFacade.getContainer(nextTask);
				if (supertask!=null) {
					taskSet.add(supertask);
				}
			}
            myModifiedTasks.clear();
		}
        myModifiedTasks.clear();
	}
	
    private void recalculateSupertaskScheduleBottomUp(Set supertasks, TaskContainmentHierarchyFacade containmentFacade) {
		for (Iterator it = supertasks.iterator(); it.hasNext();) {
			Task nextSupertask = (Task) it.next();
			recalculateSupertaskSchedule(nextSupertask, containmentFacade);
		}
	}

	private void recalculateSupertaskSchedule(Task supertask, TaskContainmentHierarchyFacade containmentFacade) {
		Task[] nested = containmentFacade.getNestedTasks(supertask);
        if (nested.length==0) {
            return;
        }
        GanttCalendar maxEnd = null;
        GanttCalendar minStart = null;
		for (int i=0; i<nested.length; i++) {
			Task nextNested = nested[i];
			GanttCalendar nextStart = nextNested.getStart();
            if (minStart==null || nextStart.compareTo(minStart) < 0) {
                minStart = nextStart;
            }
			GanttCalendar nextEnd = nextNested.getEnd();
			if (maxEnd==null || nextEnd.compareTo(maxEnd) > 0) {
				maxEnd = nextEnd;
			}
		}
		if (minStart.compareTo(supertask.getStart())!=0) {
			modifyTaskStart(supertask, minStart);
		}
		if (maxEnd.compareTo(supertask.getEnd())!=0) {
			modifyTaskEnd(supertask, maxEnd);
		}
	}

	private void modifyTaskStart(Task task, GanttCalendar newStart) {
		TaskLength duration = task.getDuration();
		task.setStart(newStart);
		task.setDuration(duration);
		myModifiedTasks.add(task);
	}

	private void modifyTaskEnd(Task task, GanttCalendar taskEnd) {
		task.setEnd(taskEnd);
		myModifiedTasks.add(task);
	}

	protected abstract TaskContainmentHierarchyFacade createContainmentFacade();

}
