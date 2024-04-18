package net.sourceforge.jvlt.io;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PipedInputStream;
import java.io.PipedOutputStream;

import net.sourceforge.jvlt.core.Dict;
import net.sourceforge.jvlt.utils.XSLTransformer;

public class DictHtmlWriter extends DictWriter {
	private boolean _add_reverse = false;

	public DictHtmlWriter(Dict dict, OutputStream stream) {
		super(dict, stream);
	}

	public void setAddReverse(boolean add) {
		_add_reverse = add;
	}

	@Override
	public void write() throws IOException {
		final PipedOutputStream pos = new PipedOutputStream();
		final PipedInputStream pis = new PipedInputStream(pos);
		final DictXMLWriter xmlwriter = new DictXMLWriter(_dict, pos,
				DictXMLWriter.FORMAT_XML);
		final XSLTransformer xsltransformer = new XSLTransformer(
				DictHtmlWriter.class
						.getResourceAsStream("/xml/export_html.xsl"));

		Thread xmlthread = new Thread() {
			@Override
			public void run() {
				try {
					xmlwriter.setAddReverse(_add_reverse);
					xmlwriter.write();
					pos.close();
				} catch (IOException ex) {
					ex.printStackTrace();
				}
			}
		};

		Thread xslthread = new Thread() {
			@Override
			public void run() {
				try {
					xsltransformer.transform(pis, _stream);
				} catch (IOException ex) {
					ex.printStackTrace();
				}
			}
		};

		xmlthread.start();
		xslthread.start();
	}
}
