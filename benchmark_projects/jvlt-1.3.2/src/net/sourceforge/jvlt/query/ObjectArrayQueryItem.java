package net.sourceforge.jvlt.query;

public class ObjectArrayQueryItem extends ObjectQueryItem {
	public static final int ITEM_CONTAINS = 0;
	public static final int EMPTY = 1;
	public static final int CONTAINS_AT_LEAST_ONE_ITEM = 2;

	private boolean _match_case = false;

	public ObjectArrayQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public ObjectArrayQueryItem() {
		this(null, 0, null);
	}

	public boolean getMatchCase() {
		return _match_case;
	}

	public void setMatchCase(boolean match) {
		_match_case = match;
	}

	@Override
	public boolean objectMatches(Object obj) {
		Object[] array = (obj == null) ? new Object[0] : (Object[]) obj;

		if (_type == EMPTY) {
			return array.length == 0;
		} else if (_type == CONTAINS_AT_LEAST_ONE_ITEM) {
			return array.length > 0;
		} else if (_type == ITEM_CONTAINS) {
			if (_value == null) {
				return true;
			}
			for (Object element : array) {
				if (_match_case) {
					if (element.toString().indexOf(_value.toString()) >= 0) {
						return true;
					}
				} else {
					if (element.toString().toLowerCase().indexOf(
							_value.toString().toLowerCase()) >= 0) {
						return true;
					}
				}
			}

			return false;
		} else {
			return false;
		}
	}
}
