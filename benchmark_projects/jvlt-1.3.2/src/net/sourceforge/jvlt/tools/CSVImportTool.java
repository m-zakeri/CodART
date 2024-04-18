package net.sourceforge.jvlt.tools;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Properties;

import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.io.CSVDictReader;
import net.sourceforge.jvlt.io.DictReaderException;
import net.sourceforge.jvlt.io.DictXMLWriter;
import net.sourceforge.jvlt.ui.JVLTUI;
import net.sourceforge.jvlt.utils.Utils;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

public class CSVImportTool {
	private static final Logger logger = Logger.getLogger(CSVImportTool.class);
	private final CSVDictReader _reader;

	public CSVImportTool(Properties props) {
		String language = props.getProperty("language");
		boolean ignore_first_line = Boolean.valueOf(
				props.getProperty("ignore_first_line", "false")).booleanValue();
		int num_senses = Integer.parseInt(props.getProperty("senses", "1"));
		int num_categories = Integer.parseInt(props.getProperty("categories",
				"1"));
		int num_mmfiles = Integer.parseInt(props.getProperty(
				"multimedia_files", "0"));
		int num_examples = Integer.parseInt(props.getProperty("examples", "0"));
		String[] attrs = Utils.split(props.getProperty("attributes", ""), ",");
		String[] attr_columns = Utils.split(props.getProperty(
				"attribute_columns", ""), ",");
		int[] columns = new int[attrs.length];
		for (int i = 0; i < columns.length; i++) {
			if (i >= attr_columns.length) {
				columns[i] = 1;
			} else {
				columns[i] = Integer.parseInt(attr_columns[i]);
			}
		}

		_reader = new CSVDictReader();
		_reader.setLanguage(language);
		_reader.setIgnoreFirstLine(ignore_first_line);
		_reader.setNumSenses(num_senses);
		_reader.setNumCategories(num_categories);
		_reader.setNumMultimediaFiles(num_mmfiles);
		_reader.setNumExamples(num_examples);
		_reader.setAttributes(attrs);
		_reader.setAttributeColumns(columns);
	}

	public Dict readDict(String filename) throws DictReaderException,
			IOException {
		FileInputStream in = new FileInputStream(filename);
		try {
			_reader.read(in);
			return _reader.getDict();
		} finally {
			in.close();
		}
	}

	public void writeDict(Dict dict, String filename) throws IOException {
		DictXMLWriter writer = new DictXMLWriter(dict, new FileOutputStream(
				filename));
		writer.write();
	}

	public static void main(String[] args) {
		PropertyConfigurator.configure(JVLTUI.class
				.getResource("/log4j.properties"));

		if (args.length != 3) {
			return;
		}

		try {
			Properties props = new Properties();
			props.load(new FileInputStream(args[0]));
			CSVImportTool tool = new CSVImportTool(props);
			Dict dict = tool.readDict(args[1]);
			tool.writeDict(dict, args[2]);
		} catch (IOException e) {
			logger.error("Could not read file", e);
		} catch (DictReaderException e) {
			logger.error("Importing failed. Reason:");
			logger.error(e.getShortMessage());
			logger.error(e.getLongMessage());
			logger.error(e);
			System.exit(1);
		}
	}
}
