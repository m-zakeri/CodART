package net.sourceforge.jvlt.actions;

import net.sourceforge.jvlt.core.Sense;

public class RemoveSenseAction extends DictObjectAction {
	private final int _position;

	public RemoveSenseAction(Sense sense, int position) {
		super(sense);
		_position = position;
	}

	public int getOldPosition() {
		return _position;
	}
}
