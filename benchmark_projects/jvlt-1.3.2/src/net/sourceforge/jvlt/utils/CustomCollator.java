package net.sourceforge.jvlt.utils;

import java.text.Collator;
import java.text.ParseException;
import java.text.RuleBasedCollator;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class CustomCollator extends RuleBasedCollator {
	private static CustomCollator _instance = null;

	private CustomCollator(String rules) throws ParseException {
		super(rules);
	}

	public static CustomCollator getInstance() {
		try {
			if (_instance == null) {
				//
				// Create a new collator. Ensure that the space character is not
				// ignored and is placed before the letter "a" in the sort order
				//
				RuleBasedCollator c = (RuleBasedCollator) Collator
						.getInstance(Locale.US);
				c.setStrength(Collator.PRIMARY);
				Pattern p = Pattern.compile("(.)\\s*<\\s*a");
				Matcher m = p.matcher(c.getRules());
				if (m.find()) {
					_instance = new CustomCollator(c.getRules() + "&"
							+ m.group(1) + "<' '");
				} else {
					_instance = new CustomCollator(c.getRules());
				}
			}

			return _instance;
		} catch (ParseException e) {
			return null; // Should not happen
		}
	}
}
