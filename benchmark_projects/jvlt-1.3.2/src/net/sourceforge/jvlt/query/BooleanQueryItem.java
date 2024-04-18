package net.sourceforge.jvlt.query;

public class BooleanQueryItem extends ObjectQueryItem {
	public static final int YES = 0;
	public static final int NO = 1;
	public static final int NOT_SET = 2;

	public BooleanQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public BooleanQueryItem() {
		super();
	}

	@Override
	public boolean objectMatches(Object obj) {
		Boolean b = (Boolean) obj;
		switch (_type) {
		case YES:
			return b != null && b;
		case NO:
			return b != null && !b;
		case NOT_SET:
			return b == null;
		default:
			return false;
		}
	}
}
