package net.sourceforge.jvlt.tools;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.core.Entry;
import net.sourceforge.jvlt.core.Example;
import net.sourceforge.jvlt.core.Sense;
import net.sourceforge.jvlt.core.Example.TextFragment;
import net.sourceforge.jvlt.io.DictReaderException;
import net.sourceforge.jvlt.metadata.MetaData;
import net.sourceforge.jvlt.model.JVLTModel;
import net.sourceforge.jvlt.ui.JVLTUI;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

public class JVLTUtils {

	private static final Logger logger = Logger.getLogger(JVLTUtils.class);

	private final JVLTModel _model;
	private String _current_file;
	private Dict _dict;

	public JVLTUtils() {
		_model = JVLTUI.getModel();
		_current_file = "";
		_dict = null;
	}

	public void print(String file_name, String field) {
		try {
			open(file_name);
			HashMap<String, TreeSet<Entry>> entry_map = new HashMap<String, TreeSet<Entry>>();
			TreeSet<String> value_set = new TreeSet<String>();
			MetaData data = _model.getDictModel().getMetaData(Entry.class);
			for (Entry entry : _dict.getEntries()) {
				String value = data.getAttribute(field)
						.getFormattedValue(entry);
				if (value_set.add(value)) {
					entry_map.put(value, new TreeSet<Entry>());
				}

				Set<Entry> set = entry_map.get(value);
				set.add(entry);
			}

			Writer writer = new BufferedWriter(new OutputStreamWriter(
					System.out, "UTF-8"));
			writer.write("<html>\n");
			Iterator<String> it = value_set.iterator();
			int i = 0;
			char last_first_char = 0;
			while (it.hasNext()) {
				String value = it.next();
				char first_char = value.length() == 0 ? 0 : value.charAt(0);
				Set<Entry> set = entry_map.get(value);
				Iterator<Entry> it2 = set.iterator();
				while (it2.hasNext()) {
					if (i > 0) {
						writer.write(", ");
					}

					if (first_char != 0 && first_char != last_first_char) {
						writer.write("<b>" + Character.toUpperCase(first_char)
								+ "</b> ");
						last_first_char = first_char;
					}

					Entry entry = it2.next();
					writer.write(entry.getOrthography());
					i++;
				}
			}
			writer.write("</html>\n");
			writer.flush();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public void findDuplicates(String file_name) {
		try {
			open(file_name);
			Writer writer = new BufferedWriter(new OutputStreamWriter(
					System.out, "UTF-8"));
			Set<String> set = new TreeSet<String>();
			for (Entry entry : _dict.getEntries()) {
				String orth = entry.getOrthography();
				if (!set.add(orth)) {
					writer.write("Duplicate: " + orth + "\n");
				}
			}

			writer.flush();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public void exampleLinkCount(String file_name) {
		try {
			open(file_name);
			Writer writer = new BufferedWriter(new OutputStreamWriter(
					System.out, "UTF-8"));
			for (Example ex : _dict.getExamples()) {
				Sense[] senses = ex.getSenses();
				writer.write(ex.getText() + ": " + senses.length + " link(s)");

				Example.TextFragment[] fragments = ex.getTextFragments();
				TreeSet<Sense> set = new TreeSet<Sense>();
				for (TextFragment fragment : fragments) {
					Sense s = fragment.getSense();
					if (s != null) {
						if (!set.add(s)) {
							writer.write(", duplicate link: " + s.getParent());
						}
					}
				}

				writer.write("\n");
			}

			writer.flush();
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}

	public void importStats(String target, String source) {
		try {
			open(target);
			JVLTModel statsModel = new JVLTModel();
			Dict statsDict = open(source, statsModel);
			for (Entry e : _dict.getEntries()) {
				Entry statsEntry = statsDict.getEntry(e);
				if (statsEntry != null) {
					e.setStats(statsEntry.getStats());
				}
			}
			_model.save(_current_file);
		} catch (DictReaderException e) {
			logger.error(e.getShortMessage() + "(" + e.getLongMessage() + ")");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void open(String file_name) throws DictReaderException, IOException {
		if (file_name.equals(_current_file)) {
			return;
		}

		_dict = open(file_name, _model);
		_current_file = file_name;
	}

	private Dict open(String file_name, JVLTModel model)
			throws DictReaderException, IOException {
		model.load(file_name);
		return model.getDict();
	}

	public static void main(String[] args) {
		PropertyConfigurator.configure(JVLTUI.class
				.getResource("/log4j.properties"));

		if (args.length < 2) {
			printHelp();
			return;
		}

		String file = args[args.length - 1];
		List<String> arg_set = new ArrayList<String>();
		for (String arg : args) {
			arg_set.add(arg);
		}

		JVLTUtils utils = new JVLTUtils();
		if (arg_set.contains("--find-duplicates")) {
			utils.findDuplicates(file);
		} else if (arg_set.contains("--example-link-count")) {
			utils.exampleLinkCount(file);
		} else if (arg_set.contains("--print-words")) {
			Iterator<String> it = arg_set.iterator();
			String field = "Orthography";
			while (it.hasNext()) {
				String arg = it.next();
				if (arg.startsWith("--sort-by=")) {
					if (arg.endsWith("Pronunciations")) {
						field = "Pronunciations";
						break;
					}
				}
			}
			utils.print(file, field);
		} else if (arg_set.contains("--import-stats")) {
			int index = arg_set.indexOf("--import-stats");
			if (index >= 0) {
				utils.importStats(file, arg_set.get(index + 1));
			}
		} else {
			printHelp();
		}
	}

	private static void printHelp() {
		logger.info("Usage: JVLTUtils <options> <file>");
		logger.info("Possible options:");
		logger.info("--print-words");
		logger.info("--find-duplicates");
		logger.info("--example-link-count");
		logger.info("--sort-by=<field>"
				+ "  Can be used together with --print-words. <field> is "
				+ "  either \"Orthography\" or \"Pronunciations\"");
		logger.info("--import-stats <file>");
	}
}
