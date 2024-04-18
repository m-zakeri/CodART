package net.sourceforge.jvlt.actions;

import java.util.ArrayList;
import java.util.List;
import java.util.ListIterator;

import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Sense;

public class EditEntryAction extends EditDictObjectAction {
	private final ArrayList<DictObjectAction> _sense_actions;

	public EditEntryAction(Entry old_entry, Entry new_entry) {
		super(old_entry, new_entry);
		_sense_actions = new ArrayList<DictObjectAction>();
	}

	public void addSenseActions(List<DictObjectAction> actions) {
		_sense_actions.addAll(actions);
	}

	@Override
	public void executeAction() throws DictException {
		super.executeAction();

		ListIterator<DictObjectAction> it = _sense_actions.listIterator();
		Entry entry = (Entry) _obj;
		while (it.hasNext()) {
			DictObjectAction a = it.next();
			Sense sense = (Sense) a.getObject();
			if (a instanceof AddDictObjectAction) {
				entry.addSense(sense);
			} else if (a instanceof EditDictObjectAction) {
				((EditDictObjectAction) a).executeAction();
			} else if (a instanceof MoveSenseAction) {
				int index = ((MoveSenseAction) a).getNewIndex();
				entry.removeSense(sense);
				entry.addSense(index, sense);
			} else if (a instanceof RemoveSenseAction) {
				entry.removeSense(sense);
			}
		}
	}

	@Override
	public void undoAction() throws DictException {
		super.undoAction();

		ListIterator<DictObjectAction> it = _sense_actions
				.listIterator(_sense_actions.size());
		Entry entry = (Entry) _obj;
		while (it.hasPrevious()) {
			DictObjectAction a = it.previous();
			Sense sense = (Sense) a.getObject();
			if (a instanceof AddDictObjectAction) {
				entry.removeSense(sense);
			} else if (a instanceof EditDictObjectAction) {
				((EditDictObjectAction) a).undoAction();
			} else if (a instanceof MoveSenseAction) {
				int index = ((MoveSenseAction) a).getOldIndex();
				entry.removeSense(sense);
				entry.addSense(index, sense);
			} else if (a instanceof RemoveSenseAction) {
				entry.addSense(((RemoveSenseAction) a).getOldPosition(), sense);
			}
		}
	}
}
