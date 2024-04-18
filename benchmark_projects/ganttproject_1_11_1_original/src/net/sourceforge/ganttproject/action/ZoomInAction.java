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
public class ZoomInAction extends GPAction implements ZoomListener  {
	private final ZoomManager myZoomManager;

	public ZoomInAction(ZoomManager zoomManager, String iconSize) {
		super("ZoomIn", iconSize);
		myZoomManager = zoomManager;
		myZoomManager.addZoomListener(this);
	}
	
	protected String getIconFilePrefix() {
        return "zoomp_";
    }
	
	public void actionPerformed(ActionEvent arg0) {
		if (myZoomManager.canZoomIn()) {
			myZoomManager.zoomIn();
		}
		setEnabled(myZoomManager.canZoomIn());
	}

	public void zoomChanged(ZoomEvent e) {
		setEnabled(myZoomManager.canZoomIn());
	}
}
