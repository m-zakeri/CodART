package net.sourceforge.jvlt.query;

import java.util.ArrayList;
import java.util.Iterator;

/**
 * Query item that contains other query items. This class can be used when a
 * match-all query should contain a match-one query. The attribute name has to
 * be equal for all query items.
 */
public class ContainerQueryItem extends ObjectQueryItem {
	public static final int MATCH_ONE = 0;
	public static final int MATCH_ALL = 1;

	private final ArrayList<ObjectQueryItem> _items = new ArrayList<ObjectQueryItem>();

	public ContainerQueryItem(String name, int type) {
		super(name, type, null);
	}

	public ContainerQueryItem() {
		this(null, MATCH_ONE);
	}

	public void addItem(ObjectQueryItem item) {
		_items.add(item);
	}

	@Override
	public boolean objectMatches(Object o) {
		Iterator<ObjectQueryItem> it = _items.iterator();
		while (it.hasNext()) {
			ObjectQueryItem item = it.next();
			if (_type == MATCH_ONE && item.objectMatches(o)) {
				return true;
			} else if (_type == MATCH_ALL && !item.objectMatches(o)) {
				return false;
			}
		}

		return _type == MATCH_ALL;
	}
}
