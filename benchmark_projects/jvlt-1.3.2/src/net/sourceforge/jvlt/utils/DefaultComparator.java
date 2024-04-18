package net.sourceforge.jvlt.utils;

import java.util.Comparator;

public class DefaultComparator implements Comparator<Object> {
	private static final DefaultComparator instance = new DefaultComparator();

	@SuppressWarnings(value = "unchecked")
	public int compare(Object o1, Object o2) {
		if (o1 == null) {
			return o2 == null ? 0 : -1;
		}

		if ((o1 instanceof Comparable<?>) && (o2 instanceof Comparable<?>)) {
			return ((Comparable) o1).compareTo(o2);
		}
		return o1.equals(o2) ? 0 : 1;
	}

	public static DefaultComparator getInstance() {
		return instance;
	}
}
