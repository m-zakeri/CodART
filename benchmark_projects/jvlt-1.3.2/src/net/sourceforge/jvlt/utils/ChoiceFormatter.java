package net.sourceforge.jvlt.utils;

import java.text.ChoiceFormat;
import java.text.MessageFormat;

public class ChoiceFormatter {
	private String _pattern;
	private final ChoiceFormat _choice_format;
	private final MessageFormat _message_format;

	public ChoiceFormatter(String pattern) {
		_pattern = pattern;
		_choice_format = new ChoiceFormat("");
		_message_format = new MessageFormat("");
	}

	public ChoiceFormatter() {
		this(null);
	}

	public String format(double value) {
		Double val = new Double(value);
		_choice_format.applyPattern(_pattern);
		String text = _choice_format.format(val);
		_message_format.applyPattern(text);

		return _message_format.format(new Object[] { val });
	}

	public void applyPattern(String pattern) {
		_pattern = pattern;
	}
}
