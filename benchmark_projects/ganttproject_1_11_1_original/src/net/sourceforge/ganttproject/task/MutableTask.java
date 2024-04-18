package net.sourceforge.ganttproject.task;

import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.shape.ShapePaint;
//import net.sourceforge.ganttproject.resource.ProjectResource;

import java.awt.*;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 06.02.2004
 */
public interface MutableTask {
    void setName(String name);

    void setMilestone(boolean isMilestone);

    void setPriority(int priority);

    void setStart(GanttCalendar start);

    void setEnd(GanttCalendar end);
    void setDuration(TaskLength length);
    void shift(TaskLength shift);
    void setCompletionPercentage(int percentage);

    void setStartFixed(boolean isFixed);

    void setShape(ShapePaint shape);

    void setColor(Color color);

    void setNotes(String notes);

    void addNotes(String notes);
	
    void setExpand(boolean expand);
}
