package net.sourceforge.jvlt.actions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;

import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Entry;

public class EditEntriesAction extends DictAction {
	private final ArrayList<EditEntryAction> _actions;

	public EditEntriesAction(EditEntryAction[] actions) {
		_actions = new ArrayList<EditEntryAction>();
		_actions.addAll(Arrays.asList(actions));
	}

	public void executeAction() throws DictException {
		for (EditEntryAction editEntryAction : _actions) {
			editEntryAction.executeAction();
		}
	}

	public void undoAction() throws DictException {
		for (EditEntryAction editEntryAction : _actions) {
			editEntryAction.undoAction();
		}
	}

	public Collection<Entry> getEntries() {
		ArrayList<Entry> entries = new ArrayList<Entry>();
		for (EditEntryAction editEntryAction : _actions) {
			entries.add((Entry) editEntryAction.getNewData());
		}

		return entries;
	}
}
