/*
 * Created on 20.11.2004
 */
package net.sourceforge.ganttproject;

import net.sourceforge.ganttproject.task.Task;

/** Class to store parameters of each task (pixel to start, end y value...*/

class GanttPaintParam {
	public int x1 /**start of task*/
	,
	x2, x3;
	/** End of task*/

	public int y;
	private int type; //0->Meeting task,   1 mother task,  2 normal task
	private final Task myTask;

	public GanttPaintParam(Task task, int x1, int x2, int x3,
	int y, int type) {
		myTask = task;
		this.x1 = x1;
		this.x2 = x2;
		this.x3 = x3;
		this.y = y;
		this.type = type;
	}

	public String toString() {
		return getName();
	}

	public String getName() {
		return myTask.getName();
	}

	public int getTaskID() {
		return myTask.getTaskID();
	}

	public int getType() {
		return type;
	}

}