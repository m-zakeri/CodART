/*
 * Created on 24.01.2005
 */
package net.sourceforge.ganttproject.chart;

import net.sourceforge.ganttproject.calendar.GPCalendar.DayType;
import net.sourceforge.ganttproject.task.TaskLength;

/**
 * @author bard
 */
public class DayTypeAlternance {

	private DayType myDayType;
	private TaskLength myDuration;

	DayTypeAlternance(DayType dayType, TaskLength duration){
		myDayType = dayType;
		myDuration = duration;
	}
	public DayType getDayType() {
		return myDayType;
	}
	public TaskLength getDuration() {
		return myDuration;
	}
	
	

	public String toString() {
		return "period length="+myDuration.getLength()+" ("+myDuration.getTimeUnit().getName()+")"+" is"+(myDayType==DayType.HOLIDAY?" holiday":" working\n");
	}
}
