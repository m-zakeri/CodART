package net.sourceforge.jvlt.io;

import java.io.IOException;
import java.io.OutputStream;

import net.sourceforge.jvlt.core.Dict;

public abstract class DictWriter {
	protected Dict _dict;
	protected OutputStream _stream;

	public DictWriter(Dict dict, OutputStream stream) {
		_dict = dict;
		_stream = stream;
	}

	public abstract void write() throws IOException;
}
