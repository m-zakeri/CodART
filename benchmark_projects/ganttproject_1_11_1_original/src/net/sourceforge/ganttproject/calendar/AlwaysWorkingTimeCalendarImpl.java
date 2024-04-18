/*
 * Created on 18.10.2004
 */
package net.sourceforge.ganttproject.calendar;

import java.util.Collections;
import java.util.Date;
import java.util.List;

import net.sourceforge.ganttproject.calendar.GPCalendar.DayType;
import net.sourceforge.ganttproject.time.TimeUnit;

/**
 * @author bard
 */
public class AlwaysWorkingTimeCalendarImpl implements GPCalendar {
	public List getActivities(Date startDate, Date endDate) {
		return Collections.singletonList(new CalendarActivityImpl(startDate, endDate, true));
	}

	public List getActivities(Date startDate, TimeUnit timeUnit, long l) {
		Date activityStart = timeUnit.adjustLeft(startDate);
		Date activityEnd = activityStart;
		for (; l>0; l--) {
			activityEnd = timeUnit.adjustRight(activityEnd);
		}
		return Collections.singletonList(new CalendarActivityImpl(activityStart, activityEnd, true));
	}

	public void setWeekDayType(int day, DayType type) {
		if (type==GPCalendar.DayType.HOLIDAY) {
			throw new IllegalArgumentException("I am always working time calendar, I don't accept holidays!");
		}
	}

	public DayType getWeekDayType(int day) {
		return GPCalendar.DayType.WORKING;
	}

	public Date findClosestWorkingTime(Date time) {
		return time;
	}

}
