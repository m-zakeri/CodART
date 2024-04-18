package net.sourceforge.jvlt.metadata;

import java.text.NumberFormat;

public class NumberAttribute extends DefaultAttribute {
	private final NumberFormat _format = NumberFormat.getInstance();

	public NumberAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	@Override
	public String getFormattedValue(Object o) {
		Number number = (Number) getValue(o);
		return number == null ? "" : _format.format(number.doubleValue());
	}
}
