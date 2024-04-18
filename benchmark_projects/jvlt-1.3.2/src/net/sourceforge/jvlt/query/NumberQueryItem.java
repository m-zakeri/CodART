package net.sourceforge.jvlt.query;

public class NumberQueryItem extends ObjectQueryItem {
	public static final int EQUALS = 0;
	public static final int GREATER = 1;
	public static final int LESS = 2;

	public NumberQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public NumberQueryItem() {
		super();
	}

	@Override
	public boolean objectMatches(Object obj) {
		double num1 = ((Number) obj).doubleValue();
		double num2 = ((Number) _value).doubleValue();
		if (_type == NumberQueryItem.EQUALS) {
			return num1 == num2;
		} else if (_type == NumberQueryItem.GREATER) {
			return num1 > num2;
		} else if (_type == NumberQueryItem.LESS) {
			return num1 < num2;
		} else {
			return false;
		}
	}
}
