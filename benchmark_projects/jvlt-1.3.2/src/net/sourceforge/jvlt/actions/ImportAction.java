package net.sourceforge.jvlt.actions;

import java.util.Collection;

import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Example;

public class ImportAction extends DictAction {
	private final Collection<Entry> _entries;
	private final Collection<Example> _examples;
	private final String _old_language;
	private final String _new_language;

	public ImportAction(String old_lang, String new_lang,
			Collection<Entry> entries, Collection<Example> examples) {
		_entries = entries;
		_examples = examples;
		_old_language = old_lang;
		_new_language = new_lang;
	}

	public Collection<Entry> getEntries() {
		return _entries;
	}

	public Collection<Example> getExamples() {
		return _examples;
	}

	public String getOldLanguage() {
		return _old_language;
	}

	public String getNewLanguage() {
		return _new_language;
	}
}
