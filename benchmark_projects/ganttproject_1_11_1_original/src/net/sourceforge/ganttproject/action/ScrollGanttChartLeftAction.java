package net.sourceforge.ganttproject.action;

import net.sourceforge.ganttproject.gui.scrolling.ScrollingManager;

import javax.swing.*;
import java.awt.event.ActionEvent;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class ScrollGanttChartLeftAction extends GPAction implements RolloverAction {
	private final ScrollingManager myScrollingManager;

    public ScrollGanttChartLeftAction(ScrollingManager scrollingManager, String iconSize) {
        super("ScrollLeft", iconSize);
        myScrollingManager = scrollingManager;
    }

    public void actionPerformed(ActionEvent e) {
        myScrollingManager.scrollLeft();
    }

    protected String getIconFilePrefix() {
        return "prev_";
    }
}
