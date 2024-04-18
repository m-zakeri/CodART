package net.sourceforge.jvlt.query;

import java.util.Arrays;
import java.util.List;

public class ChoiceObjectArrayQueryItem extends ObjectArrayQueryItem {
	public static final int CONTAINS_ALL_ITEMS = 10;
	public static final int CONTAINS_ONE_ITEM = 11;
	public static final int DOES_NOT_CONTAIN_ANY_ITEM = 12;

	public ChoiceObjectArrayQueryItem(String name, int type, Object value) {
		super(name, type, value);
	}

	public ChoiceObjectArrayQueryItem() {
		this(null, 0, null);
	}

	@Override
	public boolean objectMatches(Object obj) {
		Object[] array = (obj == null) ? new Object[0] : (Object[]) obj;

		if (_type != CONTAINS_ALL_ITEMS && _type != CONTAINS_ONE_ITEM
				&& _type != DOES_NOT_CONTAIN_ANY_ITEM) {
			return super.objectMatches(obj);
		}

		Object[] valarray = (Object[]) _value;
		List<Object> items = Arrays.asList(array);
		if (_type == CONTAINS_ALL_ITEMS) {
			for (int i = 0; i < valarray.length; i++) {
				if (!items.contains(valarray[i])) {
					return false;
				}
			}

			return true;
		} else if (_type == CONTAINS_ONE_ITEM) {
			for (Object element : valarray) {
				if (items.contains(element)) {
					return true;
				}
			}

			return false;
		} else { // if (_type == DOES_NOT_CONTAIN_ANY_ITEM)
			for (Object element : valarray) {
				if (items.contains(element)) {
					return false;
				}
			}

			return true;
		}
	}
}
