package net.sourceforge.jvlt.actions;

public class LanguageChangeAction extends DictAction {
	String _old_language = null;
	String _new_language = null;

	public LanguageChangeAction(String old_language, String new_language) {
		_old_language = old_language;
		_new_language = new_language;
	}

	public String getOldLanguage() {
		return _old_language;
	}

	public String getNewLanguage() {
		return _new_language;
	}
}
