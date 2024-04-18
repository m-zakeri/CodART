package net.sourceforge.jvlt.multimedia;

import java.io.File;
import java.io.IOException;

import net.sourceforge.jvlt.ui.JVLTUI;
import net.sourceforge.jvlt.utils.FileUtils;
import net.sourceforge.jvlt.utils.I18nService;

import org.apache.log4j.Logger;

public abstract class MultimediaFile {
	private static final Logger logger = Logger.getLogger(MultimediaFile.class);

	public static final int OTHER_FILE = 0;
	public static final int AUDIO_FILE = 1;
	public static final int IMAGE_FILE = 2;

	protected String _file_name;
	protected int _type;

	public MultimediaFile(String file_name, int type) {
		_file_name = file_name;
		_type = type;
	}

	public MultimediaFile(String file_name) {
		this(file_name, OTHER_FILE);
	}

	public String getFileName() {
		return _file_name;
	}

	public void setFileName(String name) {
		_file_name = name;
	}

	public int getType() {
		return _type;
	}

	public String getTypeString() {
		return getTypeString(_type);
	}

	public static String getTypeString(int type) {
		if (type == AUDIO_FILE) {
			return I18nService.getString("Labels", "audio_file");
		} else if (type == IMAGE_FILE) {
			return I18nService.getString("Labels", "image_file");
		} else {
			// if (type == OTHER_FILE)
			return I18nService.getString("Labels", "other_file");
		}
	}

	protected File getFile() {
		String path = System.getProperty("user.home");
		String dict_file = JVLTUI.getModel().getDictFileName();
		if (dict_file != null && !dict_file.equals("")) {
			path = new File(dict_file).getParentFile().getAbsolutePath();
		}

		File f;
		try {
			if (FileUtils.isPathRelative(_file_name)) {
				f = new File(path + File.separator + _file_name);
			} else {
				f = new File(_file_name);
			}
		} catch (IOException e) {
			logger.error("Could not determine canonical path for '"
					+ _file_name + "'", e);
			return null;
		}

		return f;
	}
}
