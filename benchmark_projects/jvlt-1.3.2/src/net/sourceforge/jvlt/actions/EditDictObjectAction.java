package net.sourceforge.jvlt.actions;

import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Reinitializable;

public class EditDictObjectAction extends DictObjectAction {
	private final Reinitializable _old_data;
	private Reinitializable _new_data;

	public EditDictObjectAction(Reinitializable obj, Reinitializable new_info) {
		super(obj);

		_old_data = (Reinitializable) obj.clone();
		_new_data = new_info;
	}

	public EditDictObjectAction(Reinitializable obj) {
		this(obj, null);
	}

	public void setNewData(Reinitializable new_data) {
		_new_data = new_data;
	}

	public Reinitializable getOldData() {
		return _old_data;
	}

	public Reinitializable getNewData() {
		return _new_data;
	}

	public void executeAction() throws DictException {
		_obj.reinit(_new_data);
	}

	public void undoAction() throws DictException {
		_obj.reinit(_old_data);
	}
}
