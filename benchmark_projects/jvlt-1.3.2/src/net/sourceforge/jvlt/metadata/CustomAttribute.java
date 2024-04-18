package net.sourceforge.jvlt.metadata;

import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.EntryClass;
import net.sourceforge.jvlt.core.SchemaAttribute;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class CustomAttribute extends DefaultAttribute {
	public CustomAttribute(String name) {
		super(name, String.class);
	}

	@Override
	public Object getValue(Object obj) {
		EntryClass ec = ((Entry) obj).getEntryClass();
		if (ec == null) {
			return null;
		}
		SchemaAttribute attr = ec.getAttribute(_name);
		if (attr == null) {
			return null;
		}
		return attr.getValue();
	}

	@Override
	public Element getXMLElement(Document doc, Object o) {
		Element elem = doc.createElement("Attribute");
		elem.setAttribute("name", _name);
		elem.appendChild(doc.createTextNode(getFormattedValue(o)));
		return elem;
	}
}
