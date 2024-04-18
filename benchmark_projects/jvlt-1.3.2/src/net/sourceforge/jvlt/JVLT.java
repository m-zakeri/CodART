package net.sourceforge.jvlt;

import java.io.IOException;
import java.io.InputStream;
import java.util.Locale;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import net.sourceforge.jvlt.utils.Config;
import net.sourceforge.jvlt.utils.PropertyMap;

import org.apache.log4j.Logger;
import org.w3c.dom.Node;
import org.xml.sax.InputSource;

public class JVLT {
	private static final Logger logger = Logger.getLogger(JVLT.class);

	private static final Locale[] _locales = {
		Locale.US,
		Locale.FRANCE,
		Locale.GERMANY,
		new Locale("cs", "CZ"),
		new Locale("pl", "PL"),
		new Locale("pt", "BR")
	};

	private PropertyMap _runtime_properties;
	private Config _config = null;

	private String _version = null;
	private String _data_version = null;

	private static JVLT _instance = null;
	
	public static JVLT getInstance() {
		return _instance;
	}

	public static Config getConfig() {
		return _instance._config;
	}

	public static Locale[] getSupportedLocales() {
		return _locales;
	}

	/**
	 * Returns a map that contains a set of properties. Unlike the properties
	 * stored in the Config object returned by method getConfig(), this map is
	 * not stored in a config file.
	 */
	public static PropertyMap getRuntimeProperties() {
		return _instance._runtime_properties;
	}

	public static String getVersion() {
		return _instance._version;
	}

	public static String getDataVersion() {
		return _instance._data_version;
	}

	public static void init(Config config) {
		_instance = new JVLT();
		
		// ----------
		// Read version info
		// ----------
		InputStream xml_stream = JVLT.class
				.getResourceAsStream("/xml/info.xml");
		InputSource src = new InputSource(xml_stream);
		XPathFactory fac = XPathFactory.newInstance();
		XPath path = fac.newXPath();
		try {
			Node root = (Node) path.evaluate("/info", src, XPathConstants.NODE);
			_instance._version = path.evaluate("version", root);
			_instance._data_version = path.evaluate("data-version", root);
		} catch (XPathExpressionException ex) {
			logger.error(ex);
		}

		// ----------
		// Read settings.
		// ----------
		_instance._config = config;
		try {
			config.load();
		} catch (IOException e) {
			logger.error(e.getMessage());
		}
	}

	private JVLT() {
		_config = null;
		_runtime_properties = new PropertyMap();
	}
}
