/***************************************************************************
                           GanttLanguage.java  -  description
                             -------------------
    begin                : jan 2003
    copyright            : (C) 2003 by Thomas Alexandre
    email                : alexthomas(at)ganttproject.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/



package net.sourceforge.ganttproject.language;

import java.awt.ComponentOrientation;
import java.text.DateFormat;
import java.text.FieldPosition;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.EventListener;
import java.util.EventObject;
import java.util.Locale;
import java.util.MissingResourceException;
import java.util.ResourceBundle;
import net.sourceforge.ganttproject.GanttCalendar;
import net.sourceforge.ganttproject.time.gregorian.GregorianCalendar;

/** 
  * Class for the language
  */
public class GanttLanguage
{
	public class Event extends EventObject {
		public Event(GanttLanguage language) {
			super(language);
		}
        
        public GanttLanguage getLanguage() {
            return (GanttLanguage) getSource();
        }

	}
	public interface Listener extends EventListener {
		public void languageChanged(Event event);
	}
    
	private static GanttLanguage ganttLanguage = null;
	private ArrayList myListeners = new ArrayList();
    
	public static GanttLanguage getInstance() {
		if (ganttLanguage == null) {
			ganttLanguage = new GanttLanguage();
		}
		return ganttLanguage;
	}
		
	Locale currentLocale = null;
	ResourceBundle i18n = null;
	DateFormat currentDateFormat = null;
	DateFormat currentTimeFormat = null;
	
	private GanttLanguage() {
		setLocale(Locale.getDefault());
	}
	
	public void setLocale(Locale locale) {
		currentLocale = locale;
		currentDateFormat = DateFormat.getDateInstance(DateFormat.MEDIUM, currentLocale);
		currentTimeFormat = DateFormat.getTimeInstance(DateFormat.MEDIUM, currentLocale);
        String resourceBase = System.getProperty("org.ganttproject.resourcebase", "language/i18n");
		i18n = ResourceBundle.getBundle(resourceBase, currentLocale);
        fireLanguageChanged();
	}
	
	public String formatDate(GanttCalendar date) {
		return currentDateFormat.format(date.getTime());
	}
	
	public String formatTime(GanttCalendar date) {
		return currentTimeFormat.format(date.getTime());
	}
	
	public GanttCalendar parseDate(String date) throws ParseException {
		Calendar tmp = Calendar.getInstance(currentLocale);
		tmp.setTime(currentDateFormat.parse(date));
		return new GanttCalendar(tmp.get(Calendar.YEAR), tmp.get(Calendar.MONTH), tmp.get(Calendar.DATE));
	}
	
	public String getMonth (int m) {
		GregorianCalendar month = new GregorianCalendar(2000, m ,1);
		SimpleDateFormat dateFormat = new SimpleDateFormat("MMMM", this.currentLocale);
		StringBuffer result = new StringBuffer();
		result = dateFormat.format(month.getTime(), result, new FieldPosition(DateFormat.MONTH_FIELD));
		return result.toString();
	}

	public String getDay (int d) {
		GregorianCalendar day = new GregorianCalendar(2000, 1, 1);
		while (day.get(Calendar.DAY_OF_WEEK) != Calendar.SUNDAY) {
			day.add(Calendar.DATE, 1);
		}
		day.add(Calendar.DATE, d);
		
		SimpleDateFormat dateFormat = new SimpleDateFormat("EEEE", this.currentLocale);
		StringBuffer result = new StringBuffer();
		result = dateFormat.format(day.getTime(), result, new FieldPosition(DateFormat.DAY_OF_WEEK_FIELD));
		return result.toString();
	}
	
	public String getText(String key) {
        try {
            return i18n.getString(key);
        } catch (MissingResourceException e) {
            return "Missing resource '"+key+"'";
        }
    };
    
    public ComponentOrientation getComponentOrientation (){
    	return ComponentOrientation.getOrientation(currentLocale);
    }

    public void addListener(Listener listener) {
        myListeners.add(listener);   
    }
    
    public void removeListener(Listener listener) {
        myListeners.remove(listener);        
    }
    private void fireLanguageChanged() {
        Event event = new Event(this);
        for (int i=0; i<myListeners.size(); i++) {
            Listener next = (Listener) myListeners.get(i);
            next.languageChanged(event);
        }
    }

	public SimpleDateFormat createDateFormat(String string) {
		return new SimpleDateFormat(string, currentLocale);
	}
    
    
}
