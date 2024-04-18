package net.sourceforge.ganttproject.chart;

import java.awt.Dimension;
import java.awt.Graphics;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.calendar.GPCalendar.DayType;
import net.sourceforge.ganttproject.chart.ChartViewState.ViewStateEvent;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Rectangle;
import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.gui.zoom.ZoomEvent;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitFunctionOfDate;
import net.sourceforge.ganttproject.time.TimeUnitStack;

public class ChartModelBase implements ChartViewState.Listener {

    private final ChartHeaderImpl myChartHeader;
    private final ChartGridImpl myChartGrid;
    private Dimension myBounds;
    private Date myStartDate;
    protected int myAtomUnitPixels;
    private TimeFrame[] myTimeFrames;
    protected final TimeUnitStack myTimeUnitStack;
    private TimeUnit myTopUnit;
    protected TimeUnit myBottomUnit;
    protected java.util.List myTimeUnitVisitors = new ArrayList();
    protected final BottomUnitLineRendererImpl myBottomUnitLineRenderer;
    protected TimeFrameWidthFunction myFrameWidthFunction;
    private RegularFramesWithFunction myRegularFrameWidthFunction = new RegularFramesWithFunction();
    private SkewedFramesWidthFunction mySkewedFrameWidthFunction = new SkewedFramesWidthFunction();
    private final BackgroundRendererImpl myBackgroundRenderer;
    private final StyledPainterImpl myPainter;
    public ChartModelBase(TaskManager taskManager, TimeUnitStack timeUnitStack, UIConfiguration projectConfig) {
        myTaskManager = taskManager;
        myChartUIConfiguration = new ChartUIConfiguration(projectConfig);
        myPainter = new StyledPainterImpl(myChartUIConfiguration);
        myTimeUnitStack = timeUnitStack;
        myChartHeader = new ChartHeaderImpl(this);
        myChartGrid = new ChartGridImpl(this);
        myBottomUnitLineRenderer = new BottomUnitLineRendererImpl(this);
        myBackgroundRenderer = new BackgroundRendererImpl(this);
        myTimeUnitVisitors.add(myChartHeader);
        myTimeUnitVisitors.add(myChartGrid);
        myTimeUnitVisitors.add(myBottomUnitLineRenderer);
    }
    
    public void paint(Graphics g) {
        int height = (int)getBounds().getHeight() - getChartUIConfiguration().getHeaderHeight(); 
        myChartGrid.setHeight(height);
        myBackgroundRenderer.setHeight(height);
    	if (getTopUnit().isConstructedFrom(myBottomUnit)) {
    		myFrameWidthFunction = myRegularFrameWidthFunction;
    		for (int i=0; i<myTimeUnitVisitors.size(); i++) {
    			((TimeUnitVisitor)myTimeUnitVisitors.get(i)).setEnabled(true);
    		}
    		paintRegularTimeFrames(g, getTimeFrames(null));
    	}
    	else {
    		myFrameWidthFunction = mySkewedFrameWidthFunction;
    		mySkewedFrameWidthFunction.initialize();
    		paintSkewedTimeFrames(g);
    	}
    }

    protected void enableRenderers1() {
        myChartHeader.setEnabled(false);
        myBottomUnitLineRenderer.setEnabled(true);
        myChartGrid.setEnabled(true);        
    }
    
    protected void enableRenderers2() {
        myChartHeader.setEnabled(true);
        myBottomUnitLineRenderer.setEnabled(false);
        myChartGrid.setEnabled(false);        
    }
    
    private void paintSkewedTimeFrames(Graphics g) {
    	TimeUnit topUnit = getTopUnit();
    	setTopUnit(myBottomUnit);
    	myTimeFrames = null;
        enableRenderers1();
    	TimeFrame[] timeFrames  = getTimeFrames(null);
    	paintRegularTimeFrames(g, timeFrames);
    	Date exactStart = timeFrames[0].getStartDate();
    	//System.err.println("... done");
    	//System.err.println("[ChartModelImpl] rendering skewed frames. Top unit="+myTopUnit+" bottom unit="+myBottomUnit);
    	//System.err.println(" rendering top line");
    	myTimeFrames = null;
    	setTopUnit(topUnit);
    	myBottomUnit = topUnit;
        enableRenderers2();
    	timeFrames  = getTimeFrames(exactStart);
    	
    	paintRegularTimeFrames(g, timeFrames);
    	
    	//
    	//System.err.println(" rendering bottom line");
    }

    protected void paintMainArea(Graphics mainArea, Painter p) {
        myChartGrid.getPrimitiveContainer().paint(p, mainArea);        
    }
    
    private void paintRegularTimeFrames(Graphics g, TimeFrame[] timeFrames) {
        fireBeforeProcessingTimeFrames();
        for (int i=0; i<timeFrames.length; i++) {
            TimeFrame next = timeFrames[i];
            fireFrameStarted(next);
            TimeUnit topUnit = next.getTopUnit();
            fireUnitLineStarted(topUnit);
            fireUnitLineFinished(topUnit);
            //
            TimeUnit bottomUnit = myBottomUnit;//next.getBottomUnit();
            fireUnitLineStarted(bottomUnit);
            visitTimeUnits(next, bottomUnit);
            fireUnitLineFinished(bottomUnit);
            fireFrameFinished(next);
        }
        fireAfterProcessingTimeFrames();
        
        myPainter.setGraphics(g);
        //Painter p = new StyledPainterImpl(g, getChartUIConfiguration());
        myChartHeader.getPrimitiveContainer().paint(myPainter, g);
        myBottomUnitLineRenderer.getPrimitiveContainer().paint(myPainter, g);
        Graphics mainArea = g.create(0, getChartUIConfiguration().getHeaderHeight(), (int)getBounds().getWidth(), (int)getBounds().getHeight());
        myPainter.setGraphics(mainArea);
        //p = new StyledPainterImpl(mainArea, getChartUIConfiguration());
        myBackgroundRenderer.getPrimitiveContainer().paint(myPainter, g);
        paintMainArea(mainArea, myPainter);
        //Graphics resourcesArea = g.create((int)getBounds().getWidth()-20, getChartUIConfiguration().getHeaderHeight(), 20, (int)getBounds().getHeight());
        //myResourcesRendererImpl.getPrimitiveContainer().paint(p, resourcesArea);
    	//myTaskProgressRendererImpl.getPrimitiveContainer().paint(p, mainArea);
    }

    void fireBeforeProcessingTimeFrames() {
        myBackgroundRenderer.beforeProcessingTimeFrames();
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.beforeProcessingTimeFrames();
        }
    }

    void fireAfterProcessingTimeFrames() {
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.afterProcessingTimeFrames();
        }
    }

    void fireFrameStarted(TimeFrame timeFrame) {
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.startTimeFrame(timeFrame);
        }
    }

    void fireFrameFinished(TimeFrame timeFrame) {
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.endTimeFrame(timeFrame);
        }
    }

    void fireUnitLineStarted(TimeUnit timeUnit) {
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.startUnitLine(timeUnit);
        }
    }

    void fireUnitLineFinished(TimeUnit timeUnit) {
        for (int i=0; i<myTimeUnitVisitors.size(); i++) {
            TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
            if (!nextVisitor.isEnabled()) {
            	continue;
            }
            nextVisitor.endUnitLine(timeUnit);
        }
    }

    void visitTimeUnits(TimeFrame timeFrame, TimeUnit timeUnit) {
        for (int j=0; j<timeFrame.getUnitCount(timeUnit); j++) {
            for (int i=0; i<myTimeUnitVisitors.size(); i++) {
                TimeUnitVisitor nextVisitor = (TimeUnitVisitor)myTimeUnitVisitors.get(i);
                if (!nextVisitor.isEnabled()) {
                	continue;
                }
                nextVisitor.nextTimeUnit(j);
            }
        }
    
    }

    public void setBounds(Dimension bounds) {
        myBounds = bounds;        
    }

    public void setStartDate(Date startDate) {
    	if (!startDate.equals(myStartDate)) {
    		myStartDate = startDate;		
    		myTimeFrames = null;
    	}
    }

    public Date getStartDate() {
        return myStartDate;
    }
    public void setBottomUnitWidth(int pixelsWidth) {
    	myAtomUnitPixels = pixelsWidth;
    }

    public void setRowHeight(int rowHeight) {
        getChartUIConfiguration().setRowHeight(rowHeight);
    }

    public void setTopTimeUnit(TimeUnit topTimeUnit) {
    	setTopUnit(topTimeUnit);
        myTimeFrames = null;
    }

    public void setBottomTimeUnit(TimeUnit bottomTimeUnit) {
    	myBottomUnit = bottomTimeUnit;
        myTimeFrames = null;
    }

    protected Dimension getBounds() {
        return myBounds;
    }

    TimeFrame[] getTimeFrames(Date exactDate) {
    	if (myTimeFrames==null) {
    		myTimeFrames = calculateTimeFrames(exactDate);
    	}
    	return myTimeFrames;
    }

    protected int getBottomUnitWidth() {
    	return myAtomUnitPixels;
    }

    private TimeFrame[] calculateTimeFrames(Date exactDate) {
    	ArrayList result = new ArrayList();
    	int totalFramesWidth = 0;
    	Date currentDate = myStartDate;
    	do {
    		
    		TimeFrame currentFrame = myTimeUnitStack.createTimeFrame(currentDate, getTopUnit(currentDate), myBottomUnit);
    		if (exactDate!=null && currentFrame.getStartDate().before(exactDate)) {
    			currentFrame.trimLeft(exactDate);
    		}
    		result.add(currentFrame);
    		int frameWidth = myFrameWidthFunction.getTimeFrameWidth(currentFrame);
    		totalFramesWidth += frameWidth;
    		currentDate = currentFrame.getFinishDate();
    		
    	} while (totalFramesWidth<=getBounds().getWidth());
    	//
    	return (TimeFrame[]) result.toArray(new TimeFrame[0]);
    }

    public GPCalendar.DayType getDayType(TimeFrame timeFrame, TimeUnit timeUnit, int unitIndex) {
        Date startDate = timeFrame.getUnitStart(timeUnit, unitIndex);
        Date endDate = timeFrame.getUnitFinish(timeUnit, unitIndex);
        Calendar c = (Calendar) Calendar.getInstance().clone();
        c.setTime(startDate);
        int startDayOfWeek = c.get(Calendar.DAY_OF_WEEK);
        c.setTime(endDate);
        int endDayOfWeek = c.get(Calendar.DAY_OF_WEEK);
    
        //return startDayOfWeek==Calendar.SATURDAY || startDayOfWeek==Calendar.SUNDAY;
        return getTaskManager().getCalendar().getWeekDayType(startDayOfWeek);
    }

    public void startDateChanged(ChartViewState.ViewStateEvent e) {
        setStartDate((Date) e.getNewValue());
    }
	public void zoomChanged(ZoomEvent e) {
	}
    /**
     * @author bard
     */
    private interface TimeFrameWidthFunction {
    	int getTimeFrameWidth(TimeFrame timeFrame);
    }

    protected TimeUnit getBottomUnit() {
    	return myBottomUnit;
    }

    protected TimeUnitStack getTimeUnitStack() {
    	return myTimeUnitStack;
    }

    protected DayTypeAlternance[] getDayTypeAlternance(TimeFrame timeFrame, TimeUnit timeUnit, int unitIndex) {
    	class AlternanceFactory {
    		private Calendar c = (Calendar) Calendar.getInstance().clone(); 
    		DayTypeAlternance createAlternance(TimeUnit timeUnit, Date startDate, Date endDate) {
    	        c.setTime(startDate);
    	        int startDayOfWeek = c.get(Calendar.DAY_OF_WEEK);
    	        c.setTime(endDate);
    	        int endDayOfWeek = c.get(Calendar.DAY_OF_WEEK);
    	        TaskLength duration = myTaskManager.createLength(timeUnit, startDate, endDate);
    	        DayType dayType = getTaskManager().getCalendar().getWeekDayType(startDayOfWeek);
    			return new DayTypeAlternance(dayType, duration);
    		}
    	}
    	AlternanceFactory f = new AlternanceFactory();
    	
    	DayTypeAlternance[] result;
        Date startDate = timeFrame.getUnitStart(timeUnit, unitIndex);
        Date endDate = timeFrame.getUnitFinish(timeUnit, unitIndex);
        
        if (timeUnit.equals(myTimeUnitStack.getDefaultTimeUnit())) {
            result = new DayTypeAlternance[] {f.createAlternance(timeUnit, startDate, endDate)};
        }
        else if (timeUnit.isConstructedFrom(myTimeUnitStack.getDefaultTimeUnit())) {
    		java.util.List buf = new ArrayList();
    		TimeUnit defaultUnit = myTimeUnitStack.getDefaultTimeUnit();
    		TimeFrame innerFrame = myTimeUnitStack.createTimeFrame(startDate, timeUnit, defaultUnit);
    		//System.err.println("[ChartModelImpl] topUnit="+timeUnit+" bottom="+defaultUnit+" count="+innerFrame.getUnitCount(defaultUnit));
    		for (int i=0; i<innerFrame.getUnitCount(defaultUnit); i++) {
    			Date start = innerFrame.getUnitStart(defaultUnit, i);
    			Date end = innerFrame.getUnitFinish(defaultUnit,i);
    			buf.add(f.createAlternance(defaultUnit, start, end));
    		}
    		result = (DayTypeAlternance[]) buf.toArray(new DayTypeAlternance[buf.size()]);
    	}
        else {
            throw new RuntimeException("We should not be here");
        }
    	//System.err.println("from "+startDate+" to "+endDate+"\n"+java.util.Arrays.asList(result));
        return result;
    }

    protected final ChartUIConfiguration myChartUIConfiguration;

    protected ChartUIConfiguration getChartUIConfiguration() {
        return myChartUIConfiguration;
    }

    private class RegularFramesWithFunction implements TimeFrameWidthFunction {
        public int getTimeFrameWidth(TimeFrame timeFrame) {
            return timeFrame.getUnitCount(myBottomUnit)*myAtomUnitPixels;
        }       
    }
    
    private class SkewedFramesWidthFunction implements TimeFrameWidthFunction {
        private float myWidthPerDefaultUnit;
        
        void initialize() {
            int defaultUnitsPerBottomUnit = myBottomUnit.getAtomCount(myTimeUnitStack.getDefaultTimeUnit());
            myWidthPerDefaultUnit = (float)myAtomUnitPixels/defaultUnitsPerBottomUnit;
        }
        public int getTimeFrameWidth(TimeFrame timeFrame) {
            int defaultUnitsPerTopUnit = timeFrame.getUnitCount(myTimeUnitStack.getDefaultTimeUnit());
            return (int) (defaultUnitsPerTopUnit*myWidthPerDefaultUnit);
        }
        
    }

    int getBottomUnitWidth(TimeFrame nextFrame) {
        int frameWidth = myFrameWidthFunction.getTimeFrameWidth(nextFrame);
        int bottomUnitsCount = nextFrame.getUnitCount(nextFrame.getBottomUnit());
        //System.err.println("ChartModelImpl: getBottomUnitWidth: nextFrame="+nextFrame+" width="+frameWidth+" bottomUnitsCount="+bottomUnitsCount);
        return frameWidth/bottomUnitsCount;
    }

    protected final TaskManager myTaskManager;

    protected TaskManager getTaskManager() {
        return myTaskManager;
    }

    public ChartHeader getChartHeader() {
        return myChartHeader;
    }
    
    protected ChartGridImpl getChartGrid() {
        return myChartGrid;
    }

    public float calculateLength(int fromX, int toX, int y) {
        //return toX - fromX;
        
        int curX = fromX;
        int totalPixels = toX - fromX;
        int holidayPixels = 0;
        while (curX<toX){
            GraphicPrimitiveContainer.GraphicPrimitive nextPrimitive = getChartGrid().getPrimitiveContainer().getPrimitive(curX, y - getChartUIConfiguration().getHeaderHeight());
            if (nextPrimitive instanceof GraphicPrimitiveContainer.Rectangle && GPCalendar.DayType.HOLIDAY==nextPrimitive.getModelObject()) {
                GraphicPrimitiveContainer.Rectangle nextRect = (Rectangle) nextPrimitive;
                holidayPixels += nextRect.getRightX() - curX;
                if (nextRect.myLeftX<curX) {
                    holidayPixels -= curX - nextRect.myLeftX;
                }
                if (nextRect.myLeftX<fromX) {
                    holidayPixels -= fromX - nextRect.myLeftX;
                }
                if (nextRect.getRightX()>toX) {
                    holidayPixels -= nextRect.getRightX()-toX;
                }
                curX = nextRect.getRightX()+1;
            }
            else {
                curX += getBottomUnitWidth();
            }           
        }
        float workPixels = (float)totalPixels - (float)holidayPixels;
        return workPixels/(float)getBottomUnitWidth();
    }

    public float calculateLengthNoWeekends(int fromX, int toX) {
        int totalPixels = toX - fromX;
        return totalPixels/(float)getBottomUnitWidth();        
    }
    
	public void setHeaderHeight(int i) {
		getChartUIConfiguration().setHeaderHeight(i);
	}

	private void setTopUnit(TimeUnit myTopUnit) {
		this.myTopUnit = myTopUnit;
	}

	private TimeUnit getTopUnit() {
		return getTopUnit(myStartDate);
	}
    
	private TimeUnit getTopUnit(Date startDate) {
		TimeUnit result = myTopUnit;
    	if (myTopUnit instanceof TimeUnitFunctionOfDate) {
    		if (startDate==null) {
    			throw new RuntimeException("No date is set");
    		}
    		else {
    			result = ((TimeUnitFunctionOfDate)myTopUnit).createTimeUnit(startDate);
    		}
    	}
    	return result;
	}
    
}
