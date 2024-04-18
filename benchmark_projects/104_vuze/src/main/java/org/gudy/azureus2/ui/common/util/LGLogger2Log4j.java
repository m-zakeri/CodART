/*
 * Created on 10.11.2003
 *
 * To change the template for this generated file go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
package org.gudy.azureus2.ui.common.util;

import org.apache.log4j.Logger;
import org.gudy.azureus2.core3.logging.ILogAlertListener;
import org.gudy.azureus2.core3.logging.ILogEventListener;
import org.gudy.azureus2.core3.logging.LogAlert;
import org.gudy.azureus2.core3.logging.LogEvent;

/**
 * @author tobi
 *
 * To change the template for this generated type comment go to
 * Window>Preferences>Java>Code Generation>Code and Comments
 */
public class LGLogger2Log4j implements ILogEventListener {

	public static Logger core = Logger.getLogger("azureus2.core");

	private static LGLogger2Log4j inst = null;

	public static LGLogger2Log4j getInstance() {
		if (inst == null)
			inst = new LGLogger2Log4j();
		return inst;
	}

	public static void set() {
		org.gudy.azureus2.core3.logging.Logger.addListener(getInstance());
	}

	public void log(LogEvent event) {
		if (event.entryType == LogEvent.LT_ERROR)
			core.error(event.text);
		else if (event.entryType == LogEvent.LT_WARNING)
			core.log(SLevel.CORE_WARNING, event.text);
		else
			core.log(SLevel.CORE_INFO, event.text);
	}
}
