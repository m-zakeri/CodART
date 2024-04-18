/*
 * Created on 17.06.2004
 *
 */
package net.sourceforge.ganttproject.chart;

import java.awt.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.Calendar;

import net.sourceforge.ganttproject.calendar.GPCalendar;
import net.sourceforge.ganttproject.calendar.GPCalendar.DayType;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Rectangle;
import net.sourceforge.ganttproject.chart.item.ChartItem;
import net.sourceforge.ganttproject.chart.item.TaskBoundaryChartItem;
import net.sourceforge.ganttproject.chart.item.TaskProgressChartItem;
import net.sourceforge.ganttproject.chart.item.TaskRegularAreaChartItem;
import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitFunctionOfDate;
import net.sourceforge.ganttproject.time.TimeUnitStack;
import net.sourceforge.ganttproject.time.gregorian.GregorianTimeUnitStack;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;

/**
 * @author bard
 *
 */
public class ChartModelImpl extends ChartModelBase implements ChartModel {
    
    private java.util.List/*<Task>*/ myVisibleTasks;
    private final TaskRendererImpl myTaskRendererImpl;
    private TaskContainmentHierarchyFacade myTaskContainment;
	private final TaskGridRendererImpl myTaskGridRendererImpl;
	private final ResourcesRendererImpl myResourcesRendererImpl;
	//private final TaskProgressRendererImpl myTaskProgressRendererImpl;
    
	public static class TuningOptions {
		private final boolean renderProgress;
		private final boolean renderDependencies;

		public TuningOptions(boolean renderProgress, boolean renderDependencies) {
			this.renderProgress = renderProgress;
			this.renderDependencies = renderDependencies;
		}
		
		public static final TuningOptions DEFAULT = new TuningOptions(true, true);
	}
	
    public ChartModelImpl(TaskManager taskManager, TimeUnitStack timeUnitStack, UIConfiguration projectConfig)  {
        super(taskManager, timeUnitStack, projectConfig);
        myTaskRendererImpl = new TaskRendererImpl(this);
        myTaskGridRendererImpl = new TaskGridRendererImpl(this);
        myResourcesRendererImpl = new ResourcesRendererImpl(this);
        //myTaskProgressRendererImpl = new TaskProgressRendererImpl(this);
        //myTimeUnitVisitors.add(myResourcesRendererImpl);
        //myTimeUnitVisitors.add(myTaskProgressRendererImpl);
        myTimeUnitVisitors.add(myTaskRendererImpl);
        myTimeUnitVisitors.add(myTaskGridRendererImpl);
    }
    
    
    protected void enableRenderers1() {
        super.enableRenderers1();
        myTaskRendererImpl.setEnabled(true);
    }
    protected void enableRenderers2() {
        super.enableRenderers2();
        myTaskRendererImpl.setEnabled(false);
    }
    
    
    protected void paintMainArea(Graphics mainArea, Painter p) {
        myTaskRendererImpl.getPrimitiveContainer().paint(p, mainArea);
        myTaskRendererImpl.getPrimitiveContainer().getLayer(1).paint(p, mainArea);
        super.paintMainArea(mainArea, p);
        myTaskRendererImpl.getPrimitiveContainer().getLayer(2).paint(p, mainArea);
        myTaskGridRendererImpl.getPrimitiveContainer().paint(p, mainArea);
    }
    public void setVisibleTasks(java.util.List/*<Task>*/ visibleTasks) {
        myVisibleTasks = visibleTasks;
    }

    public Task findTaskWithCoordinates(int x, int y) {
        GraphicPrimitiveContainer.GraphicPrimitive primitive = myTaskRendererImpl.getPrimitiveContainer().getPrimitive(x, y-getChartUIConfiguration().getHeaderHeight());
        if (primitive instanceof GraphicPrimitiveContainer.Rectangle) {
        	TaskActivity activity = (TaskActivity) primitive.getModelObject();
        	return activity==null ? null : activity.getTask();
        }
        return null;
    }
	public ChartItem getChartItemWithCoordinates(int x, int y) {
		ChartItem result = findTaskProgressItem(x,y);
		if (result==null) {
			result = findTaskBoundaryItem(x, y);
		}
        return result;
	}
	
	
    
    private ChartItem findTaskProgressItem(int x, int y) {
    	ChartItem result = null;
		GraphicPrimitiveContainer.GraphicPrimitive primitive = 
			myTaskRendererImpl.getPrimitiveContainer().getLayer(1).getPrimitive(x, y-getChartUIConfiguration().getHeaderHeight());
		if (primitive instanceof GraphicPrimitiveContainer.Rectangle) {
			GraphicPrimitiveContainer.Rectangle rect = (GraphicPrimitiveContainer.Rectangle)primitive;
			if ("task.progress.end".equals(primitive.getStyle()) && rect.getRightX()>=x-2 && rect.getRightX()<=x+2) {				
				result = new TaskProgressChartItem(x, getBottomUnitWidth(), getBottomUnit(), (Task)primitive.getModelObject());
			}
		}
		return result;
	}
	private ChartItem findTaskBoundaryItem(int x, int y) {
    	ChartItem result = null;
		GraphicPrimitiveContainer.GraphicPrimitive primitive = myTaskRendererImpl.getPrimitiveContainer().getPrimitive(x, y-getChartUIConfiguration().getHeaderHeight());
        if (primitive==null) {
            primitive = myTaskRendererImpl.getPrimitiveContainer().getLayer(2).getPrimitive(x, y-getChartUIConfiguration().getHeaderHeight()); 
        }
        if (primitive instanceof GraphicPrimitiveContainer.Rectangle) {
        	GraphicPrimitiveContainer.Rectangle rect = (Rectangle) primitive;
        	TaskActivity activity = (TaskActivity) primitive.getModelObject();
        	if (activity!=null) {
	        	if (activity.isFirst() && rect.myLeftX-2 <= x && rect.myLeftX+2>=x) {
	        		result = new TaskBoundaryChartItem(activity.getTask(), true);
	        	}
	        	if (result==null && activity.isLast() && rect.myLeftX+rect.myWidth-2 <= x && rect.myLeftX+rect.myWidth+2>=x) {
	        		result = new TaskBoundaryChartItem(activity.getTask(), false);
	        	}
	        	if (result==null) {
	        		result = new TaskRegularAreaChartItem(activity.getTask());
	        	}
        	}
        }
		return result;
	}
	public java.awt.Rectangle getBoundingRectangle(Task task) {
    	java.awt.Rectangle result = null;
    	TaskActivity[] activities = task.getActivities();
    	for (int i=0; i<activities.length; i++) {
    		GraphicPrimitiveContainer.Rectangle nextRectangle = (GraphicPrimitiveContainer.Rectangle) myTaskRendererImpl.getPrimitiveContainer().getPrimitive(activities[i]);
    		if (nextRectangle!=null) {
	    		java.awt.Rectangle nextAwtRectangle = new java.awt.Rectangle(nextRectangle.myLeftX, nextRectangle.myTopY, nextRectangle.myWidth, nextRectangle.myHeight);
	    		if (result==null) {
	    			result = nextAwtRectangle;
	    		}
	    		else {
	    			result = result.union(nextAwtRectangle);
	    		}
    		}
    	}
    	return result;
    }
	
    java.util.List/*<Task>*/ getVisibleTasks() {
        return myVisibleTasks;
    }


	/* (non-Javadoc)
	 * @see net.sourceforge.ganttproject.chart.ChartModel#setTaskContainment(net.sourceforge.ganttproject.task.TaskContainmentHierarchyFacade)
	 */
	public void setTaskContainment(TaskContainmentHierarchyFacade taskContainment) {
		myTaskContainment = taskContainment;
	}
	
	TaskContainmentHierarchyFacade getTaskContainment() {
		return myTaskContainment;
	}
	
	public void setTuningOptions(TuningOptions tuningOptions) {
		myTaskRendererImpl.setProgressRenderingEnabled(tuningOptions.renderProgress);
		myTaskRendererImpl.setDependenciesRenderingEnabled(tuningOptions.renderDependencies);
	}
	
}
