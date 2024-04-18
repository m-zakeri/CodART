package net.sourceforge.jvlt.io;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.Arrays;
import java.util.HashSet;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class XMLWriter {
	private boolean _do_indent;
	private final HashSet<String> _no_indent_tags;
	private final OutputStream _stream;
	private String _indent;
	private Writer _writer;

	public XMLWriter(OutputStream stream) {
		_stream = stream;
		_indent = "";
		_writer = null;
		_do_indent = true;
		_no_indent_tags = new HashSet<String>();
	}

	public void setNoIndentTags(String[] tags) {
		_no_indent_tags.addAll(Arrays.asList(tags));
	}

	public void write(Document doc) throws IOException {
		_writer = new BufferedWriter(new OutputStreamWriter(_stream, "UTF-8"));
		_writer.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n");

		write(doc.getDocumentElement());

		_writer.flush();
		_writer = null;
	}

	private void write(Element elem) throws IOException {
		boolean indent_this_node = _do_indent;
		boolean indent_child_nodes = indent_this_node
				&& !_no_indent_tags.contains(elem.getTagName());

		if (indent_this_node) {
			_writer.write(_indent);
		}

		// Write tag name and attributes.
		_writer.write("<" + elem.getTagName());
		NamedNodeMap attributes = elem.getAttributes();
		for (int i = 0; i < attributes.getLength(); i++) {
			Node node = attributes.item(i);
			_writer.write(" " + node.getNodeName() + "=\""
					+ node.getNodeValue() + "\"");
		}
		_writer.write(">");

		// Check whether there is a child text node. If there is one, then
		// do not indent.
		NodeList childnodes = elem.getChildNodes();
		if (indent_child_nodes) {
			for (int i = 0; i < childnodes.getLength(); i++) {
				if (childnodes.item(i).getNodeType() == Node.TEXT_NODE) {
					indent_child_nodes = false;
					break;
				}
			}
		}

		if (indent_child_nodes) {
			_writer.write("\n");
		}

		for (int i = 0; i < childnodes.getLength(); i++) {
			Node node = childnodes.item(i);
			if (node.getNodeType() == Node.ELEMENT_NODE) {
				Element element = (Element) node;
				_do_indent = indent_child_nodes;
				if (indent_child_nodes) {
					_indent += "\t";
					write(element);
					_indent = _indent.substring(0, _indent.length() - 1);
				} else {
					write(element);
				}
				_do_indent = indent_this_node;
			} else if (node.getNodeType() == Node.TEXT_NODE) {
				_writer.write(node.getNodeValue());
			}
		}

		if (indent_child_nodes) {
			_writer.write(_indent);
		}
		_writer.write("</" + elem.getTagName() + ">");
		if (indent_this_node) {
			_writer.write("\n");
		}
	}
}
