
/***************************************************************************
                           ResourceTagHandler.java  -  description
                             -------------------
    begin                : may 2003

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
package net.sourceforge.ganttproject.parser;

import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;

import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.roles.Role;
import net.sourceforge.ganttproject.roles.RoleManager;
import net.sourceforge.ganttproject.roles.RolePersistentID;
import net.sourceforge.ganttproject.roles.RoleSet;

import org.xml.sax.Attributes;

/** Class to parse the attibute of resources handler */
public class ResourceTagHandler implements TagHandler, ParsingListener {
	public ResourceTagHandler(ResourceManager resourceManager, RoleManager roleManager) {
		myResourceManager = (HumanResourceManager) resourceManager;
        myResourceManager.clear(); //CleanUP the old stuff
        myRoleManager = roleManager;
	}

	/**
	 * @see net.sourceforge.ganttproject.parser.TagHandler#endElement(String, String, String)
	 */
	public void endElement(String namespaceURI, String sName, String qName) {

	}

	/**
	 * @see net.sourceforge.ganttproject.parser.TagHandler#startElement(String, String, String, Attributes)
	 */
	public void startElement(
		String namespaceURI,
		String sName,
		String qName,
		Attributes attrs) {

		if (qName.equals("resource")) {
            loadResource(attrs);            
		}
	}
	
	/** Las a resources */
    private void loadResource(Attributes atts) {
        HumanResource hr;
        
        try {        
            String id = atts.getValue("id");
            if (id==null) {
                hr = getResourceManager().newHumanResource();
                hr.setName(atts.getValue("name"));
                getResourceManager().add(hr);
            }
            else {
                hr = (HumanResource)getResourceManager().create(atts.getValue("name"), Integer.parseInt(id));
            }
        }
        catch (NumberFormatException e) {
            System.out.println ("ERROR in parsing XML File id is not numeric: "+e.toString());
            return;
        }            
        
        hr.setMail(atts.getValue("contacts"));
        hr.setPhone(atts.getValue("phone"));
        try {
            String roleID = atts.getValue("function");
            myLateResource2roleBinding.put(hr, roleID);
            //hr.setFunction(Integer.parseInt());
        }
        catch (NumberFormatException e) {
            System.out.println ("ERROR in parsing XML File function id is not numeric: "+e.toString());
        }
    }

    private HumanResourceManager getResourceManager() {
        return myResourceManager;
    }
    
    private final HashMap myLateResource2roleBinding = new HashMap();
    private final HumanResourceManager myResourceManager;
    private final RoleManager myRoleManager;
	//private GanttPeoplePanel myPeople;
    
    private Role findRole(String persistentIDasString) {
//
        RolePersistentID persistentID = new RolePersistentID(persistentIDasString);
        String rolesetName = persistentID.getRoleSetID();
        int roleID = persistentID.getRoleID();
        RoleSet roleSet;
        if (rolesetName==null) {
            roleSet = myRoleManager.getProjectRoleSet();
            if (roleSet.findRole(roleID)==null) {
                if (roleID<=10 && roleID>2) {
                    roleSet = myRoleManager.getRoleSet(RoleSet.SOFTWARE_DEVELOPMENT);
                    roleSet.setEnabled(true);
                }
                else if (roleID<=2) {
                    roleSet = myRoleManager.getRoleSet(RoleSet.DEFAULT);
                }
            }
        }
        else {
            roleSet = myRoleManager.getRoleSet(rolesetName);
        }
        Role result = roleSet.findRole(roleID);
        return result;
    }
    
    public void parsingStarted() {
    }

    public void parsingFinished() {
        //System.err.println("[ResourceTagHandler] parsingFinished():");
        for (Iterator lateBindingEntries = myLateResource2roleBinding.entrySet().iterator(); lateBindingEntries.hasNext();) {
            Map.Entry nextEntry = (Entry) lateBindingEntries.next();
            String persistentID = (String) nextEntry.getValue();
            Role nextRole = findRole(persistentID);
            if (nextRole!=null) {
                lateBindingEntries.remove();
                ((HumanResource)nextEntry.getKey()).setRole(nextRole);
            }
            
        }
        if (!myLateResource2roleBinding.isEmpty()) {
        	System.err.println("[ResourceTagHandler] parsingFinished(): not found roles:\n"+myLateResource2roleBinding);
        }
    }
    
        
}
