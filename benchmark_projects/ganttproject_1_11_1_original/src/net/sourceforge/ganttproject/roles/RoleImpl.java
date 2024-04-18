package net.sourceforge.ganttproject.roles;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 25.01.2004
 */
public class RoleImpl implements Role {
    private final String myName;
    private final int myID;
    private final RoleSet myRoleSet;

    public RoleImpl(int id, String name, RoleSet roleSet) {
        myID = id;
        myName = name;
        myRoleSet = roleSet;
    }

    public int getID() {
        return myID;
    }

    public String getName() {
        return myName;
    }

    public String getPersistentID() {
        return (myRoleSet.getName()==null ? "" : myRoleSet.getName()+":")+getID();
    }

    public String toString() {
        return getName();
    }

}
