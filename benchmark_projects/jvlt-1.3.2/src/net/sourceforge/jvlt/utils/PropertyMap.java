package net.sourceforge.jvlt.utils;

import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.util.HashMap;
import java.util.Vector;

public class PropertyMap {
	private final Vector<PropertyChangeListener> _listeners;
	private final HashMap<String, Object> _value_map;

	public PropertyMap() {
		_listeners = new Vector<PropertyChangeListener>();
		_value_map = new HashMap<String, Object>();
	}

	public boolean containsKey(String key) {
		return _value_map.containsKey(key);
	}

	/**
	 * Returns a property given by a certain key
	 * 
	 * @param key The key
	 * @return The value that is mapped to the key or null if there is no value
	 *         for the key
	 */
	public Object get(String key) {
		return _value_map.get(key);
	}

	public void put(String key, Object value) {
		boolean fire;
		if (!_value_map.containsKey(key)) {
			fire = true;
		} else {
			Object obj = _value_map.get(key);
			if (obj == null) {
				fire = (value != null);
			} else {
				fire = (!obj.equals(value));
			}
		}

		_value_map.put(key, value);
		if (fire) {
			firePropertyChangeEvent(key, _value_map.get(key), value);
		}
	}

	public void addPropertyChangeListener(PropertyChangeListener l) {
		_listeners.add(l);
	}

	public void removePropertyChangeListener(PropertyChangeListener l) {
		_listeners.remove(l);
	}

	private void firePropertyChangeEvent(String key, Object old_value,
			Object new_value) {
		for (PropertyChangeListener propertyChangeListener : _listeners) {
			propertyChangeListener.propertyChange(new PropertyChangeEvent(this,
					key, old_value, new_value));
		}
	}
}
