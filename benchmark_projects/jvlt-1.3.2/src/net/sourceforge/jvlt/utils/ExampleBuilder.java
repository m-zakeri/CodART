package net.sourceforge.jvlt.utils;

import java.util.Vector;

import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.core.Sense;

public class ExampleBuilder {
	private Example _example = null;

	public ExampleBuilder(Example example) {
		_example = example;
	}

	public void setExample(Example example) {
		_example = example;
	}

	public void addSense(Sense sense, int start_index, int end_index)
			throws DictException {
		Example.TextFragment[] tfs = getTextFragments(start_index, end_index);
		if (tfs.length != 1) {
			throw new DictException(I18nService.getString("Messages",
					"selection_too_large"));
		}

		Example.TextFragment tf = tfs[0];
		if (tf.getSense() != null) {
			throw new DictException(I18nService.getString("Messages",
					"selection_already_linked"));
		}

		String text = tf.getText();
		// Offset is the position of the marked text relative to the
		// text fragment, len is the length of the marked text.
		int offset = start_index - getTextFragmentOffset(tf);
		int len = end_index - start_index + 1;
		// System.out.println(""+offset+"/"+len);
		if (offset > 0) {
			String new_text = text.substring(0, offset);
			Example.TextFragment new_tf = new Example.TextFragment(new_text);
			_example.insertTextFragmentBefore(new_tf, tf);
			// System.out.println(new_tf.getText());
		}
		tf.setText(text.substring(offset, offset + len));
		tf.setSense(sense);
		// System.out.println(tf.getText());
		if (offset + len < text.length()) {
			String new_text = text.substring(offset + len, text.length());
			Example.TextFragment new_tf = new Example.TextFragment(new_text);
			_example.insertTextFragmentAfter(new_tf, tf);
			// System.out.println(new_tf.getText());
		}
	}

	public void removeTextFragment(Example.TextFragment tf) {
		Example.TextFragment[] fragments = _example.getTextFragments();
		tf.setSense(null);
		for (int i = 0; i < fragments.length; i++) {
			if (fragments[i] == tf) {
				if (i > 0) {
					Example.TextFragment tf_before = fragments[i - 1];
					if (tf_before.getSense() == null) {
						_example.removeTextFragment(tf_before);
						tf.setText(tf_before.getText() + tf.getText());
					}
				}
				if (i < fragments.length - 1) {
					Example.TextFragment tf_after = fragments[i + 1];
					if (tf_after.getSense() == null) {
						_example.removeTextFragment(tf_after);
						tf.setText(tf.getText() + tf_after.getText());
					}
				}

				break;
			}
		}
	}

	private Example.TextFragment[] getTextFragments(int start_index,
			int end_index) {
		Vector<Example.TextFragment> tfs = new Vector<Example.TextFragment>();
		Example.TextFragment[] fragments = _example.getTextFragments();
		int tf_start = 0;
		for (Example.TextFragment tf : fragments) {
			int tf_end = tf_start + tf.getText().length() - 1;
			if (start_index < tf_start && end_index >= tf_start) {
				tfs.add(tf);
			} else if (start_index >= tf_start && start_index <= tf_end) {
				tfs.add(tf);
			}

			tf_start += tf.getText().length();
		}

		return tfs.toArray(new Example.TextFragment[0]);
	}

	private int getTextFragmentOffset(Example.TextFragment fragment) {
		Example.TextFragment[] fragments = _example.getTextFragments();
		int offset = 0;
		for (Example.TextFragment tf : fragments) {
			if (tf.equals(fragment)) {
				return offset;
			}

			offset += tf.getText().length();
		}

		return -1;
	}
}
