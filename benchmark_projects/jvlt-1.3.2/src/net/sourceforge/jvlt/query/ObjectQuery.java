package net.sourceforge.jvlt.query;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

import net.sourceforge.jvlt.metadata.Attribute;
import net.sourceforge.jvlt.metadata.MetaData;
import net.sourceforge.jvlt.model.DictModel;
import net.sourceforge.jvlt.ui.JVLTUI;

public class ObjectQuery {
	public static final int MATCH_ONE = 0;
	public static final int MATCH_ALL = 1;

	private static final long serialVersionUID = 1L;

	/* Serialized attributes */
	Class<? extends Object> _object_class;
	private int _type;
	private String _name;
	private final ArrayList<ObjectQueryItem> _items;

	/* Not serialized attributes */
	private MetaData _metadata = null;

	public ObjectQuery(Class<? extends Object> cl, int type) {
		_type = type;
		_name = "";
		_items = new ArrayList<ObjectQueryItem>();

		setObjectClass(cl);
	}

	public ObjectQuery(Class<? extends Object> cl) {
		this(cl, MATCH_ALL);
	}

	public ObjectQuery() {
		this(null, MATCH_ALL);
	}

	public Class<? extends Object> getObjectClass() {
		return _object_class;
	}

	public int getType() {
		return _type;
	}

	public void setType(int type) {
		_type = type;
	}

	public ObjectQueryItem[] getItems() {
		return _items.toArray(new ObjectQueryItem[0]);
	}

	public void addItem(ObjectQueryItem item) {
		_items.add(item);
	}

	public void setItems(ObjectQueryItem[] items) {
		_items.clear();
		_items.addAll(Arrays.asList(items));
	}

	public String getName() {
		return _name;
	}

	public void setName(String name) {
		_name = name;
	}

	public boolean objectMatches(Object obj) {
		if (_items.size() == 0) {
			return true;
		}

		Iterator<ObjectQueryItem> it = _items.iterator();
		while (it.hasNext()) {
			ObjectQueryItem item = it.next();
			Attribute attr = _metadata.getAttribute(item.getName());
			Object value = attr.getValue(obj);
			if (item.objectMatches(value) && _type == MATCH_ONE) {
				return true;
			} else if (!item.objectMatches(value) && _type == MATCH_ALL) {
				return false;
			}
		}
		return _type == MATCH_ALL;
	}

	public boolean isValid() {
		for (ObjectQueryItem item : _items) {
			if (item == null) {
				return false;
			}
		}

		return true;
	}

	private void setObjectClass(Class<? extends Object> cl) {
		_object_class = cl;

		DictModel model = JVLTUI.getModel().getDictModel();
		if (cl != null) {
			_metadata = model.getMetaData(cl);
		}
	}
}
