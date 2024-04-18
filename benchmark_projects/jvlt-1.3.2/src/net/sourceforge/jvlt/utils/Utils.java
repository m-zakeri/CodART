package net.sourceforge.jvlt.utils;

import java.awt.Font;
import java.net.MalformedURLException;
import java.net.URL;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Utils {
	private static Pattern WRAP_PATTERN = Pattern
			.compile("(.{0,79}[^\\s]\\s+)|(.{0,79}[^\\s])");

	public static String removeSubstring(String s, int begin_index,
			int end_index) {
		StringBuffer buf = new StringBuffer();
		for (int i = 0; i < s.length(); i++) {
			if (i < begin_index || i > end_index) {
				buf.append(s.charAt(i));
			}
		}

		return buf.toString();
	}

	/**
	 * Insert a String into an other.
	 * 
	 * @param s The string into which the other string is inserted. <i>s</i>
	 *            will not be modified itself - instead, the result will be
	 *            returned by the function.
	 * @param index The index of the character before which the the string will
	 *            be inserted. If index is equal to the length of <i>s</i> then
	 *            the string will be appended.
	 * @param t The string to be inserted.
	 */
	public static String insertString(String s, int index, String t) {
		String before;
		if (index == 0) {
			before = "";
		} else {
			before = s.substring(0, index);
		}
		String after;
		if (index == s.length()) {
			after = "";
		} else {
			after = s.substring(index, s.length());
		}

		return before + t + after;
	}

	public static void removeClassInstances(Collection<? extends Object> c,
			Class<?> clazz) {
		Iterator<? extends Object> it = c.iterator();
		while (it.hasNext()) {
			Object obj = it.next();
			if (clazz.isInstance(obj)) {
				it.remove();
			}
		}
	}

	public static boolean arrayContainsItem(Object[] array, Object item) {
		for (Object element : array) {
			if (element.equals(item)) {
				return true;
			}
		}

		return false;
	}

	public static URL getDirectory(URL url) {
		try {
			String p = url.getPath().substring(0,
					url.getPath().lastIndexOf("/") + 1);
			URL d = new URL(url.getProtocol(), url.getHost(), url.getPort(), p);
			return d;
		} catch (MalformedURLException ex) {
			ex.printStackTrace();
			return null;
		}
	}

	public static String fontToString(Font font) {
		if (font == null) {
			return "";
		}

		int style = font.getStyle();
		String style_str;
		switch (style) {
		case Font.PLAIN:
			style_str = "PLAIN";
			break;
		case Font.BOLD:
			style_str = "BOLD";
			break;
		case Font.ITALIC:
			style_str = "ITALIC";
			break;
		case Font.BOLD | Font.ITALIC:
			style_str = "BOLDITALIC";
			break;
		default:
			throw new RuntimeException("Invalid style:" + style);
		}

		return font.getFamily() + "-" + style_str + "-" + font.getSize();
	}

	public static String[] split(String str) {
		return split(str, ";");
	}

	/**
	 * Split a single string into multiple strings.
	 * 
	 * @return An empty array if argument str is the empty string, otherwise the
	 *         same as {@link String#split(String)} yields.
	 */
	public static String[] split(String str, String delim) {
		if (str == null || str.equals("")) {
			return new String[0];
		}
		return str.split(delim);
	}

	public static String calendarToString(Calendar date) {
		if (date == null) {
			return "";
		}

		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
		return sdf.format(date.getTime());
	}

	public static String[] objectArrayToStringArray(Object[] values) {
		String[] array = new String[values.length];
		for (int i = 0; i < array.length; i++) {
			array[i] = values[i].toString();
		}

		return array;
	}

	public static List<String> objectArrayToStringList(Object[] values) {
		List<String> result = new ArrayList<String>(values.length);
		for (Object value : values) {
			result.add(value.toString());
		}
		return result;
	}

	public static boolean arraysEqual(Object[] array1, Object[] array2) {
		if (array1 == null) {
			return array2 == null;
		}
		if (array1.length != array2.length) {
			return false;
		}

		for (int i = 0; i < array1.length; i++) {
			if (!array1[i].equals(array2[i])) {
				return false;
			}
		}

		return true;
	}

	/**
	 * Escape a character. The escape sequence consists of the prefix /u and 4
	 * digits that represent the hex-code for the character.
	 */
	public static String escapeChar(char ch) {
		String hex = Integer.toHexString(ch);
		if (hex.length() == 1) {
			return "/u000" + hex;
		} else if (hex.length() == 2) {
			return "/u00" + hex;
		} else if (hex.length() == 3) {
			return "/u0" + hex;
		} else {
			return "/u" + hex;
		}
	}

	/**
	 * Wraps a string into lines with at most 80 characters each.
	 * 
	 * @param s The string to be wrapped
	 * @param delim The line delimiter
	 * @return The wrapped string
	 */
	public static String wrapString(String s, String delim) {
		StringBuilder builder = new StringBuilder();
		Matcher m = WRAP_PATTERN.matcher(s);
		while (m.find()) {
			builder.append(s.substring(m.start(), m.end()));
			if (m.end() < s.length()) {
				builder.append(delim);
			}
		}

		return builder.toString();
	}

	public static String arrayToString(Object[] values, String delim) {
		StringBuffer buf = new StringBuffer();
		for (int i = 0; i < values.length; i++) {
			if (i > 0) {
				buf.append(delim);
			}
			buf.append(values[i].toString());
		}
	
		return buf.toString();
	}

	public static String arrayToString(Object[] values) {
		return arrayToString(values, ";");
	}
}
