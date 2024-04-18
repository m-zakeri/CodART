/*
 * Created on 05.07.2003
 *
 */
package net.sourceforge.ganttproject.parser;

import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.task.TaskManager;
//import net.sourceforge.ganttproject.task.ResourceAssignment;
//import net.sourceforge.ganttproject.task.TaskMutator;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.ResourceAssignment;

import org.xml.sax.Attributes;

/**
 * @author bard
 *
 */
public class AllocationTagHandler implements TagHandler {
    public AllocationTagHandler(ResourceManager resourceMgr, TaskManager taskMgr) {
        myResourceManager = resourceMgr;
        myTaskManager = taskMgr;    
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.parser.TagHandler#startElement(java.lang.String, java.lang.String, java.lang.String, org.xml.sax.Attributes)
     */
    public void startElement(
        String namespaceURI,
        String sName,
        String qName,
        Attributes attrs) throws FileFormatException {
                        
        if (qName.equals("allocation")) {
            loadAllocation(attrs);
        }
    }

    /* (non-Javadoc)
     * @see net.sourceforge.ganttproject.parser.TagHandler#endElement(java.lang.String, java.lang.String, java.lang.String)
     */
    public void endElement(String namespaceURI, String sName, String qName) {
        // TODO Auto-generated method stub

    }
    
    private void loadAllocation(Attributes attrs) throws FileFormatException {
        String aName;
        int taskId = 0;
        int resourceId = 0;
        float load = 0;

        String taskIdAsString = attrs.getValue("task-id");
        String resourceIdAsString = attrs.getValue("resource-id");
        String loadAsString = attrs.getValue("load");
        
        if (taskIdAsString==null || resourceIdAsString==null) {
            throw new FileFormatException("Failed to load <allocation> tag: task or resource identifier is missing");
        }
        
        try {
            taskId = Integer.parseInt(taskIdAsString);
            resourceId = Integer.parseInt(resourceIdAsString);
            
            if (loadAsString!=null) {
                load = Float.parseFloat(loadAsString);
            }
        }
        catch (NumberFormatException e) {
            throw new FileFormatException("Failed to load <allocation> tag: one of attribute values is invalid", e);
        }

        // if no load is specified I assume 100% load
        // this should only be the case if old files
        // were loaded.
        if (load == 0) {
            load = 100;
        }
        
        HumanResource human = (HumanResource)getResourceManager().getById(resourceId);
        if (human==null) {
            throw new FileFormatException("Human resource with id="+resourceId+" not found");
        }
        
        Task task = getTaskManager().getTask(taskId);
        if (task==null) {
            throw new FileFormatException("Task with id="+taskId+" not found");
        }
//        TaskMutator mutator = task.createMutator();
//        ResourceAssignment assignment = mutator.addResource(human);
//        assignment.setLoad(load);
//        mutator.commit();
        ResourceAssignment assignment = task.getAssignmentCollection().addAssignment(human);
        assignment.setLoad(load);

    }
    
    private ResourceManager getResourceManager() {
        return myResourceManager;
    }
    
    private TaskManager getTaskManager() {
        return myTaskManager; 
    }
    
    private ResourceManager myResourceManager;
    private TaskManager myTaskManager;

}
