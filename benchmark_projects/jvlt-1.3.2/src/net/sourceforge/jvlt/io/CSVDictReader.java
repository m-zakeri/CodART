package net.sourceforge.jvlt.io;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Vector;

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
import net.sourceforge.jvlt.utils.AttributeResources;
import net.sourceforge.jvlt.utils.ExampleBuilder;
import net.sourceforge.jvlt.utils.I18nService;
import net.sourceforge.jvlt.utils.SimpleHTMLParser;
import net.sourceforge.jvlt.utils.Utils;

public class CSVDictReader extends DictReader {
	private char _field_delimiter = ',';
	private char _text_delimiter = '"';
	private String _charset = "UTF-8";
	private String _language = null;
	private boolean _ignore_first_line = false;
	private int _num_senses = 1;
	private int _num_categories = 0;
	private int _num_mmfiles = 0;
	private int _num_examples = 0;
	private String[] _attributes = new String[0];
	private int[] _attribute_columns = new int[0];
	private final SimpleHTMLParser _parser = new SimpleHTMLParser();
	private final Map<String, Example> _example_map;
	private final List<Entry> _duplicate_entries;
	// _attribute_translations maps the translations to the keys
	private final Map<String, Object> _attribute_translations;

	public CSVDictReader() {
		_example_map = new HashMap<String, Example>();
		_duplicate_entries = new ArrayList<Entry>();
		_attribute_translations = new HashMap<String, Object>();

		AttributeResources resources = new AttributeResources();
		for (Enumeration<String> keys = resources.getKeys(); keys
				.hasMoreElements();) {
			String key = keys.nextElement();
			String val = resources.getString(key);
			_attribute_translations.put(val, key);
		}
	}

	public void setTextDelimiter(char c) {
		_text_delimiter = c;
	}

	public void setFieldDelimiter(char c) {
		_field_delimiter = c;
	}

	public void setCharset(String charset) {
		_charset = charset;
	}

	public void setLanguage(String language) {
		_language = language;
	}

	public void setIgnoreFirstLine(boolean ignore) {
		_ignore_first_line = ignore;
	}

	public void setNumSenses(int num) {
		_num_senses = num;
	}

	public void setNumCategories(int num) {
		_num_categories = num;
	}

	public void setNumMultimediaFiles(int num) {
		_num_mmfiles = num;
	}

	public void setNumExamples(int num) {
		_num_examples = num;
	}

	public void setAttributes(String[] attrs) {
		_attributes = attrs;
	}

	public void setAttributeColumns(int[] columns) {
		_attribute_columns = columns;
	}

	@Override
	public void read(InputStream stream) throws DictReaderException,
			IOException {
		_dict = new Dict();
		_duplicate_entries.clear();
		_example_map.clear();
		try {
			_dict.setLanguage(_language);
		} catch (DictException e) {
			throw new DictReaderException("No such language: " + _language);
		}
		InputStreamReader isr = new InputStreamReader(stream, _charset);
		BufferedReader br = new BufferedReader(isr);
		ArrayList<String> fields = new ArrayList<String>();
		String msg = I18nService.getString("Messages", "invalid_file_format");
		int line_no = 0;
		if (_ignore_first_line && br.ready()) {
			br.readLine();
			line_no++;
		}
		while (br.ready()) {
			line_no++;
			String line = br.readLine();
			fields.clear();
			int index = 0;
			while (index < line.length()) {
				int i = index;
				boolean text_delim = false;
				if (line.charAt(i) == _text_delimiter) {
					text_delim = true;
					i++;
				}

				// Increase i until the next delimiter is reached.
				for (; i < line.length(); i++) {
					if (text_delim) {
						if (line.charAt(i) == _text_delimiter) {
							break;
						}
					} else if (line.charAt(i) == _field_delimiter) {
						break;
					}
				}

				// Add a new field
				if (text_delim) {
					fields.add(line.substring(index + 1, i));
					if (i + 1 < line.length()
							&& line.charAt(i + 1) != _field_delimiter) {
						String str = "Error at line " + line_no + ", column "
								+ (i + 2) + ": Character \""
								+ line.charAt(i + 1) + "\" unexpected.";
						throw new DictReaderException(msg, str);
					}
					index = i + 2;
				} else {
					fields.add(line.substring(index, i));
					index = i + 1;
				}
			}

			try {
				processRow(fields);
			} catch (DictReaderException e) {
				String long_message = line + "\n" + e.getShortMessage();
				if (!e.getLongMessage().equals("")) {
					long_message += "\n" + e.getLongMessage();
				}
				String short_message = "Error in line " + line_no;
				throw new DictReaderException(short_message, long_message);
			}
		}
		if (!_duplicate_entries.isEmpty()) {
			Entry[] entries = _duplicate_entries.toArray(new Entry[0]);
			String long_msg = I18nService.getString("Messages",
					"duplicate_entries", new String[] { Utils
							.arrayToString(entries) });
			throw new DictReaderException(msg, long_msg);
		}
	}

	private void processRow(Collection<String> fields)
			throws DictReaderException {
		Iterator<String> it = fields.iterator();
		Entry entry = new Entry(_dict.getNextUnusedEntryID());
		String translation = "";
		String definition = "";
		String example_str = "";
		HashMap<SchemaAttribute, Vector<String>> attr_value_map = new HashMap<SchemaAttribute, Vector<String>>();
		int senses_index = 2;
		int lesson_index = senses_index + 2 * _num_senses;
		int categories_index = lesson_index + 1;
		int mmfiles_index = categories_index + _num_categories;
		int examples_index = mmfiles_index + _num_mmfiles;
		int class_index = examples_index + 3 * _num_examples;
		int attr_index = class_index + 1;

		int num_cols;
		if (_dict.getLanguage() == null) {
			num_cols = class_index;
		} else {
			int num_attr_cols = 0;
			for (int attributeColumn : _attribute_columns) {
				num_attr_cols += attributeColumn;
			}
			num_cols = attr_index + num_attr_cols;
		}
		if (fields.size() > num_cols) {
			throw new DictReaderException("Too many columns, expected "
					+ num_cols);
		}

		for (int i = 0; it.hasNext(); i++) {
			String s = it.next();
			if (i == 0) {
				entry.setOrthography(s);
			} else if (i == 1) {
				// Only one pronunciation is supported at the moment
				if (!"".equals(s)) {
					entry.addPronunciation(s);
				}
			} else if (i < lesson_index) {
				if (i % 2 == 0) {
					translation = s;
				} else {
					definition = s;
					if (!"".equals(translation) || !"".equals(definition)) {
						Sense sense = new Sense(translation, definition);
						try {
							entry.addSense(sense);
						} catch (DictException e) {
							throw new DictReaderException(e.getMessage());
						}
					}
				}
			} else if (i < categories_index) {
				entry.setLesson(s);
			} else if (i < mmfiles_index) {
				if (!"".equals(s)) {
					entry.addCategory(s);
				}
			} else if (i < examples_index) {
				if (!"".equals(s)) {
					entry.addMultimediaFile(s);
				}
			} else if (i < class_index) {
				if ((i - examples_index) % 3 == 0) {
					if ("".equals(s)) {
						continue;
					}

					try {
						_parser.parse(s);
					} catch (ParseException e) {
						throw new DictReaderException(e.getMessage());
					}

					if (!_example_map.containsKey(s)) {
						Example example = new Example(_dict
								.getNextUnusedExampleID());
						example.addTextFragment(new Example.TextFragment(s));
						_example_map.put(s, example);
						try {
							_dict.addExample(example);
						} catch (DictException e) {
							throw new DictReaderException(e.getMessage());
						}
					}
					example_str = s;
				} else if ((i - examples_index) % 3 == 1) {
					if (example_str.equals("")) {
						continue;
					}

					int index = -1;
					String str = "";
					if ("".equals(s)) {
						index = 0;
						str = entry.getOrthography();
					} else if (s.indexOf(";") >= 0) {
						// By using -1 as second argument, trailing empty
						// strings are not ignored
						String[] values = s.split(";", -1);
						str = values[0];
						try {
							index = Integer.parseInt(values[1]) - 1;
						} catch (NumberFormatException e) {
							throw new DictReaderException(
									"Invalid number format: \"" + values[1]
											+ "\"");
						}
					} else {
						// Test whether string s represents a number
						boolean is_number = true;
						for (int j = 0; j < s.length(); j++) {
							if (!Character.isDigit(s.charAt(j))) {
								is_number = false;
								break;
							}
						}

						if (is_number) {
							index = Integer.parseInt(s) - 1;
							str = entry.getOrthography();
						} else {
							index = 0;
							str = s;
						}
					} // end of else

					int pos = example_str.indexOf(str);
					if (pos < 0) {
						throw new DictReaderException(
								"Could not create link to " + str);
					}

					Sense[] senses = entry.getSenses();
					if (index < 0 || index >= senses.length) {
						throw new DictReaderException("Invalid sense index "
								+ index);
					}

					Example ex = _example_map.get(example_str);
					ExampleBuilder builder = new ExampleBuilder(ex);
					try {
						builder.addSense(senses[index], pos, pos + str.length()
								- 1);
					} catch (DictException e) {
						throw new DictReaderException(e.getMessage());
					}
				} // else if ((i - examples_index) % 3 == 1)
				else {
					if ("".equals(s) || "".equals(example_str)) {
						example_str = "";
						continue;
					}

					try {
						_parser.parse(s);
					} catch (ParseException e) {
						throw new DictReaderException(e.getMessage());
					}

					Example ex = _example_map.get(example_str);
					ex.setTranslation(s);
					example_str = "";
				}
			} else if (i < attr_index) {
				if (!"".equals(s)) {
					EntryAttributeSchema eas = _dict.getEntryAttributeSchema();
					if (eas == null) {
						throw new DictReaderException("No language set");
					}

					EntryClass ec = eas.getEntryClass(s);
					if (ec == null) {
						// Maybe the translation instead of the key has been
						// specified
						ec = eas.getEntryClass((String) _attribute_translations
								.get(s));
						if (ec == null) {
							throw new DictReaderException(
									"Unknown word class: '" + s + "'");
						}
					}
					entry.setEntryClass((EntryClass) ec.clone());
				}
			} else { // if (i >= attr_index)
				if (!"".equals(s)) {
					EntryClass cl = entry.getEntryClass();
					if (cl == null) {
						throw new DictReaderException("Error: no entry class.");
					}

					String attr_name = getAttribute(i - attr_index);
					if (attr_name == null) {
						throw new DictReaderException(
								"Column index too large: " + (i + 1));
					}

					SchemaAttribute attr = cl.getAttribute(attr_name);
					if (attr == null) {
						attr = cl.getAttribute((String) _attribute_translations
								.get(attr_name));
						if (attr == null) {
							throw new DictReaderException(
									"Unknown attribute: '" + attr_name + "'");
						}
					}

					if (!attr_value_map.containsKey(attr)) {
						attr_value_map.put(attr, new Vector<String>());
					}

					attr_value_map.get(attr).add(s);
				}
			}
		} // end of for (int i=0; it.hasNext(); i++)

		// -----
		// Set values for language-specific attributes
		// -----
		Iterator<SchemaAttribute> iter = attr_value_map.keySet().iterator();
		while (iter.hasNext()) {
			SchemaAttribute attr = iter.next();
			List<String> vec = attr_value_map.get(attr);
			if (!vec.isEmpty()) {
				String[] vals = vec.toArray(new String[0]);
				if (attr instanceof ChoiceSchemaAttribute) {
					AttributeChoice[] choices = new AttributeChoice[vals.length];
					for (int i = 0; i < vals.length; i++) {
						String val = vals[i];
						AttributeChoice ac = ((ChoiceSchemaAttribute) attr)
								.getChoice(val);
						if (ac == null) {
							ac = ((ChoiceSchemaAttribute) attr)
									.getChoice((String) _attribute_translations
											.get(vals));
							if (ac == null) {
								throw new DictReaderException(
										"Invalid attribute value: '" + val
												+ "'");
							}
						}

						choices[i] = ac;
					}
					if (attr instanceof ArraySchemaAttribute) {
						attr.setValue(choices);
					} else {
						attr.setValue(choices[0]);
					}
				} else {
					attr.setValue(Utils.arrayToString(vals));
				}
			}
		}

		try {
			_dict.addEntry(entry);
		} catch (DictException e) {
			_duplicate_entries.add(entry);
		}
	}

	private String getAttribute(int index) {
		int pos = 0;
		for (int i = 0; i < _attributes.length; i++) {
			pos += _attribute_columns[i];
			if (index < pos) {
				return _attributes[i];
			}
		}
		return null;
	}
}
