package net.sourceforge.ganttproject.importer;

import javax.swing.JFileChooser;
import javax.swing.filechooser.*;

import net.sourceforge.ganttproject.GanttOptions;
import net.sourceforge.ganttproject.filter.ExtensionBasedFileFilter;

public abstract class ImporterFactory {
    public static Importer createImporter(FileFilter fileFilter) {
        if (fileFilter==txtFilter) {
            return new ImporterFromTxtFile();
        }
//				if (fileFilter==mppFilter) {
//            return new ImporterFromMsProjectFile();
//        }
        if (fileFilter==ganFilter) {
            return new ImporterFromGanttFile();
        }
//        else if (fileFilter==plannerFilter) {
//        	return new ImporterFromPlannerFile();
//        }
        return null;
    }
    
    public static JFileChooser createFileChooser(GanttOptions options) {
		JFileChooser fc = new JFileChooser(options.getWorkingDir());
		FileFilter[] filefilters = fc.getChoosableFileFilters();
		for (int i = 0; i < filefilters.length; i++) {
			fc.removeChoosableFileFilter(filefilters[i]);
		}
		fc.addChoosableFileFilter(ganFilter);
		//fc.addChoosableFileFilter(mppFilter);
		fc.addChoosableFileFilter(txtFilter);
		//fc.addChoosableFileFilter(plannerFilter);

		return fc;

	}
    private static FileFilter txtFilter = new ExtensionBasedFileFilter("txt", "Text files (.txt)");
		//private static FileFilter mppFilter = new ExtensionBasedFileFilter("mpp|mpx|xml", "MsProject files (.mpp, .mpx, .xml)");
		private static FileFilter mppFilter = new ExtensionBasedFileFilter("mpp|mpx", "MsProject files (.mpp, .mpx)");
    private static FileFilter ganFilter = new ExtensionBasedFileFilter("xml|gan", "GanttProject files (.gan, .xml)");
    //private static FileFilter plannerFilter = new ExtensionBasedFileFilter("mrproject|planner", "Planner (MrProject) files (.mrproject)");
    
}
