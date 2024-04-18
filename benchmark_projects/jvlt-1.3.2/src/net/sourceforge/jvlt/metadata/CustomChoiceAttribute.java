package net.sourceforge.jvlt.metadata;

import java.util.ArrayList;
import java.util.Arrays;

import net.sourceforge.jvlt.utils.AttributeResources;

public class CustomChoiceAttribute extends CustomAttribute implements
		ChoiceAttribute {
	protected AttributeResources _resources = new AttributeResources();
	protected ArrayList<Object> _values = new ArrayList<Object>();

	public CustomChoiceAttribute(String name) {
		super(name);
	}

	@Override
	public String getFormattedValue(Object o) {
		return _resources.getString(super.getFormattedValue(o));
	}

	public void addValues(Object[] values) {
		_values.addAll(Arrays.asList(values));
	}

	public void setValues(Object[] values) {
		_values.clear();
		addValues(values);
	}

	public Object[] getValues() {
		return _values.toArray();
	}
}
