package net.sourceforge.ganttproject.action;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.net.URL;

import javax.swing.*;

import net.sourceforge.ganttproject.gui.GanttDialogPerson;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.GanttProject;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.roles.RoleManager;

/**
  *Action connected to the menu item for insert a new resource
  */
public class NewHumanAction extends ResourceAction {
    private final RoleManager myRoleManager;
    
	public NewHumanAction(ResourceManager hrManager, RoleManager roleManager, JFrame projectFrame) {
		super(hrManager);
        myRoleManager = roleManager;
        myProjectFrame = projectFrame;
        
		this.putValue(AbstractAction.NAME, GanttProject.correctLabel(getLanguage().getText("newHuman")));
        this.putValue(Action.ACCELERATOR_KEY, KeyStroke.getKeyStroke(KeyEvent.VK_H, MENU_MASK));
        URL iconUrl = this.getClass().getClassLoader().getResource("icons/insert_16.gif");
        if(iconUrl!=null) {
            this.putValue(Action.SMALL_ICON, new ImageIcon(iconUrl));
        }
    }
    
	public void actionPerformed(ActionEvent event) {        
		HumanResource people = ((HumanResourceManager)getManager()).newHumanResource();
        people.setRole(myRoleManager.getDefaultRole());
		GanttDialogPerson dp = new GanttDialogPerson(getProjectFrame(), getLanguage(), people);
		dp.show();
		if(dp.result()) {
			getManager().add(people);
		}
	}
    
    public void languageChanged() {
    	this.putValue(AbstractAction.NAME, GanttProject.correctLabel(getLanguage().getText("newHuman")));
    }

    private JFrame getProjectFrame() {
        return myProjectFrame;
    }

    private final int MENU_MASK = Toolkit.getDefaultToolkit().getMenuShortcutKeyMask();
    private JFrame myProjectFrame;
}
