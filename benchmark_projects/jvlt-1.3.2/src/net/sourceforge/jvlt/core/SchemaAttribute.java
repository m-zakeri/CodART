package net.sourceforge.jvlt.core;

public class SchemaAttribute implements Comparable<SchemaAttribute>, Cloneable {
	protected String _name = null;
	protected String _group = null;
	protected Object _value = null;

	public SchemaAttribute(String name, String group) {
		_name = name;
		_group = group;
	}

	public SchemaAttribute(String name) {
		this(name, "");
	}

	public String getName() {
		return _name;
	}

	public String getGroup() {
		return _group;
	}

	public Object getValue() {
		return _value;
	}

	public void setValue(Object value) {
		_value = value;
	}

	@Override
	public Object clone() {
		try {
			return super.clone();
		} catch (CloneNotSupportedException e) {
			return null;
		}
	}

	@Override
	public boolean equals(Object o) {
		//Added by John Fan
		if (o == null) {
			return false;
		}
		if (! (o instanceof SchemaAttribute)) {
			return false;
		}
		SchemaAttribute att = (SchemaAttribute) o;
		return att._name.equals(_name) && att._group.equals(_group);
	}
	
	public int compareTo(SchemaAttribute attr) {
		if (!_name.equals(attr._name)) {
			return _name.compareTo(attr._name);
		}
		return _group.compareTo(attr._group);
	}

	@Override
	public String toString() {
		StringBuffer buf = new StringBuffer();
		buf.append("SchemaAttribute{name=");
		buf.append(_name);
		if (_group != null && !_group.equals("")) {
			buf.append(";group=");
			buf.append(_group);
		}
		if (_value != null) {
			buf.append(";value=");
			buf.append(_value.toString());
		}
		buf.append('}');

		return buf.toString();
	}
}
