package net.sourceforge.jvlt.utils;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class FileUtils {
	public static boolean isPathRelative(String path) throws IOException {
		File f = new File(path);
		return !f.getCanonicalPath().equals(path);
	}

	/**
	 * Get relative path of file <i>f</i> with respect to <i>d</i> directory.
	 */
	public static String getRelativePath(File d, File f) {
		List<String> homelist = getPathList(d);
		List<String> filelist = getPathList(f);

		return matchPathLists(homelist, filelist);
	}

	public static String getFileExtension(String file_name) {
		int index = file_name.lastIndexOf('.');
		if (index < 0 || index == file_name.length() - 1) {
			return "";
		}
		return file_name.substring(index + 1);
	}

	private static List<String> getPathList(File f) {
		ArrayList<String> l = new ArrayList<String>();
		try {
			File r = f.getCanonicalFile();
			while (r != null) {
				l.add(r.getName());
				r = r.getParentFile();
			}
		} catch (IOException e) {
			e.printStackTrace();
			l = null;
		}

		return l;
	}

	private static String matchPathLists(List<String> r, List<String> f) {
		String s = "";
		int i = r.size() - 1;
		int j = f.size() - 1;

		// Eliminate common root.
		while ((i >= 0) && (j >= 0) && r.get(i).equals(f.get(j))) {
			i--;
			j--;
		}

		for (; i >= 0; i--) {
			s += ".." + File.separator;
		}
		for (; j >= 1; j--) {
			s += f.get(j) + File.separator;
		}

		s += f.get(j);

		return s;
	}
}
