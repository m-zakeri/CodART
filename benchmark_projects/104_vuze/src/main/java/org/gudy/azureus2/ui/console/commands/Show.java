/*
 * Written and copyright 2001-2003 Tobias Minich. Distributed under the GNU
 * General Public License; see the README file. This code comes with NO
 * WARRANTY.
 * 
 * Show.java
 * 
 * Created on 23.03.2004
 *
 */
package org.gudy.azureus2.ui.console.commands;

import java.io.FileWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.gudy.azureus2.core3.disk.DiskManagerFileInfo;
import org.gudy.azureus2.core3.download.DownloadManager;
import org.gudy.azureus2.core3.download.DownloadManagerStats;
import org.gudy.azureus2.core3.global.GlobalManager;
import org.gudy.azureus2.core3.internat.MessageText;
import org.gudy.azureus2.core3.peer.PEPeerManager;
import org.gudy.azureus2.core3.peer.PEPeerManagerStats;
import org.gudy.azureus2.core3.peer.PEPiece;
import org.gudy.azureus2.core3.tracker.client.TRTrackerAnnouncer;
import org.gudy.azureus2.core3.tracker.client.TRTrackerScraperResponse;
import org.gudy.azureus2.core3.util.AEDiagnostics;
import org.gudy.azureus2.core3.util.DisplayFormatters;
import org.gudy.azureus2.core3.util.IndentWriter;
import org.gudy.azureus2.core3.util.TorrentUtils;
import org.gudy.azureus2.plugins.PluginInterface;
import org.gudy.azureus2.ui.console.ConsoleInput;

import com.aelitis.azureus.core.dht.DHT;
import com.aelitis.azureus.core.dht.control.DHTControlStats;
import com.aelitis.azureus.core.dht.db.DHTDBStats;
import com.aelitis.azureus.core.dht.netcoords.DHTNetworkPosition;
import com.aelitis.azureus.core.dht.router.DHTRouterStats;
import com.aelitis.azureus.core.dht.transport.*;
import com.aelitis.azureus.core.networkmanager.admin.NetworkAdmin;
import com.aelitis.azureus.core.peermanager.piecepicker.PiecePicker;
import com.aelitis.azureus.core.stats.AzureusCoreStats;
import com.aelitis.azureus.plugins.dht.DHTPlugin;

/**
 * @author Tobias Minich
 */
public class Show extends IConsoleCommand {
	
	private static final class TorrentComparator implements Comparator {
		public final int compare(Object a, Object b) {
			DownloadManager aDL = (DownloadManager) a;
			DownloadManager bDL = (DownloadManager) b;
			boolean aIsComplete = aDL.getStats().getDownloadCompleted(false) == 1000;
			boolean bIsComplete = bDL.getStats().getDownloadCompleted(false) == 1000;
			if (aIsComplete && !bIsComplete)
				return 1;
			if (!aIsComplete && bIsComplete)
				return -1;
			return aDL.getPosition() - bDL.getPosition();
		}
	}

	public Show()
	{
		super("show", "sh");
	}

	public String getCommandDescriptions() {
		return("show [<various options>]\tsh\tShow info. Use without parameter to get a list of available options.");
	}

	public void printHelpExtra(PrintStream out, List args) {
		out.println("> -----");
		out.println("'show' options: ");
		out.println("<#>\t\t\t\tFurther info on a single torrent. Run 'show torrents' first for the number.");
		out.println("options\t\t\to\tShow list of options for 'set' (also available by 'set' without parameters).");
		out.println("files\t\t\tf\tShow list of files found from the 'add -f' command (also available by 'add -l')");
		out.println("dht\t\t\td\tShow distributed database statistics");
		out.println("nat\t\t\tn\tShow NAT status");
		out.println("stats [pattern] [on|off]\ts\tShow stats [with a given pattern] [turn averages on/off]");
		out.println("torrents [opts] [expr]\tt\tShow list of torrents. torrent options may be any (or none) of:");
		out.println("\t\ttransferring\tx\tShow only transferring torrents.");
		out.println("\t\tactive\t\ta\tShow only active torrents.");
		out.println("\t\tcomplete\tc\tShow only complete torrents.");
		out.println("\t\tincomplete\ti\tShow only incomplete torrents.");
		out.println("\te.g. show t a *Az* - shows all active torrents with 'Az' occurring in their name." );
		out.println("> -----");
	}

	public void execute(String commandName, ConsoleInput ci, List args) {
		if( args.isEmpty() )
		{
			printHelp(ci.out, args);
			return;
		}
		String subCommand = (String) args.remove(0);
		if (subCommand.equalsIgnoreCase("options") || subCommand.equalsIgnoreCase("o")) {
			ci.invokeCommand("set", null);
		} else if(subCommand.equalsIgnoreCase("files") || subCommand.equalsIgnoreCase("f")) {
			ci.invokeCommand("add", Arrays.asList( new String[] { "--list"} ));
		} else if (subCommand.equalsIgnoreCase("torrents") || subCommand.equalsIgnoreCase("t")) {
			ci.out.println("> -----");
			ci.torrents.clear();
			ci.torrents.addAll(ci.getGlobalManager().getDownloadManagers());
			Collections.sort(ci.torrents, new TorrentComparator());

			if (ci.torrents.isEmpty()) {
				ci.out.println("No Torrents");
				ci.out.println("> -----");
				return;
			}
			
			long totalReceived = 0;
			long totalSent = 0;
			long totalDiscarded = 0;
			int connectedSeeds = 0;
			int connectedPeers = 0;
			PEPeerManagerStats ps;
			boolean bShowOnlyActive = false;
			boolean bShowOnlyComplete = false;
			boolean bShowOnlyIncomplete = false;
			boolean bShowOnlyTransferring = false;
			for (Iterator iter = args.iterator(); iter.hasNext();) {
				String arg = (String) iter.next();
				if ("active".equalsIgnoreCase(arg) || "a".equalsIgnoreCase(arg)) {
					bShowOnlyActive = true;
					iter.remove();
				} else if ("complete".equalsIgnoreCase(arg) || "c".equalsIgnoreCase(arg)) {
					bShowOnlyComplete = true;
					iter.remove();
				} else if ("incomplete".equalsIgnoreCase(arg) || "i".equalsIgnoreCase(arg)) {
					bShowOnlyIncomplete = true;
					iter.remove();
				} else if ("transferring".equalsIgnoreCase(arg) || "x".equalsIgnoreCase(arg)) {
					bShowOnlyTransferring = true;
					bShowOnlyActive = true;
					iter.remove();
				}
				
			}
			
			Iterator torrent;
			if( args.size() > 0 )
			{
				List matchedTorrents = new TorrentFilter().getTorrents(ci.torrents, args);
				torrent = matchedTorrents.iterator();
			}
			else
				torrent = ci.torrents.iterator();
			
			List shown_torrents = new ArrayList();

			while (torrent.hasNext()) {
								
				DownloadManager dm = (DownloadManager) torrent.next();
								
				DownloadManagerStats stats = dm.getStats();

				boolean bDownloadCompleted = stats.getDownloadCompleted(false) == 1000;
				boolean bCanShow = ((bShowOnlyComplete == bShowOnlyIncomplete) || (bDownloadCompleted && bShowOnlyComplete) || (!bDownloadCompleted && bShowOnlyIncomplete));

				if (bCanShow && bShowOnlyActive) {
					int dmstate = dm.getState();
					bCanShow = (dmstate == DownloadManager.STATE_SEEDING) || (dmstate == DownloadManager.STATE_DOWNLOADING) || (dmstate == DownloadManager.STATE_CHECKING) || (dmstate == DownloadManager.STATE_INITIALIZING) || (dmstate == DownloadManager.STATE_ALLOCATING);
				}
				
				if (bCanShow && bShowOnlyTransferring) {
					try {
						ps = dm.getPeerManager().getStats();
						bCanShow = ps.getDataSendRate() > 0 || ps.getDataReceiveRate() > 0;
					}
					catch (Exception e) {}
				}

				if (bCanShow) {
					
					shown_torrents.add( dm );

					try {
						ps = dm.getPeerManager().getStats();
					} catch (Exception e) {
						ps = null;
					}
					if (ps != null) {
						totalReceived += dm.getStats().getTotalDataBytesReceived();
						totalSent += dm.getStats().getTotalDataBytesSent();
						totalDiscarded += ps.getTotalDiscarded();
						connectedSeeds += dm.getNbSeeds();
						connectedPeers += dm.getNbPeers();
					}				
					ci.out.print(((shown_torrents.size() < 10) ? " " : "") + shown_torrents.size() + " ");
					ci.out.println(getTorrentSummary(dm));
					ci.out.println();
				}
			}
			
			ci.torrents.clear();
			ci.torrents.addAll( shown_torrents );
			
			GlobalManager	gm = ci.getGlobalManager();
			
			ci.out.println("Total Speed (down/up): " + DisplayFormatters.formatByteCountToKiBEtcPerSec(gm.getStats().getDataReceiveRate() + gm.getStats().getProtocolReceiveRate() ) + " / " + DisplayFormatters.formatByteCountToKiBEtcPerSec(gm.getStats().getDataSendRate() + gm.getStats().getProtocolSendRate() ));

			ci.out.println("Transferred Volume (down/up/discarded): " + DisplayFormatters.formatByteCountToKiBEtc(totalReceived) + " / " + DisplayFormatters.formatByteCountToKiBEtc(totalSent) + " / " + DisplayFormatters.formatByteCountToKiBEtc(totalDiscarded));
			ci.out.println("Total Connected Peers (seeds/peers): " + Integer.toString(connectedSeeds) + " / " + Integer.toString(connectedPeers));
			ci.out.println("> -----");
		} else if (subCommand.equalsIgnoreCase("dht") || subCommand.equalsIgnoreCase("d")) {

			showDHTStats( ci );
		
		} else if (subCommand.equalsIgnoreCase("nat") || subCommand.equalsIgnoreCase("n")) {

			IndentWriter	iw = new IndentWriter( new PrintWriter( ci.out ));
			
			iw.setForce( true );
			
			NetworkAdmin.getSingleton().logNATStatus( iw );
		
		} else if (subCommand.equalsIgnoreCase("stats") || subCommand.equalsIgnoreCase("s")) {

			String	pattern = AzureusCoreStats.ST_ALL;
			
			if( args.size() > 0 ){
				
				pattern = (String)args.get(0);
				
				if ( pattern.equals("*")){
					
					pattern = ".*";
				}
			}
		
			if ( args.size() > 1 ){
				
				AzureusCoreStats.setEnableAverages(((String)args.get(1)).equalsIgnoreCase( "on" ));
			}
			
			java.util.Set	types = new HashSet();
			
			types.add( pattern );
			
			Map	reply = AzureusCoreStats.getStats( types );
			
			Iterator	it = reply.entrySet().iterator();
			
			List	lines = new ArrayList();
			
			while( it.hasNext()){
				
				Map.Entry	entry = (Map.Entry)it.next();
				
				lines.add( entry.getKey() + " -> " + entry.getValue());
			}
			
			Collections.sort( lines );
			
			for ( int i=0;i<lines.size();i++){
				
				ci.out.println( lines.get(i));
			}
		} else if (subCommand.equalsIgnoreCase("diag") || subCommand.equalsIgnoreCase("z")) {

			try{
				ci.out.println( "Writing diagnostics to file 'az.diag'" );
				
				FileWriter	fw = new FileWriter( "az.diag" );
				
				PrintWriter	pw = new PrintWriter( fw );
				
				AEDiagnostics.generateEvidence( pw );
				
				pw.flush();
				
				fw.close();
			
			}catch( Throwable e ){
				
				ci.out.println( e );
			}
			
		} else {
			if ((ci.torrents == null) || (ci.torrents != null) && ci.torrents.isEmpty()) {
				ci.out.println("> Command 'show': No torrents in list (try 'show torrents' first).");
				return;
			}
			try {
				int number = Integer.parseInt(subCommand);
				if ((number == 0) || (number > ci.torrents.size())) {
					ci.out.println("> Command 'show': Torrent #" + number + " unknown.");
					return;
				}
				DownloadManager dm = (DownloadManager) ci.torrents.get(number - 1);
				printTorrentDetails(ci.out, dm, number, args.size() > 0  );
			}
			catch (Exception e) {
				ci.out.println("> Command 'show': Subcommand '" + subCommand + "' unknown.");
				return;
			}				
		} 
	}

	/**
	 * returns the summary details for the specified torrent. - we do this by obtaining
	 * the summary format and then performing variable substitution 
	 * NOTE: we currently reprocess
	 * the summary format string each time however we could pre-parse this once.. its 
	 * probably not that important though.
	 * @return
	 */
	protected String getTorrentSummary(DownloadManager dm) {
		StringBuffer tstate = new StringBuffer();
		String summaryFormat = getDefaultSummaryFormat();
		char lastch = '0';
		char []summaryChars = summaryFormat.toCharArray();
		for (int i = 0; i < summaryChars.length; i++) {
			char ch = summaryChars[i];
			if( ch == '%' && lastch != '\\' )
			{
				i++;
				if( i >= summaryChars.length )
					tstate.append('%');
				else
					tstate.append(expandVariable(summaryChars[i], dm));
			}
			else
				tstate.append(ch);
			
			lastch = ch;			
		}
		return tstate.toString();
	}

	/**
	 * expands the specified variable character into a string. <br>currently available
	 * variables that can be expanded are:<br>
	 * <hr>
	 * %a for state<br>
	 * %c percentage complete<br>
	 * %t torrent details - error message if error, otherwise torrent name<br>
	 * %z size<br>
	 * %e ETA<br>
	 * %r progress, if we have disabled some files<br>
	 * %d download speed<br>
	 * %u upload speed<br>
	 * %D amount downloaded<br>
	 * %U amount uploaded<br>
	 * %v upload slots
	 * %s connected seeds<br>
	 * %p connected peers<br>
	 * %S tracker seeds<br>
	 * %P tracker peers<br>
	 * @param variable variable character, eg: 'e' for ETA
	 * @param dm download manager object
	 * @return string expansion of the variable
	 */
	protected String expandVariable( char variable, DownloadManager dm )
	{
		switch( variable )
		{
			case 'a':
				return getShortStateString(dm.getState());
			case 'c':
				DecimalFormat df = new DecimalFormat("000.0%");
				return df.format(dm.getStats().getCompleted() / 1000.0);
			case 't':
				if (dm.getState() == DownloadManager.STATE_ERROR)
					return dm.getErrorDetails();
				else {
					if (dm.getDisplayName() == null)
						return "?";
					else
						return dm.getDisplayName();
				}
			case 'z':
				return DisplayFormatters.formatByteCountToKiBEtc(dm.getSize());
			case 'e':
				return DisplayFormatters.formatETA(dm.getStats().getETA());
			case 'r':
				long to = 0;
				long tot = 0;
				if (dm.getDiskManager() != null) {
					DiskManagerFileInfo files[] = dm.getDiskManager().getFiles();
					if (files != null) {
						if (files.length>1) { 
							int c=0;
							for (int i = 0; i < files.length; i++) {
								if (files[i] != null) {
									if (!files[i].isSkipped()) {
										c += 1;
										tot += files[i].getLength();
										to += files[i].getDownloaded();
									}
								}
							}
							if (c == files.length)
								tot = 0;
						}
					}
				}
				DecimalFormat df1 = new DecimalFormat("000.0%");
				if (tot > 0) {
					return "      ("+df1.format(to * 1.0 / tot)+")";
				} else
					return "\t";
			case 'd':
				return DisplayFormatters.formatByteCountToKiBEtcPerSec(dm.getStats().getDataReceiveRate());
			case 'u':
				return DisplayFormatters.formatByteCountToKiBEtcPerSec(dm.getStats().getDataSendRate());
			case 'D':
				return DisplayFormatters.formatDownloaded(dm.getStats());
			case 'U':
				return DisplayFormatters.formatByteCountToKiBEtc(dm.getStats().getTotalDataBytesSent());
			case 's':
				return Integer.toString(dm.getNbSeeds());
			case 'p':
				return Integer.toString(dm.getNbPeers());	
			case 'v':
				return Integer.toString(dm.getMaxUploads());
			case 'I':
				int downloadSpeed = dm.getStats().getDownloadRateLimitBytesPerSecond();
				if( downloadSpeed <= 0 )
					return "";
				return "(max " + DisplayFormatters.formatByteCountToKiBEtcPerSec(downloadSpeed) + ")";
			case 'O':
				int uploadSpeed = dm.getStats().getUploadRateLimitBytesPerSecond();
				if( uploadSpeed <= 0 )
					return "";
				return "(max " + DisplayFormatters.formatByteCountToKiBEtcPerSec(uploadSpeed) + ")";
				
			case 'S':
			case 'P':
				TRTrackerScraperResponse hd = dm.getTrackerScrapeResponse();
				if (hd == null || !hd.isValid())
					return "?";
				else
				{
					if( variable == 'S' )
						return Integer.toString(hd.getSeeds());
					else
						return Integer.toString(hd.getPeers());
				}
			default: 
				return "??" + variable + "??";
		}
	}
	
	/**
	 * returns the format string (in printf style format) to use for displaying the torrent summary
	 * @return
	 */
	protected String getDefaultSummaryFormat()
	{
		return "[%a] %c\t%t (%z) ETA: %e\r\n%r\tSpeed: %d%I / %u%O\tAmount: %D / %U\tConnections: %s(%S) / %p(%P)";
	}
	
	/**
	 * returns a string representation of the specified state number
	 * suitable for inclusion in a torrent summary
	 * @param dmstate
	 * @return
	 */
	private static String getShortStateString(int dmstate) {
		switch( dmstate )
		{
		case DownloadManager.STATE_INITIALIZING:
			return("I");
		case DownloadManager.STATE_ALLOCATING:
			return("A");
		case DownloadManager.STATE_CHECKING:
			return("C");
		case DownloadManager.STATE_DOWNLOADING:
			return(">");
		case DownloadManager.STATE_ERROR:
			return("E");
		case DownloadManager.STATE_SEEDING:
			return("*");
		case DownloadManager.STATE_STOPPED:
			return("!");
		case DownloadManager.STATE_WAITING:
			return(".");
		case DownloadManager.STATE_READY:
			return(":");
		case DownloadManager.STATE_QUEUED:
			return("-");
		default:
			return("?");
		}
	}

	/**
	 * prints out the full details of a particular torrent
	 * @param out
	 * @param dm
	 * @param torrentNum
	 */
	private static void printTorrentDetails( PrintStream out, DownloadManager dm, int torrentNum, boolean verbose)
	{
		String name = dm.getDisplayName();
		if (name == null)
			name = "?";
		out.println("> -----");
		out.println("Info on Torrent #" + torrentNum + " (" + name + ")");
		out.println("- General Info -");
		String[] health = { "- no info -", "stopped", "no remote connections", "no tracker", "OK", "ko" };
		try {
			out.println("Health: " + health[dm.getHealthStatus()]);
		} catch (Exception e) {
			out.println("Health: " + health[0]);
		}
		out.println("State: " + Integer.toString(dm.getState()));
		if (dm.getState() == DownloadManager.STATE_ERROR)
			out.println("Error: " + dm.getErrorDetails());
		out.println("Hash: " + TorrentUtils.nicePrintTorrentHash(dm.getTorrent(), true));
		out.println("- Torrent file -");
		out.println("Torrent Filename: " + dm.getTorrentFileName());
		out.println("Saving to: " + dm.getSaveLocation());
		out.println("Created By: " + dm.getTorrentCreatedBy());
		out.println("Comment: " + dm.getTorrentComment());
		out.println("- Tracker Info -");
		TRTrackerAnnouncer trackerclient = dm.getTrackerClient();
		if (trackerclient != null) {
			out.println("URL: " + trackerclient.getTrackerURL());
			String timestr;
			try {
				int time = trackerclient.getTimeUntilNextUpdate();
				if (time < 0) {
					timestr = MessageText.getString("GeneralView.label.updatein.querying");
				} else {
					int minutes = time / 60;
					int seconds = time % 60;
					String strSeconds = "" + seconds;
					if (seconds < 10) {
						strSeconds = "0" + seconds; //$NON-NLS-1$
					}
					timestr = minutes + ":" + strSeconds;
				}
			} catch (Exception e) {
				timestr = "unknown";
			}
			out.println("Time till next Update: " + timestr);
			out.println("Status: " + trackerclient.getStatusString());
		} else
			out.println("  Not available");
		
		out.println("- Files Info -");
		DiskManagerFileInfo files[] = dm.getDiskManagerFileInfo();
		if (files != null) {
			for (int i = 0; i < files.length; i++) {
				out.print(((i < 9) ? "   " : "  ") + Integer.toString(i + 1)
						+ " (");
				String tmp = ">";
				if (files[i].getPriority()>0)
					tmp = "+";
				if (files[i].isSkipped())
					tmp = "!";
				out.print(tmp + ") ");
				if (files[i] != null) {
					long fLen = files[i].getLength();
					if (fLen > 0) {
						DecimalFormat df = new DecimalFormat("000.0%");
						out.print(df.format(files[i].getDownloaded() * 1.0
								/ fLen));
						out.println("\t" + files[i].getFile(true).getName());
					} else
						out.println("Info not available.");
				} else
					out.println("Info not available.");
			}
		} else
			out.println("  Info not available.");
		
		if ( verbose ){
			
			out.println( "Pieces" );
			
			PEPeerManager pm = dm.getPeerManager();
			
			if ( pm != null ){
				
				PiecePicker picker = pm.getPiecePicker();
				
				PEPiece[] pieces = pm.getPieces();
				
				String	line = "";
				
				for (int i=0;i<pieces.length;i++){
					
					String str = picker.getPieceString( i );
					
					line += (line.length()==0?(i + " "):",") + str;
					
					PEPiece piece = pieces[i];

					if ( piece != null ){
					
						line += ":" + piece.getString();
					}
					
					if ( (i+1)%10 == 0 ){
						
						out.println( line );
						
						line = "";
					}
				}
				
				if ( line.length() > 0 ){
					
					out.println( line );
				}
			}
		}
		
		out.println("> -----");
	}
	
	protected void
	showDHTStats(
		ConsoleInput	ci )
	{
		try{
			PluginInterface	def = ci.azureus_core.getPluginManager().getDefaultPluginInterface();
			
			PluginInterface dht_pi = 
				def.getPluginManager().getPluginInterfaceByClass(DHTPlugin.class );
			
			if ( dht_pi == null ){
			
				ci.out.println( "\tDHT isn't present" );
				
				return;
			}
			
			DHTPlugin	dht_plugin = (DHTPlugin)dht_pi.getPlugin();
			
			if ( dht_plugin.getStatus() != DHTPlugin.STATUS_RUNNING ){
				
				ci.out.println( "\tDHT isn't running yet (disabled or initialising)" );
				
				return;
			}
			
			DHT[]	dhts = dht_plugin.getDHTs();
			
			for (int i=0;i<dhts.length;i++){
				
				if ( i > 0 ){
					ci.out.println("");
				}
				
				DHT	dht = dhts[i];
				
				DHTTransport transport = dht.getTransport();
				
				DHTTransportStats	t_stats = transport.getStats();
				DHTDBStats			d_stats	= dht.getDataBase().getStats();
				DHTControlStats		c_stats = dht.getControl().getStats();
				DHTRouterStats		r_stats = dht.getRouter().getStats();
				
				long[]	rs = r_stats.getStats();
	
				DHTNetworkPosition[]	nps = transport.getLocalContact().getNetworkPositions();
				
				String	np_str = "";
				
				for (int j=0;j<nps.length;j++){
					np_str += (j==0?"":",") + nps[j];
				}
				
				ci.out.println( 	"DHT:ip=" + transport.getLocalContact().getAddress() + 
									",net=" + transport.getNetwork() +
									",prot=V" + transport.getProtocolVersion() + 
									",np=" + np_str);
				
				ci.out.println( 	
							"Router" +
							":nodes=" + rs[DHTRouterStats.ST_NODES] +
							",leaves=" + rs[DHTRouterStats.ST_LEAVES] +
							",contacts=" + rs[DHTRouterStats.ST_CONTACTS] +
							",replacement=" + rs[DHTRouterStats.ST_REPLACEMENTS] +
							",live=" + rs[DHTRouterStats.ST_CONTACTS_LIVE] +
							",unknown=" + rs[DHTRouterStats.ST_CONTACTS_UNKNOWN] +
							",failing=" + rs[DHTRouterStats.ST_CONTACTS_DEAD]);
	
				ci.out.println( 
							"Transport" + 
							":" + t_stats.getString()); 
						
				int[]	dbv_details = d_stats.getValueDetails();
				
				ci.out.println( 
							"Control:dht=" + c_stats.getEstimatedDHTSize() + 
						   	", Database:keys=" + d_stats.getKeyCount() +
						   	",vals=" + dbv_details[DHTDBStats.VD_VALUE_COUNT]+
						   	",loc=" + dbv_details[DHTDBStats.VD_LOCAL_SIZE]+
						   	",dir=" + dbv_details[DHTDBStats.VD_DIRECT_SIZE]+
						   	",ind=" + dbv_details[DHTDBStats.VD_INDIRECT_SIZE]+
						   	",div_f=" + dbv_details[DHTDBStats.VD_DIV_FREQ]+
						   	",div_s=" + dbv_details[DHTDBStats.VD_DIV_SIZE] );
			}
			
		}catch( Throwable e ){
			
			e.printStackTrace( ci.out );
		}
	}
}
