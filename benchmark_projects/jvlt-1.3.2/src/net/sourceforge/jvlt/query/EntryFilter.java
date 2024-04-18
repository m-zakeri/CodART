package net.sourceforge.jvlt.query;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import net.sourceforge.jvlt.core.Entry;

public class EntryFilter {
	protected ObjectQuery _query;

	public EntryFilter(ObjectQuery query) {
		_query = query;
	}

	public EntryFilter() {
		this(new ObjectQuery(Entry.class));
	}

	public ObjectQuery getQuery() {
		return _query;
	}

	public void setQuery(ObjectQuery query) {
		_query = query;
	}

	public List<Entry> getMatchingEntries(Collection<Entry> entries) {
		ArrayList<Entry> entry_list = new ArrayList<Entry>();
		for (Entry entry : entries) {
			if (entryMatches(entry)) {
				entry_list.add(entry);
			}
		}

		return entry_list;
	}

	public boolean entryMatches(Entry entry) {
		return _query.objectMatches(entry);
	}
}
