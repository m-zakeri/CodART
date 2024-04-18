/*
 * ProjectResource.java
 *
 * Created on 27. Mai 2003, 08:11
 */

package net.sourceforge.ganttproject.resource;

import java.util.ArrayList;
import java.util.List;

import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;

/**
 *
 * @author  barmeier
 */
public abstract class ProjectResource {
    
    protected int id;
    protected String name;
    private double costsPerUnit;
    private int maximumUnitsPerDay;
    private String unitMeasure; // means hours, days, meter, ...
    private String description;
    
    public void setName(String name) {
        this.name=name;
    }
    
    public String getName() {
        return name;
    }
    
    public void setDescription(String description) {
        this.description=description;
    }
    
    public String getDescription() {
        return description;
    }

    public void setUnitMeasure(String unitMeasure) {
        this.unitMeasure=unitMeasure;
    }
    
    public String getUnitMeasure() {
        return unitMeasure;
    }
    
    public void setCostsPerUnit(double costsPerUnit) {
        this.costsPerUnit=costsPerUnit;
    }
    
    public double getCostsPerUnit() {
        return costsPerUnit;
    }
    
    public void setMaximumUnitsPerDay(int maximumUnitsPerDay) {
        this.maximumUnitsPerDay=maximumUnitsPerDay;
    }
    
    public int getMaximumUnitsPerDay() {
        return maximumUnitsPerDay;
    }
    
    public void setId(int id) {
        if (this.id==-1)        // setting the id is only allowed when id is not assigned
            this.id=id;
    }
    
    public int getId() {
        return id;
    }
    
    
    public String toString() {
        return name;
    }
    
    public ResourceAssignment createAssignment(ResourceAssignment assignmentToTask) {
    	for (int i=0; i<myAssignments.size(); i++) {
    		if (((ResourceAssignment)myAssignments.get(i)).getTask().equals(assignmentToTask.getTask())) {
    			//throw new IllegalStateException("An attemp to assign resource to the same task twice");
    		}
    	}
        ResourceAssignment result =  new ResourceAssignmentImpl(assignmentToTask);
        myAssignments.add(result);
        return result;
    }
    
    private List myAssignments = new ArrayList();
    
    private class ResourceAssignmentImpl implements ResourceAssignment {

        private final ResourceAssignment myAssignmentToTask;
        private float myLoad;

        private ResourceAssignmentImpl(ResourceAssignment assignmentToTask) {
            myAssignmentToTask = assignmentToTask;
        }

        public Task getTask() {
            return myAssignmentToTask.getTask();
        }

        public ProjectResource getResource() {
            return ProjectResource.this;
        }

        public float getLoad() {
            return myLoad;
        }

        public void setLoad(float load) {
            myLoad = load;
        }

        public void delete() {
            ProjectResource.this.myAssignments.remove(this);
        }
        
    }

    public ResourceAssignment[] getAssignments() {
        return (ResourceAssignment[]) myAssignments.toArray(new ResourceAssignment[0]);
    }
}
