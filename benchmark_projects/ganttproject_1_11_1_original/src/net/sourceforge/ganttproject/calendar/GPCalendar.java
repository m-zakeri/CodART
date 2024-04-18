/*
 * Created on 18.10.2004
 */
package net.sourceforge.ganttproject.calendar;

import java.util.Date;
import java.util.List;

import net.sourceforge.ganttproject.time.TimeUnit;

/**
 * 
 * @author bard
 */
public interface GPCalendar {
	List getActivities(Date startDate, Date endDate);
	List getActivities(Date startDate, TimeUnit timeUnit, long l);
	void setWeekDayType(int day, DayType type);
	DayType getWeekDayType(int day);
	
	final class DayType {
		public static final DayType WORKING = new DayType();
		public static final DayType HOLIDAY = new DayType();
	}

	Date findClosestWorkingTime(Date time);

}
