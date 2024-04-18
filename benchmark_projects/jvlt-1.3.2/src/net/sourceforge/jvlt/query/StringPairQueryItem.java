package net.sourceforge.jvlt.query;

import net.sourceforge.jvlt.core.StringPair;

public class StringPairQueryItem extends ObjectQueryItem {
	public static final int KEY_CONTAINS = 0;
	public static final int VALUE_CONTAINS = 1;

	private boolean _match_case = false;

	public StringPairQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public StringPairQueryItem() {
		super();
	}

	public boolean getMatchCase() {
		return _match_case;
	}

	public void setMatchCase(boolean match) {
		_match_case = match;
	}

	@Override
	public boolean objectMatches(Object o) {
		String text = _value != null ? (String) _value : "";
		StringPair[] pairs = (StringPair[]) o;

		switch (_type) {
		case KEY_CONTAINS:
			for (StringPair p : pairs) {
				if (_match_case) {
					if (p.getFirst().indexOf(text) >= 0) {
						return true;
					}
				} else {
					if (p.getFirst().toLowerCase().indexOf(text.toLowerCase()) >= 0) {
						return true;
					}

				}
			}

			return text.length() == 0;
		case VALUE_CONTAINS:
			for (StringPair p : pairs) {
				if (_match_case) {
					if (p.getSecond().indexOf(text) >= 0) {
						return true;
					}
				} else {
					if (p.getSecond().toLowerCase().indexOf(text.toLowerCase()) >= 0) {
						return true;
					}

				}
			}

			return text.length() == 0;
		default:
			return false;
		}
	}
}
