package net.sourceforge.jvlt.metadata;

import net.sourceforge.jvlt.utils.XMLUtils;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class ArrayAttribute extends DefaultAttribute {
	private String _delimiter = ", ";
	private boolean _enable_numbering = false;

	public ArrayAttribute(String name, Class<? extends Object> type) {
		super(name, type);
	}

	@Override
	public String getFormattedValue(Object o) {
		StringBuffer buffer = new StringBuffer();
		Object[] val = (Object[]) getValue(o);
		for (int i = 0; i < val.length; i++) {
			if (i > 0) {
				buffer.append(_delimiter);
			}
			if (_enable_numbering && val.length > 1) {
				buffer.append(String.valueOf(i + 1) + ". ");
			}
			buffer.append(val[i].toString());
		}
		return buffer.toString();
	}

	@Override
	public Element getXMLElement(Document doc, Object o) {
		Element elem = doc.createElement(_name);
		Object[] objs = (Object[]) getValue(o);
		for (Object obj : objs) {
			Element e = XMLUtils.createTextElement(doc, "item", obj.toString());
			elem.appendChild(e);
		}
		return elem;
	}

	public void setDelimiter(String delim) {
		_delimiter = delim;
	}

	public void setEnableNumbering(boolean enable) {
		_enable_numbering = enable;
	}
}
