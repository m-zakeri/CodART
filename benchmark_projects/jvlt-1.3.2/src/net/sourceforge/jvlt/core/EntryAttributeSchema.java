package net.sourceforge.jvlt.core;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

public class EntryAttributeSchema {
	private String _language = null;
	private final HashMap<String, EntryClass> _class_map;
	private final ArrayList<EntryClass> _classes;

	public EntryAttributeSchema(String lang) {
		_language = lang;
		_class_map = new HashMap<String, EntryClass>();
		_classes = new ArrayList<EntryClass>();
	}

	public String getLanguage() {
		return _language;
	}

	public EntryClass[] getEntryClasses() {
		return _classes.toArray(new EntryClass[0]);
	}

	public EntryClass getEntryClass(String name) {
		return _class_map.get(name);
	}

	public void addEntryClass(EntryClass c) {
		_classes.add(c);
		_class_map.put(c.getName(), c);
	}

	public void removeEntryClass(String name) {
		_classes.remove(_class_map.get(name));
		_class_map.remove(name);
	}

	@Override
	public String toString() {
		StringBuffer buf = new StringBuffer();
		buf.append("EntryAttributeSchema{lang=");
		buf.append(_language);
		buf.append(';');
		Iterator<EntryClass> it = _classes.iterator();
		for (int index = 0; it.hasNext(); index++) {
			if (index > 0) {
				buf.append(';');
			}
			buf.append(it.next().toString());
		}
		buf.append('}');

		return buf.toString();
	}
}
