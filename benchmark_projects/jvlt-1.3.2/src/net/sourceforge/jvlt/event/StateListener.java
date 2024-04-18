package net.sourceforge.jvlt.event;

import java.util.EventObject;

public interface StateListener {
	class StateEvent extends EventObject {
		private static final long serialVersionUID = 1L;

		private final int _state;

		public StateEvent(Object src, int state) {
			super(src);
			_state = state;
		}

		public int getState() {
			return _state;
		}
	}

	void stateChanged(StateEvent ev);
}
