package net.sourceforge.jvlt.metadata;

import net.sourceforge.jvlt.core.Sense;

public class SenseMetaData extends MetaData {
	public SenseMetaData() {
		super(Sense.class);

		addAttribute(new CustomFieldsAttribute());
	}
}
