package net.sourceforge.jvlt.metadata;

import net.sourceforge.jvlt.core.StringPair;
import net.sourceforge.jvlt.utils.XMLUtils;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class CustomFieldsAttribute extends DefaultChoiceAttribute {
	public CustomFieldsAttribute() {
		super("CustomFields", StringPair[].class);
	}

	@Override
	public Element getXMLElement(Document doc, Object o) {
		Element elem = doc.createElement("CustomFields");

		StringPair[] fields = (StringPair[]) getValue(o);
		for (StringPair p : fields) {
			Element item = doc.createElement("item");
			item.appendChild(XMLUtils.createTextElement(doc, "key", p
					.getFirst()));
			item.appendChild(XMLUtils.createTextElement(doc, "value", p
					.getSecond()));
			elem.appendChild(item);
		}

		return elem;
	}
	
	@Override
	public String getFormattedValue(Object o) {
		StringBuilder builder = new StringBuilder();
		StringPair[] fields = (StringPair[]) getValue(o);
		for (int i=0; i<fields.length; i++) {
			if (i > 0)
				builder.append(", ");
			
			builder.append(fields[i].getFirst());
			builder.append(": ");
			builder.append(fields[i].getSecond());
		}
		
		return builder.toString(); 
	}
}

