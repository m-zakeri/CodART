package net.sourceforge.jvlt.io;

import java.io.InputStream;
import java.util.Iterator;
import java.util.TreeMap;
import java.util.TreeSet;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import net.sourceforge.jvlt.core.ArraySchemaAttribute;
import net.sourceforge.jvlt.core.AttributeChoice;
import net.sourceforge.jvlt.core.ChoiceSchemaAttribute;
import net.sourceforge.jvlt.core.EntryAttributeSchema;
import net.sourceforge.jvlt.core.EntryClass;
import net.sourceforge.jvlt.core.SchemaAttribute;
import net.sourceforge.jvlt.utils.Utils;

import org.apache.log4j.Logger;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

public class EntryAttributeSchemaReader {
	private static final Logger logger = Logger
			.getLogger(EntryAttributeSchemaReader.class);

	public EntryAttributeSchema readSchema(String language)
			throws XPathExpressionException {
		String file_name = "/xml/details_" + language + ".xml";
		XPathFactory xpf = XPathFactory.newInstance();
		XPath path = xpf.newXPath();
		InputStream input = EntryAttributeSchemaReader.class
				.getResourceAsStream(file_name);
		InputSource src = new InputSource(input);
		Element root = (Element) path.evaluate("/schema", src,
				XPathConstants.NODE);
		EntryAttributeSchema eas = new EntryAttributeSchema(root
				.getAttribute("lang"));

		// -----
		// Read classes
		// -----
		TreeMap<String, EntryClass> entry_classes = new TreeMap<String, EntryClass>();
		NodeList node_list = (NodeList) path.evaluate("class", root,
				XPathConstants.NODESET);
		for (int i = 0; i < node_list.getLength(); i++) {
			Element elem = (Element) node_list.item(i);
			String name = elem.getAttribute("name");
			EntryClass ec = new EntryClass(name);
			entry_classes.put(name, ec);
			eas.addEntryClass(ec);
		}

		// -----
		// Read attributes
		// -----
		NodeList attr_list = (NodeList) path.evaluate("attribute", root,
				XPathConstants.NODESET);
		for (int i = 0; i < attr_list.getLength(); i++) {
			Element elem = (Element) attr_list.item(i);
			String name = elem.getAttribute("name");
			String group = elem.getAttribute("group");
			String[] classes = Utils.split(elem.getAttribute("classes"), ";");
			SchemaAttribute attribute;

			// Create schema element
			NodeList nl = (NodeList) path.evaluate("choice", elem,
					XPathConstants.NODESET);
			if (nl.getLength() > 0) {
				attribute = readChoiceAttribute(path, elem, group);
			} else {
				attribute = new SchemaAttribute(name, group);
			}

			// Assign attributes to entry classes
			if (classes.length == 0) {
				Iterator<EntryClass> it = entry_classes.values().iterator();
				while (it.hasNext()) {
					it.next().addAttribute(attribute);
				}
			} else {
				for (String classe : classes) {
					EntryClass ec = entry_classes.get(classe);
					ec.addAttribute(attribute);
				}
			}
		} // end of for (int i=0; i<attr_list.getLength(); i++)

		// -----
		// Handle inheritance of classes.
		// -----
		TreeSet<EntryClass> root_nodes = new TreeSet<EntryClass>();
		for (int i = 0; i < node_list.getLength(); i++) {
			Element elem = (Element) node_list.item(i);
			String name = elem.getAttribute("name");
			String parent_name = elem.getAttribute("extends");
			if (parent_name == null || parent_name.equals("")) {
				continue;
			}

			EntryClass child = entry_classes.get(name);
			EntryClass parent = entry_classes.get(parent_name);
			child.setParentClass(parent);
			root_nodes.remove(child);
			root_nodes.add(parent);
		}
		for (EntryClass entryClass : root_nodes) {
			copyAttributes(entryClass);
		}

		return eas;
	}

	private void copyAttributes(EntryClass cl) {
		EntryClass parent = cl.getParentClass();
		if (parent != null) {
			cl.addAttributes(parent.getAttributes());
		}

		EntryClass[] children = cl.getChildClasses();
		for (EntryClass element : children) {
			copyAttributes(element);
		}
	}

	private ChoiceSchemaAttribute readChoiceAttribute(XPath path, Element elem,
			String group) throws XPathExpressionException {
		ChoiceSchemaAttribute csa;
		String name = elem.getAttribute("name");
		if (elem.getAttribute("occurrence").equals("multiple")) {
			csa = new ArraySchemaAttribute(name, group);
		} else {
			csa = new ChoiceSchemaAttribute(name, group);
		}

		TreeMap<String, AttributeChoice> choice_map = new TreeMap<String, AttributeChoice>();
		NodeList nl = (NodeList) path.evaluate("choice", elem,
				XPathConstants.NODESET);
		for (int j = 0; j < nl.getLength(); j++) {
			Element e = (Element) nl.item(j);
			AttributeChoice ac = new AttributeChoice(e.getAttribute("name"));
			csa.addChoice(ac);
			choice_map.put(e.getAttribute("name"), ac);
		}

		// -----
		// Handle inheritance of choices.
		// -----
		for (int i = 0; i < nl.getLength(); i++) {
			Element e = (Element) nl.item(i);
			String child_name = e.getAttribute("name");
			String parent_name = e.getAttribute("extends");
			if (parent_name != null && !parent_name.equals("")) {
				AttributeChoice ac = choice_map.get(parent_name);
				if (ac == null) {
					logger.warn("Choice '" + parent_name + "' does not exist.");
				} else {
					(choice_map.get(child_name)).setParent(ac);
				}
			}
		}

		return csa;
	}
}
