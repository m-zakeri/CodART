package net.sourceforge.jvlt.metadata;

import java.util.Arrays;
import java.util.HashSet;

public class DefaultChoiceAttribute extends DefaultAttribute implements
		ChoiceAttribute {
	private final HashSet<Object> _values = new HashSet<Object>();

	public DefaultChoiceAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	public void addValues(Object[] values) {
		_values.addAll(Arrays.asList(values));
	}

	public Object[] getValues() {
		return _values.toArray();
	}

	public void setValues(Object[] values) {
		_values.clear();
		addValues(values);
	}
}
