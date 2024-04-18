package net.sourceforge.jvlt.utils;

import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

public class SimpleHTMLParser {
	public static final String[] SUPPORTED_TAGS = { "b", "br", "i", "p", "a" };
	public static final String[] SOLO_TAGS = { "br" };

	private static final Pattern ELEM_PATTERN = Pattern
			.compile("<(/?[a-zA-Z]+)((?:\\s+[\\w-]+=\"[\\w-]+\")*)>");
	private static final Pattern ATTRIBUTE_PATTERN = Pattern
			.compile("([\\w-]+)=\"([\\w-]+)\"");

	private final HashSet<String> _supported_tags = new HashSet<String>();
	private final HashSet<String> _solo_tags = new HashSet<String>();
	private Node[] _nodes = new Node[0];

	public SimpleHTMLParser() {
		_supported_tags.addAll(Arrays.asList(SUPPORTED_TAGS));
		_solo_tags.addAll(Arrays.asList(SOLO_TAGS));
	}

	public void parse(String input) throws ParseException {
		parse(input, null);
	}

	public void parse(String input, Document doc) throws ParseException {
		// -----
		// Check whether the argument input contains only the supported html
		// tags and whether all opening tags are closed. If the argument doc
		// is not null, build a DOM tree representing the html structure.
		// -----
		Stack<String> tags = new Stack<String>();
		Matcher matcher = ELEM_PATTERN.matcher(input);
		ArrayList<Node> list = doc == null ? null : new ArrayList<Node>();
		Element current_elem = null;
		int pos = 0;
		while (matcher.find()) {
			String match = matcher.group(1);
			if (match.charAt(0) == '/') { /* end tag */
				match = match.substring(1);
				Object o = tags.pop();
				if (!o.equals(match)) {
					throw new ParseException(
							"Unexpected closing tag: " + match, matcher.start());
				}

				if (doc != null) {
					/* read text starting from the last tag until this tag */
					int start = matcher.start();
					if (start > pos) {
						current_elem.appendChild(doc.createTextNode(input
								.substring(pos, start)));
					}

					current_elem = (Element) current_elem.getParentNode();
					pos = matcher.end();
				}
			} else { /* start tag */
				if (!_supported_tags.contains(match)) {
					throw new ParseException("Invalid tag: \"" + match + "\"",
							matcher.start());
				}

				if (!_solo_tags.contains(match)) {
					tags.push(match);
				}
				if (doc != null) {
					int start = matcher.start();
					// If text was read, add a text node
					if (start > pos) {
						Node node = doc.createTextNode(input.substring(pos,
								start));
						if (current_elem != null) {
							current_elem.appendChild(node);
						} else {
							list.add(node);
						}
					}

					Element elem = doc.createElement(match);
					addAttributes(elem, matcher.group(2));
					if (current_elem != null) {
						current_elem.appendChild(elem);
					} else {
						list.add(elem);
					}

					current_elem = elem;
					pos = matcher.end();
				}
			} // else
		} // while
		if (tags.size() > 0) {
			throw new ParseException("Tag \"" + tags.peek()
					+ "\" was not closed", input.length());
		}
		if (doc != null && pos < input.length()) {
			list.add(doc.createTextNode(input.substring(pos, input.length())));
		}

		if (doc != null) {
			_nodes = list.toArray(new Node[0]);
		} else {
			_nodes = new Node[0];
		}
	}

	public Node[] getNodes() {
		return _nodes;
	}

	private void addAttributes(Element elem, String attr_string) {
		Matcher matcher = ATTRIBUTE_PATTERN.matcher(attr_string);
		while (matcher.find()) {
			elem.setAttribute(matcher.group(1), matcher.group(2));
		}
	}
}
