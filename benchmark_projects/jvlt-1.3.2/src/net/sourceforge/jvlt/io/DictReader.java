package net.sourceforge.jvlt.io;

import java.io.IOException;
import java.io.InputStream;

import net.sourceforge.jvlt.JVLT;
import net.sourceforge.jvlt.core.Dict;

public abstract class DictReader {
	protected Dict _dict;
	protected String _version;

	public DictReader(String version) {
		_dict = null;
		_version = version;
	}

	public DictReader() {
		this(JVLT.getDataVersion());
	}

	public Dict getDict() {
		return _dict;
	}

	public abstract void read(InputStream stream) throws DictReaderException,
			IOException;
}
