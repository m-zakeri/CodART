/*
 * Created on 27.04.2005
 */
package net.sourceforge.ganttproject.resource;

import java.util.Date;
import java.util.LinkedList;
import java.util.List;

import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.time.TimeUnitStack;


public class LoadDistribution {
	public static class Load {
		public final TaskLength startDelta;
		public float load;
		Load(TaskLength startDelta, float load) {
			this.startDelta = startDelta;
			this.load = load;
		}
		
		public String toString() {
			return "delta="+this.startDelta+" load="+this.load;
		}
	}
	private final List myDaysOff = new LinkedList();
    private final List myLoads = new LinkedList();
	private final ProjectResource myResource;
    private final Date myStartDate;
    private final TimeUnitStack myTimeUnitStack;
    private final TaskManager myTaskManager;
	//private final int myPosY;
	public LoadDistribution(ProjectResource resource, Date startDate, TimeUnitStack timeUnitStack, TaskManager taskManager) {
	    myStartDate = startDate;
	    myTimeUnitStack = timeUnitStack;
	    myTaskManager = taskManager;
		myLoads.add(new Load(null, 0));
        myDaysOff.add(new Load(null, 0));
		myResource = resource;
        ResourceAssignment[] assignments = myResource.getAssignments();    		
        for (int j=0; j<assignments.length; j++) {
        	processAssignment(assignments[j]);
        }
	}
	

    private void processAssignment(ResourceAssignment assignment) {
	    Task task = assignment.getTask();
	    if (task.getEnd().getTime().before(myStartDate)) {
	        return;
	    }
	    TaskActivity[] activities = task.getActivities();
	    for (int i=0; i<activities.length; i++) {
	        processActivity(activities[i], assignment.getLoad());
	    }
	}

	private void processActivity(TaskActivity activity, float load) {
	    Date startDate = myStartDate;
	    if (activity.getEnd().before(startDate)) {
	        return;
	    }
	    if (activity.getIntensity()==0) {
	        return;
	    }
	    TaskManager taskManager = activity.getTask().getManager(); 
	    TaskLength startDelta = taskManager.createLength(myTimeUnitStack.getDefaultTimeUnit(), startDate, activity.getStart());
	    TaskLength endDelta = taskManager.createLength(myTimeUnitStack.getDefaultTimeUnit(), startDate, activity.getEnd());
	    addLoad(startDelta, endDelta, load);
    }

    void addDayOff(TaskLength startDelta, TaskLength endDelta) {
        addLoad(startDelta, endDelta, 100, myDaysOff);
    }
    
	void addLoad(TaskLength startDelta, TaskLength endDelta, float load) {
        addLoad(startDelta, endDelta, load, myLoads);
	}
    
    private void addLoad(TaskLength startDelta, TaskLength endDelta, float load, List loads) {
        //System.err.println("[LoadDistribution] addLoad: startDelta="+startDelta+" endDelta="+endDelta+" load="+load);
        int idxStart = -1;
        float currentLoad = 0;
        if (startDelta==null) {
            idxStart = 0;
        }
        else {
            for (int i=1; i<loads.size(); i++) {
                Load nextLoad = (Load)loads.get(i);
                if (startDelta.getValue()>=nextLoad.startDelta.getValue()) {
                    currentLoad = ((Load)loads.get(i)).load; 
                }
                if (startDelta.getValue()>nextLoad.startDelta.getValue()) {
                    continue;
                }
                idxStart = i;
                if (startDelta.getValue()<nextLoad.startDelta.getValue()) {
                    loads.add(i, new Load(startDelta, currentLoad));                        
                }
                break;
            }
        }
        if (idxStart==-1) {
            idxStart = loads.size();
            loads.add(new Load(startDelta, 0));
        }
        int idxEnd = -1;
        if (endDelta==null) {
            idxEnd = loads.size()-1;
        }
        else {
            for (int i=idxStart; i<loads.size(); i++) {
                Load nextLoad = (Load) loads.get(i);
                if (endDelta.getValue()>nextLoad.startDelta.getValue()) {
                    nextLoad.load+=load;
                    continue;
                }
                idxEnd = i;
                if (endDelta.getValue()<nextLoad.startDelta.getValue()) {
                    Load prevLoad = (Load) loads.get(i-1);
                    loads.add(i, new Load(endDelta, prevLoad.load-load));
                }
                break;
            }
        }
        if (idxEnd==-1) {
            idxEnd = loads.size();
            loads.add(new Load(endDelta, 0));             
        }
        //System.err.println("[LoadDistribution] addLoad: \nloads="+myLoads);
        
    }

    public List getLoads() {
        return myLoads;
    }

    public List getDaysOff() {
        return myDaysOff;
    }
}