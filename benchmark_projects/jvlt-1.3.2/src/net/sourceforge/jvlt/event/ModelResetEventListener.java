package net.sourceforge.jvlt.event;

import net.sourceforge.jvlt.model.AbstractModel;

public interface ModelResetEventListener {
	class ModelResetEvent {
		public static final int RESET_ALL = 0;
		public static final int RESET_COUNTER = 1;

		private final AbstractModel _source;
		private final int _type;

		public ModelResetEvent(AbstractModel source, int type) {
			_source = source;
			_type = type;
		}

		public ModelResetEvent(AbstractModel source) {
			this(source, RESET_ALL);
		}

		public AbstractModel getSource() {
			return _source;
		}

		public int getType() {
			return _type;
		}
	}

	void modelResetted(ModelResetEvent event);
}
