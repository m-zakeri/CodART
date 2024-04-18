package net.sourceforge.jvlt.metadata;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class CalendarAttribute extends DefaultAttribute {
	private static SimpleDateFormat _format = new SimpleDateFormat(
			"yyyy-MM-dd HH:mm");

	public CalendarAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	@Override
	public String getFormattedValue(Object o) {
		Calendar val = (Calendar) getValue(o);
		if (val == null) {
			return "";
		}
		return _format.format(val.getTime());
	}
}
