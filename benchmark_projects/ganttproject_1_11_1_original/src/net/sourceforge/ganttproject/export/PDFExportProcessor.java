/*
LICENSE:
                                                                 
   This program is free software; you can redistribute it and/or modify  
   it under the terms of the GNU General Public License as published by  
   the Free Software Foundation; either version 2 of the License, or     
   (at your option) any later version.                                   
                                                                         
   Copyright (C) 2004, GanttProject Development Team
 */
package net.sourceforge.ganttproject.export;

import net.sourceforge.ganttproject.IGanttProject;
import net.sourceforge.ganttproject.io.GanttPDFExport;
import net.sourceforge.ganttproject.resource.HumanResourceManager;

import org.apache.fop.apps.Driver;
import org.apache.fop.apps.Options;
import org.apache.fop.apps.FOPException;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.AttributesImpl;

import javax.xml.transform.sax.SAXTransformerFactory;
import javax.xml.transform.sax.TransformerHandler;
import javax.xml.transform.sax.SAXResult;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.stream.StreamSource;
import javax.xml.transform.stream.StreamResult;
import java.io.*;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 */
public class PDFExportProcessor extends ProjectExportProcessor {
    private String myStylesheetPath;

    public void doExport(DeprecatedProjectExportData exportData) throws ExportException {
        try {
            Class.forName("org.apache.fop.apps.Driver").newInstance();
        } catch (InstantiationException e) {
            throw new ExportException("Failed to load FOP library", e);
        } catch (IllegalAccessException e) {
            throw new ExportException("Failed to load FOP library", e);
        } catch (ClassNotFoundException e) {
            throw new ExportException("Failed to load FOP library", e);
        }
        String filename = exportData.myFilename;
        if (!filename.toUpperCase().endsWith(".PDF")) {
            filename += ".pdf";
        }
        File file = new File(filename);
        try {
            GanttPDFExport.save(file, 
                    (IGanttProject)exportData.myProject,
                    (HumanResourceManager) exportData.myProject.getHumanResourceManager(), exportData.myTree, exportData.myGanttChart,
                    exportData.myResourceChart, exportData.myExportOptions, exportData.myXslFoScript);            
        } catch (IOException e1) {
            throw new ExportException("Error creating output file", e1);            
        } catch (TransformerException e1) {
            throw new ExportException("Error running XSL-FO transformations", e1);            
        }
        if (file.length()==0) {
            StringBuffer report = new StringBuffer();
            report.append("PDF file after export seems to be empty.\n There have been no exceptions during the export.\n");
            report.append("Export data:\n");
            report.append("Filename="+file.getAbsolutePath()+" is writable="+file.canWrite()+"\n");
            report.append("XSL-FO script location="+exportData.myXslFoScript);
            throw new ExportException(report.toString());
        }
        
    }

    
    public void run(PDFExportData data) throws IOException, TransformerConfigurationException, FOPException, SAXException {
        if (isInfoable()) {
            info("Starting PDF export");
            info("File to export to="+data.myOutputFile);
            info("stylesheet="+data.myStylesheet);
        }
        myStylesheetPath = new File(data.myStylesheet).getParent();
        File chartFile = exportGanttChart(data);
        File resourceChartFile = exportResourceChart(data);

        Driver fopDriver = createDriver(data);
        SAXTransformerFactory factory = getTransformerFactory();
        TransformerHandler ganttProjectHandler = factory.newTransformerHandler();
        TransformerHandler stylesheetHandler = factory.newTransformerHandler(new StreamSource(new File(data.myStylesheet)));
        stylesheetHandler.setResult(new SAXResult(fopDriver.getContentHandler()));
        ganttProjectHandler.setResult(new StreamResult(System.out));
        //ganttProjectHandler.setResult(new SAXResult(stylesheetHandler));
        exportProject(ganttProjectHandler);

    }

    protected void exportProject(TransformerHandler handler) throws SAXException {
        handler.startDocument();
        handler.startPrefixMapping("ganttproject", "http://ganttproject.sf.net");
        handler.endPrefixMapping("ganttproject");
        AttributesImpl attrs = getCleanAttrs();
        attrs.addAttribute("", "xslfo-path", "xslfo-path", "CDATA", myStylesheetPath);
        handler.startElement("", "report", "ganttproject:report", attrs);
        handler.endElement("", "report", "ganttproject:report");
        handler.endDocument();

    }

    private Driver createDriver(PDFExportData data) throws FileNotFoundException, FOPException {
        if (isInfoable()) {
            info("Creating FOP driver...");
        }
        Driver driver = new Driver();
        driver.setRenderer(Driver.RENDER_PDF);
        OutputStream out = new java.io.FileOutputStream(data.myOutputFile);
        Options o = createOptions();
        driver.setOutputStream(out);
        if (isInfoable()) {
            info("... done!");
        }
        return driver;
    }

    protected File exportGanttChart(ProjectExportData exportData) throws IOException {
        File outputFile = File.createTempFile("ganttchart", ".jpg");
        if (isInfoable()) {
            info("Exporting gantt chart to JPG image into file="+outputFile);
        }
        GanttChartExportData chartExportData = new GanttChartExportData(outputFile, exportData.myExportSettings, "jpg");
        exportData.myGanttChartExportProcessor.run(chartExportData);
        if (isInfoable()) {
            info("...done!");
        }
        return outputFile;
    }

    protected File exportResourceChart(ProjectExportData exportData) throws IOException {
        File outputFile = File.createTempFile("resourcechart", ".jpg");
        if (isInfoable()) {
            info("Exporting resource chart to file="+outputFile);
        }
        ResourceChartExportData chartExportData = new ResourceChartExportData(outputFile, "jpg");
        exportData.myResourceChartExportProcessor.run(chartExportData);
        if (isInfoable()) {
            info("...done!");
        }
        return outputFile;
    }

    private Options createOptions() throws FOPException {
        //JDKFontLocator locator = new JDKFontLocator();
        //FontRecord[] fontRecords = locator.getFontRecords();
        FontRecord[] fontRecords = new FontRecord[0];
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        StreamResult output = new StreamResult(outputStream);
        try {
            TransformerHandler handler = getTransformerFactory().newTransformerHandler();
            handler.setResult(output);
            //just for nifty debugging :)
            //handler.getTransformer().setOutputProperty(OutputKeys.INDENT, "yes");
            createConfiguration(handler, fontRecords);
        }
        catch (TransformerConfigurationException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        catch (SAXException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        Options result = new Options(new ByteArrayInputStream(outputStream.toByteArray()));

        //return result;
        System.err.println(outputStream.toString());
        return result;
    }

    private void createConfiguration(TransformerHandler handler, FontRecord[] fontRecords) throws SAXException {
        AttributesImpl attrs = new AttributesImpl();
        handler.startDocument();
        handler.startElement("", "configuration", "configuration", attrs);
        handler.startElement("", "fonts", "fonts", attrs);

        for (int i=0; i<fontRecords.length; i++) {
            FontRecord nextRecord = fontRecords[i];
            attrs.clear();
            attrs.addAttribute("", "metrics-file", "metrics-file", "CDATA", nextRecord.getMetricsLocation().toString());
            attrs.addAttribute("", "kerning", "kerning", "CDATA", "yes");
            attrs.addAttribute("", "embed-file", "embed-file", "CDATA", nextRecord.getFontLocation().getPath());
            handler.startElement("", "font", "font", attrs);
            writeTriplets(handler, nextRecord.getFontTriplets());
            handler.endElement("", "font", "font");
        }
        handler.endElement("", "fonts", "fonts");
        handler.endElement("", "configuration", "configuration");
        handler.endDocument();
    }

    private void writeTriplets(TransformerHandler handler, FontTriplet[] fontTriplets) throws SAXException {
        AttributesImpl attrs = new AttributesImpl();
        for (int i=0; i<fontTriplets.length; i++) {
            FontTriplet next = fontTriplets[i];
            attrs.clear();
            attrs.addAttribute("", "name", "name", "CDATA", next.getName());
            attrs.addAttribute("", "style", "style", "CDATA", next.isItalic() ? "italic" : "normal");
            attrs.addAttribute("", "weight", "weight", "CDATA", next.isBold() ? "bold" : "normal");
            handler.startElement("", "font-triplet", "font-triplet", attrs);
            handler.endElement("", "font-triplet", "font-triplet");
        }
    }

}
