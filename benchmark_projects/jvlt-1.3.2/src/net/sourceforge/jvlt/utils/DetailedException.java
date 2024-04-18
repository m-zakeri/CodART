package net.sourceforge.jvlt.utils;

public class DetailedException extends Exception {
	private static final long serialVersionUID = 1L;

	private String _long_message;

	public DetailedException(String short_message, String long_message) {
		this(short_message);
		_long_message = long_message;
	}

	public DetailedException(String short_message) {
		super(short_message);
	}

	public String getShortMessage() {
		return super.getMessage();
	}

	public String getLongMessage() {
		return _long_message;
	}
}
