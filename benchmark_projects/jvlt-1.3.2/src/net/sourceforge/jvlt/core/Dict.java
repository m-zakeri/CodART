package net.sourceforge.jvlt.core;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

import javax.xml.xpath.XPathExpressionException;

import net.sourceforge.jvlt.io.EntryAttributeSchemaReader;

public class Dict extends Object {
	private static Entry.Comparator _entry_comparator = new Entry.Comparator();
	private static Example.Comparator _example_comparator = new Example.Comparator();

	private final TreeSet<Entry> _entry_set;
	private final TreeSet<Example> _example_set;
	private final HashMap<String, Entry> _id_entry_map;
	private final HashMap<String, Example> _id_example_map;
	private String _language;
	private EntryAttributeSchema _schema;

	public Dict() {
		_entry_set = new TreeSet<Entry>(new Entry.Comparator());
		_example_set = new TreeSet<Example>(new Example.Comparator());
		_id_entry_map = new HashMap<String, Entry>();
		_id_example_map = new HashMap<String, Example>();
		_language = null;
	}

	/**
	 * @throws DictException If an entry with the same primary key as the
	 *             argument entry already exists in the dictionary.
	 */
	public void addEntry(Entry entry) throws DictException {
		if (_entry_set.contains(entry)) {
			throw new DictException("Entry \"" + entry + "\" already exists.");
		}

		if (_id_entry_map.containsKey(entry.getID())) {
			entry.setID(getNextUnusedEntryID());
		}

		_entry_set.add(entry);
		_id_entry_map.put(entry.getID(), entry);
	}

	public void removeEntry(Entry entry) throws DictException {
		Collection<Example> examples = getExamples(entry);
		if (examples.size() > 0) {
			String msg = "Entry \"" + entry + "\" cannot be removed "
					+ "as there are " + examples.size() + " linked examples.";
			throw new DictException(msg);
		}
		_id_entry_map.remove(entry.getID());
		_entry_set.remove(entry);
	}

	public int getEntryCount() {
		return _entry_set.size();
	}

	public Entry getEntry(String id) {
		if (_id_entry_map.containsKey(id)) {
			return _id_entry_map.get(id);
		}
		return null;
	}

	public Entry getEntry(Entry entry) {
		SortedSet<Entry> tail = _entry_set.tailSet(entry);
		if (tail.size() == 0) {
			return null;
		}
		Entry first = tail.iterator().next();
		if (_entry_comparator.compare(first, entry) != 0) {
			return null;
		}
		return first;
	}

	public Collection<Entry> getEntries() {
		return _entry_set;
	}

	public String getNextUnusedEntryID() {
		Set<String> keys = _id_entry_map.keySet();
		for (int i = 1;; i++) {
			String id = "e" + i;
			if (!keys.contains(id)) {
				return id;
			}
		}
	}

	public String getNextUnusedExampleID() {
		Set<String> keys = _id_example_map.keySet();
		for (int i = 1;; i++) {
			String id = "x" + i;
			if (!keys.contains(id)) {
				return id;
			}
		}
	}

	public void addExample(Example example) throws DictException {
		if (_example_set.contains(example)) {
			throw new DictException("Example \"" + example
					+ "\" already exists.");
		}

		if (_id_example_map.containsKey(example.getID())) {
			example.setID(getNextUnusedExampleID());
		}

		_example_set.add(example);
		_id_example_map.put(example.getID(), example);
	}

	public void removeExample(Example example) {
		_id_example_map.remove(example.getID());
		_example_set.remove(example);
	}

	public int getExampleCount() {
		return _example_set.size();
	}

	public Example getExample(String id) {
		if (_id_example_map.containsKey(id)) {
			return _id_example_map.get(id);
		}
		return null;
	}

	public Example getExample(Example example) {
		SortedSet<Example> tail = _example_set.tailSet(example);
		if (tail.size() == 0) {
			return null;
		}
		Example first = tail.iterator().next();
		if (_example_comparator.compare(first, example) != 0) {
			return null;
		}
		return first;
	}

	public Collection<Example> getExamples(Sense sense) {
		TreeSet<Example> example_set = new TreeSet<Example>();
		Iterator<Example> it = _example_set.iterator();
		while (it.hasNext()) {
			Example example = it.next();
			List<Sense> senses = Arrays.asList(example.getSenses());
			if (senses.contains(sense)) {
				example_set.add(example);
			}
		}

		return example_set;
	}

	public Collection<Example> getExamples(Entry entry) {
		TreeSet<Example> example_set = new TreeSet<Example>();
		if (entry == null) {
			return example_set;
		}

		Sense[] senses = entry.getSenses();
		for (Sense sense : senses) {
			example_set.addAll(getExamples(sense));
		}

		return example_set;
	}

	public Collection<Example> getExamples() {
		return _example_set;
	}

	public String getLanguage() {
		return _language;
	}

	public void setLanguage(String lang) throws DictException {
		if (lang == null || lang.equals("")) {
			_language = null;
		} else {
			_language = lang;
		}

		_schema = null;
		if (lang == null) {
			return;
		}

		try {
			EntryAttributeSchemaReader reader = new EntryAttributeSchemaReader();
			_schema = reader.readSchema(lang);
		} catch (XPathExpressionException ex) {
			throw new DictException("Could not read schema file for language '"
					+ lang + "'.");
		}
	}

	public EntryAttributeSchema getEntryAttributeSchema() {
		return _schema;
	}
}
