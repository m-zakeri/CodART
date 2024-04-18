package net.sourceforge.jvlt.query;

import net.sourceforge.jvlt.core.EntryClass;

public class EntryClassQueryItem extends ObjectQueryItem {
	public static final int EQUALS = 0;
	public static final int NOT_EQUAL = 1;

	/**
	 * Constructor
	 * 
	 * @param name The name
	 * @param type The type
	 * @param value The value (of type java.lang.String)
	 */
	public EntryClassQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public EntryClassQueryItem() {
		super();
	}

	@Override
	public boolean objectMatches(Object obj) {
		EntryClass ec = (EntryClass) obj;
		if (_type == EntryClassQueryItem.EQUALS) {
			return _value == null ? obj == null : ec != null
					&& _value.equals(ec.getName());
		} else if (_type == EntryClassQueryItem.NOT_EQUAL) {
			return !(_value == null ? obj == null : ec != null
					&& _value.equals(ec.getName()));
		} else {
			return false;
		}
	}
}
