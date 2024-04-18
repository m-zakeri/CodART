package net.sourceforge.jvlt.io;

import java.io.IOException;
import java.io.OutputStream;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import net.sourceforge.jvlt.JVLT;
import net.sourceforge.jvlt.core.ArraySchemaAttribute;
import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.EntryClass;
import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.core.SchemaAttribute;
import net.sourceforge.jvlt.core.Sense;
import net.sourceforge.jvlt.core.StringPair;
import net.sourceforge.jvlt.core.Example.TextFragment;
import net.sourceforge.jvlt.utils.CollatingEntryComparator;
import net.sourceforge.jvlt.utils.CustomCollator;
import net.sourceforge.jvlt.utils.Utils;
import net.sourceforge.jvlt.utils.XMLUtils;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

public class DictXMLWriter extends DictWriter {
	public static final int FORMAT_ZIP = 0;
	public static final int FORMAT_XML = 1;

	private static final Comparator<Sense> SENSE_COMPARATOR = new Comparator<Sense>() {
		private final Collator _collator = CustomCollator.getInstance();

		public int compare(Sense s1, Sense s2) {
			return _collator.compare(s1.getTranslation(), s2.getTranslation());
		}
	};

	private DocumentBuilder _builder;
	private final XMLFormatter _formatter;
	private boolean _clear_stats = false;
	private boolean _add_reverse = false;
	private final int _format;

	public DictXMLWriter(Dict dict, OutputStream stream, int format) {
		super(dict, stream);
		_format = format;
		_formatter = new XMLFormatter();
		_formatter.setNoIndentTags(new String[] { "ex" });
		try {
			DocumentBuilderFactory fac = DocumentBuilderFactory.newInstance();
			_builder = fac.newDocumentBuilder();
		} catch (ParserConfigurationException ex) {
			ex.printStackTrace();
		}
	}

	public DictXMLWriter(Dict dict, OutputStream stream) {
		this(dict, stream, FORMAT_ZIP);
	}

	public void setClearStats(boolean clear) {
		_clear_stats = clear;
	}

	/**
	 * Set whether a reverse version of the dictionary (sense - original) will
	 * be added.
	 */
	public void setAddReverse(boolean add) {
		_add_reverse = add;
	}

	@Override
	public void write() throws IOException {
		if (_format == FORMAT_ZIP) {
			ZipOutputStream zos = new ZipOutputStream(_stream);
			zos.putNextEntry(new ZipEntry("dict.xml"));
			writeDict(zos);
			zos.flush();
			zos.closeEntry();
			zos.putNextEntry(new ZipEntry("stats.xml"));
			writeStats(zos);
			zos.close();
		} else if (_format == FORMAT_XML) {
			writeDict(_stream);
		}
	}

	private void writeStats(OutputStream stream) {
		Document doc = _builder.newDocument();

		Element root = doc.createElement("stats");
		root.setAttribute("version", JVLT.getDataVersion());
		doc.appendChild(root);

		Iterator<Entry> it = _dict.getEntries().iterator();
		while (it.hasNext()) {
			Entry entry = it.next();
			if (_clear_stats) {
				entry = (Entry) entry.clone();
				entry.resetStats();
			}
			root.appendChild(_formatter.getXMLForEntryInfo(doc, entry));
		}

		_formatter.printXML(doc, stream);
	}

	private void writeDict(OutputStream stream) {
		Document doc = _builder.newDocument();

		Element root = doc.createElement("dictionary");
		root.setAttribute("version", JVLT.getDataVersion());
		if (_dict.getLanguage() != null) {
			root.setAttribute("language", _dict.getLanguage());
		}
		doc.appendChild(root);

		// Sort and write entries
		ArrayList<Entry> entries = new ArrayList<Entry>(_dict.getEntries());
		Collections.sort(entries, new CollatingEntryComparator());
		Iterator<Entry> it = entries.iterator();
		while (it.hasNext()) {
			root.appendChild(_formatter.getXMLForEntry(doc, it.next()));
		}

		// Write reverse entries
		if (_add_reverse) {
			Node reverse = root.appendChild(doc.createElement("reverse"));
			ArrayList<Sense> senses = new ArrayList<Sense>();
			for (Entry e : entries) {
				for (Sense s : e.getSenses()) {
					senses.add(s);
				}
			}

			Collections.sort(senses, SENSE_COMPARATOR);

			for (Sense s : senses) {
				reverse.appendChild(_formatter.getXMLForSenseReverse(doc, s));
			}
		}

		// Write examples
		Iterator<Example> example_it = _dict.getExamples().iterator();
		while (example_it.hasNext()) {
			root.appendChild(_formatter
					.getXMLForExample(doc, example_it.next()));
		}

		_formatter.printXML(doc, stream);
	}
}

class XMLFormatter {
	private String[] _no_indent_tags;

	public XMLFormatter() {
		_no_indent_tags = new String[0];
	}

	public void setNoIndentTags(String[] tags) {
		_no_indent_tags = tags;
	}

	public Element getXMLForEntry(Document doc, Entry entry) {
		Element entry_elem = doc.createElement("entry");
		entry_elem.setAttribute("id", entry.getID());

		entry_elem.appendChild(XMLUtils.createTextElement(doc, "orth", entry
				.getOrthography()));

		String[] pronunciations = entry.getPronunciations();
		for (String pronunciation : pronunciations) {
			entry_elem.appendChild(XMLUtils.createTextElement(doc, "pron",
					pronunciation));
		}

		EntryClass ec = entry.getEntryClass();
		if (ec != null) {
			entry_elem.setAttribute("class", ec.getName());
			SchemaAttribute[] attrs = ec.getAttributes();
			for (SchemaAttribute attr : attrs) {
				Object value = attr.getValue();
				if (value == null) {
					continue;
				}

				Element attr_elem = doc.createElement("attr");
				entry_elem.appendChild(attr_elem);
				attr_elem.setAttribute("name", attr.getName());
				if (attr instanceof ArraySchemaAttribute) {
					Object[] vals = (Object[]) value;
					for (Object val : vals) {
						Element item_elem = doc.createElement("item");
						attr_elem.appendChild(item_elem);
						item_elem.appendChild(doc
								.createTextNode(val == null ? "" : val
										.toString()));
					}
				} else {
					attr_elem.appendChild(doc.createTextNode(value.toString()));
				}
			}
		}

		Sense[] senses = entry.getSenses();
		for (Sense sense : senses) {
			Element sense_elem = doc.createElement("sense");
			sense_elem.setAttribute("id", sense.getID());

			String trans = sense.getTranslation();
			if (trans != null && !trans.equals("")) {
				sense_elem.appendChild(XMLUtils.createTextElement(doc, "trans",
						trans));
			}

			String def = sense.getDefinition();
			if (def != null && !def.equals("")) {
				sense_elem.appendChild(XMLUtils.createTextElement(doc, "def",
						def));
			}

			for (StringPair p : sense.getCustomFields()) {
				Element field_elem = doc.createElement("custom-field");
				field_elem.appendChild(XMLUtils.createTextElement(doc, "key",
						p.getFirst()));
				field_elem.appendChild(XMLUtils.createTextElement(doc, "value",
						p.getSecond()));
				sense_elem.appendChild(field_elem);
			}

			entry_elem.appendChild(sense_elem);
		}

		String[] categories = entry.getCategories();
		for (String categorie : categories) {
			entry_elem.appendChild(XMLUtils.createTextElement(doc, "category",
					categorie));
		}

		for (StringPair p : entry.getCustomFields()) {
			Element field_elem = doc.createElement("custom-field");
			field_elem.appendChild(XMLUtils.createTextElement(doc, "key", p
					.getFirst()));
			field_elem.appendChild(XMLUtils.createTextElement(doc, "value", p
					.getSecond()));
			entry_elem.appendChild(field_elem);
		}

		entry_elem.appendChild(XMLUtils.createTextElement(doc, "lesson", entry
				.getLesson()));

		String[] mm_files = entry.getMultimediaFiles();
		for (String mmFile : mm_files) {
			entry_elem.appendChild(XMLUtils.createTextElement(doc,
					"multimedia", mmFile));
		}

		return entry_elem;
	}

	public Element getXMLForEntryInfo(Document doc, Entry entry) {
		Element entry_elem = doc.createElement("entry-info");
		entry_elem.setAttribute("entry-id", entry.getID());
		entry_elem.setAttribute("queried", String
				.valueOf(entry.getNumQueried()));
		entry_elem.setAttribute("mistakes", String.valueOf(entry
				.getNumMistakes()));
		if (entry.getLastQueried() != null) {
			entry_elem.setAttribute("last-queried", Utils
					.calendarToString(entry.getLastQueried()));
		}
		if (entry.getDateAdded() != null) {
			entry_elem.setAttribute("date-added", Utils.calendarToString(entry
					.getDateAdded()));
		}
		entry_elem.setAttribute("batch", String.valueOf(entry.getBatch()));
		entry_elem.setAttribute("flags", String.valueOf(entry.getUserFlags()));
		if (entry.getLastQuizResult() != null) {
			entry_elem.setAttribute("last-result", String.valueOf(entry
					.getLastQuizResult()));
		}

		return entry_elem;
	}

	public Element getXMLForExample(Document doc, Example example) {
		Element example_elem = doc.createElement("example");
		example_elem.setAttribute("id", example.getID());

		Element ex_elem = doc.createElement("ex");
		example_elem.appendChild(ex_elem);

		Example.TextFragment[] fragments = example.getTextFragments();
		for (TextFragment tf : fragments) {
			if (tf.getSense() == null) {
				ex_elem.appendChild(doc.createTextNode(XMLUtils.escapeText(tf
						.getText())));
			} else {
				Sense sense = tf.getSense();
				Element link_elem = doc.createElement("link");
				link_elem.setAttribute("sid", sense.getID());
				link_elem.appendChild(doc.createTextNode(XMLUtils.escapeText(tf
						.getText())));
				ex_elem.appendChild(link_elem);
			}
		}

		String translation = example.getTranslation();
		if (translation != null && !translation.equals("")) {
			example_elem.appendChild(XMLUtils.createTextElement(doc, "tr",
					translation));
		}

		return example_elem;
	}

	public Element getXMLForSenseReverse(Document doc, Sense s) {
		Element elem = doc.createElement("sense-ref");
		elem.setAttribute("sense-id", s.getID());
		elem.setAttribute("entry-id", s.getParent().getID());

		return elem;
	}

	public void printXML(Document doc, OutputStream stream) {
		try {
			XMLWriter writer = new XMLWriter(stream);
			writer.setNoIndentTags(_no_indent_tags);
			writer.write(doc);
		} catch (IOException ex) {
			ex.printStackTrace();
		}
	}
}
