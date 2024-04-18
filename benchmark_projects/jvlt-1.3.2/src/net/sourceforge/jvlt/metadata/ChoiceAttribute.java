package net.sourceforge.jvlt.metadata;

public interface ChoiceAttribute extends Attribute {
	void addValues(Object[] values);

	void setValues(Object[] values);

	Object[] getValues();
}
