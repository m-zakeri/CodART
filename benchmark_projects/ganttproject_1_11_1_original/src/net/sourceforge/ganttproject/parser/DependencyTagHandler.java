package net.sourceforge.ganttproject.parser;

import java.util.ArrayList;
import java.util.List;
import org.xml.sax.Attributes;
import net.sourceforge.ganttproject.GanttTaskRelationship;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyException;
import net.sourceforge.ganttproject.task.dependency.TaskDependency;

public class DependencyTagHandler implements TagHandler, ParsingListener {
    private final TaskManager myTaskManager;

    public DependencyTagHandler(ParsingContext context, TaskManager taskManager) {
        myContext = context;
        myTaskManager = taskManager;
    }
	/**
	 * @see net.sourceforge.ganttproject.parser.TagHandler#endElement(String, String, String)
	 */
	public void endElement(String namespaceURI, String sName, String qName) {
        /*
        if ("dependencies".equals (qName)) {
            myDependenciesSectionStarted = false;
        }
        */
	}

	/**
	 * @see net.sourceforge.ganttproject.parser.TagHandler#startElement(String, String, String, Attributes)
	 */
	public void startElement(
		String namespaceURI,
		String sName,
		String qName,
		Attributes attrs) {

        /*
        if ("dependencies".equals (qName)) {
            myDependenciesSectionStarted = true;
        }
        */
        if ("depend".equals (qName)) {
            /*
            if (!myDependenciesSectionStarted) {
                throw new RuntimeException("Invalid file format. Found 'dependency' tag without prior 'dependencies' tag");                
            }
            else {
            */
            loadDependency(attrs);
        }
    }
    
    public void parsingStarted() {
    }
    
    public void parsingFinished() {
        for (int i = 0; i < getDependencies().size(); i++) {
            GanttDependStructure ds = (GanttDependStructure) getDependencies().get(i);
            Task dependee = myTaskManager.getTask(ds.taskID); //By CL
            Task dependant = myTaskManager.getTask(ds.successorTaskID);
            if (dependee==null || dependant==null) {
                continue;
            }
            try {
                TaskDependency dep = myTaskManager.getDependencyCollection().createDependency(dependant,dependee);
                dep.setConstraint(myTaskManager.createConstraint(ds.dependType));
            } catch (TaskDependencyException e) {
                e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
            }
        }
    }

    protected void loadDependency(Attributes attrs) {
        if (attrs != null) {
            GanttDependStructure gds = new GanttDependStructure();
            gds.setTaskID(getDependencyAddressee(attrs));               
            gds.setDependTaskID(getDependencyAddresser(attrs));            
            String dependencyTypeAsString = attrs.getValue("type");
            if (dependencyTypeAsString!=null) {
                try {
                    int dependencyType = Integer.parseInt(dependencyTypeAsString);
                    gds.setDependType(dependencyType);
                }
                catch (NumberFormatException e) {
                }
            }
            
            getDependencies().add(gds);
        }
    }

    protected int getDependencyAddressee(Attributes attrs) {
        return getContext().getTaskID();
    }

    protected int getDependencyAddresser(Attributes attrs) {        
        try {
            return Integer.parseInt(attrs.getValue("id"));
        }
        catch (NumberFormatException e) {
            throw new RuntimeException("Failed to parse 'depend' tag. Attribute 'id' seems to be invalid: "+attrs.getValue("id"), e);
        }
    }
    
    private List getDependencies() {
        return myDependencies;
    }

    private ParsingContext getContext() {
        return myContext;
    }
    private List myDependencies = new ArrayList();
    private boolean myDependenciesSectionStarted = false;
    private ParsingContext myContext;

    private class GanttDependStructure {
        public int taskID, successorTaskID;
        public int dependType = GanttTaskRelationship.FS; //
        public GanttDependStructure(int a, int b) {
            taskID = a;
            successorTaskID = b;
        }

        public GanttDependStructure(int taskID, int successorID, int relationType) {
            this.taskID = taskID;
            this.successorTaskID = successorID;
            this.dependType = relationType;
        }

        public GanttDependStructure() {}

        public void setTaskID(int taskID) {
            this.taskID = taskID;
        }

        public void setDependTaskID(int successorTaskID) {
            this.successorTaskID = successorTaskID;
        }

        public void setDependType(int dependType) {
            this.dependType = dependType;
        }
    }

}
