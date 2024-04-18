package net.sourceforge.jvlt.metadata;

import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Vector;

public class MetaData {
	private Class<? extends Object> _type = null;
	private final Vector<Attribute> _attributes = new Vector<Attribute>();
	private final Vector<String> _names = new Vector<String>();
	private final HashMap<String, Attribute> _name_map;

	public MetaData(Class<? extends Object> type) {
		_type = type;
		_name_map = new HashMap<String, Attribute>();
		init();
	}

	public Class<? extends Object> getType() {
		return _type;
	}

	public Attribute getAttribute(String name) {
		return _name_map.get(name);
	}

	/**
	 * Returns the list of attributes. An attribute is represented by a public
	 * method with prefix "get" and with no parameters.
	 */
	public Attribute[] getAttributes() {
		return _attributes.toArray(new Attribute[0]);
	}

	public String[] getAttributeNames() {
		return _names.toArray(new String[0]);
	}

	protected void init() {
		Method[] methods = _type.getMethods();
		for (Method m : methods) {
			String name = m.getName().substring(3);
			Class<? extends Object> cl = m.getReturnType();
			if (m.getName().startsWith("get")
					&& m.getDeclaringClass().equals(_type)
					&& Modifier.isPublic(m.getModifiers())
					&& m.getParameterTypes().length == 0) {
				if (cl.equals(Byte.TYPE)) {
					cl = Byte.class;
				} else if (cl.equals(Short.TYPE)) {
					cl = Short.class;
				} else if (cl.equals(Integer.TYPE)) {
					cl = Integer.class;
				} else if (cl.equals(Long.TYPE)) {
					cl = Long.class;
				} else if (cl.equals(Float.TYPE)) {
					cl = Float.class;
				} else if (cl.equals(Double.TYPE)) {
					cl = Double.class;
				} else if (cl.equals(Boolean.TYPE)) {
					cl = Boolean.class;
				} else if (cl.equals(Character.TYPE)) {
					cl = Character.class;
				}

				if (Calendar.class.isAssignableFrom(cl)) {
					addAttribute(new CalendarAttribute(name, cl));
				} else if (Number.class.isAssignableFrom(cl)) {
					addAttribute(new NumberAttribute(name, cl));
				} else if (Boolean.class.isAssignableFrom(cl)) {
					addAttribute(new BooleanAttribute(name, cl));
				} else if (Object[].class.isAssignableFrom(cl)) {
					addAttribute(new ArrayAttribute(name, cl));
				} else {
					addAttribute(new DefaultAttribute(name, cl));
				}
			} // end of if
		} // end of for
	}

	/**
	 * Add a custom attribute. Existing attributes with the same name will be
	 * overwritten.
	 */
	protected void addAttribute(Attribute attribute) {
		if (_name_map.containsKey(attribute.getName())) {
			removeAttribute(attribute.getName());
		}

		_name_map.put(attribute.getName(), attribute);
		_names.add(attribute.getName());
		_attributes.add(attribute);
	}

	protected void removeAttribute(String name) {
		_attributes.remove(_name_map.get(name));
		_names.remove(name);
		_name_map.remove(name);
	}
}
