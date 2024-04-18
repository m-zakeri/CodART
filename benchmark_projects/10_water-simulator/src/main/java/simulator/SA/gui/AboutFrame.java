package simulator.SA.gui;

import java.awt.Dimension;
import java.awt.Font;

import javax.swing.BorderFactory;
import javax.swing.JInternalFrame;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

/**
 * @author Ioannis N. Athanasiadis
 * @version 1.9
 * @since 2003-2006
 */

public class AboutFrame extends JInternalFrame {
	private static final long serialVersionUID = -3332140195203607928L;

	static final int xOffset = 30, yOffset = 30;

	// Constructor
	public AboutFrame() {
		super("About DAWN" ,
		          true, //resizable
		          true, //closable
		          true, //maximizable
		          true);
		//		Create a text area.
        JTextArea textArea = new JTextArea(about);
        textArea.setFont(new Font(
//        		"Dialog" 
        		"DialogInput" 
//        		"Monospaced" 
//        		"Serif" 
//        		"SansSerif"
        		, Font.PLAIN, 12));
        textArea.setLineWrap(true);
        textArea.setWrapStyleWord(true);
        JScrollPane areaScrollPane = new JScrollPane(textArea);
        areaScrollPane.setVerticalScrollBarPolicy(
                        JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
        areaScrollPane.setPreferredSize(new Dimension(500, 500));
        areaScrollPane.setBorder(
            BorderFactory.createCompoundBorder(
                BorderFactory.createCompoundBorder(
                                BorderFactory.createTitledBorder("The Distributed Agent-based Water Demand Simulator"),
                                BorderFactory.createEmptyBorder(5,5,5,5)),
                areaScrollPane.getBorder()));
        
		this.add(areaScrollPane);
        //...Then set the window size or call pack...
        setSize(500,500);

        //Set the window's location.
        setLocation(xOffset, yOffset);
	}
	
private final String about =
	"DAWN: Distributed Agent-based Water Demand Simulator " +
	"\nCopyright (c) 2003-2006  I.N.Athanasiadis, P.Vartalas, and P.A.Mitkas" +
	"\n"+
	"\n"+
	"\n"+
	"\nThis program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or any later version." +
	"\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details." +
	"\nYou should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. " +
	"\nThe GNU General Public Licence is available online: http://www.gnu.org/licenses/gpl.txt" +
	"\nDAWN uses the following libraries: JADE ver.2.6, jOpenChart ver.0.94, log4j ver.1.2.8. Their licences are distributed along with this library. DAWN includes software developed by the Apache Software Foundation (http://www.apache.org/)." +
	"\n" +
	"\n"+
	"\n"+
	"DAWN was implemented by I. N. Athanasiadis and P. Vartalas, while with the Intelligent Systems and Software Engineering Laboratory of the Aristotle University of Thessaloniki." +
	"\nRevision 1.9: I. N. Athanasiadis, June 2006" +
	"\nContact information: I.N.Athanasiadis: ioannis<at>athanasiadis<dot>info" +
	"\n"+
	"\n"+
	"\n"+
	"\nCurrently DAWN is distributed at SourceForge (http://sourceforge.net/projects/water-simulator). Both binaries and source code are available on SourceForge." +
	"\n"+
	"\n"+
	"\n"+
	"\nDAWN use has been reported in the following articles." +
	"\n[1] I. N. Athanasiadis and P. A. Mitkas, Social influence and water conservation: An agent-based approach,IEEE Computing in Science and Engineering, 7 (1) : 65-70, Jan/Feb 2005. " +
	"\n[2] I. N. Athanasiadis, A. K. Mentes, P. A. Mitkas, and Y. A. Mylopoulos, A hybrid agent-based model for estimating residential water demand, SIMULATION, Transactions of the International Modeling and Simulation Society, 81 (3): 175-187, 2005." +
	"\n[3] I. N. Athanasiadis, P. Vartalas and P. A. Mitkas, DAWN: A platform for evaluating water-pricing policies using a software agent society, Transactions of the 2nd Biennial Meeting of the Int'l Environmental Modelling and Software Society: Complexity and Integrated Resources Management, Osnabrueck, Germany, June 2004, iEMSs, vol.2, pp. 643-648." +
	"\nHave you reported your results using DAWN in scientific or other publications, contact ioannis<at>athanasiadis<dot>info to update this list."
	;
}




	
