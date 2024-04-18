package net.sourceforge.jvlt.utils;

import java.util.Collections;
import java.util.Enumeration;
import java.util.HashSet;
import java.util.Locale;
import java.util.ResourceBundle;
import java.util.Set;

public class AttributeResources extends ResourceBundle {
	private final Set<String> _keys;
	private final ResourceBundle _bundle;

	public AttributeResources() {
		_keys = new HashSet<String>();
		_bundle = ResourceBundle.getBundle("i18n/Attributes", Locale
				.getDefault());
		for (Enumeration<String> e = _bundle.getKeys(); e.hasMoreElements();) {
			_keys.add(e.nextElement());
		}
	}

	@Override
	public Enumeration<String> getKeys() {
		return Collections.enumeration(_keys);
	}

	@Override
	protected Object handleGetObject(String key) {
		if (key == null || key.equals("")) {
			return key;
		}
		if (_keys.contains(key)) {
			return _bundle.getObject(key);
		}
		return key;
	}
}
