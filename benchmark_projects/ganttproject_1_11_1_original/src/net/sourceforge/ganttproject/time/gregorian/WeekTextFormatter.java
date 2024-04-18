package net.sourceforge.ganttproject.time.gregorian;

import java.text.MessageFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.time.TextFormatter;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitText;

public class WeekTextFormatter extends CachingTextFormatter implements TextFormatter {
    private Calendar myCalendar;
    WeekTextFormatter(String formatString) {
        myCalendar = (Calendar) Calendar.getInstance().clone();
    }

    protected TimeUnitText createTimeUnitText(Date startDate) {
        myCalendar.setTime(startDate);
        myCalendar.setMinimalDaysInFirstWeek(7);
        Integer weekNo = new Integer(myCalendar.get(Calendar.WEEK_OF_YEAR));
        String shortText = MessageFormat.format("{0}", new Object[] {weekNo});
        String middleText = MessageFormat.format(GanttLanguage.getInstance().getText("week")+" {0}", new Object[] {weekNo});
        String longText = middleText;
        /*
        myCalendar.add(Calendar.WEEK_OF_YEAR, 1);
        myCalendar.add(Calendar.HOUR, -1);
        Date endDate = myCalendar.getTime();
        SimpleDateFormat formatter = GanttLanguage.getInstance().createDateFormat("dd/MM");
        String startDateString = GanttLanguage.getInstance().formatDateShort(startDate);
        String endDateString = GanttLanguage.getInstance().formatDateShort(endDate);
        String longText = MessageFormat.format("{0} - {1}", new Object[] {startDateString, endDateString});
        */
        return new TimeUnitText(longText, middleText, shortText);
	}

}
