package net.sourceforge.jvlt.core;

import java.util.Iterator;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.Vector;

public class EntryClass implements Comparable<EntryClass> {
	private String _name = null;
	private EntryClass _parent_class = null;
	private final Vector<SchemaAttribute> _attributes = new Vector<SchemaAttribute>();
	private final Vector<String> _groups = new Vector<String>();
	// Maps groups to vectors of attributes
	private final TreeMap<String, Vector<SchemaAttribute>> _group_map;
	// Maps names to attributes
	private final TreeMap<String, SchemaAttribute> _name_map;
	private final TreeSet<EntryClass> _children = new TreeSet<EntryClass>();

	public EntryClass(String name) {
		_name = name;
		_group_map = new TreeMap<String, Vector<SchemaAttribute>>();
		_name_map = new TreeMap<String, SchemaAttribute>();
	}

	public String getName() {
		return _name;
	}

	public String[] getGroups() {
		return _groups.toArray(new String[0]);
	}

	public SchemaAttribute[] getAttributes() {
		return _attributes.toArray(new SchemaAttribute[0]);
	}

	/**
	 * Return the attributes for a certain group. If the argument group is null
	 * or the empty string, the attributes not being assigned to a group are
	 * returned.
	 */
	public SchemaAttribute[] getAttributes(String group) {
		Vector<SchemaAttribute> atts = _group_map.get(group);
		if (atts == null) {
			return new SchemaAttribute[0];
		}
		return atts.toArray(new SchemaAttribute[0]);
	}

	public SchemaAttribute getAttribute(String name) {
		return _name_map.get(name);
	}

	/**
	 * Add an attribute. The attribute is only added if there does not already
	 * exist an attribute with the same name and the same group.
	 */
	public void addAttribute(SchemaAttribute attr) {
		if (_name_map.containsKey(attr.getName())) {
			return;
		}

		String group = attr.getGroup();
		if (_group_map.containsKey(group)) {
			Vector<SchemaAttribute> vec = _group_map.get(group);
			vec.add(attr);
		} else {
			Vector<SchemaAttribute> vec = new Vector<SchemaAttribute>();
			vec.add(attr);
			_group_map.put(group, vec);
			_groups.add(group);
		}
		_name_map.put(attr.getName(), attr);
		_attributes.add(attr);
	}

	public void addAttributes(SchemaAttribute[] atts) {
		for (SchemaAttribute att : atts) {
			addAttribute(att);
		}
	}

	public EntryClass[] getChildClasses() {
		return _children.toArray(new EntryClass[0]);
	}

	public EntryClass getParentClass() {
		return _parent_class;
	}

	public void setParentClass(EntryClass cl) {
		_parent_class = cl;
		if (cl != null) {
			_parent_class._children.add(this);
		}
	}

	@Override
	public Object clone() {
		EntryClass cl = new EntryClass(_name);
		Iterator<SchemaAttribute> it = _attributes.iterator();
		while (it.hasNext()) {
			cl.addAttribute((SchemaAttribute) it.next().clone());
		}
		return cl;
	}

	public int compareTo(EntryClass o) {
		return _name.compareTo((o)._name);
	}

	@Override
	public boolean equals(Object o) {
		if (o == null) {
			return false;
		}
		return ((EntryClass) o)._name.equals(_name);
	}

	@Override
	public int hashCode() {
		return _name.hashCode();
	}

	@Override
	public String toString() {
		return _name;
	}
}
