

package net.sourceforge.ganttproject.roles;

import java.util.ArrayList;
import java.util.*;

import net.sourceforge.ganttproject.language.GanttLanguage;

/**
 * @author athomas
 *
 */
public class RoleManagerImpl implements RoleManager {
	String [] defaultRoles;
    //private ArrayList myDefaultRoles = new ArrayList();
    //private final ArrayList myProjectLevelRoles = new ArrayList();
    private RoleSetImpl myProjectRoleSet = new RoleSetImpl();
    private ArrayList myRoleSets = new ArrayList();
    
    public RoleManagerImpl () {
        clear();
        myRoleSets.add(DEFAULT_ROLE_SET);
        myRoleSets.add(SOFTWARE_DEVELOPMENT_ROLE_SET);        
        myProjectRoleSet.setEnabled(true);
        SOFTWARE_DEVELOPMENT_ROLE_SET.setEnabled(false);
	}

    public void clear(){
		myProjectRoleSet = new RoleSetImpl();
        for (int i=0; i<myRoleSets.size(); i++) {
            RoleSet next = (RoleSet) myRoleSets.get(i);
            next.setEnabled(false);
        }
        myProjectRoleSet.setEnabled(true);
        DEFAULT_ROLE_SET.setEnabled(true);
        SOFTWARE_DEVELOPMENT_ROLE_SET.setEnabled(false);
	}
        	
    public Role[] getProjectLevelRoles() {
        return myProjectRoleSet.getRoles();
    }
	
	/** Add a role on the list */
	public void add (int ID, String roleName){
		//myProjectLevelRoles.add(newRole(ID, role));
        myProjectRoleSet.createRole(roleName, ID);
	}

    public RoleSet[] getRoleSets() {
        return (RoleSet[]) myRoleSets.toArray(new RoleSet[0]);
    }

    public RoleSet createRoleSet(String name) {
        RoleSet result = new RoleSetImpl(name);
        myRoleSets.add(result);
        //System.err.println("[RoleManagerImpl] createRoleSet(): created:"+name);
        return result;
    }

    public RoleSet getProjectRoleSet() {
        return myProjectRoleSet;
    }

    public RoleSet getRoleSet(String rolesetName) {
        RoleSet result = null;
        RoleSet[] roleSets = getRoleSets();
        for (int i=0; i<roleSets.length; i++) {
            if (roleSets[i].getName().equals(rolesetName)) {
                result = roleSets[i];
                break;
            }
        }
        return result;
    }
    
    public Role[] getEnabledRoles() {
        ArrayList result = new ArrayList();
        RoleSet[] roleSets = getRoleSets();
        for (int i=0; i<roleSets.length; i++) {
            if (roleSets[i].isEnabled()) {
                result.addAll(Arrays.asList(roleSets[i].getRoles()));
            }
        }
        result.addAll(Arrays.asList(getProjectRoleSet().getRoles()));
        return (Role[]) result.toArray(new Role[0]);
    }
    
    public Role getDefaultRole() {
        return DEFAULT_ROLE_SET.findRole(0);
    }
    
	public void importData(RoleManager original) {
		myProjectRoleSet.importData(original.getProjectRoleSet());
		RoleSet[] originalRoleSets = original.getRoleSets();
		HashSet thisNames = new HashSet();
		for (int i=0; i<myRoleSets.size(); i++) {
			RoleSet next = (RoleSet) myRoleSets.get(i);
			thisNames.add(next.getName());
		}
		for (int i=0; i<originalRoleSets.length; i++) {
			RoleSet next = originalRoleSets[i];
			if (!thisNames.contains(next.getName())) {
				myRoleSets.add(next);
			}
		}
		//myRoleSets.addAll(Arrays.asList(originalRoleSets));
	}
    
    static final RoleSetImpl SOFTWARE_DEVELOPMENT_ROLE_SET;
    static final RoleSetImpl DEFAULT_ROLE_SET;
    
    static {
        GanttLanguage language=GanttLanguage.getInstance();
        SOFTWARE_DEVELOPMENT_ROLE_SET = new RoleSetImpl(RoleSet.SOFTWARE_DEVELOPMENT);
//        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resUndefined"), 0);
//        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resProjectManager"), 1);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resDeveloper"), 2);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resDocWriter"), 3);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resTester"), 4);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resGraphicDesigner"), 5);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resDocTranslator"), 6);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resPackager"), 7);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resAnalysis"), 8);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resWebDesigner"), 9);
        SOFTWARE_DEVELOPMENT_ROLE_SET.createRole(language.getText("resNoSpecificRole"), 10);
        DEFAULT_ROLE_SET = new RoleSetImpl(RoleSet.DEFAULT);
        DEFAULT_ROLE_SET.createRole(language.getText("resUndefined"), 0);
        DEFAULT_ROLE_SET.createRole(language.getText("resProjectManager"), 1);
        DEFAULT_ROLE_SET.setEnabled(true);
    }

}
