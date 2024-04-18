package net.sourceforge.jvlt.quiz;

import net.sourceforge.jvlt.utils.I18nService;

public class QuizInfo {
	private static QuizInfo[] _default_quiz_infos;

	static {
		_default_quiz_infos = new QuizInfo[2];

		_default_quiz_infos[0] = new QuizInfo();
		_default_quiz_infos[0]
				.setName(I18nService.getString("Labels", "original"));
		_default_quiz_infos[0]
				.setQuizzedAttributes(new String[] { "Orthography" });
		_default_quiz_infos[0].setShownAttributes(new String[] { "Senses" });

		_default_quiz_infos[1] = new QuizInfo();
		_default_quiz_infos[1]
				.setName(I18nService.getString("Labels", "meanings"));
		_default_quiz_infos[1].setQuizzedAttributes(new String[] { "Senses" });
		_default_quiz_infos[1]
				.setShownAttributes(new String[] { "Orthography" });
	}

	public static QuizInfo[] getDefaultQuizInfos() {
		return _default_quiz_infos;
	}

	/* Serialized members */
	private String _name = null;
	private String _language = null;
	private String[] _quizzed_attributes = new String[0];
	private String[] _shown_attributes = new String[0];

	public String getName() {
		return _name;
	}

	public void setName(String name) {
		_name = name;
	}

	public String getLanguage() {
		return _language;
	}

	public void setLanguage(String language) {
		_language = language;
	}

	public String[] getQuizzedAttributes() {
		return _quizzed_attributes;
	}

	public void setQuizzedAttributes(String[] attributes) {
		_quizzed_attributes = attributes;
	}

	public String[] getShownAttributes() {
		return _shown_attributes;
	}

	public void setShownAttributes(String[] attributes) {
		_shown_attributes = attributes;
	}

	@Override
	public int hashCode() {
		return _name.hashCode();
	}
}
