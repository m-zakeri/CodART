/*
 * Created on 18.10.2004
 */
package net.sourceforge.ganttproject.calendar;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.LinkedList;
import java.util.List;

import net.sourceforge.ganttproject.calendar.GPCalendar.DayType;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.gregorian.FramerImpl;

/**
 * @author bard
 */
public class WeekendCalendarImpl implements GPCalendar{

	private final Calendar myCalendar = (Calendar) Calendar.getInstance().clone();
	private final FramerImpl myFramer = new FramerImpl(Calendar.DAY_OF_WEEK);
	private DayType[] myTypes = new DayType[7];
	private int myWeekendDaysCount;
	private AlwaysWorkingTimeCalendarImpl myRestlessCalendar = new AlwaysWorkingTimeCalendarImpl();
	
	public WeekendCalendarImpl() {
		for (int i=0; i<myTypes.length; i++) {
			myTypes[i] = GPCalendar.DayType.WORKING;
		}
		setWeekDayType(GregorianCalendar.SATURDAY, GPCalendar.DayType.HOLIDAY);
		setWeekDayType(GregorianCalendar.SUNDAY, GPCalendar.DayType.HOLIDAY);
	}
	public List/*<GPCalendarActivity>*/ getActivities(Date startDate, final Date endDate) {
		if (myWeekendDaysCount==0) {
			return myRestlessCalendar.getActivities(startDate, endDate);
		}
		List result = new ArrayList();		
		Date curDayStart = myFramer.adjustLeft(startDate);
		boolean isWeekendState = isWeekend(curDayStart);
		//System.err.println("getActivities(): start="+startDate+" end="+endDate);
		while (curDayStart.before(endDate)) {
			//System.err.println("curDayStart="+curDayStart);
			Date changeStateDayStart = getStateChangeDate(curDayStart, !isWeekendState);
			//System.err.println("changeStateDayStart="+changeStateDayStart);
			if (changeStateDayStart.before(endDate)) {
				result.add(new CalendarActivityImpl(curDayStart, changeStateDayStart, !isWeekendState));
				curDayStart = changeStateDayStart;
				isWeekendState = !isWeekendState;
				continue;
			}
			else {
				result.add(new CalendarActivityImpl(curDayStart, endDate, !isWeekendState));
				break;
			}			
		}
		return result;
		
	}
	
	private boolean isWeekend(Date curDayStart) {
		myCalendar.setTime(curDayStart);
		int dayOfWeek = myCalendar.get(Calendar.DAY_OF_WEEK);
		return myTypes[dayOfWeek-1]==GPCalendar.DayType.HOLIDAY;
	}

	private Date getStateChangeDate(Date startDate, boolean changeToWeekend) {
		Date nextDayStart = myFramer.adjustRight(startDate);
		if (! (changeToWeekend ^ isWeekend(nextDayStart))) {
			return nextDayStart;
		}
		else {
			return getStateChangeDate(nextDayStart, changeToWeekend);
		}
	}

	private Date getStateChangeDate(Date startDate, TimeUnit timeUnit, boolean changeToWeekend, boolean moveRightNotLeft) {
		Date nextUnitStart = moveRightNotLeft ? timeUnit.adjustRight(startDate) : timeUnit.jumpLeft(startDate);
		if (! (changeToWeekend ^ isWeekend(nextUnitStart))) {
			return nextUnitStart;
		}
		else {
			return getStateChangeDate(nextUnitStart, timeUnit, changeToWeekend, moveRightNotLeft);
		}
		
	}
	public List getActivities(Date startDate, TimeUnit timeUnit, long unitCount) {
		return unitCount>0 ? 
				getActivitiesForward(startDate, timeUnit, unitCount) :
				getActivitiesBackward(startDate, timeUnit, -unitCount);
	}
	
	private List getActivitiesForward(Date startDate, TimeUnit timeUnit, long unitCount) {
		List result = new ArrayList();		
		Date unitStart = timeUnit.adjustLeft(startDate);
		while (unitCount>0) {
			boolean isWeekendState = isWeekend(unitStart);
			if (isWeekendState) {
				Date workingUnitStart = getStateChangeDate(unitStart, timeUnit, false, true);
				result.add(new CalendarActivityImpl(unitStart, workingUnitStart, false));
				unitStart = workingUnitStart;
				continue;
			}
			Date nextUnitStart = timeUnit.adjustRight(unitStart);
			result.add(new CalendarActivityImpl(unitStart, nextUnitStart, true));
			unitStart = nextUnitStart;
			unitCount--;
		}
		return result;
	}
	
	private List getActivitiesBackward(Date startDate, TimeUnit timeUnit, long unitCount) {
		List result = new LinkedList();
		Date unitStart = timeUnit.adjustLeft(startDate);
		while (unitCount>0) {
			Date prevUnitStart = timeUnit.jumpLeft(unitStart);
			boolean isWeekendState = isWeekend(prevUnitStart);
			if (isWeekendState) {
				Date lastWorkingUnitStart = getStateChangeDate(prevUnitStart, timeUnit, false, false);
				Date firstWeekendUnitStart = timeUnit.adjustRight(lastWorkingUnitStart);
				Date lastWeekendUnitEnd = unitStart;
				result.add(0, new CalendarActivityImpl(firstWeekendUnitStart, lastWeekendUnitEnd, false));
				unitStart = firstWeekendUnitStart;
			}
			else {
				result.add(0, new CalendarActivityImpl(prevUnitStart, unitStart, true));
				unitCount--;
				unitStart = prevUnitStart;
			}
		}
		return result;
	}
	public void setWeekDayType(int day, DayType type) {
		if (type!=myTypes[day-1]) {
			myWeekendDaysCount += (type==DayType.HOLIDAY ? 1 : -1);
		}
		myTypes[day-1] = type; 
	}
	public DayType getWeekDayType(int day) {
		return myTypes[day-1];
	}
	public Date findClosestWorkingTime(Date time) {
		if (myWeekendDaysCount==0) {
			return time;
		}
		if (!isWeekend(time)) {
			return time;
		}
		return getStateChangeDate(time, false);
	}

}
