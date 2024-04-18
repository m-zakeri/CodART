package net.sourceforge.jvlt.actions;

public abstract class UndoableAction {
	protected String _message;

	public UndoableAction() {
		this("");
	}

	public UndoableAction(String message) {
		_message = message;
	}

	public String getMessage() {
		return _message;
	}

	public void setMessage(String s) {
		_message = s;
	}
}
