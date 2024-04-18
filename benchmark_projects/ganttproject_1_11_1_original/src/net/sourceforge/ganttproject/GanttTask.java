/***************************************************************************
                           GanttTask.java  -  description
                             -------------------
    begin                : dec 2002
    copyright            : (C) 2002 by Thomas Alexandre
    email                : alexthomas(at)ganttproject.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

package net.sourceforge.ganttproject;

import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskImpl;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.task.TaskMutator;
import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.time.TimeUnit;

import java.io.Serializable;
import java.util.Vector;

/**
 * Class that generate a task
 */

public class GanttTask extends TaskImpl

    implements Serializable {

  public static int LOW = 0;

  public static int NORMAL = 1;

  public static int HIGHT = 2;


/////////////////////////////////////////////////////////////////////////////////

  /** Constructor 
 * @param taskID*/

  public GanttTask(String name, GanttCalendar start, long length, TaskManager taskManager, int taskID) {
      super(taskManager, taskID);
      TaskMutator mutator = createMutator();
      mutator.setName(name);
      mutator.setStart(start);
      mutator.setDuration(taskManager.createLength(length));
      mutator.commit();
      enableEvents(true);      
  }


   public GanttTask(GanttTask copy) {
        super(copy, false);
//        for (int i = 0; i < getPredecessorsOld().size(); i++) {
//          GanttTaskRelationship tempRel = (GanttTaskRelationship) ( (
//              GanttTaskRelationship) getPredecessorsOld().get(i)).clone();
//          addPredecessor(tempRel);
//        }

//        for (int i = 0; i < successors.size(); i++) {
//          GanttTaskRelationship tempRel = (GanttTaskRelationship) ( (
//              GanttTaskRelationship) successors.get(i)).clone();
//          addSuccessor(tempRel);
//        }
        enableEvents(true);

    }


  /**
   * @return a clone of the Task
   */
  public GanttTask Clone() {
      return new GanttTask(this);
  }

  /** Return the name. */
  public String toString() {
    return getName();
    //return getName();
  }

  /** Return the shape of the task */


  /** Return the duration */

  public int getLength() {

    return (int) getDuration().getLength();

  }


  /** Change the duration */
  public void setLength(int l) {
  	  if (l<=0) {
  	  	throw new IllegalArgumentException("Length of task must be >=0. You've passed length="+l+" to task="+this);
  	  }
      TaskMutator mutator = createMutator();
      mutator.setDuration(getManager().createLength(getDuration().getTimeUnit(), l));
      mutator.commit();
  }



  /**whether the time relationship between this task and other has been checked. property will be used in scheduling check*/

  private boolean checked = false;


  public Vector getPredecessorsOld() {
      TaskDependency[] deps = getDependenciesAsDependant().toArray();
      Vector result = new Vector(deps.length);
      for (int i=0; i<deps.length; i++) {
          TaskDependency next = deps[i];
          GanttTaskRelationship rel = new GanttTaskRelationship(next.getDependee().getTaskID(), getTaskID(), next.getConstraint().getID(), getManager());
          result.add(rel);
      }
    return result;
  }

    public Vector getSuccessorsOld() {
        TaskDependency[] deps = getDependenciesAsDependee().toArray();
        Vector result = new Vector(deps.length);
        for (int i=0; i<deps.length; i++) {
            TaskDependency next = deps[i];
            GanttTaskRelationship rel = new GanttTaskRelationship(getTaskID(), next.getDependant().getTaskID(), next.getConstraint().getID(), getManager());
            result.add(rel);
        }
        return result;
    }


  /** Unlink the task from all relationship */
  public void unlink () {
      getDependencies().clear();

  }
  
  /**return true if the realtionship between this task and others has been checked*/

  public boolean isChecked() {

    return checked;

  }

  /**set the checked state of task: true if the relationship has been check. or else, false*/

  public void setChecked(boolean checked) {

    this.checked = checked;

  }

  /**
       *set the task ID. the uniquness of ID should be check before using this method
   * @param taskID
   */
  public void setTaskID(int taskID) {
      setTaskIDHack(taskID);
  }
}
