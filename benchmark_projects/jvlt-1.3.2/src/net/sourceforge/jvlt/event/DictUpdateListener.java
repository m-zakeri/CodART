package net.sourceforge.jvlt.event;

import java.util.Collection;

import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Example;

public interface DictUpdateListener {
	abstract class DictUpdateEvent {
		protected int _type;

		public DictUpdateEvent(int type) {
			_type = type;
		}

		public int getType() {
			return _type;
		}
	}

	class EntryDictUpdateEvent extends DictUpdateEvent {
		public static final int ENTRIES_ADDED = 1;
		public static final int ENTRIES_CHANGED = 2;
		public static final int ENTRIES_REMOVED = 3;

		private final Collection<Entry> _entries;

		public EntryDictUpdateEvent(int type, Collection<Entry> entries) {
			super(type);
			_entries = entries;
		}

		public Collection<Entry> getEntries() {
			return _entries;
		}
	}

	class ExampleDictUpdateEvent extends DictUpdateEvent {
		public static final int EXAMPLES_ADDED = 1;
		public static final int EXAMPLES_CHANGED = 2;
		public static final int EXAMPLES_REMOVED = 3;

		private final Collection<Example> _examples;

		public ExampleDictUpdateEvent(int type, Collection<Example> examples) {
			super(type);
			_examples = examples;
		}

		public Collection<Example> getExamples() {
			return _examples;
		}
	}

	class NewDictDictUpdateEvent extends DictUpdateEvent {
		private final Dict _dict;

		public NewDictDictUpdateEvent(Dict dict) {
			super(0);
			_dict = dict;
		}

		public Dict getDict() {
			return _dict;
		}
	}

	class LanguageDictUpdateEvent extends DictUpdateEvent {
		private final String _new_language;

		public LanguageDictUpdateEvent(String new_language) {
			super(0);
			_new_language = new_language;
		}

		public String getLanguage() {
			return _new_language;
		}
	}

	void dictUpdated(DictUpdateEvent event);
}
