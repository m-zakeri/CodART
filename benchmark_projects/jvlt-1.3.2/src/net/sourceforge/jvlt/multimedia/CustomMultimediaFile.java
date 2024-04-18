package net.sourceforge.jvlt.multimedia;

import java.io.File;
import java.io.IOException;


public class CustomMultimediaFile extends MultimediaFile {
	private String _command;

	public CustomMultimediaFile(String file_name, int type) {
		super(file_name);
		_type = type;
	}

	public CustomMultimediaFile(String file_name) {
		super(file_name);
	}

	public CustomMultimediaFile(int type) {
		this("", type);
	}

	public void setType(int type) {
		_type = type;
	}

	public String getCommand() {
		return _command;
	}

	public void setCommand(String command) {
		_command = command;
	}

	public void play() throws IOException {
		if (_command == null || _command.equals("")) {
			return;
		}

		File f = getFile();
		if (!f.exists() || !f.isFile()) {
			String msg = "File " + f.getAbsolutePath() + " does not exist"
					+ " or cannot be opened.";
			throw new IOException(msg);
		}

		String c = _command.replaceAll("%f", f.getAbsolutePath());
		// System.out.println(c);
		Runtime rt = Runtime.getRuntime();
		rt.exec(c);
	}
}
