package net.sourceforge.jvlt.io;

import java.io.IOException;
import java.io.InputStream;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import net.sourceforge.jvlt.JVLT;
import net.sourceforge.jvlt.core.ArraySchemaAttribute;
import net.sourceforge.jvlt.core.AttributeChoice;
import net.sourceforge.jvlt.core.ChoiceSchemaAttribute;
import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.EntryAttributeSchema;
import net.sourceforge.jvlt.core.EntryClass;
import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.core.SchemaAttribute;
import net.sourceforge.jvlt.core.Sense;
import net.sourceforge.jvlt.utils.I18nService;
import net.sourceforge.jvlt.utils.Utils;
import net.sourceforge.jvlt.utils.XMLUtils;

import org.apache.log4j.Logger;
import org.xml.sax.Attributes;
import org.xml.sax.Locator;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class SAXDictReader extends DictReader {
	static class NonCloseableZipInputStream extends ZipInputStream {
		NonCloseableZipInputStream(InputStream is) {
			super(is);
		}
		
		public void close() throws IOException {
			// Do nothing. Solves the problem that SAXParser closes the stream
			// after reading it.
		}
		
		public void doClose() throws IOException {
			// Really close
			super.close();
		}
	}
	
	public SAXDictReader(String version) {
		super(version);
	}

	public SAXDictReader() {
		super();
	}

	@Override
	public void read(InputStream stream) throws DictReaderException,
			IOException {
		_dict = new Dict();
		NonCloseableZipInputStream zis = new NonCloseableZipInputStream(stream);
		
		try {
			for (int i=0; i<2; i++) {
				ZipEntry entry = zis.getNextEntry();
				if (entry == null) {
					throw new IOException("Invalid file format");
				} else if (entry.getName().equals("dict.xml")) {
					readDict(zis);
				} else if (entry.getName().equals("stats.xml")) {
					readStats(zis);
				} else {
					throw new IOException("Invalid file format");
				}
			}
		} finally {
			zis.doClose();
		}
	}

	protected void readDict(InputStream stream) throws DictReaderException {
		if (_version == null) {
			readXML(stream, new DictHandler(_dict));
		} else {
			readXML(stream, new DictHandler(_dict, _version));
		}
	}

	protected void readStats(InputStream stream) throws DictReaderException {
		if (_version == null) {
			readXML(stream, new StatsHandler(_dict));
		} else {
			readXML(stream, new StatsHandler(_dict, _version));
		}
	}

	private void readXML(InputStream stream, DefaultHandler handler)
			throws DictReaderException {
		SAXParserFactory fac = SAXParserFactory.newInstance();
		try {
			SAXParser parser = fac.newSAXParser();
			parser.parse(stream, handler);
		} catch (SAXException ex) {
			Exception e = ex.getException();
			if (e != null) {
				if (e instanceof DictReaderException) {
					throw (DictReaderException) e;
				} else if (e instanceof VersionException) {
					throw new DictReaderException(I18nService.getString(
							"Messages", "invalid_xml"), e);
				}
			} else {
				throw new DictReaderException(I18nService.getString("Messages",
						"invalid_xml"), ex.getMessage());
			}
		} catch (Exception ex) {
			ex.printStackTrace();
			throw new DictReaderException(I18nService.getString("Messages",
					"invalid_xml"), ex.getMessage());
		}
	}
}

abstract class AbstractHandler extends DefaultHandler {
	protected Dict _dict;
	protected Locator _locator;
	protected String _version;

	private StringBuffer _current_chars = null;

	public AbstractHandler(Dict dict, String version) {
		_dict = dict;
		_version = version;
	}

	public AbstractHandler(Dict dict) {
		this(dict, JVLT.getDataVersion());
	}

	@Override
	public void characters(char[] ch, int start, int length) {
		if (_current_chars == null) {
			_current_chars = new StringBuffer();
		}

		String s = new String(ch, start, length);
		_current_chars.append(s);
	}

	@Override
	public void setDocumentLocator(Locator loc) {
		_locator = loc;
	}

	protected SAXException getSAXException(String type, String message) {
		String str = "Error at line " + _locator.getLineNumber() + ": "
				+ message;
		DictReaderException ex = new DictReaderException(I18nService.getString(
				"Messages", type), str);

		return new SAXException(str, ex);
	}

	protected String getChars() {
		if (_current_chars == null) {
			return "";
		}
		String str = XMLUtils.unescapeText(_current_chars.toString());
		_current_chars = null;
		return str;
	}
}

class DictHandler extends AbstractHandler {
	private Entry _current_entry = null;
	private Example _current_example = null;
	private Example.TextFragment _current_fragment = null;
	private final HashMap<String, Sense> _id_sense_map;
	private final HashMap<Example.TextFragment, String> _fragment_id_map;
	private Sense _current_sense = null;
	private String _current_trans = null;
	private String _current_def = null;
	private String[] _current_custom_field = null;
	private EntryClass _current_class = null;
	private SchemaAttribute _current_attr = null;
	private ArrayList<AttributeChoice> _current_items = null;
	private final ArrayList<Entry> _duplicate_entries = new ArrayList<Entry>();
	private final ArrayList<Example> _duplicate_examples = new ArrayList<Example>();

	public DictHandler(Dict dict, String version) {
		super(dict, version);
		_id_sense_map = new HashMap<String, Sense>();
		_fragment_id_map = new HashMap<Example.TextFragment, String>();
	}

	public DictHandler(Dict dict) {
		this(dict, JVLT.getDataVersion());
	}

	@Override
	public void endDocument() throws SAXException {
		if (_duplicate_entries.size() > 0 || _duplicate_examples.size() > 0) {
			String msg = I18nService.getString("Messages",
					"duplicate_entries_examples");
			Entry[] entries = _duplicate_entries.toArray(new Entry[0]);
			Example[] examples = _duplicate_examples.toArray(new Example[0]);
			String long_msg = "";
			if (entries.length > 0) {
				long_msg += I18nService.getString("Messages", "duplicate_entries",
						new String[] { Utils.arrayToString(entries) });
			}
			if (examples.length > 0) {
				if (entries.length > 0) {
					long_msg += "\n";
				}
				long_msg += I18nService.getString("Messages",
						"duplicate_examples", new String[] { Utils
								.arrayToString(examples) });
			}

			throw new SAXException(msg, new DictReaderException(msg, long_msg));
		}

		// Create links from examples to senses.
		Iterator<Example.TextFragment> it = _fragment_id_map.keySet()
				.iterator();
		while (it.hasNext()) {
			Example.TextFragment fragment = it.next();
			String id = _fragment_id_map.get(fragment);
			if (!_id_sense_map.containsKey(id)) {
				throw getSAXException("invalid_xml",
						"Invalid link from example to sense.");
			}

			Sense sense = _id_sense_map.get(id);
			fragment.setSense(sense);
		}
	}

	@Override
	public void endElement(String uri, String local_name, String qname)
			throws SAXException {
		if (qname.equals("entry")) {
			// Older versions of jVLT created files which contained tags trans
			// and def that were not children of a sense tag - in case there
			// was only one sense for the specific word.
			if (_current_trans != null || _current_def != null) {
				Sense sense = new Sense();
				_id_sense_map.put(_current_entry.getID(), sense);
				if (_current_trans != null) {
					sense.setTranslation(_current_trans);
				}
				if (_current_def != null) {
					sense.setDefinition(_current_def);
				}
				try {
					_current_entry.addSense(sense);
				} catch (DictException ex) {
					throw getSAXException("invalid_xml", "Duplicate sense: "
							+ ex.getMessage());
				}

				_current_trans = null;
				_current_def = null;
			}

			try {
				_dict.addEntry(_current_entry);
			} catch (DictException ex) {
				_duplicate_entries.add(_current_entry);
			}

			_current_entry = null;
			_current_class = null;
		} else if (qname.equals("orth")) {
			_current_entry.setOrthography(getChars());
		} else if (qname.equals("pron")) {
			_current_entry.addPronunciation(getChars());
		} else if (qname.equals("sense")) {
			if (_current_trans != null) {
				_current_sense.setTranslation(_current_trans);
			}
			if (_current_def != null) {
				_current_sense.setDefinition(_current_def);
			}
			try {
				_current_entry.addSense(_current_sense);
			} catch (DictException ex) {
				throw getSAXException("invalid_xml", "Duplicate sense: "
						+ ex.getMessage());
			}

			_current_trans = null;
			_current_def = null;
			_current_sense = null;
		} else if (qname.equals("trans")) {
			_current_trans = getChars();
		} else if (qname.equals("def")) {
			_current_def = getChars();
		} else if (qname.equals("example")) {
			try {
				_dict.addExample(_current_example);
			} catch (DictException ex) {
				_duplicate_examples.add(_current_example);
			}

			_current_example = null;
		} else if (qname.equals("ex")) {
			String chars = getChars();
			if (!chars.equals("")) {
				_current_example
						.addTextFragment(new Example.TextFragment(chars));
			}
		} else if (qname.equals("link")) {
			_current_fragment.setText(getChars());
			_current_example.addTextFragment(_current_fragment);

			_current_fragment = null;
		} else if (qname.equals("tr")) {
			_current_example.setTranslation(getChars());
		} else if (qname.equals("category")) {
			if (_current_entry != null) {
				_current_entry.addCategory(getChars());
			}
		} else if (qname.equals("custom-field")) {
			if (_current_custom_field != null
					&& _current_custom_field[0] != null
					&& _current_custom_field[1] != null) {
				if (_current_sense != null) {
					_current_sense.addCustomField(_current_custom_field[0],
							_current_custom_field[1]);
				} else if (_current_entry != null) {
					_current_entry.addCustomField(_current_custom_field[0],
							_current_custom_field[1]);
				}
			}

			_current_custom_field = null;
		} else if (qname.equals("key")) {
			if (_current_custom_field != null) {
				_current_custom_field[0] = getChars();
			}
		} else if (qname.equals("value")) {
			if (_current_custom_field != null) {
				_current_custom_field[1] = getChars();
			}
		} else if (qname.equals("lesson")) {
			if (_current_entry != null) {
				_current_entry.setLesson(getChars());
			}
		} else if (qname.equals("multimedia")) {
			if (_current_entry != null) {
				_current_entry.addMultimediaFile(getChars());
			}
		} else if (qname.equals("attr")) {
			if (_current_attr instanceof ArraySchemaAttribute) {
				_current_attr.setValue(_current_items
						.toArray(new AttributeChoice[0]));
			} else if (_current_attr instanceof ChoiceSchemaAttribute) {
				_current_attr.setValue(getAttributeChoice(
						(ChoiceSchemaAttribute) _current_attr, getChars()));
			} else {
				String val = getChars();
				if (val.length() > 0) {
					_current_attr.setValue(val);
				}
			}

			_current_attr = null;
			_current_items = null;
		} else if (qname.equals("item")) {
			_current_items.add(getAttributeChoice(
					(ChoiceSchemaAttribute) _current_attr, getChars()));
		}
	}

	@Override
	public void startElement(String uri, String local_name, String qname,
			Attributes attributes) throws SAXException {
		if (qname.equals("dictionary")) {
			String language = attributes.getValue("language");
			if (language != null && !language.equals("")) {
				try {
					_dict.setLanguage(attributes.getValue("language"));
				} catch (DictException e) {
					throw getSAXException("invalid_xml", e.getMessage());
				}
			}
			String version = attributes.getValue("version");
			if (version != null && !version.equals(_version)) {
				throw new SAXException(new VersionException(version));
			}
		} else if (qname.equals("entry")) {
			String id = attributes.getValue("id");
			if (id == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"id\" is missing.");
			}

			String cl = attributes.getValue("class");
			if (cl != null && !cl.equals("")) {
				EntryAttributeSchema schema = _dict.getEntryAttributeSchema();
				if (schema == null) {
					throw getSAXException("invalid_xml", "No language set.");
				}

				EntryClass ec = schema.getEntryClass(cl);
				if (ec == null) {
					throw getSAXException("invalid_xml",
							"Unknown word class: '" + cl + "'");
				}
				_current_class = (EntryClass) ec.clone();
			}

			_current_entry = new Entry(id);
			_current_entry.setEntryClass(_current_class);
		} else if (qname.equals("sense")) {
			String id = attributes.getValue("id");
			if (id == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"id\" is missing.");
			}

			_current_sense = new Sense();
			_id_sense_map.put(id, _current_sense);
		} else if (qname.equals("example")) {
			String id = attributes.getValue("id");
			if (id == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"id\" is missing.");
			}

			_current_example = new Example(id);
		} else if (qname.equals("link")) {
			// Save text fragment before link.
			String chars = getChars();
			if (!chars.equals("")) {
				_current_example
						.addTextFragment(new Example.TextFragment(chars));
			}

			String id = attributes.getValue("sid");
			_current_fragment = new Example.TextFragment();
			_fragment_id_map.put(_current_fragment, id);
		} else if (qname.equals("orth") || qname.equals("pron")
				|| qname.equals("trans") || qname.equals("def")
				|| qname.equals("ex") || qname.equals("tr")
				|| qname.equals("category") || qname.equals("lesson")
				|| qname.equals("multimedia") || qname.equals("key")
				|| qname.equals("value")) {
			getChars(); // Clear character cache.
		} else if (qname.equals("custom-field")) {
			getChars();

			_current_custom_field = new String[2];
		} else if (qname.equals("attr")) {
			getChars();
			if (_current_class == null) {
				throw getSAXException("invalid_xml", "No word class set.");
			}

			String name = attributes.getValue("name");
			_current_attr = _current_class.getAttribute(name);
			if (_current_attr == null) {
				throw getSAXException("invalid_xml", "Unknown attribute: '"
						+ name + "'");
			}
			_current_items = new ArrayList<AttributeChoice>();
		} else if (qname.equals("item")) {
			getChars();
		}
	}

	private AttributeChoice getAttributeChoice(ChoiceSchemaAttribute attr,
			String name) throws SAXException {
		AttributeChoice ac = attr.getChoice(name);
		if (ac == null) {
			throw getSAXException("invalid_xml", "Invalid attribute value: '"
					+ name + "'");
		}
		return ac;
	}
}

class StatsHandler extends AbstractHandler {
	private static final Logger logger = Logger.getLogger(SAXDictReader.class);

	public StatsHandler(Dict dict, String version) {
		super(dict, version);
	}

	public StatsHandler(Dict dict) {
		this(dict, JVLT.getDataVersion());
	}

	@Override
	public void startElement(String uri, String local_name, String qname,
			Attributes attributes) throws SAXException {
		if (qname.equals("stats")) {
			String version = attributes.getValue("version");
			if (!version.equals(_version)) {
				throw new SAXException(new VersionException(version));
			}
		} else if (qname.equals("entry-info")) {
			String batchstr = attributes.getValue("batch");
			if (batchstr == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"batch\" is missing.");
			}
			int batch = Integer.decode(batchstr).intValue();
			String entry_id = attributes.getValue("entry-id");
			String queried = attributes.getValue("queried");
			String mistakes = attributes.getValue("mistakes");
			String last_queried = attributes.getValue("last-queried");
			String date_added = attributes.getValue("date-added");
			String last_result = attributes.getValue("last-result");
			String flags = attributes.getValue("flags");
			if (entry_id == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"entry-id\" is missing.");
			} else if (queried == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"queried\" is missing.");
			} else if (mistakes == null) {
				throw getSAXException("invalid_xml",
						"Attribute \"mistakes\" is missing.");
			}

			int num_queried = Integer.decode(queried).intValue();
			int num_mistakes = Integer.decode(mistakes).intValue();
			int user_flags = flags == null ? 0 : Integer.decode(flags)
					.intValue();
			Boolean last_quiz_result = last_result == null ? null : Boolean
					.parseBoolean(last_result);

			Entry entry = _dict.getEntry(entry_id);
			if (entry != null) {
				entry.setLastQueried(stringToDate(last_queried));
				entry.setDateAdded(stringToDate(date_added));
				entry.setNumQueried(num_queried);
				entry.setNumMistakes(num_mistakes);
				entry.setBatch(batch);
				entry.setUserFlags(user_flags);
				if (last_quiz_result != null) {
					entry.setLastQuizResult(last_quiz_result);
				}
			} else {
				logger.warn("No entry with id \"" + entry_id + "\"");
				return;
			}
		} // else if (qname.equals("entry-info"))
	}

	private Calendar stringToDate(String str) throws SAXException {
		Calendar cal = null;
		if (str != null && !str.equals("")) {
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
			Date date;
			try {
				date = sdf.parse(str);
			} catch (ParseException e) {
				throw getSAXException("invalid_xml", "Invalid date format.");
			}
			cal = new GregorianCalendar();
			cal.setTime(date);
		}

		return cal;
	}
}
