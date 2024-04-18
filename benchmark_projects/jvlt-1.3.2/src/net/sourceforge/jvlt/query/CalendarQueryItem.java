package net.sourceforge.jvlt.query;

import java.util.Calendar;

public class CalendarQueryItem extends ObjectQueryItem {
	public static final int ON = 1;
	public static final int BEFORE = 2;
	public static final int AFTER = 3;

	public CalendarQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public CalendarQueryItem() {
		super();
	}

	@Override
	public boolean objectMatches(Object obj) {
		if (_value == null || obj == null) {
			return _value == null && obj == null;
		}

		Calendar cal = (Calendar) obj;
		if (_type == CalendarQueryItem.ON) {
			return compare(cal, (Calendar) _value) == 0;
		} else if (_type == CalendarQueryItem.BEFORE) {
			return compare(cal, (Calendar) _value) < 0;
		} else if (_type == CalendarQueryItem.AFTER) {
			return compare(cal, (Calendar) _value) > 0;
		} else {
			return false;
		}
	}

	/**
	 * Returns zero if <i>first</i> is equal to <i>second</i>, a negative value
	 * if <i>first</i> is before <i>second</i> and a positive value otherwise.
	 * Only takes the date fields into account, hour, minute and second are
	 * ignored.
	 */
	private int compare(Calendar first, Calendar second) {
		int year1 = first.get(Calendar.YEAR);
		int year2 = second.get(Calendar.YEAR);
		if (year1 != year2) {
			return year1 - year2;
		}

		int month1 = first.get(Calendar.MONTH);
		int month2 = second.get(Calendar.MONTH);
		if (month1 != month2) {
			return month1 - month2;
		}

		int day1 = first.get(Calendar.DAY_OF_MONTH);
		int day2 = second.get(Calendar.DAY_OF_MONTH);
		return day1 - day2;
	}
}
