package net.sourceforge.jvlt.event;

import java.util.ArrayList;
import java.util.Iterator;

import net.sourceforge.jvlt.event.SelectionListener.SelectionEvent;

public class SelectionNotifier {
	private final ArrayList<SelectionListener> _listeners;

	public SelectionNotifier() {
		_listeners = new ArrayList<SelectionListener>();
	}

	public void addSelectionListener(SelectionListener l) {
		_listeners.add(l);
	}

	public void removeSelectionListener(SelectionListener l) {
		_listeners.remove(l);
	}

	public void fireSelectionEvent(SelectionEvent e) {
		Iterator<SelectionListener> it = _listeners.iterator();
		while (it.hasNext()) {
			it.next().objectSelected(e);
		}
	}
}
