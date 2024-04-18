package net.sourceforge.jvlt.core;

import java.util.Arrays;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.TreeSet;

public class Example implements Reinitializable, Comparable<Example> {
	public static class Comparator implements java.util.Comparator<Example> {
		public int compare(Example e1, Example e2) {
			return e1.getText().compareTo(e2.getText());
		}

		@Override
		public boolean equals(Object obj) {
			return super.equals(obj);
		}
	}

	public static class TextFragment {
		private String _text;
		private Sense _sense;

		public TextFragment(String text, Sense sense) {
			_text = text;
			_sense = sense;
		}

		public TextFragment(TextFragment fragment) {
			this(fragment.getText(), fragment.getSense());
		}

		public TextFragment(String text) {
			this(text, null);
		}

		public TextFragment() {
			this("", null);
		}

		public String getText() {
			return _text;
		}

		public Sense getSense() {
			return _sense;
		}

		public void setText(String text) {
			_text = text;
		}

		public void setSense(Sense sense) {
			_sense = sense;
		}

		@Override
		public String toString() {
			return _text;
		}
	}

	private final LinkedList<TextFragment> _fragments;
	private String _id;
	private String _translation;

	public Example(String id, TextFragment[] fragments, String translation) {
		_id = id;
		_fragments = new LinkedList<TextFragment>(Arrays.asList(fragments));
		_translation = translation;
	}

	public Example(String id) {
		this(id, new TextFragment[0], "");
	}

	public String getID() {
		return _id;
	}

	/**
	 * Creates a copy with depth one, i.e. the instances of class
	 * Example.TextFragment are copied, but not the text fragment's instances of
	 * class Sense.
	 */
	@Override
	public Object clone() {
		Example example = new Example(_id);
		example.setTranslation(_translation);
		Iterator<TextFragment> it = _fragments.iterator();
		while (it.hasNext()) {
			TextFragment tf = new TextFragment(it.next());
			example.addTextFragment(tf);
		}

		return example;
	}

	public void reinit(Reinitializable obj) {
		Example example = (Example) obj;
		_id = example._id;
		_translation = example._translation;
		_fragments.clear();
		_fragments.addAll(example._fragments);
	}

	public String getText() {
		String text = "";
		Iterator<TextFragment> it = _fragments.iterator();
		while (it.hasNext()) {
			TextFragment tf = it.next();
			text += tf.getText();
		}

		return text;
	}

	/**
	 * Returns the example text as HTML string. Links to words are marked with
	 * the &lt;a&gt; tag.
	 */
	public String getHTMLText() {
		StringBuilder builder = new StringBuilder();
		for (TextFragment fragment : _fragments) {
			if (fragment.getSense() == null) {
				builder.append(fragment.getText());
			} else {
				builder.append("<a href=\"" + fragment.getSense().getID()
						+ "\">" + fragment.getText() + "</a>");
			}
		}

		return builder.toString();
	}

	public String getTranslation() {
		return _translation;
	}

	public Sense[] getSenses() {
		TreeSet<Sense> senses = new TreeSet<Sense>();
		Iterator<TextFragment> it = _fragments.iterator();
		while (it.hasNext()) {
			TextFragment tf = it.next();
			if (tf.getSense() != null) {
				senses.add(tf.getSense());
			}
		}

		return senses.toArray(new Sense[0]);
	}

	public TextFragment[] getTextFragments() {
		return _fragments.toArray(new TextFragment[0]);
	}

	public void setID(String id) {
		_id = id;
	}

	public void setTranslation(String t) {
		_translation = t;
	}

	public void addTextFragment(TextFragment fragment) {
		_fragments.add(fragment);
	}

	public void insertTextFragmentBefore(TextFragment fragment,
			TextFragment before) {
		int index = _fragments.indexOf(before);
		_fragments.add(index, fragment);
	}

	public void insertTextFragmentAfter(TextFragment fragment,
			TextFragment after) {
		int index = _fragments.indexOf(after);
		_fragments.add(index + 1, fragment);
	}

	public void removeTextFragment(TextFragment fragment) {
		_fragments.remove(fragment);
	}

	@Override
	public String toString() {
		String str = getText();
		if ((_translation != null) && (!_translation.equals(""))) {
			str += " - ";
			str += _translation;
		}

		return str;
	}

	public int compareTo(Example e) {
		return _id.compareTo(e.getID());
	}

	/**
	 * Returns true if <i>o</i> is a clone of this example or if <i>o</i> and
	 * this example are the same object.
	 */
	@Override
	public boolean equals(Object o) {
		//Added by John Fan
		if (o == null) {
			return false;
		}
		
		if (!(o instanceof Example)) {
			return false;
		}

		return (compareTo((Example) o) == 0);
	}
}
