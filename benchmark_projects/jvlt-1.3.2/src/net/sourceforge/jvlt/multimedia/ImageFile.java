package net.sourceforge.jvlt.multimedia;

import java.awt.Frame;
import java.io.File;
import java.io.IOException;

import javax.swing.ImageIcon;
import javax.swing.JDialog;
import javax.swing.JLabel;

import net.sourceforge.jvlt.ui.utils.GUIUtils;
import net.sourceforge.jvlt.utils.I18nService;

/**
 * This class represents an image file that can be viewed with jVLT. Other image
 * files are represented by CustomMultimediaFile.
 */
public class ImageFile extends MultimediaFile {
	public ImageFile(String file_name) {
		super(file_name, IMAGE_FILE);
	}

	public ImageFile() {
		this("");
	}

	public void show(Frame parent) throws IOException {
		File f = getFile();
		if (!f.exists() || !f.isFile()) {
			String msg = "File " + f.getAbsolutePath() + " does not exist "
					+ "or cannot be opened.";
			throw new IOException(msg);
		}

		ImageIcon icon = new ImageIcon(f.getAbsolutePath());
		JDialog dlg = new JDialog(parent,
				I18nService.getString("Labels", "image"), false);
		JLabel lbl = new JLabel(icon);
		dlg.setContentPane(lbl);
		GUIUtils.showDialog(parent, dlg);
	}
}
