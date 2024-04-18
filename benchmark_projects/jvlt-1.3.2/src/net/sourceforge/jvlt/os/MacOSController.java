package net.sourceforge.jvlt.os;

import net.sourceforge.jvlt.ui.JVLTUI;

import com.apple.eawt.Application;
import com.apple.eawt.ApplicationAdapter;
import com.apple.eawt.ApplicationEvent;

public class MacOSController extends Application implements OSController {
	public MacOSController() {
		setEnabledPreferencesMenu(true);
		addApplicationListener(new MacAdapter());
	}

	JVLTUI _mainUI;

	public void setMainView(JVLTUI ui) {
		_mainUI = ui;
	}

	public class MacAdapter extends ApplicationAdapter {
		@Override
		public void handleAbout(ApplicationEvent e) {
			_mainUI.showAbout();
			e.setHandled(true);
		}

		@Override
		public void handleQuit(ApplicationEvent e) {
			// Check to see if user has unsaved changes, if not set
			// e.setHandled(true)
			// If user has unsaved changes set e.setHandled(false) and move into
			// code
			// that handles saving files.
			if (_mainUI.requestQuit()) {
				_mainUI.prepareForQuit();
				e.setHandled(true);
			} else {
				e.setHandled(false);
			}
		}

		@Override
		public void handlePreferences(ApplicationEvent e) {
			_mainUI.showSettings();
			e.setHandled(true);
		}
	}
}
