package net.sourceforge.jvlt.utils;

import java.text.MessageFormat;
import java.util.Locale;
import java.util.ResourceBundle;

public class I18nService {
	public static String getLabelString(String name) {
		return getString("Labels", name);
	}

	public static String getMessageString(String name) {
		return getString("Messages", name);
	}

	public static String getString(String resource_bundle, String name) {
		return getString(resource_bundle, name, null);
	}

	public static String getString(String resource_bundle, String name,
			Object[] args) {
		ResourceBundle messages = ResourceBundle.getBundle("i18n/"
				+ resource_bundle, Locale.getDefault());
		String str = messages.getString(name);

		if (args == null) {
			return str;
		}
		MessageFormat formatter = new MessageFormat("");
		formatter.setLocale(Locale.getDefault());
		formatter.applyPattern(str);
		return formatter.format(args);
	}
}
