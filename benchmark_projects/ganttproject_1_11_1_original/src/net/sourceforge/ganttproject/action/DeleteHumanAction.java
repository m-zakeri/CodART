package net.sourceforge.ganttproject.action;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;

import java.net.URL;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.ImageIcon;
import javax.swing.KeyStroke;

import net.sourceforge.ganttproject.gui.GanttDialogInfo;
import net.sourceforge.ganttproject.resource.ProjectResource;
import net.sourceforge.ganttproject.resource.ResourceContext;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.GanttProject;
/**
  *Action connected to the menu item for delete a resource
  */
public class DeleteHumanAction extends ResourceAction {
    public DeleteHumanAction(ResourceManager hrManager, ResourceContext context, GanttProject projectFrame) {
		super(hrManager);
		myProjectFrame = projectFrame;
		this.putValue(AbstractAction.NAME, GanttProject.correctLabel(getLanguage().getText("deleteHuman")));
        this.putValue(Action.ACCELERATOR_KEY, KeyStroke.getKeyStroke(KeyEvent.VK_J, MENU_MASK));
	URL iconUrl = this.getClass().getClassLoader().getResource(ICON_URL);
        if(iconUrl!=null) {
            this.putValue(Action.SMALL_ICON, new ImageIcon(iconUrl));
        }
		myContext = context;
	}

	public void actionPerformed(ActionEvent event) {
		myProjectFrame.tabpane.setSelectedIndex(1);
		ProjectResource[] context = getContext().getResources();
		if (context.length>0) {
          GanttDialogInfo gdi = new GanttDialogInfo
			 	    	(null, GanttDialogInfo.WARNING,	GanttDialogInfo.YES_NO_OPTION,
						 getLanguage().getText("msg6")+" "+getDisplayName(context)+"??", getLanguage().getText("warning"));
          gdi.show();
          if(gdi.res==GanttDialogInfo.YES) {
						deleteResources(context);
						getProjectFrame().setAskForSave(true);
						getProjectFrame().refreshProjectInfos();
          }
		}
	}
	
	private GanttProject getProjectFrame() {
        return myProjectFrame;
  }
	
	private void deleteResources(ProjectResource[] context) {
		for (int i=0; i<context.length; i++) {
			getManager().remove(context[i]);
		}
	}

	private String getDisplayName(ProjectResource[] resources) {
		if (resources.length==1) {
			return resources[0].toString();
		}
		StringBuffer result = new StringBuffer();
		for (int i=0; i<resources.length; i++) {
			result.append(resources[i].toString());
			if (i<resources.length-1) {
				result.append(", ");
			}
		}
		return result.toString();
	}

	private ResourceContext getContext() {
		return myContext;
	}
	private final ResourceContext myContext;
	private static final String ICON_URL="icons/delete_16.gif";
	private final int MENU_MASK = Toolkit.getDefaultToolkit().getMenuShortcutKeyMask();
    private GanttProject myProjectFrame;
}
