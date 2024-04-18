package net.sourceforge.jvlt.utils;

import java.text.Collator;
import java.util.Comparator;

import net.sourceforge.jvlt.core.Entry;

public class CollatingEntryComparator implements Comparator<Entry> {
	Collator _collator;

	public CollatingEntryComparator() {
		_collator = CustomCollator.getInstance();
	}

	public int compare(Entry e1, Entry e2) {
		return _collator.compare(e1.getOrthography(), e2.getOrthography());
	}
}
