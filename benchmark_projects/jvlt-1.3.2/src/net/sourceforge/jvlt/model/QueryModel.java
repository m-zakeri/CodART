package net.sourceforge.jvlt.model;

import java.util.Iterator;
import java.util.LinkedList;

import net.sourceforge.jvlt.actions.StatsUpdateAction;
import net.sourceforge.jvlt.actions.UndoableAction;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.event.DictUpdateListener;
import net.sourceforge.jvlt.event.DictUpdateListener.DictUpdateEvent;
import net.sourceforge.jvlt.event.DictUpdateListener.EntryDictUpdateEvent;

public class QueryModel extends AbstractModel {
	private final LinkedList<DictUpdateListener> _dict_update_listeners;

	public QueryModel() {
		_dict_update_listeners = new LinkedList<DictUpdateListener>();
	}

	public void addDictUpdateListener(DictUpdateListener listener) {
		_dict_update_listeners.add(listener);
	}

	public void removeDictUpdateListener(DictUpdateListener listener) {
		_dict_update_listeners.remove(listener);
	}

	@Override
	protected void execute(UndoableAction a) {
		if (a instanceof StatsUpdateAction) {
			performStatsUpdateAction((StatsUpdateAction) a, false);
		}

		_executed_actions++;
	}

	@Override
	protected void undo(UndoableAction a) {
		if (a instanceof StatsUpdateAction) {
			performStatsUpdateAction((StatsUpdateAction) a, true);
		}

		_executed_actions--;
	}

	private void fireDictUpdateEvent(DictUpdateEvent event) {
		Iterator<DictUpdateListener> it = _dict_update_listeners.iterator();
		while (it.hasNext()) {
			it.next().dictUpdated(event);
		}
	}

	private void performStatsUpdateAction(StatsUpdateAction sua, boolean undo) {
		if (undo) {
			sua.undoAction();
		} else {
			sua.executeAction();
		}

		LinkedList<Entry> entry_list = new LinkedList<Entry>();
		for (Entry entry : sua.getKnownEntries()) {
			entry_list.add(entry);
		}
		for (Entry entry : sua.getUnknownEntries()) {
			entry_list.add(entry);
		}
		fireDictUpdateEvent(new EntryDictUpdateEvent(
				EntryDictUpdateEvent.ENTRIES_CHANGED, entry_list));
	}
}
