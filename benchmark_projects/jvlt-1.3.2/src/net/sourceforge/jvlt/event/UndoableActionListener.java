package net.sourceforge.jvlt.event;

import net.sourceforge.jvlt.actions.UndoableAction;

public interface UndoableActionListener {
	class UndoableActionEvent {
		public static final int UNDO_TYPE = 0; // Action is undone.
		public static final int REDO_TYPE = 1; // Action is redone.
		public static final int EXEC_TYPE = 2; // Action is executed for the
		// first time.

		private final UndoableAction _action;
		private final int _type;

		public UndoableActionEvent(UndoableAction action, int type) {
			_action = action;
			_type = type;
		}

		public UndoableAction getAction() {
			return _action;
		}

		public int getType() {
			return _type;
		}
	}

	void actionPerformed(UndoableActionEvent event);
}
