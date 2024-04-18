package net.sourceforge.jvlt.metadata;

import java.util.Arrays;
import java.util.HashSet;

public class ArrayChoiceAttribute extends ArrayAttribute implements
		ChoiceAttribute {
	private final HashSet<Object> _values = new HashSet<Object>();

	public ArrayChoiceAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	public void addValues(Object[] values) {
		_values.addAll(Arrays.asList(values));
	}

	public void setValues(Object[] values) {
		_values.clear();
		_values.addAll(Arrays.asList(values));
	}

	public Object[] getValues() {
		return _values.toArray();
	}
}
