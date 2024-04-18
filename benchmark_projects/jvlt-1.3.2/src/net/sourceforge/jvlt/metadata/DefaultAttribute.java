package net.sourceforge.jvlt.metadata;

import java.lang.reflect.Method;

import net.sourceforge.jvlt.utils.XMLUtils;

import org.apache.log4j.Logger;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class DefaultAttribute implements Attribute,
		Comparable<DefaultAttribute> {
	private static final Logger logger = Logger
			.getLogger(DefaultAttribute.class);
	protected String _name;
	protected Class<? extends Object> _type;

	public DefaultAttribute(String name, Class<? extends Object> type) {
		_name = name;
		_type = type;
	}

	public String getName() {
		return _name;
	}

	public Class<? extends Object> getType() {
		return _type;
	}

	public Object getValue(Object o) {
		return getValue(o, _name);
	}

	public String getFormattedValue(Object o) {
		Object val = getValue(o);
		if (val == null) {
			return "";
		}
		return val.toString();
	}

	public Element getXMLElement(Document doc, Object o) {
		return XMLUtils.createTextElement(doc, _name, getFormattedValue(o));
	}

	@Override
	public String toString() {
		return _name;
	}

	public int compareTo(DefaultAttribute o) {
		return _name.compareTo((o)._name);
	}

	@Override
	public boolean equals(Object o) {
		//Added by John Fan
		if (o == null) {
			return false;
		}
		if (! (o instanceof DefaultAttribute)) {
			return false;
		}
		return _name.equals(((DefaultAttribute) o)._name);
	}
	
	//Added by John Fan
	@Override
	public int hashCode() {
		return this._name.hashCode();
	}

	protected Object getValue(Object o, String name) {
		try {
			Method method = o.getClass().getMethod("get" + name, new Class[0]);
			return method.invoke(o, new Object[0]);
		} catch (Exception ex) {
			logger.error(ex);
			return null;
		}
	}
}
