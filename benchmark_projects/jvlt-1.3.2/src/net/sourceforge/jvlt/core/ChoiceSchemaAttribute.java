package net.sourceforge.jvlt.core;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

import net.sourceforge.jvlt.utils.Utils;

public class ChoiceSchemaAttribute extends SchemaAttribute {
	private final ArrayList<AttributeChoice> _choices;
	private final HashMap<String, AttributeChoice> _choice_map;

	public ChoiceSchemaAttribute(String name, String group) {
		super(name, group);

		_choices = new ArrayList<AttributeChoice>();
		_choice_map = new HashMap<String, AttributeChoice>();
	}

	public ChoiceSchemaAttribute(String name) {
		this(name, "");
	}

	public AttributeChoice[] getChoices() {
		return _choices.toArray(new AttributeChoice[0]);
	}

	public AttributeChoice getChoice(String name) {
		return _choice_map.get(name);
	}

	public void addChoice(AttributeChoice val) {
		_choices.add(val);
		_choice_map.put(val.getName(), val);
	}

	public void setChoices(AttributeChoice[] vals) {
		_choices.clear();
		_choice_map.clear();
		for (AttributeChoice val : vals) {
			addChoice(val);
		}
	}

	@Override
	public String toString() {
		StringBuffer buf = new StringBuffer();
		buf.append(super.toString());
		buf.deleteCharAt(buf.length() - 1);
		buf.append(";choices=");
		String[] choices = new String[_choices.size()];
		int i = 0;
		for (Iterator<AttributeChoice> it = _choices.iterator(); it.hasNext(); i++) {
			choices[i] = it.next().getName();
		}
		buf.append(Utils.arrayToString(choices, ","));
		buf.append('}');

		return buf.toString();
	}
}
