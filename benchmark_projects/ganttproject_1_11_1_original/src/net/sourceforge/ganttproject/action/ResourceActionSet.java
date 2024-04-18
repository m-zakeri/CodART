package net.sourceforge.ganttproject.action;

import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.IGanttProject;
import net.sourceforge.ganttproject.resource.ResourceContext;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.roles.RoleManager;

import javax.swing.AbstractAction;

public class ResourceActionSet {
    public ResourceActionSet (IGanttProject project, ResourceContext context, GanttProject projectFrame) {
		myManager = project.getHumanResourceManager();
        myRoleManager = project.getRoleManager();
		myContext = context;
		myProjectFrame = projectFrame;
	}
	
	public AbstractAction[] getActions() {
		if (myActions==null) {
			myActions = new AbstractAction[] {
				new NewHumanAction(myManager, myRoleManager, myProjectFrame), new DeleteHumanAction(myManager, myContext,myProjectFrame)
			};
		}
		return myActions;
	}
	
    private final RoleManager myRoleManager;
	private final ResourceManager myManager;
	private final ResourceContext myContext;
	private final GanttProject myProjectFrame;
	private AbstractAction[] myActions;
}
