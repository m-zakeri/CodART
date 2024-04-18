package net.sourceforge.jvlt.utils;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

import javax.swing.filechooser.FileFilter;

public class SimpleFileFilter extends FileFilter {
	private final ArrayList<String> _extensions;
	private final String _description;

	public SimpleFileFilter(String description) {
		_extensions = new ArrayList<String>();
		_description = description;
	}

	@Override
	public boolean accept(File f) {
		if (f.isDirectory()) {
			return true;
		}

		String name = f.getName();
		Iterator<String> it = _extensions.iterator();
		while (it.hasNext()) {
			if (name.endsWith(it.next())) {
				return true;
			}
		}

		return false;
	}

	@Override
	public String getDescription() {
		return _description;
	}

	public void setExtensions(String[] extensions) {
		_extensions.addAll(Arrays.asList(extensions));
	}

	public void addExtension(String extension) {
		_extensions.add(extension);
	}
}
