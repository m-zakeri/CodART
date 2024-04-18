package net.sourceforge.jvlt.actions;

import java.util.Collection;

import net.sourceforge.jvlt.core.Example;

public class RemoveExamplesAction extends DictAction {
	private final Collection<Example> _examples;

	public RemoveExamplesAction(Collection<Example> examples) {
		_examples = examples;
	}

	public Collection<Example> getExamples() {
		return _examples;
	}
}
