/*
LICENSE:
                                                                 
   This program is free software; you can redistribute it and/or modify  
   it under the terms of the GNU General Public License as published by  
   the Free Software Foundation; either version 2 of the License, or     
   (at your option) any later version.                                   
                                                                         
   Copyright (C) 2004, GanttProject Development Team
 */
package net.sourceforge.ganttproject.export;

import org.xml.sax.helpers.AttributesImpl;

import javax.xml.transform.sax.SAXTransformerFactory;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 */
public abstract class ProjectExportProcessor {
    private SAXTransformerFactory myTransformerFactory;
    private Logger myLogger;
    private static String LOGGER_NAME = "net.sourceforge.ganttproject.export.pdf";
    private AttributesImpl myAttrs = new AttributesImpl();

    /**
     * @deprecated
     * It is a temporary method for export subsystem refactoring only
     */
    public abstract void doExport(DeprecatedProjectExportData exportData) throws ExportException;
    
    protected SAXTransformerFactory getTransformerFactory() {
        if (myTransformerFactory==null) {
            myTransformerFactory = (SAXTransformerFactory)SAXTransformerFactory.newInstance();
        }
        return myTransformerFactory;
    }

    protected boolean isInfoable() {
        return getLogger().isLoggable(Level.INFO);
    }

    protected void info(String message) {
        getLogger().info(message);
    }

    protected Logger getLogger() {
        if (myLogger==null) {
            myLogger = Logger.getLogger(LOGGER_NAME);
        }
        return myLogger;
    }

    protected AttributesImpl getCleanAttrs() {
        myAttrs.clear();
        return myAttrs;
    }

}
