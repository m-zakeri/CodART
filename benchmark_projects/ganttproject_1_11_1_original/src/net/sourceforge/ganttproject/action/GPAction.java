/*
 * Created on 26.03.2005
 */
package net.sourceforge.ganttproject.action;

import java.awt.event.ActionEvent;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.Icon;
import javax.swing.ImageIcon;

/**
 * @author bard
 */
abstract class GPAction extends AbstractAction implements RolloverAction  {
    protected GPAction(String name, String iconSize) {
        super(name);
        setIconSize(iconSize);
    }

    public Icon getIconOnMouseOver() {
        return (Icon) getValue(Action.SMALL_ICON);
    }
    
    public void setIconSize(String iconSize) {
        putValue(Action.SMALL_ICON, createIcon(iconSize));
    }
    
    protected Icon createIcon(String iconSize) {
        return new ImageIcon(getClass().getResource(getIconFileDirectory()+"/"+getIconFilePrefix()+iconSize+".gif"));
    }
    
    protected String getIconFileDirectory() {
        return "/icons";
    }
    
    protected abstract String getIconFilePrefix();
}
