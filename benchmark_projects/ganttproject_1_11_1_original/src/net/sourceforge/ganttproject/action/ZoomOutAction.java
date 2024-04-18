/*
 * Created on 03.11.2004
 */
package net.sourceforge.ganttproject.action;

import java.awt.event.ActionEvent;

import javax.swing.AbstractAction;
import javax.swing.Action;
import javax.swing.Icon;
import javax.swing.ImageIcon;

import net.sourceforge.ganttproject.gui.zoom.ZoomEvent;
import net.sourceforge.ganttproject.gui.zoom.ZoomListener;
import net.sourceforge.ganttproject.gui.zoom.ZoomManager;

/**
 * @author bard
 */
public class ZoomOutAction extends GPAction implements ZoomListener {
	private final ZoomManager myZoomManager;

	public ZoomOutAction(ZoomManager zoomManager, String iconSize) {
		super("ZoomOut", iconSize);
		myZoomManager = zoomManager;
		myZoomManager.addZoomListener(this);
		
	}
	public void actionPerformed(ActionEvent arg0) {
		if (myZoomManager.canZoomOut()) {
			myZoomManager.zoomOut();
		}
		setEnabled(myZoomManager.canZoomOut());
	}
	
	public void zoomChanged(ZoomEvent e) {
		setEnabled(myZoomManager.canZoomOut());
	}
    protected String getIconFilePrefix() {
        return "zoomm_";
    }
	
}
