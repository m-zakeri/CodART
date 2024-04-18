package net.sourceforge.jvlt.io;

import net.sourceforge.jvlt.utils.DetailedException;

public class DictReaderException extends DetailedException {
	private static final long serialVersionUID = 1L;

	private final Exception _exception;

	public DictReaderException(String short_message, String long_message,
			Exception exception) {
		super(short_message, long_message);
		_exception = exception;
	}

	public DictReaderException(String short_message, String long_message) {
		this(short_message, long_message, null);
	}

	public DictReaderException(String message, Exception exception) {
		super(message);
		_exception = exception;
	}

	public DictReaderException(String message) {
		this(message, "");
	}

	public Exception getException() {
		return _exception;
	}
}
