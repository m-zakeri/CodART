package net.sourceforge.jvlt.metadata;

import java.util.Comparator;

import net.sourceforge.jvlt.utils.ItemContainer;

public class AttributeComparator implements Comparator<Object> {
	private final ItemContainer _container;

	public AttributeComparator(ItemContainer container) {
		_container = container;
	}

	public int compare(Object o1, Object o2) {
		if (!(o1 instanceof CustomAttribute) && o2 instanceof CustomAttribute) {
			return -1;
		} else if (o1 instanceof CustomAttribute
				&& !(o2 instanceof CustomAttribute)) {
			return 1;
		} else {
			return _container.getTranslation(o1).compareTo(
					_container.getTranslation(o2));
		}
	}
}
