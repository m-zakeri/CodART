package net.sourceforge.ganttproject;

/** Class to store 3 boolean values */
public class GanttExportSettings {
	public boolean name,  percent, depend, border3d, ok;
	public GanttExportSettings() {
		name = percent  = depend = ok = true;
	}
	
	public GanttExportSettings(boolean bName, boolean bPercent, boolean bDepend, boolean b3dBorders)
	{
		name = bName;
		percent = bPercent; 
		depend = bDepend;
		border3d = b3dBorders;
		ok = true;
	}
}
