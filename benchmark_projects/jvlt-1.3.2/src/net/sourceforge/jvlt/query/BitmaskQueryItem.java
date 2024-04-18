package net.sourceforge.jvlt.query;

public class BitmaskQueryItem extends ObjectQueryItem {
	public static final int CONTAINS_ALL_ITEMS = 0;
	public static final int CONTAINS_ONE_ITEM = 1;

	public BitmaskQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public BitmaskQueryItem() {
		super();
	}

	@Override
	public boolean objectMatches(Object o) {
		Integer val1 = (Integer) _value;
		Integer val2 = (Integer) o;

		switch (_type) {
		case CONTAINS_ALL_ITEMS:
			return (val1 & val2) == val1;
		case CONTAINS_ONE_ITEM:
			return (val1 & val2) != 0;
		default:
			return false;
		}
	}
}
