package net.sourceforge.ganttproject.action;

import net.sourceforge.ganttproject.gui.scrolling.ScrollingManager;

import javax.swing.*;
import java.awt.event.ActionEvent;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class ScrollGanttChartRightAction extends GPAction {
	private final ScrollingManager myScrollingManager;

    public ScrollGanttChartRightAction(ScrollingManager scrollingManager, String iconSize) {
        super("ScrollRight", iconSize);
        myScrollingManager = scrollingManager;
    }

    public void actionPerformed(ActionEvent e) {
        myScrollingManager.scrollRight();
    }

    protected String getIconFilePrefix() {
        return "next_";
    }
}
