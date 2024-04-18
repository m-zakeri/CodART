package net.sourceforge.jvlt.utils;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.TreeMap;


public class ItemContainer {
	private boolean _translate_items = false;
	private final AttributeResources _resources = new AttributeResources();
	private final ArrayList<Object> _values;
	private final TreeMap<Object, String> _value_translation_map;
	private final TreeMap<String, Object> _translation_value_map;

	public ItemContainer() {
		_values = new ArrayList<Object>();
		_value_translation_map = new TreeMap<Object, String>();
		_translation_value_map = new TreeMap<String, Object>();
	}

	public Object getItem(Object translation) {
		if (translation == null) {
			return null;
		} else if (_translation_value_map.containsKey(translation)) {
			return _translation_value_map.get(translation);
		} else {
			return translation;
		}
	}

	public Object[] getItems() {
		return _values.toArray();
	}

	public Object[] getItems(Object[] translations) {
		Object[] items = new Object[translations.length];
		for (int i = 0; i < translations.length; i++) {
			items[i] = getItem(translations[i]);
		}

		return items;
	}

	public String getTranslation(Object item) {
		if (item == null) {
			return null;
		} else if (_value_translation_map.containsKey(item)) {
			return _value_translation_map.get(item);
		} else {
			return item.toString();
		}
	}

	public String[] getTranslations() {
		return getTranslations(_values.toArray());
	}

	public String[] getTranslations(Object[] items) {
		String[] translations = new String[items.length];
		for (int i = 0; i < items.length; i++) {
			translations[i] = getTranslation(items[i]);
		}

		return translations;
	}

	public void addItem(Object item) {
		String translation = _translate_items ? _resources.getString(item
				.toString()) : item.toString();
		_value_translation_map.put(item, translation);
		_translation_value_map.put(translation, item);
	}

	public void addItems(Object[] items) {
		_values.addAll(Arrays.asList(items));
		updateMaps();
	}

	public void setItems(Object[] items) {
		removeAllItems();
		addItems(items);
	}

	public void removeAllItems() {
		_values.clear();
	}

	public void setTranslateItems(boolean translate) {
		_translate_items = translate;
		updateMaps();
	}

	public boolean getTranslateItems() {
		return _translate_items;
	}

	private void updateMaps() {
		_value_translation_map.clear();
		_translation_value_map.clear();
		if (_translate_items) {
			for (Object value : _values) {
				String translation = _resources.getString(value.toString());
				_value_translation_map.put(value, translation);
				_translation_value_map.put(translation, value);
			}
		}
	}
}
