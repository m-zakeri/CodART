package net.sourceforge.jvlt.event;

import java.util.EventListener;

import javax.swing.JComponent;

public interface ComponentReplacementListener extends EventListener {
	class ComponentReplacementEvent {
		private final JComponent _old_component;
		private final JComponent _new_component;

		public ComponentReplacementEvent(JComponent o, JComponent n) {
			_old_component = o;
			_new_component = n;
		}

		public JComponent getOldComponent() {
			return _old_component;
		}

		public JComponent getNewComponent() {
			return _new_component;
		}
	}

	void componentReplaced(ComponentReplacementEvent e);
}
