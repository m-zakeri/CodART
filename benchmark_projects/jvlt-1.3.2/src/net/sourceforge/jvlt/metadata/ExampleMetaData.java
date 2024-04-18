package net.sourceforge.jvlt.metadata;

import java.text.ParseException;

import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.utils.SimpleHTMLParser;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

public class ExampleMetaData extends MetaData {
	private static class TextAttribute extends DefaultAttribute {
		private final SimpleHTMLParser _parser = new SimpleHTMLParser();

		public TextAttribute() {
			super("HTMLText", String.class);
		}

		@Override
		public Element getXMLElement(Document doc, Object o) {
			Element elem = doc.createElement("HTMLText");
			String val = (String) getValue(o);
			try {
				_parser.parse(val, doc);
				Node[] nodes = _parser.getNodes();
				for (Node node : nodes) {
					elem.appendChild(node);
				}
			} catch (ParseException ex) {
				ex.printStackTrace();
			}

			return elem;
		}
	}

	private static class TranslationAttribute extends DefaultAttribute {
		private final SimpleHTMLParser _parser = new SimpleHTMLParser();

		public TranslationAttribute() {
			super("Translation", String.class);
		}

		@Override
		public Element getXMLElement(Document doc, Object o) {
			Element elem = doc.createElement("Translation");
			String val = (String) getValue(o);
			try {
				_parser.parse(val, doc);
				Node[] nodes = _parser.getNodes();
				for (Node node : nodes) {
					elem.appendChild(node);
				}
			} catch (ParseException ex) {
				ex.printStackTrace();
			}

			return elem;
		}
	}

	public ExampleMetaData() {
		super(Example.class);

		addAttribute(new TextAttribute());
		addAttribute(new TranslationAttribute());
	}
}
