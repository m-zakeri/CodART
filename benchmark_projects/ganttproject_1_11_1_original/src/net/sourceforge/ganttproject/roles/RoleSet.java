/*
 * Created on 18.06.2004
 *
 */
package net.sourceforge.ganttproject.roles;

import net.sourceforge.ganttproject.language.GanttLanguage;

/**
 * @author bard
 *
 */
public interface RoleSet {
    String SOFTWARE_DEVELOPMENT = "SoftwareDevelopment";
    String DEFAULT = "Default";
    String getName();
    Role[] getRoles();
    Role createRole(String name, int persistentID);
    void deleteRole(Role role);
    Role findRole(int roleID);
    boolean isEnabled();
    void setEnabled(boolean isEnabled);
    boolean isEmpty();
    void clear();
}
