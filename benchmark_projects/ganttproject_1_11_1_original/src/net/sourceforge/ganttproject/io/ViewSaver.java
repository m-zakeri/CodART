/*
 * Created on 06.03.2005
 */
package net.sourceforge.ganttproject.io;

import javax.xml.transform.sax.TransformerHandler;

import org.xml.sax.SAXException;
import org.xml.sax.helpers.AttributesImpl;

import net.sourceforge.ganttproject.gui.UIFacade;

/**
 * @author bard
 */
class ViewSaver extends SaverBase {
	public void save(UIFacade facade, TransformerHandler handler) throws SAXException {
		AttributesImpl attrs = new AttributesImpl();
		addAttribute("zooming-state", facade.getZoomManager().getZoomState().getPersistentName(), attrs);
		emptyElement("view", attrs, handler);
	}
	
}
