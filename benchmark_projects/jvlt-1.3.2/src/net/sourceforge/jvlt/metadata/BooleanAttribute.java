package net.sourceforge.jvlt.metadata;

public class BooleanAttribute extends DefaultAttribute {
	public BooleanAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	@Override
	public String getFormattedValue(Object o) {
		Boolean b = (Boolean) getValue(o);
		return b == null ? "" : String.valueOf(b);
	}
}
