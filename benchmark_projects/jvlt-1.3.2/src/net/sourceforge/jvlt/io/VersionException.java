package net.sourceforge.jvlt.io;

public class VersionException extends Exception {
	private static final long serialVersionUID = 1L;

	private final String _version;

	public VersionException(String version) {
		_version = version;
	}

	public String getVersion() {
		return _version;
	}
}
