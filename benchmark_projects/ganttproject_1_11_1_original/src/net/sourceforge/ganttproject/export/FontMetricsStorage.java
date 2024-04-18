package net.sourceforge.ganttproject.export;

import java.net.URI;
import java.net.URL;
import java.net.URISyntaxException;

/**
 * Created by IntelliJ IDEA.
 * @author bard
 * Date: 07.01.2004
 */
public class FontMetricsStorage {
    public URI getFontMetricsURI(TTFFileExt ttfFile) {
        URI result = null;
        String fontName = ttfFile.getFile().getName();
        String resourceName = "font-metrics/"+fontName+".xml";
        URL resourceUrl = getClass().getClassLoader().getResource(resourceName);

        try {
            result = resourceUrl==null ? null : new URI(resourceUrl.toString());
        }
        catch (URISyntaxException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
        return result;
    }
}
