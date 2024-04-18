package net.sourceforge.jvlt.quiz;

import net.sourceforge.jvlt.core.Entry;

public class QueryResult {
	private final Entry _entry;
	private final boolean _known;
	private String _answer;

	public QueryResult(Entry entry, boolean known) {
		this(entry, known, null);
	}

	public QueryResult(Entry entry, boolean known, String answer) {
		_entry = entry;
		_known = known;
		_answer = answer;
	}

	public Entry getEntry() {
		return _entry;
	}

	public String getAnswer() {
		return _answer;
	}

	public boolean isKnown() {
		return _known;
	}

	public void setAnswer(String answer) {
		_answer = answer;
	}
}
