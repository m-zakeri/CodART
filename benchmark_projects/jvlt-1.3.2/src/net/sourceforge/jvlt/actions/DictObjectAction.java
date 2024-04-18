package net.sourceforge.jvlt.actions;

import net.sourceforge.jvlt.core.Reinitializable;

public abstract class DictObjectAction extends DictAction {
	protected Reinitializable _obj;

	public DictObjectAction(Reinitializable obj) {
		super();
		_obj = obj;
	}

	public Reinitializable getObject() {
		return _obj;
	}
}
