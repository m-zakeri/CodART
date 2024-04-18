/*
 * HumanResource.java
 *
 * Created on 27. Mai 2003, 22:19
 */

package net.sourceforge.ganttproject.resource;

import net.sourceforge.ganttproject.roles.Role;

/**
 *
 * @author  barmeier
 */
public class HumanResource extends ProjectResource {
    
    private String phone="";
    private String email="";
    private int function;
    private Role myRole;

    
    HumanResource () {
        this.name="";
        this.id=-1;     //has to be assigned from the managr when resource is added
    }
    
    /** Creates a new instance of HumanResource */
    HumanResource(String name, int id) {
        this.name=name;
        this.id=id;
    }
    
    public void setMail (String email) {
        this.email = email;
    }
    
    public String getMail() {
        return email;
    }
    
    public void setPhone (String phone) {
        this.phone = phone;
    }
    
    public String getPhone() {
        return phone;
    }
    
//    public void setFunction (int function) {
//        this.function=function;
//    }
    
//    public int getFunction () {
//        return myRole==null ? 0 : myRole.getID();
//    }

    public void setRole(Role role) {
        myRole = role;
    }
    
    public Role getRole() {
        if (myRole==null) {
            System.err.println("[HumanResource] getRole(): I have no role :( name="+getName());
        }
        return myRole;
    }
}
