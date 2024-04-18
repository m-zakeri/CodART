package net.sourceforge.jvlt.query;

public class StringQueryItem extends ObjectQueryItem {
	public static final int EQUALS = 0;
	public static final int CONTAINS = 1;

	private boolean _match_case = false;

	public StringQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public StringQueryItem() {
		super();
	}

	public boolean getMatchCase() {
		return _match_case;
	}

	public void setMatchCase(boolean match) {
		_match_case = match;
	}

	@Override
	public boolean objectMatches(Object obj) {
		if (obj == null || _value == null) {
			return obj == null && _value == null;
		}

		String str = _match_case ? obj.toString() : obj.toString()
				.toLowerCase();
		String val = _match_case ? _value.toString() : _value.toString()
				.toLowerCase();
		if (_type == StringQueryItem.EQUALS) {
			return str.equals(val);
		} else if (_type == StringQueryItem.CONTAINS) {
			return str.indexOf(val) >= 0;
		} else {
			return false;
		}
	}
}
