package net.sourceforge.jvlt.tools;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.TreeMap;
import java.util.Vector;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import net.sourceforge.jvlt.ui.JVLTUI;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

class ResourceBundleUtils {

	private static final Logger logger = Logger
			.getLogger(ResourceBundleUtils.class);
	private static final String[] LANGUAGES = new String[] { "cs_CZ", "de_DE",
			"fr_FR", "pl_PL" };

	private final String[] _files;
	private final String[] _languages;

	public ResourceBundleUtils(String[] files, String[] languages) {
		_files = files;
		_languages = languages;
	}

	public void sync() {
		for (String file2 : _files) {
			PropertiesFile file = readFile(file2 + ".properties");
			for (String language : _languages) {
				String file_name = file2 + "_" + language + ".properties";
				PropertiesFile tfile = readFile(file_name);
				try {
					FileOutputStream fos = new FileOutputStream(file_name);
					OutputStreamWriter osw = new OutputStreamWriter(fos, "UTF8");
					BufferedWriter writer = new BufferedWriter(osw);
					Line[] lines = file.getLines();
					int k = 0;
					while (k < lines.length) {
						Line line = lines[k];
						String key = file.getKey(line);
						if (key == null) {
							k++;
							writer.write(line.content + "\n");
						} else {
							Line[] file_lines = file.getLines(key);
							k = file_lines[file_lines.length - 1].index + 1;
							if (tfile.containsKey(key)) {
								Line[] tfile_lines = tfile.getLines(key);
								for (Line tfileLine : tfile_lines) {
									writer.write(tfileLine.content + "\n");
								}
							} else {
								for (Line fileLine : file_lines) {
									writer
											.write("# " + fileLine.content
													+ "\n");
								}
							}
						}
					}

					writer.close();
				} catch (Exception ex) {
					ex.printStackTrace();
				}
			}
		}
	}

	public static void main(String[] args) {
		PropertyConfigurator.configure(JVLTUI.class
				.getResource("/log4j.properties"));

		if (args.length < 1) {
			logger.error("No path specified");
			System.exit(1);
		}

		ArrayList<String> files = new ArrayList<String>();
		files.add(args[0] + "/Actions");
		files.add(args[0] + "/Attributes");
		files.add(args[0] + "/Labels");
		files.add(args[0] + "/Messages");
		ResourceBundleUtils utils = new ResourceBundleUtils(files
				.toArray(new String[0]), LANGUAGES);
		utils.sync();
	}

	private PropertiesFile readFile(String filename) {
		PropertiesFile pf = new PropertiesFile();
		Pattern assign_pattern = Pattern.compile("([a-zA-Z0-9_-]+)\\s*=.*");
		Pattern empty_pattern = Pattern.compile("\\s*|#.*");
		File file = new File(filename);
		if (file.exists()) {
			try {
				FileInputStream fis = new FileInputStream(file);
				InputStreamReader isr = new InputStreamReader(fis, "UTF8");
				BufferedReader reader = new BufferedReader(isr);
				String current_key = null;
				boolean new_key = true;
				for (int i = 0; reader.ready(); i++) {
					String line = reader.readLine();
					if (new_key) {
						Matcher matcher = assign_pattern.matcher(line);
						if (!matcher.matches()) {
							if (empty_pattern.matcher(line).matches()) {
								pf.addLine(new Line(i, line), null);
								continue;
							}
							throw new Exception("Invalid line: " + line);
						}
						current_key = matcher.group(1);
						pf.addLine(new Line(i, line), current_key);
						if (line.endsWith("\\")) {
							new_key = false;
						}
					} else {
						pf.addLine(new Line(i, line), current_key);
						if (!line.endsWith("\\")) {
							new_key = true;
							current_key = null;
						}
					}
				}
				reader.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
		}

		return pf;
	}
}

class Line implements Comparable<Line> {
	public int index;
	public String content;

	public Line(int i, String c) {
		this.index = i;
		this.content = c;
	}

	public int compareTo(Line line) {
		Line l = line;
		if (index != l.index) {
			return index - l.index;
		}
		return content.compareTo(l.content);
	}
}

class PropertiesFile {
	private final TreeMap<Line, String> _line_map;
	private final TreeMap<String, Vector<Line>> _key_map;

	public PropertiesFile() {
		_line_map = new TreeMap<Line, String>();
		_key_map = new TreeMap<String, Vector<Line>>();
	}

	public void addLine(Line l, String k) {
		_line_map.put(l, k);
		if (k != null) {
			if (!_key_map.containsKey(k)) {
				_key_map.put(k, new Vector<Line>());
			}

			Vector<Line> v = _key_map.get(k);
			v.add(l);
		}
	}

	public Line[] getLines() {
		return _line_map.keySet().toArray(new Line[0]);
	}

	public Line[] getLines(String key) {
		return _key_map.get(key).toArray(new Line[0]);
	}

	public boolean containsKey(String key) {
		return _key_map.containsKey(key);
	}

	public String getKey(Line line) {
		return _line_map.get(line);
	}
}
