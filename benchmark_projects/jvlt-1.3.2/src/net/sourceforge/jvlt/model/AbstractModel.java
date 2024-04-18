package net.sourceforge.jvlt.model;

import java.util.Iterator;
import java.util.LinkedList;

import net.sourceforge.jvlt.actions.UndoableAction;
import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.event.ModelResetEventListener;
import net.sourceforge.jvlt.event.UndoableActionListener;
import net.sourceforge.jvlt.event.ModelResetEventListener.ModelResetEvent;
import net.sourceforge.jvlt.event.UndoableActionListener.UndoableActionEvent;

public abstract class AbstractModel {
	protected Dict _dict;
	protected LinkedList<UndoableAction> _undoable_actions;
	protected LinkedList<UndoableAction> _redoable_actions;
	protected LinkedList<UndoableActionListener> _undoable_action_listeners;
	protected LinkedList<ModelResetEventListener> _reset_event_listeners;
	protected int _executed_actions;

	public AbstractModel() {
		_dict = null;
		_executed_actions = 0;
		_undoable_actions = new LinkedList<UndoableAction>();
		_redoable_actions = new LinkedList<UndoableAction>();
		_undoable_action_listeners = new LinkedList<UndoableActionListener>();
		_reset_event_listeners = new LinkedList<ModelResetEventListener>();
	}

	public void addUndoableActionListener(UndoableActionListener listener) {
		_undoable_action_listeners.add(listener);
	}

	public void removeUndoableActionListener(UndoableActionListener listener) {
		_undoable_action_listeners.remove(listener);
	}

	public void addModelResetEventListener(ModelResetEventListener listener) {
		_reset_event_listeners.add(listener);
	}

	public void removeModelResetEventListener(ModelResetEventListener listener) {
		_reset_event_listeners.remove(listener);
	}

	public void undo() throws ModelException {
		if (_undoable_actions.size() == 0) {
			return;
		}
		UndoableAction a = _undoable_actions.getFirst();
		undo(a);
		_redoable_actions.addFirst(a);
		_undoable_actions.removeFirst();

		fireEvent(new UndoableActionEvent(a, UndoableActionEvent.UNDO_TYPE));
	}

	public void redo() throws ModelException {
		if (_redoable_actions.size() == 0) {
			return;
		}
		UndoableAction a = _redoable_actions.getFirst();
		execute(a);
		_undoable_actions.addFirst(a);
		_redoable_actions.removeFirst();

		fireEvent(new UndoableActionEvent(a, UndoableActionEvent.REDO_TYPE));
	}

	public void reset() {
		_redoable_actions.clear();
		_undoable_actions.clear();
		_executed_actions = 0;
		fireEvent(new ModelResetEvent(this, ModelResetEvent.RESET_ALL));
	}

	/**
	 * This method sets the number of executed actions to zero while the list of
	 * actions is not cleared. This causes the method <i>isDataModified()</i> to
	 * return <i>false</i>, but it is still possible to undo and redo actions.
	 */
	public void resetActionCounter() {
		_executed_actions = 0;
		fireEvent(new ModelResetEvent(this, ModelResetEvent.RESET_COUNTER));
	}

	public void executeAction(UndoableAction a) throws ModelException {
		execute(a);
		_redoable_actions.clear();
		_undoable_actions.addFirst(a);

		fireEvent(new UndoableActionEvent(a, UndoableActionEvent.EXEC_TYPE));
	}

	public boolean isDataModified() {
		return _executed_actions != 0;
	}

	public int getNumUndoableActions() {
		return _undoable_actions.size();
	}

	public UndoableAction getFirstUndoableAction() {
		return _undoable_actions.getFirst();
	}

	public int getNumRedoableActions() {
		return _redoable_actions.size();
	}

	public UndoableAction getFirstRedoableAction() {
		return _redoable_actions.getFirst();
	}

	/** Sets a new dictionary and calls reset(). */
	public void setDict(Dict dict) {
		_dict = dict;
		reset();
	}

	protected abstract void execute(UndoableAction a) throws ModelException;

	protected abstract void undo(UndoableAction a) throws ModelException;

	protected void fireEvent(Object obj) {
		if (obj instanceof UndoableActionEvent) {
			UndoableActionEvent event = (UndoableActionEvent) obj;
			Iterator<UndoableActionListener> it = _undoable_action_listeners
					.iterator();
			while (it.hasNext()) {
				it.next().actionPerformed(event);
			}
		} else if (obj instanceof ModelResetEvent) {
			ModelResetEvent event = (ModelResetEvent) obj;
			Iterator<ModelResetEventListener> it = _reset_event_listeners
					.iterator();
			while (it.hasNext()) {
				it.next().modelResetted(event);
			}
		}
	}
}
