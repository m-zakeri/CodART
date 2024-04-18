package net.sourceforge.jvlt.core;

import java.util.ArrayList;
import java.util.List;

public class AttributeChoice implements Comparable<AttributeChoice> {
	private final String _name;
	private AttributeChoice _parent = null;
	private List<AttributeChoice> _children = null;

	public AttributeChoice(String name) {
		_name = name;
		_children = new ArrayList<AttributeChoice>();
	}

	public String getName() {
		return _name;
	}

	public AttributeChoice getParent() {
		return _parent;
	}

	public AttributeChoice[] getChildren() {
		return _children.toArray(new AttributeChoice[0]);
	}

	public void setParent(AttributeChoice parent) {
		_parent = parent;
		parent._children.add(this);
	}

	public int compareTo(AttributeChoice o) {
		if (o == null) {
			return -1;
		}
		return _name.compareTo(o._name);
	}

	@Override
	public boolean equals(Object o) {
		//Added by John Fan
		if (o == null) {
			return false;
		}
		if (! (o instanceof AttributeChoice)) {
			return false;
		}
		
		return compareTo((AttributeChoice) o) == 0;
	}
	
	@Override
	public String toString() {
		return _name;
	}
}
