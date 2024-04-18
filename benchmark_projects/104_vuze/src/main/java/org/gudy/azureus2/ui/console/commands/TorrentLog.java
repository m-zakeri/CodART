/**
 * 
 */
package org.gudy.azureus2.ui.console.commands;

import java.text.FieldPosition;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Vector;

import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.core3.global.GlobalManagerAdapter;
import org.gudy.azureus2.core3.logging.ILogEventListener;
import org.gudy.azureus2.core3.logging.LogEvent;
import org.gudy.azureus2.core3.logging.LogRelation;
import org.gudy.azureus2.core3.logging.Logger;
import org.gudy.azureus2.core3.util.AEMonitor;
import org.gudy.azureus2.ui.console.ConsoleInput;

import com.aelitis.azureus.core.AzureusCoreFactory;

/**
 * @author TuxPaper
 * @created Dec 21, 2006
 *
 */
public class TorrentLog extends TorrentCommand implements ILogEventListener
{
	private static int MODE_OFF = 0;
	private static int MODE_ON = 1;
	private static int MODE_FLIP = 2;
	
	private static SimpleDateFormat dateFormatter;

	private static FieldPosition formatPos;

	private int mode = 0;

	private AEMonitor dms_mon = new AEMonitor("TorrentLog");

	private ArrayList dms = new ArrayList();

	private boolean	gm_listener_added;
	
	static {
		dateFormatter = new SimpleDateFormat("[h:mm:ss.SSS] ");
		formatPos = new FieldPosition(0);
	}

	/**
	 * @param commandNames
	 * @param action
	 */
	public TorrentLog() {
		super("tlog", "tl", "Torrent Logging");
	}

	public void execute(String commandName, ConsoleInput ci, List args) {
		mode = MODE_ON;
		Vector newargs = new Vector(args);
		if (newargs.isEmpty()) {
			mode = MODE_FLIP;
		} else if (newargs.contains("off")) {
			newargs.removeElement("off");
			mode = MODE_OFF;
		} else if (!newargs.contains("on")) {
			mode = MODE_FLIP;
		} 
		super.execute(commandName, ci, args);
	}

	protected boolean performCommand(ConsoleInput ci, DownloadManager dm,
			List args) {
		try {
			dms_mon.enter();
			
				// defer this so that a non-running core doesn't prevent console ui init
			
			if ( !gm_listener_added ){
				
				gm_listener_added = true;
				
				GlobalManager gm = AzureusCoreFactory.getSingleton().getGlobalManager();
				gm.addListener(new GlobalManagerAdapter() {
					public void downloadManagerRemoved(DownloadManager dm) {
						dms.remove(dm);
					}
				}, false);
			}
			
			boolean turnOn;
			if (mode == MODE_FLIP) {
				turnOn = !dms.contains(dm);
			} else {
				turnOn = mode == MODE_ON;
			}

			if (turnOn) {
				ci.out.print("->on] ");
				if (dms.contains(dm)) {
					return true;
				}
				dms.add(dm);
				if (dms.size() == 1) {
					Logger.addListener(this);
				}
			} else {
				ci.out.print("->off] ");
				dms.remove(dm);
				if (dms.size() == 0) {
					Logger.removeListener(this);
				}
			}
		} catch (Exception e) {
			e.printStackTrace(ci.out);
			return false;
		} finally {
			dms_mon.exit();
		}
		return true;
	}

	public String getCommandDescriptions() {
		return "tl [on|off]\tTorrentLogging";
	}

	public void log(LogEvent event) {
		boolean bMatch = false;

		if (event.relatedTo == null) {
			return;
		}

		try {
			dms_mon.enter();

			for (int i = 0; !bMatch && i < event.relatedTo.length; i++) {
				Object obj = event.relatedTo[i];

				if (obj == null)
					continue;

				for (int j = 0; !bMatch && j < dms.size(); j++) {
					if (obj instanceof LogRelation) {
						//System.err.println(obj.getClass().getSimpleName() + " is Logrelation");

						Object newObj = ((LogRelation) obj).queryForClass(DownloadManager.class);
						if (newObj != null)
							obj = newObj;
					}

					//System.err.println(obj.getClass().getName() + " matches " + filter[j].getClass().getSimpleName() + "?");

					if (obj == dms.get(j))
						bMatch = true;
				} // for filter
			} // for relatedTo

		} finally {
			dms_mon.exit();
		}

		if (bMatch) {
			final StringBuffer buf = new StringBuffer();
			dateFormatter.format(event.timeStamp, buf, formatPos);
			buf.append("{").append(event.logID).append("} ");

			buf.append(event.text);
			if (event.relatedTo != null) {
				buf.append("; \t| ");
				for (int j = 0; j < event.relatedTo.length; j++) {
					Object obj = event.relatedTo[j];
					if (j > 0)
						buf.append("; ");
					if (obj instanceof LogRelation) {
						buf.append(((LogRelation) obj).getRelationText());
					} else if (obj != null) {
						buf.append(obj.getClass().getName()).append(": '").append(
								obj.toString()).append("'");
					}
				}
			}
			System.out.println(buf.toString());
		}
	}

}
