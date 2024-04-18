package net.sourceforge.ganttproject.chart;

import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Line;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitStack;

import java.awt.*;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

/**
 * Created by IntelliJ IDEA.
 */
public class ChartGridImpl extends ChartRendererBase implements TimeUnitVisitor {
    private int myPosX;
    private TimeFrame myCurrentFrame;
    private boolean areUnitsAccepted;
    private TimeUnit myCurrentUnit;
	private boolean myWasHoliday;
	private Date myToday;

    public ChartGridImpl(ChartModelBase chartModel) {
        super(chartModel);
    }
    
    public void beforeProcessingTimeFrames() {
        getPrimitiveContainer().clear();
        myPosX = 0;
        myToday = GregorianCalendar.getInstance().getTime();
    }

    public void startTimeFrame(TimeFrame timeFrame) {
        myCurrentFrame = timeFrame;
    }

    public void endTimeFrame(TimeFrame timeFrame) {
        myCurrentFrame = null;
    }

    public void startUnitLine(TimeUnit timeUnit) {
        if (timeUnit==myCurrentFrame.getBottomUnit()) {
            areUnitsAccepted = true;
            myCurrentUnit = timeUnit;
        }
    }

    public void endUnitLine(TimeUnit timeUnit) {
        areUnitsAccepted = false;
        myCurrentUnit = null;
    }

    public void nextTimeUnit(int unitIndex) {
        if (areUnitsAccepted) {
            if (getChartModel().getChartUIConfiguration().isRedlineOn() &&
                    myCurrentFrame.getUnitStart(myCurrentUnit, unitIndex).compareTo(myToday)<=0 &&
                	myCurrentFrame.getUnitFinish(myCurrentUnit, unitIndex).compareTo(myToday)>0) {
                	
            	Line redLine = getPrimitiveContainer().createLine(myPosX+2, 0, myPosX+2, getHeight());
            	redLine.setForegroundColor(Color.RED);
            }
            DayTypeAlternance[] alternance = getChartModel().getDayTypeAlternance(myCurrentFrame, myCurrentUnit, unitIndex);
            int posX = myPosX;
            float delta = (float)getChartModel().getBottomUnitWidth()/(float)alternance.length; 
            for (int i=0; i<alternance.length; i++) {
            	posX = (int)(myPosX+delta*i);
            	int nextPosX = i<alternance.length-1 ? (int)(myPosX+delta*(i+1)) : myPosX+getChartModel().getBottomUnitWidth();
            	int width = nextPosX-posX;
            	DayTypeAlternance next = alternance[i];
            	if (GPCalendar.DayType.HOLIDAY==next.getDayType()) {
                    GraphicPrimitiveContainer.Rectangle r = getPrimitiveContainer().createRectangle(posX, 0, width, getHeight());
                    r.setStyle("calendar.holiday");
                    r.setBackgroundColor(getConfig().getHolidayTimeBackgroundColor());
                    getPrimitiveContainer().bind(r, next.getDayType());            		
                    myWasHoliday = true;
            	}
            }
            //
            myPosX += getChartModel().getBottomUnitWidth();
        }        
    }

    private GPCalendar.DayType getDayType(int unitIndex) {
        return getChartModel().getDayType(myCurrentFrame, myCurrentUnit, unitIndex);
    }

	/* (non-Javadoc)
	 * @see net.sourceforge.ganttproject.chart.TimeUnitVisitor#afterProcesingTimeFrames()
	 */
	public void afterProcessingTimeFrames() {
		// TODO Auto-generated method stub
		
	}

}
