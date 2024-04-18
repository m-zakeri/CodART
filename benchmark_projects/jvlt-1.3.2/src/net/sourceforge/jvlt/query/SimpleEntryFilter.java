package net.sourceforge.jvlt.query;

import net.sourceforge.jvlt.core.Entry;

public class SimpleEntryFilter extends EntryFilter implements StringEntryFilter {
	private final StringQueryItem _orth_item;
	private final ObjectArrayQueryItem _pron_item;
	private final SenseArrayQueryItem _trans_item;
	private final SenseArrayQueryItem _def_item;
	private final ObjectArrayQueryItem _category_item;
	private final StringPairQueryItem _custom_field_key_item;
	private final StringPairQueryItem _custom_field_value_item;
	private final StringQueryItem _lesson_item;

	public SimpleEntryFilter() {
		super();
		_orth_item = new StringQueryItem("Orthography",
				StringQueryItem.CONTAINS, "");
		_pron_item = new ObjectArrayQueryItem("Pronunciations",
				ObjectArrayQueryItem.ITEM_CONTAINS, "");
		_trans_item = new SenseArrayQueryItem(
				SenseArrayQueryItem.TRANSLATION_CONTAINS, "");
		_def_item = new SenseArrayQueryItem(
				SenseArrayQueryItem.DEFINITION_CONTAINS, "");
		_category_item = new ObjectArrayQueryItem("Categories",
				ObjectArrayQueryItem.ITEM_CONTAINS, "");
		_custom_field_key_item = new StringPairQueryItem("CustomFields",
				StringPairQueryItem.KEY_CONTAINS, "");
		_custom_field_value_item = new StringPairQueryItem("CustomFields",
				StringPairQueryItem.VALUE_CONTAINS, "");
		_lesson_item = new StringQueryItem("Lesson", StringQueryItem.CONTAINS,
				"");
		_query = new ObjectQuery(Entry.class);
		_query.setType(ObjectQuery.MATCH_ONE);
		_query.addItem(_orth_item);
		_query.addItem(_pron_item);
		_query.addItem(_trans_item);
		_query.addItem(_def_item);
		_query.addItem(_category_item);
		_query.addItem(_custom_field_key_item);
		_query.addItem(_custom_field_value_item);
		_query.addItem(_lesson_item);
	}

	public String getFilterString() {
		return (String) _orth_item.getValue();
	}

	public void setFilterString(String value) {
		_orth_item.setValue(value);
		_pron_item.setValue(value);
		_trans_item.setValue(value);
		_def_item.setValue(value);
		_category_item.setValue(value);
		_custom_field_key_item.setValue(value);
		_custom_field_value_item.setValue(value);
		_lesson_item.setValue(value);
	}

	public void setMatchCase(boolean match) {
		_orth_item.setMatchCase(match);
		_pron_item.setMatchCase(match);
		_trans_item.setMatchCase(match);
		_def_item.setMatchCase(match);
		_category_item.setMatchCase(match);
		_custom_field_key_item.setMatchCase(match);
		_custom_field_value_item.setMatchCase(match);
		_lesson_item.setMatchCase(match);
	}
}
