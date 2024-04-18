package net.sourceforge.ganttproject.roles;


/**
 * @author athomas
 *
 */
public interface RoleManager {
	public RoleSet createRoleSet(String name);
    public RoleSet[] getRoleSets();
	/** Clear the role list */
	public void clear();
	/** Return all roles exept the default roles*/
	//public String [] getRolesShort();
    public Role[] getProjectLevelRoles();    
	/** Load roles from the file*/
	/** Add a role on the list */
	public void add (int ID, String role);
	
    public class Access {
    	public static RoleManager getInstance() {
    		return ourInstance;
    	}
    	
    	private static RoleManager ourInstance = new RoleManagerImpl();
    }
	
	public static int DEFAULT_ROLES_NUMBER=11;

    public RoleSet getProjectRoleSet();
    public RoleSet getRoleSet(String rolesetName);
    public Role[] getEnabledRoles();
    public Role getDefaultRole();
	public void importData(RoleManager roleManager);
}
