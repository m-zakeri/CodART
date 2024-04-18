package net.sourceforge.jvlt.metadata;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public interface Attribute {
	String getName();

	Class<? extends Object> getType();

	Object getValue(Object o);

	String getFormattedValue(Object o);

	Element getXMLElement(Document doc, Object o);
}
