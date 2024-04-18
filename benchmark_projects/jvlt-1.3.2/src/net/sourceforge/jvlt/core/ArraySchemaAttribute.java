package net.sourceforge.jvlt.core;


public class ArraySchemaAttribute extends ChoiceSchemaAttribute {
	public ArraySchemaAttribute(String name, String group) {
		super(name, group);
	}

	public ArraySchemaAttribute(String name) {
		this(name, "");
	}
}
