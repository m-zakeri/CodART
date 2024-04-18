package net.sourceforge.jvlt.utils;

import java.awt.Dimension;
import java.awt.Font;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.Map;
import java.util.TreeMap;

import org.apache.log4j.Logger;


public class UIConfig implements Config {
	private static final Logger logger = Logger.getLogger(UIConfig.class);

	private final TreeMap<String, String> properties = new TreeMap<String, String>();

	/** where to find/store configuration information */
	private final String configDir = getConfigPath();
;

	/** from old versions, used to move old data */
	private static final String OLD_CONFIG_DIR = System
			.getProperty("user.home")
			+ File.separator + ".jvlt";

	public String[] getKeys() {
		return properties.keySet().toArray(new String[0]);
	}

	public boolean containsKey(String key) {
		return properties.containsKey(key);
	}

	public String getProperty(String key) {
		return getProperty(key, null);
	}

	public String getProperty(String key, String default_value) {
		if (properties.containsKey(key)) {
			return properties.get(key);
		}
		return default_value;
	}

	public float getFloatProperty(String key, float default_val) {
		String str = getProperty(key, String.valueOf(default_val));
		float val;
		try {
			val = Float.parseFloat(str);
		} catch (NumberFormatException ex) {
			val = default_val;
		}

		return val;
	}

	public int getIntProperty(String key, int default_val) {
		String str = getProperty(key, String.valueOf(default_val));
		int val;
		try {
			val = Integer.parseInt(str);
		} catch (NumberFormatException e) {
			val = default_val;
		}
		return val;
	}

	public boolean getBooleanProperty(String key, boolean default_val) {
		String str = getProperty(key);
		if (str == null) {
			return default_val;
		} else if (str.equals("true")) {
			return true;
		} else if (str.equals("false")) {
			return false;
		} else {
			return default_val;
		}
	}

	public Font getFontProperty(String key) {
		String str = getProperty(key);

		if (str == null || str.equals("")) {
			return null;
		}
		return Font.decode(str);
	}

	public String[] getStringListProperty(String key, String[] def) {
		String prop = getProperty(key, Utils.arrayToString(def));
		return Utils.split(prop, ";");
	}

	public String[] getStringListProperty(String key) {
		return Utils.split(getProperty(key), ";");
	}

	public double[] getNumberListProperty(String key, double[] def) {
		String[] defstr = new String[def.length];
		for (int i = 0; i < def.length; i++) {
			defstr[i] = String.valueOf(def[i]);
		}

		String[] strings = getStringListProperty(key, defstr);
		double[] values = new double[strings.length];
		for (int i = 0; i < strings.length; i++) {
			values[i] = Double.parseDouble(strings[i]);
		}

		return values;
	}

	public Locale getLocaleProperty(String key, Locale def) {
		Locale loc = def;
		String str = getProperty(key, def.toString());
		int indexof = str.indexOf("_");
		if (indexof < 0) {
			loc = new Locale(str);
		} else {
			String lang = str.substring(0, indexof);
			String country = str.substring(indexof + 1, str.length());
			loc = new Locale(lang, country);
		}

		return loc;
	}

	public Dimension getDimensionProperty(String key, Dimension default_dim) {
		String val;
		if (default_dim != null) {
			val = getProperty(key, String.valueOf(default_dim.width) + ";"
					+ String.valueOf(default_dim.height));
		} else {
			val = getProperty(key);
		}

		try {
			String[] size = val.split(";");
			if (size.length != 2) {
				return null;
			}

			return new Dimension(Integer.parseInt(size[0]), Integer
					.parseInt(size[1]));
		} catch (NumberFormatException e) {
			return null;
		}
	}

	public void setProperty(String key, String value) {
		properties.put(key, value);
	}

	public void setProperty(String key, boolean value) {
		setProperty(key, String.valueOf(value));
	}

	public void setProperty(String key, int value) {
		setProperty(key, String.valueOf(value));
	}

	public void setProperty(String key, float value) {
		setProperty(key, String.valueOf(value));
	}

	public void setProperty(String key, Font value) {
		setProperty(key, Utils.fontToString(value));
	}

	public void setProperty(String key, Object[] values) {
		String str = Utils.arrayToString(values);
		setProperty(key, str);
	}

	public void setProperty(String key, Locale value) {
		setProperty(key, value.toString());
	}

	public void setProperty(String key, Dimension dim) {
		setProperty(key, Utils.arrayToString(new String[] {
				String.valueOf(dim.width), String.valueOf(dim.height) }, ";"));
	}

	public void remove(String key) {
		properties.remove(key);
	}

	public void load() throws IOException {
		File dir = getOrBuildConfigDirectory(new File(configDir), new File(
				OLD_CONFIG_DIR));
		String prop_file_name = dir.getPath() + File.separator + "config";
		FileInputStream fis = new FileInputStream(prop_file_name);
		load(fis);
		fis.close();
	}
	
	public void store() throws IOException {
		String prop_file_name = configDir + File.separator + "config";
		FileOutputStream fos = new FileOutputStream(prop_file_name);
		store(fos);
	}

	public String getConfigDir() {
		return configDir;
	}

	private void load(FileInputStream in) throws IOException {
		BufferedReader reader = new BufferedReader(new InputStreamReader(in,
				"UTF-8"));
		try {
			while (reader.ready()) {
				String line = reader.readLine();
				if (line.startsWith("#")) {
					continue;
				}

				int pos = line.indexOf('=');
				if (pos < 0) {
					continue;
				}

				String key = line.substring(0, pos);
				String value = line.substring(pos + 1, line.length());
				properties.put(key, value);
			}
		} finally {
			reader.close();
		}
	}

	private void store(FileOutputStream out) throws IOException {
		PrintWriter writer = new PrintWriter(new OutputStreamWriter(out,
				"UTF-8"));
		try {
			writer.println("#jVLT property file");
			writer.println("#"
					+ DateFormat.getDateTimeInstance().format(new Date()));
			for (Map.Entry<String, String> e : properties.entrySet()) {
				writer.println(e.getKey() + "=" + e.getValue());
			}
		} finally {
			writer.flush();
			writer.close();
		}
	}

	/**
	 * Returns the folder where to store JVLT config information, creating it if
	 * necessary. If no configuration exists but there is a configuration
	 * defined for an older version, the old configuration will be moved to the
	 * new folder.
	 * 
	 * @param config where to read/store the configuration information
	 * @param oldConfig configuration directory from previous versions
	 * @return the folder to use for reading/storing config information
	 */
	private static File getOrBuildConfigDirectory(File config, File oldConfig) {
		// TODO what do we do if we can't write the config for whatever reason?
		if (config.exists()) {
			if (!config.isDirectory()) {
				logger.info(config.getPath()
						+ " already exists but it is not a directory");
			}
			return config;
		}

		if (oldConfig.exists() && oldConfig.renameTo(config)) {
			logger.info(oldConfig.getPath() + " migrated to "
					+ config.getPath());
			return config;
		}

		if (!config.mkdirs()) {
			logger.info(config.getPath() + " could not be created.");
		}
		return config;
	}

	/**
	 * Determines the folder where to read and store config information. This
	 * method should only be called during initialization, refer to the
	 * {@link #configDir} field afterwards.
	 * 
	 * @return the folder where to read and store config information
	 */
	private static String getConfigPath() {
		String pathSuffix = "jvlt";

		String configOverride = System.getProperty("config");
		if (configOverride != null && new File(configOverride).canWrite()) {
			// a writable config folder was specified
			String configPath = configOverride + File.separator + pathSuffix;
			logger.info("Using config folder: " + configPath);
			return configPath;
		}

		// set path based on OS
		String os = System.getProperty("os.name");
		if (os.toLowerCase(Locale.getDefault()).startsWith("windows")) {
			return System.getenv("APPDATA") + File.separator + pathSuffix;
		}

		if (os.toLowerCase(Locale.getDefault()).startsWith("mac os x")) {
			return System.getProperty("user.home") + File.separator + "Library"
					+ File.separator + "Application Support" + File.separator
					+ pathSuffix;
		}
		String dir = System.getenv("XDG_CONFIG_HOME");
		if (dir == null || dir.equals("")) {
			dir = System.getProperty("user.home") + File.separator + ".config";
		}

		return dir + File.separator + pathSuffix;
	}
}
