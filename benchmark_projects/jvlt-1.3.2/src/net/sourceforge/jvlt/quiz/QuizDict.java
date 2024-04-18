package net.sourceforge.jvlt.quiz;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeSet;

import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Entry.Stats.UserFlag;
import net.sourceforge.jvlt.metadata.Attribute;
import net.sourceforge.jvlt.model.JVLTModel;
import net.sourceforge.jvlt.query.EntryFilter;

public class QuizDict {
	private final JVLTModel _model;
	private QuizInfo _info = null;
	private EntryFilter[] _filters = null;
	private boolean _ignore_batches;
	private final ArrayList<Entry> _available_entries; // Entries available for
														// quiz
	private final ArrayList<Entry> _current_entries; // Entries during the quiz
	private int _current_index;
	private final Map<Entry, QueryResult> _results;

	public QuizDict(JVLTModel model) {
		_current_index = 0;
		_model = model;
		_filters = null;
		_info = null;
		_results = new HashMap<Entry, QueryResult>();
		_available_entries = new ArrayList<Entry>();
		_current_entries = new ArrayList<Entry>();
	}

	public boolean isIgnoreBatches() {
		return _ignore_batches;
	}

	public void setIgnoreBatches(boolean ignore) {
		_ignore_batches = ignore;
	}

	public int getResultCount() {
		return _results.size();
	}

	public QueryResult getResult(Entry entry) {
		return _results.get(entry);
	}

	public void setResult(Entry entry, QueryResult result) {
		_results.put(entry, result);
	}

	public QuizInfo getQuizInfo() {
		return _info;
	}

	public int getAvailableEntryCount() {
		return _available_entries.size();
	}

	public int getCurrentEntryCount() {
		return _current_entries.size();
	}

	public Entry getCurrentEntry() {
		if (_current_index < 0 || _current_index >= _current_entries.size()) {
			return null;
		}
		return _current_entries.get(_current_index);
	}

	public boolean hasNextEntry() {
		return _current_index + 1 < _current_entries.size();
	}

	public Entry nextEntry() {
		_current_index = _current_index < _current_entries.size() - 1 ? _current_index + 1
				: _current_index;

		return getCurrentEntry();
	}

	public boolean hasPreviousEntry() {
		return _current_index - 1 >= 0
				&& _current_index - 1 < _current_entries.size();
	}

	public Entry previousEntry() {
		_current_index = _current_index > 0 ? _current_index - 1
				: _current_index;

		return getCurrentEntry();
	}

	public Entry[] getKnownEntries() {
		ArrayList<Entry> list = new ArrayList<Entry>();
		for (Map.Entry<Entry, QueryResult> entry : _results.entrySet()) {
			if (entry.getValue().isKnown()) {
				list.add(entry.getKey());
			}
		}

		return list.toArray(new Entry[0]);
	}

	public Entry[] getNotKnownEntries() {
		ArrayList<Entry> list = new ArrayList<Entry>();
		for (Map.Entry<Entry, QueryResult> entry : _results.entrySet()) {
			if (!entry.getValue().isKnown()) {
				list.add(entry.getKey());
			}
		}

		return list.toArray(new Entry[0]);
	}

	/**
	 * Starts a new quiz
	 */
	public void start() {
		_results.clear();
		_current_entries.clear();
		_current_entries.addAll(_available_entries);
		_current_index = 0;
	}

	/**
	 * Reset the dictionary. Clear the result list and reinitialize the entry
	 * list using the not known entries.
	 */
	public void reset() {
		Entry[] not_known = getNotKnownEntries();
		_results.clear();
		_current_entries.clear();
		_current_entries.addAll(Arrays.asList(not_known));
		Collections.shuffle(_current_entries, new Random(new Date().getTime()));
		_current_index = 0;
	}

	/**
	 * Update the quiz dictionary using a new set of filters and/or a different
	 * quiz type.
	 */
	public void update(EntryFilter[] filters, QuizInfo info) {
		_filters = filters;
		_info = info;

		_available_entries.clear();
		_available_entries.addAll(getEntryList(_model.getDict().getEntries(),
				filters));
	}

	/**
	 * Update the quiz dictionary when entries have been added, changed or
	 * removed.
	 */
	public void update(Collection<Entry> new_entries,
			Collection<Entry> changed_entries, Collection<Entry> removed_entries) {
		if (new_entries != null) {
			_available_entries.addAll(getEntryList(new_entries, _filters));
			// Do not add entries to _current_entries, as _current_entries
			// might only contain the not known entries
		}

		if (changed_entries != null) {
			_available_entries.removeAll(changed_entries);
			_available_entries.addAll(getEntryList(changed_entries, _filters));
			// Do not update _current_entries, so entries
			// that do no longer match the filters are not removed
		}

		if (removed_entries != null) {
			_available_entries.removeAll(removed_entries);

			for (Entry e : removed_entries) {
				int index = _current_entries.indexOf(e);

				// Update current index
				if (index >= 0 && index < _current_index) {
					_current_index--;
				}

				if (index >= 0) {
					_current_entries.remove(index);
					_results.remove(e);
				}
			}
		}
	}

	private List<Entry> getEntryList(Collection<Entry> entries,
			EntryFilter[] filters) {
		ArrayList<Entry> return_list = null;

		if (_info == null) {
			return Collections.emptyList();
		}

		// -----
		// Only add those values that
		// 1) have a value for the quizzed attribute,
		// 2) are not yet expired, and
		// 3) don't have a flag that disables them.
		//
		// 2) doesn't need to be fulfilled when batches are ignored. If the
		// flag ALWAYS_QUIZ is set, the entry is always added.
		// -----

		String[] attr_str = _info.getQuizzedAttributes();
		Attribute[] attr = new Attribute[attr_str.length];
		for (int i = 0; i < attr.length; i++) {
			attr[i] = _model.getDictModel().getMetaData(Entry.class)
					.getAttribute(attr_str[i]);
		}

		GregorianCalendar now = new GregorianCalendar();
		ArrayList<Entry> entry_array = new ArrayList<Entry>();
		for (Entry entry : entries) {
			Calendar expiry_date = entry.getExpireDate();

			/* Check whether at least one quizzed attribute is set */
			boolean attribute_set = false;
			for (Attribute element : attr) {
				attribute_set |= (element.getValue(entry) != null);
			}
			if (!attribute_set) {
				continue;
			}

			int flags = entry.getUserFlags();
			if ((flags & UserFlag.ALWAYS_QUIZ.getValue()) != 0) {
				/* Always add the entry if the flag "Quiz until known" is set */
				entry_array.add(entry);
			} else {
				/* Skip if "Inactive" or "Known" flag is set */
				if ((flags & UserFlag.INACTIVE.getValue()) != 0
						|| (flags & UserFlag.KNOWN.getValue()) != 0) {
					continue;
				}

				/* Check for batch and expiry date */
				if (_ignore_batches || entry.getBatch() == 0
						|| expiry_date == null || expiry_date.before(now)) {
					entry_array.add(entry);
				}
			}
		}

		// -----
		// Add the entries that match the filters: First, all entries that
		// match the first filter are added, after that all entries that match
		// the second filter etc.
		// -----
		if (filters.length > 0) {
			TreeSet<Entry> entry_set = new TreeSet<Entry>();
			ArrayList<Entry> entry_list = new ArrayList<Entry>();
			for (EntryFilter filter : filters) {
				entry_list.clear();
				for (Entry entry : entry_array) {
					if (!entry_set.contains(entry)
							&& filter.entryMatches(entry)) {
						entry_set.add(entry);
						entry_list.add(entry);
					}
				}

				Collections.shuffle(entry_list,
						new Random(new Date().getTime()));
				return_list = entry_list;
			}
		}
		// -----
		// If there is no filter, all entries that have been expired are added.
		// -----
		else {
			Collections.shuffle(entry_array, new Random(new Date().getTime()));
			return_list = entry_array;
		}

		return return_list;
	}
}
