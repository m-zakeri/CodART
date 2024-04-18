package net.sourceforge.jvlt.model;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.LinkedList;

import net.sourceforge.jvlt.JVLT;
import net.sourceforge.jvlt.actions.DictAction;
import net.sourceforge.jvlt.actions.QueryAction;
import net.sourceforge.jvlt.actions.UndoableAction;
import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.event.ModelResetEventListener;
import net.sourceforge.jvlt.event.UndoableActionListener;
import net.sourceforge.jvlt.io.DictReader;
import net.sourceforge.jvlt.io.DictReaderException;
import net.sourceforge.jvlt.io.DictWriter;
import net.sourceforge.jvlt.io.DictXMLWriter;
import net.sourceforge.jvlt.io.SAXDictReader;
import net.sourceforge.jvlt.utils.DetailedException;
import net.sourceforge.jvlt.utils.I18nService;
import net.sourceforge.jvlt.utils.Utils;

import org.apache.log4j.Logger;

public class JVLTModel implements UndoableActionListener,
		ModelResetEventListener {

	private static final Logger logger = Logger.getLogger(JVLTModel.class);

	private Dict _dict;
	private String _dict_file_name;
	private final DictModel _dict_model;
	private final QueryModel _query_model;
	private final LinkedList<UndoableAction> _redoable_actions;
	private final LinkedList<UndoableAction> _undoable_actions;

	public JVLTModel() {
		_dict = null;
		_dict_file_name = null;
		_redoable_actions = new LinkedList<UndoableAction>();
		_undoable_actions = new LinkedList<UndoableAction>();

		// Init the submodels.
		// Note that this class has to be notified about changes
		// of the submodels first because the lists of actions has to
		// be up to date. Therefore, it adds itself to the submodels'
		// action listeners right after the submodels have been initialized.
		_dict_model = new DictModel();
		_dict_model.addUndoableActionListener(this);
		_dict_model.addModelResetEventListener(this);
		_query_model = new QueryModel();
		_query_model.addUndoableActionListener(this);
		_query_model.addModelResetEventListener(this);
	}

	public void newDict() {
		_dict = new Dict();
		_dict_file_name = null;
		_query_model.setDict(_dict);
		// This causes a DictUpdateEvent:
		_dict_model.setDict(_dict);
	}

	/**
	 * Save the current dictionary and the statistics file. This will even be
	 * done if no changes have been made.
	 */
	public void save(String dict_file_name) throws DetailedException {
		if (dict_file_name == null) {
			throw new DetailedException(I18nService.getString("Messages",
					"no_file"));
		}

		String exception_text = I18nService.getString("Messages", "saving_failed");

		File file = new File(dict_file_name);
		String path = file.getParent();
		String file_name = file.getName();

		String backup_file_name = file_name + "~";
		String temp_file_name = "." + file_name + "~";
		if (path != null) {
			backup_file_name = path + "/" + backup_file_name;
			temp_file_name = path + "/" + temp_file_name;
		}

		// The temporary file allows to restore the backup file if the
		// dictionary cannot be saved.
		File temp_file = new File(temp_file_name);
		if (temp_file.exists()) {
			if (!temp_file.delete()) {
				throw new DetailedException(exception_text,
						"Could not delete temporary file" + temp_file_name
								+ ".");
			}
		}

		File backup_file = new File(backup_file_name);
		if (backup_file.exists()) {
			if (!backup_file.renameTo(temp_file)) {
				throw new DetailedException(exception_text, "Could not rename "
						+ backup_file_name + " to " + temp_file_name + ".");
			}
		}

		if (file.exists()) {
			if (!file.renameTo(backup_file)) {
				throw new DetailedException(exception_text, "Could not rename "
						+ dict_file_name + " to " + backup_file_name + ".");
			}
		}

		try {
			file = new File(dict_file_name);
			FileOutputStream fos = new FileOutputStream(file, false);
			DictWriter writer = new DictXMLWriter(_dict, fos);
			writer.write();
			temp_file.delete();
		} catch (IOException ex) {
			temp_file.renameTo(backup_file);
			logger.error("Failed to write dictionary", ex);
			throw new DetailedException(exception_text, "Could not write "
					+ dict_file_name + ".");
		}

		_dict_model.resetActionCounter();
		_query_model.resetActionCounter();
		_dict_file_name = dict_file_name;
	}

	/**
	 * Try to save the dictionary and the statistics file using the current file
	 * name. If no changes have been made then nothing is saved.
	 * 
	 * @see #getDictFileName()
	 */
	public void save() throws DetailedException {
		if (_dict_model.isDataModified() || _query_model.isDataModified()) {
			save(_dict_file_name);
		}
	}

	/**
	 * Load a dictionary from a file. If no error occurs then the file name is
	 * saved. Otherwise, the old file name is kept.
	 * 
	 * @see #getDictFileName()
	 */
	public void load(String dict_file_name, String version)
			throws DictReaderException, IOException {
		if (dict_file_name == null) {
			throw new IOException("No file specified.");
		}

		File file = new File(dict_file_name);
		if (!file.exists()) {
			throw new IOException("File " + dict_file_name + " does not exist.");
		}

		DictReader reader = new SAXDictReader(version);
		FileInputStream in = new FileInputStream(file);
		try {
			reader.read(in);
			_dict = reader.getDict();
			_dict_file_name = dict_file_name;
	
			_query_model.setDict(_dict);
			// This causes a DictUpdateEvent:
			_dict_model.setDict(_dict);
		} finally {
			in.close();
		}
	}

	public void load(String dict_file_name) throws DictReaderException,
			IOException {
		this.load(dict_file_name, JVLT.getDataVersion());
	}

	public String getDictFileName() {
		return _dict_file_name;
	}

	public void setDictFileName(String dict_file_name) {
		_dict_file_name = dict_file_name;
	}

	public Dict getDict() {
		return _dict;
	}

	public DictModel getDictModel() {
		return _dict_model;
	}

	public QueryModel getQueryModel() {
		return _query_model;
	}

	public void actionPerformed(UndoableActionEvent event) {
		if (event.getType() == UndoableActionEvent.UNDO_TYPE) {
			_redoable_actions.addFirst(event.getAction());
			_undoable_actions.removeFirst();
		} else if (event.getType() == UndoableActionEvent.REDO_TYPE) {
			_undoable_actions.addFirst(event.getAction());
			_redoable_actions.removeFirst();
		} else if (event.getType() == UndoableActionEvent.EXEC_TYPE) {
			_redoable_actions.clear();
			_undoable_actions.addFirst(event.getAction());
		}
	}

	public void modelResetted(ModelResetEvent event) {
		if (event.getSource() == _dict_model
				&& event.getType() == ModelResetEvent.RESET_ALL) {
			Utils.removeClassInstances(_redoable_actions, DictAction.class);
			Utils.removeClassInstances(_undoable_actions, DictAction.class);
		} else if (event.getSource() == _query_model
				&& event.getType() == ModelResetEvent.RESET_ALL) {
			Utils.removeClassInstances(_redoable_actions, QueryAction.class);
			Utils.removeClassInstances(_undoable_actions, QueryAction.class);
		}
	}

	public int getNumUndoableActions() {
		return _undoable_actions.size();
	}

	public UndoableAction getFirstUndoableAction() {
		return _undoable_actions.getFirst();
	}

	public int getNumRedoableActions() {
		return _redoable_actions.size();
	}

	public UndoableAction getFirstRedoableAction() {
		return _redoable_actions.getFirst();
	}

	public boolean isDataModified() {
		return _dict_model.isDataModified() || _query_model.isDataModified();
	}

	public void undo() throws ModelException {
		UndoableAction action = _undoable_actions.getFirst();
		if (action instanceof DictAction) {
			_dict_model.undo();
		} else if (action instanceof QueryAction) {
			_query_model.undo();
		}
	}

	public void redo() throws ModelException {
		UndoableAction action = _redoable_actions.getFirst();
		if (action instanceof DictAction) {
			_dict_model.redo();
		} else if (action instanceof QueryAction) {
			_query_model.redo();
		}
	}
}
