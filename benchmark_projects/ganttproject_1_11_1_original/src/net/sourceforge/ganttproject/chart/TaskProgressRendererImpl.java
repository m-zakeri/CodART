/*
 * Created on 27.11.2004
 */
package net.sourceforge.ganttproject.chart;

import java.awt.Rectangle;
import java.util.List;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.GraphicPrimitive;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;

/**
 * @author bard
 */
public class TaskProgressRendererImpl extends ChartRendererBase implements TimeUnitVisitor {
	TaskProgressRendererImpl(ChartModelImpl model) {
		super(model);
	}

	public void beforeProcessingTimeFrames() {
	}

	public void afterProcessingTimeFrames() {
		getPrimitiveContainer().clear();
		List/*<Task>*/ tasks = ((ChartModelImpl)getChartModel()).getVisibleTasks();
		for (int i=0; i<tasks.size(); i++) {
			Task nextTask = (Task) tasks.get(i);
			Rectangle nextRectangle = ((ChartModelImpl)getChartModel()).getBoundingRectangle(nextTask);
			int nextProgress = nextTask.getCompletionPercentage();
			int nextProgressWidth = (int) (nextRectangle.getWidth()*nextProgress/100);
			GraphicPrimitive nextProgressRect = getPrimitiveContainer().createRectangle((int)nextRectangle.getMinX(), (int)nextRectangle.getMinY()+2, nextProgressWidth, (int)nextRectangle.getHeight()-4);
			nextProgressRect.setStyle("task.progress");
		}
	}

	public void startTimeFrame(TimeFrame timeFrame) {
	}

	public void endTimeFrame(TimeFrame timeFrame) {
	}

	public void startUnitLine(TimeUnit timeUnit) {
	}

	public void endUnitLine(TimeUnit timeUnit) {
	}

	public void nextTimeUnit(int unitIndex) {
	}

}
