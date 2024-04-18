package net.sourceforge.jvlt.actions;

import java.util.ArrayList;
import java.util.Collection;
import java.util.TreeMap;
import java.util.TreeSet;

import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.core.DictException;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.core.Sense;
import net.sourceforge.jvlt.core.Example.TextFragment;

public class RemoveEntriesAction extends DictAction {
	private final Dict _dict;
	private final Collection<Entry> _entries;
	private final TreeSet<Example> _removed_examples;
	private final ArrayList<EditDictObjectAction> _example_actions;

	public RemoveEntriesAction(Dict dict, Collection<Entry> entries) {
		_dict = dict;
		_entries = entries;
		_removed_examples = new TreeSet<Example>();
		_example_actions = new ArrayList<EditDictObjectAction>();

		TreeSet<Entry> removed_entries = new TreeSet<Entry>();
		removed_entries.addAll(entries);

		TreeMap<Example, TreeSet<Entry>> example_map = new TreeMap<Example, TreeSet<Entry>>();
		for (Entry entry : entries) {
			Collection<Example> examples = _dict.getExamples(entry);
			for (Example example : examples) {
				if (!example_map.containsKey(example)) {
					// Add all linked entries except for the current entry.
					TreeSet<Entry> entry_set = new TreeSet<Entry>();
					Sense[] senses = example.getSenses();
					for (Sense sense : senses) {
						entry_set.add(sense.getParent());
					}
					entry_set.remove(entry);
					example_map.put(example, entry_set);
				} else {
					TreeSet<Entry> entry_set = example_map.get(example);
					entry_set.remove(entry);
				}
			}
		}

		for (Example example : example_map.keySet()) {
			TreeSet<Entry> entry_set = example_map.get(example);
			if (entry_set.size() == 0) {
				_removed_examples.add(example);
			} else {
				Example new_example = (Example) example.clone();
				Example.TextFragment[] fragments = new_example
						.getTextFragments();
				for (TextFragment f : fragments) {
					if (f.getSense() != null
							&& removed_entries.contains(f.getSense()
									.getParent())) {
						f.setSense(null);
					}
				}
				_example_actions.add(new EditDictObjectAction(example,
						new_example));
			}
		}
	}

	public Collection<Entry> getRemovedEntries() {
		return _entries;
	}

	public Collection<Example> getRemovedExamples() {
		return _removed_examples;
	}

	public Collection<Example> getModifiedExamples() {
		TreeSet<Example> examples = new TreeSet<Example>();
		for (EditDictObjectAction editDictObjectAction : _example_actions) {
			examples.add((Example) editDictObjectAction.getObject());
		}

		return examples;
	}

	public void executeAction() throws DictException {
		for (EditDictObjectAction editDictObjectAction : _example_actions) {
			editDictObjectAction.executeAction();
		}

		for (Example example : _removed_examples) {
			_dict.removeExample(example);
		}

		for (Entry entry : _entries) {
			_dict.removeEntry(entry);
		}
	}

	public void undoAction() throws DictException {
		for (Entry entry : _entries) {
			_dict.addEntry(entry);
		}

		for (EditDictObjectAction editDictObjectAction : _example_actions) {
			editDictObjectAction.undoAction();
		}

		for (Example example : _removed_examples) {
			_dict.addExample(example);
		}
	}
}
