package net.sourceforge.jvlt.actions;

import net.sourceforge.jvlt.core.Sense;

public class MoveSenseAction extends DictObjectAction {
	private final int _old_index;
	private final int _new_index;

	public MoveSenseAction(Sense sense, int old_index, int new_index) {
		super(sense);
		_old_index = old_index;
		_new_index = new_index;
	}

	public int getOldIndex() {
		return _old_index;
	}

	public int getNewIndex() {
		return _new_index;
	}
}
