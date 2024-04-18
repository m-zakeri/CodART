package net.sourceforge.jvlt.utils;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class XMLUtils {
	public static Element createTextElement(Document doc, String name,
			String value) {
		Element elem = doc.createElement(name);
		elem.appendChild(doc.createTextNode(escapeText(value)));
		return elem;
	}

	public static String escapeText(String text) {
		String str = text;
		str = str.replaceAll("&", "&amp;");
		str = str.replaceAll("\"", "&quot;");
		str = str.replaceAll("<", "&lt;");
		str = str.replaceAll(">", "&gt;");

		return str;
	}

	public static String unescapeText(String text) {
		String str = text;
		str = str.replaceAll("&gt;", ">");
		str = str.replaceAll("&lt;", "<");
		str = str.replaceAll("&quot;", "\"");
		str = str.replaceAll("&amp;", "&");

		return str;
	}
}
