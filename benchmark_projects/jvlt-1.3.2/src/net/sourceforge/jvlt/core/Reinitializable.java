package net.sourceforge.jvlt.core;

public interface Reinitializable extends Cloneable {
	void reinit(Reinitializable object);

	Object clone();
}
