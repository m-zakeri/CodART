/*
 * Created on 06.03.2005
 */
package net.sourceforge.ganttproject.time.gregorian;

import java.text.MessageFormat;
import java.util.Calendar;
import java.util.Date;

import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.time.TextFormatter;
import net.sourceforge.ganttproject.time.TimeUnitText;

/**
 * @author bard
 */
public class YearTextFormatter extends CachingTextFormatter implements TextFormatter {

    private Calendar myCalendar;
    YearTextFormatter() {
        myCalendar = (Calendar) Calendar.getInstance().clone();
    }
    
	protected TimeUnitText createTimeUnitText(Date startDate) {
        myCalendar.setTime(startDate);
        Integer yearNo = new Integer(myCalendar.get(Calendar.YEAR));
        String shortText = MessageFormat.format("{0}", new Object[] {yearNo});
        return new TimeUnitText(shortText);
	}

}
