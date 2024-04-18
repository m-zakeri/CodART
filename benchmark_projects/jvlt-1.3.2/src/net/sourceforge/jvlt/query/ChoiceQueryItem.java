package net.sourceforge.jvlt.query;

public class ChoiceQueryItem extends ObjectQueryItem {
	public static final int EQUALS = 0;
	public static final int NOT_EQUAL = 1;
	public static final int CONTAINS = 2;
	public static final int EMPTY = 3;
	public static final int NOT_EMPTY = 4;

	public ChoiceQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public ChoiceQueryItem() {
		this("", EQUALS, null);
	}

	@Override
	public boolean objectMatches(Object obj) {
		if (_type == StringQueryItem.EQUALS) {
			if (obj == null) {
				return _value == null;
			} else if (_value == null) {
				return false;
			} else {
				return obj.toString().equals(_value.toString());
			}
		} else if (_type == NOT_EQUAL) {
			if (obj == null) {
				return _value != null;
			} else if (_value == null) {
				return true;
			} else {
				return !obj.toString().equals(_value.toString());
			}
		} else if (_type == CONTAINS) {
			if (_value == null) {
				return true;
			} else if (obj == null) {
				return false;
			} else {
				return obj.toString().toLowerCase().indexOf(
						_value.toString().toLowerCase()) >= 0;
			}
		} else if (_type == EMPTY) {
			return obj == null || obj.toString().length() == 0;
		} else if (_type == NOT_EMPTY) {
			return obj != null && obj.toString().length() > 0;
		} else {
			return false;
		}
	}
}
