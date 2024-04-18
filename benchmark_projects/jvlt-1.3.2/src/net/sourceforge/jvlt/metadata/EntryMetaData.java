package net.sourceforge.jvlt.metadata;

import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import net.sourceforge.jvlt.core.ArraySchemaAttribute;
import net.sourceforge.jvlt.core.ChoiceSchemaAttribute;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.EntryAttributeSchema;
import net.sourceforge.jvlt.core.EntryClass;
import net.sourceforge.jvlt.core.SchemaAttribute;
import net.sourceforge.jvlt.core.Sense;
import net.sourceforge.jvlt.utils.AttributeResources;
import net.sourceforge.jvlt.utils.DictObjectFormatter;
import net.sourceforge.jvlt.utils.I18nService;
import net.sourceforge.jvlt.utils.Utils;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class EntryMetaData extends MetaData {
	public static class SensesAttribute extends ArrayAttribute {
		private final MetaData _sense_data = new SenseMetaData();

		public SensesAttribute() {
			super("Senses", Sense[].class);
			setDelimiter("; ");
			setEnableNumbering(true);
		}

		@Override
		public Element getXMLElement(Document doc, Object o) {
			DictObjectFormatter formatter = new DictObjectFormatter(doc);
			Element elem = doc.createElement("Senses");
			Sense[] senses = (Sense[]) getValue(o);
			for (Sense sense : senses) {
				elem.appendChild(formatter.getElementForObject(sense,
						_sense_data.getAttributes()));
			}

			return elem;
		}
	}

	public static class EntryClassAttribute extends DefaultAttribute {
		public EntryClassAttribute() {
			super("EntryClass", EntryClass.class);
		}

		@Override
		public String getFormattedValue(Object o) {
			EntryClass cl = (EntryClass) getValue(o);
			if (cl == null) {
				return "";
			}
			AttributeResources resources = new AttributeResources();
			return resources.getString(cl.getName());
		}
	}

	public static class UserFlagsAttribute extends DefaultAttribute {
		public UserFlagsAttribute() {
			super("UserFlags", Integer.class);
		}

		@Override
		public String getFormattedValue(Object o) {
			Integer value = (Integer) getValue(o);
			List<Entry.Stats.UserFlag> flags = new ArrayList<Entry.Stats.UserFlag>();
			for (Entry.Stats.UserFlag f : Entry.Stats.UserFlag.values()) {
				if ((value & f.getValue()) != 0) {
					flags.add(f);
				}
			}

			String[] string_list = new String[flags.size()];
			for (int i = 0; i < string_list.length; i++) {
				string_list[i] = I18nService.getString("Labels", flags.get(i)
						.getShortName());
			}

			return Utils.arrayToString(string_list, ", ");
		}
	}

	private EntryAttributeSchema _schema = null;
	private final Vector<CustomAttribute> _custom_attributes;

	public EntryMetaData() {
		super(Entry.class);

		_custom_attributes = new Vector<CustomAttribute>();

		// Remove attributes that shouldn't be visible for the user
		removeAttribute("ID");
		removeAttribute("Stats");

		addAttribute(new SensesAttribute());
		addAttribute(new DefaultChoiceAttribute("Lesson", String.class));
		addAttribute(new ArrayChoiceAttribute("Categories", String[].class));
		addAttribute(new CustomFieldsAttribute());
		addAttribute(new EntryClassAttribute());
		addAttribute(new UserFlagsAttribute());
	}

	public EntryAttributeSchema getAttributeSchema() {
		return _schema;
	}

	public void setAttributeSchema(EntryAttributeSchema schema) {
		_schema = schema;
		for (CustomAttribute customAttribute : _custom_attributes) {
			removeAttribute(customAttribute.getName());
		}
		_custom_attributes.clear();

		if (schema == null) {
			return;
		}

		EntryClass[] ecs = schema.getEntryClasses();
		for (EntryClass ec : ecs) {
			SchemaAttribute[] attrs = ec.getAttributes();
			for (SchemaAttribute attr : attrs) {
				CustomAttribute ca;
				if (attr instanceof ChoiceSchemaAttribute) {
					ChoiceSchemaAttribute csa = (ChoiceSchemaAttribute) attr;
					CustomChoiceAttribute cca;
					if (attr instanceof ArraySchemaAttribute) {
						cca = new CustomArrayAttribute(csa.getName());
					} else {
						cca = new CustomChoiceAttribute(csa.getName());
					}

					cca.setValues(csa.getChoices());
					ca = cca;
				} else {
					ca = new CustomAttribute(attr.getName());
				}
				_custom_attributes.add(ca);
				addAttribute(ca);
			}
		}
	}
}
