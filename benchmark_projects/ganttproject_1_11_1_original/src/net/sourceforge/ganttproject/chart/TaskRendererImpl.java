package net.sourceforge.ganttproject.chart;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.GraphicPrimitive;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Rectangle;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.task.algorithm.SortTasksAlgorithm;
import net.sourceforge.ganttproject.task.dependency.TaskDependency;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.task.TaskLength;

import java.awt.Dimension;
import java.awt.Point;
import java.util.*;


/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class TaskRendererImpl extends ChartRendererBase implements TimeUnitVisitor{
    private List/*<TaskActivity>*/ myVisibleActivities;
    private static final SortTasksAlgorithm ourAlgorithm = new SortTasksAlgorithm();
    private List/*<TaskActivity>*/ myCurrentlyProcessed = new ArrayList();
    private Map/*<TaskActivity,Integer>*/ myActivity2ordinalNumber = new HashMap();
    private Map/*<Task, Integer>*/ myTask_WorkingRectanglesLength = new HashMap();
    private int myPosX;
    private TimeFrame myCurrentTimeFrame;
    private TimeUnit myCurrentUnit;
	private Date myUnitStart;
	private boolean myProgressRenderingEnabled = true;
	private boolean myDependenciesRenderingEnabled = true;
	private GraphicPrimitiveContainer myRegularTaskContainer = new GraphicPrimitiveContainer();
    
    public TaskRendererImpl(ChartModelImpl model) {
        super(model);
        getPrimitiveContainer().newLayer();
        getPrimitiveContainer().newLayer();
    }

    public void beforeProcessingTimeFrames() {
        getPrimitiveContainer().clear();
        getPrimitiveContainer().getLayer(1).clear();
        getPrimitiveContainer().getLayer(2).clear();
        myActivity2ordinalNumber.clear();
        myTask_WorkingRectanglesLength.clear();
        myVisibleActivities = getSortedTaskActivities();
        myCurrentlyProcessed.clear();
        myPosX = 0;
    }

	public void afterProcessingTimeFrames() {
		if (myDependenciesRenderingEnabled) {
			createDependencyLines();
		}
	}

	private List/*<Task>*/ getSortedTaskActivities() {
        List visibleTasks = ((ChartModelImpl)getChartModel()).getVisibleTasks();
        List visibleActivities = new ArrayList();
        myActivity2ordinalNumber.clear();
        for (int i=0; i<visibleTasks.size(); i++) {
        	Task nextTask = (Task) visibleTasks.get(i);
        	Integer nextOrdinal = new Integer(i);
        	TaskActivity[] activities = nextTask.getActivities();
        	//System.err.println("[TaskRendererImpl] task="+nextTask+"\nactivities="+Arrays.asList(activities));
        	for (int j=0; j<activities.length; j++) {
                myActivity2ordinalNumber.put(activities[j], nextOrdinal);
                visibleActivities.add(activities[j]);
        	}
        	float totalTaskLength = nextTask.getDuration().getLength(getChartModel().getBottomUnit())*getChartModel().getBottomUnitWidth();
        	myTask_WorkingRectanglesLength.put(nextTask, new Long((long)(totalTaskLength*nextTask.getCompletionPercentage()/100)));
        }
        ourAlgorithm.sortByStartDate(visibleActivities);
        return visibleActivities;
    }

    public void startTimeFrame(TimeFrame timeFrame) {
        myCurrentTimeFrame = timeFrame;
    }

    public void endTimeFrame(TimeFrame timeFrame) {
        myCurrentTimeFrame = null;
    }

    public void startUnitLine(TimeUnit timeUnit) {
        if (myCurrentTimeFrame.getBottomUnit()==timeUnit) {
            myCurrentUnit = timeUnit;
        }
    }

    public void endUnitLine(TimeUnit timeUnit) {
        myCurrentUnit = null;
    }

    public void nextTimeUnit(int unitIndex) {
        if (myCurrentUnit!=null) {
            Date unitStart = myCurrentTimeFrame.getUnitStart(myCurrentUnit, unitIndex);
            Date unitFinish = myCurrentTimeFrame.getUnitFinish(myCurrentUnit, unitIndex);
            myUnitStart = unitStart;
            pullQueue(unitStart, unitFinish);
            //System.err.println("[TaskRendererImpl] nextTimeUnit(): unitStart="+unitStart+" posX="+myPosX);
            //if (!myCurrentlyProcessed.isEmpty()) {
            //    System.err.println("[TaskRendererImpl] nextTimeUnit(): processing:"+myCurrentlyProcessed);
            //}
            for (Iterator startedActivities = myCurrentlyProcessed.iterator(); startedActivities.hasNext();startedActivities.remove())  {
                TaskActivity nextStarted = (TaskActivity) startedActivities.next();
                processActivity(nextStarted);
            }        
            myPosX+=getChartModel().getBottomUnitWidth();
        }
    }

    private void processActivity(TaskActivity nextStarted) {
        if (nextStarted.isLast()) {
        	processLastActivity(nextStarted);
        }
        else if (nextStarted.isFirst()) {
        	processFirstActivity(nextStarted);
        }
        else {
        	processRegularActivity(nextStarted);
        }
    }
    
	private Rectangle processRegularActivity(TaskActivity nextStarted) {
        Task nextTask = nextStarted.getTask();
        boolean nextHasNested = ((ChartModelImpl)getChartModel()).getTaskContainment().getNestedTasks(nextTask).length>0;
        if (nextTask.isMilestone() && !nextStarted.isFirst()) {
            return null;
        }
        java.awt.Rectangle nextBounds = getBoundingRectangle(nextStarted);
        int nextLength = (int)nextBounds.width;
        int topy = nextBounds.y;
    
        int posX = myPosX;
        GraphicPrimitiveContainer.Rectangle nextRectangle;
        //if (nextStarted.getStart().compareTo(myUnitStart)>=0) {
        	TaskLength deltaLength = nextTask.getManager().createLength(getChartModel().getTimeUnitStack().getDefaultTimeUnit(), myUnitStart, nextStarted.getStart());
        	
        	int deltaX = (int) (deltaLength.getLength(myCurrentUnit)*getChartModel().getBottomUnitWidth());
        	posX += deltaX;
        	//System.err.println("[TaskRendererImpl] myUnitStart="+myUnitStart+" nextActivity="+nextStarted+" deltaX="+deltaX+" deltaLength="+deltaLength.getLength(myCurrentUnit));
        //}
//        else {
//        	nextRectangle = getPrimitiveContainer().createRectangle(myPosX+getChartModel().getBottomUnitWidth()-nextLength, topy, nextLength, getRowHeight()*3/5);
//        }
            
            GraphicPrimitiveContainer container = nextHasNested ? getPrimitiveContainer().getLayer(2) : getPrimitiveContainer();
    	nextRectangle = container.createRectangle(posX, topy, (int)nextLength, getRowHeight()*3/5);
        //System.err.println("task="+nextStarted.getTask()+" nested tasks length="+nextStarted.getTask().getNestedTasks().length);
        if (nextStarted.getTask().isMilestone()) {
        	nextRectangle.setStyle("task.milestone");
        }
        else if (nextHasNested) {
       		nextRectangle.setStyle("task.supertask");
       		if (nextStarted.isFirst()) {
       			GraphicPrimitiveContainer.Rectangle supertaskStart =  container.createRectangle(nextRectangle.myLeftX, topy, (int)nextLength, getRowHeight()*3/5);
       			supertaskStart.setStyle("task.supertask.start");
       		}
       		if (nextStarted.isLast()) {
       			GraphicPrimitiveContainer.Rectangle supertaskEnd =  container.createRectangle(posX, topy, (int)nextLength, getRowHeight()*3/5); // JA (added -1)
       			supertaskEnd.setStyle("task.supertask.end");
       			
       		}
        }
        else if (nextStarted.getIntensity()==0f) {
        	nextRectangle.setStyle("task.holiday");
        }
        else {
            nextRectangle.setStyle("task");
            if (myProgressRenderingEnabled) {
            	renderProgressBar(nextTask, nextRectangle);
            }
        }
        if (!"task.holiday".equals(nextRectangle.getStyle()) && !"task.supertask".equals(nextRectangle.getStyle())) {            	
        	nextRectangle.setBackgroundColor(nextStarted.getTask().getColor());
        }
        container.bind(nextRectangle, nextStarted);
        return nextRectangle;
	}

	private void renderProgressBar(Task nextTask, GraphicPrimitiveContainer.Rectangle nextActivityRectangle) {
		int nextLength = nextActivityRectangle.myWidth;
		Long workingRectanglesLength = (Long) myTask_WorkingRectanglesLength.get(nextTask);
		if (workingRectanglesLength!=null) {
			long nextProgressLength = nextLength;
			String style;
			if (workingRectanglesLength.longValue()>nextLength) {
				myTask_WorkingRectanglesLength.put(nextTask, new Long(workingRectanglesLength.longValue()-nextLength));
				style = "task.progress";
			}
			else {
				nextProgressLength = workingRectanglesLength.longValue();
				myTask_WorkingRectanglesLength.remove(nextTask);
				style = "task.progress.end";
			}
			int nextMidY = nextActivityRectangle.getMiddleY();
			GraphicPrimitive nextProgressRect = getPrimitiveContainer().getLayer(1).createRectangle(nextActivityRectangle.myLeftX, nextMidY-1, (int)nextProgressLength, 3);
			nextProgressRect.setStyle(style);
			getPrimitiveContainer().getLayer(1).bind(nextProgressRect, nextTask);
		}
	}

	private void processFirstActivity(TaskActivity taskActivity) {
        boolean stop = taskActivity.getIntensity()==0f;
		if (!stop) {
			processRegularActivity(taskActivity);
		}
	}

	private void processLastActivity(TaskActivity taskActivity) {
        java.awt.Rectangle bounds = getBoundingRectangle(taskActivity);
		if (taskActivity.getIntensity()!=0f) {
			processRegularActivity(taskActivity);            
		}		        
        if (taskActivity.getTask().isMilestone()) {
            return;
        }            
        int xText = (int)bounds.getMaxX()+9;
        int yText = (int) bounds.getCenterY()+3;
        getPrimitiveContainer().getLayer(2).createText(xText, yText, getTaskLabel(taskActivity.getTask()));
	}
	
	private String getTaskLabel(Task task) {
		StringBuffer result = new StringBuffer();
		if (myProgressRenderingEnabled) {
			result.append("[ ");
			result.append(task.getCompletionPercentage()+"%");
			result.append(" ] ");
		}
		ResourceAssignment[] assignments = task.getAssignments();
		if (assignments.length>0) {
			for (int i=0; i<assignments.length; i++) {
				result.append(assignments[i].getResource().getName());
				if (i<assignments.length-1) {
					result.append(",");
				}
			}
		}
		return result.toString();
	}
    
    private java.awt.Rectangle getBoundingRectangle(TaskActivity activity) {
    	//System.err.println("[TaskRendererImpl] activity="+activity+"\nstartDate="+myUnitStart+"\nduration="+activity.getDuration().getLength(myCurrentUnit));
    	int posX = myPosX;
        if (activity.getStart().compareTo(myUnitStart)>=0) {
        	TaskLength deltaLength = activity.getTask().getManager().createLength(getChartModel().getTimeUnitStack().getDefaultTimeUnit(), myUnitStart, activity.getStart());
        	
        	int deltaX = (int) (deltaLength.getLength(myCurrentUnit)*getChartModel().getBottomUnitWidth());
        	posX += deltaX;
        }
        int length = (int)(activity.getDuration().getLength(myCurrentUnit)*getChartModel().getBottomUnitWidth());
        Integer nextOrdNumber = (Integer)myActivity2ordinalNumber.get(activity);
        int topy = nextOrdNumber.intValue()*getRowHeight() + 4; // JA Added 4 so that it draws in middle of row
        return new java.awt.Rectangle(posX, topy, length, getRowHeight());
    }

	private void createDependencyLines() {
		List/*<DependencyDrawData>*/ dependencyDrawData = prepareDependencyDrawData();
		drawDependencies(dependencyDrawData);
	}
    
    /**
	 * @param dependencyDrawData
	 */
	private void drawDependencies(List dependencyDrawData) {
        GraphicPrimitiveContainer primitiveContainer = getPrimitiveContainer().getLayer(2);
        int arrowLength = 7;
		for (int i=0; i<dependencyDrawData.size(); i++) {
			DependencyDrawData next = (DependencyDrawData)dependencyDrawData.get(i);
            if (next.myDependeeVector.reaches(next.myDependantVector.getPoint())) {
                // when dependee.end <= dependant.start && dependency.type is any
                // or dependee.end <= dependant.end && dependency.type==FF
                // or dependee.start >= dependant.end && dependency.type==SF
                int ysign = signum(next.myDependantVector.getPoint().y - next.myDependeeVector.getPoint().y);
            	Point first =new Point(next.myDependeeVector.getPoint().x, next.myDependeeVector.getPoint().y);
            	Point second= new Point(next.myDependantVector.getPoint(-3).x, next.myDependeeVector.getPoint().y);
                Point third = new Point(next.myDependantVector.getPoint(-3).x, next.myDependantVector.getPoint().y);
                java.awt.Rectangle arrowBoundary = null;
                String style;
                if (next.myDependantVector.reaches(third)){
                    second.x += arrowLength;
                    third.x += arrowLength;
                	Point forth = next.myDependantVector.getPoint();
                	primitiveContainer.createLine(third.x,third.y,forth.x,forth.y);
                    arrowBoundary = new java.awt.Rectangle(forth.x, forth.y-3, arrowLength, 6);
                    style = "dependency.arrow.left";
                }
                else {
                    third.y -= ysign*next.myDependantRectangle.myHeight/2;
                    arrowBoundary = new java.awt.Rectangle(third.x-3, third.y - (ysign>0 ? ysign*arrowLength : 0), 6, arrowLength);
                    style = ysign>0 ? "dependency.arrow.down" : "dependency.arrow.up";
                }
                primitiveContainer.createLine(first.x,first.y,second.x,second.y);
                primitiveContainer.createLine(second.x,second.y,third.x,third.y);
                if (arrowBoundary!=null) {
                    Rectangle arrow=primitiveContainer.createRectangle(arrowBoundary.x, arrowBoundary.y, arrowBoundary.width, arrowBoundary.height);
                    arrow.setStyle(style);
                }
            }
            else {
            	Point first = next.myDependeeVector.getPoint(3);
            	if (next.myDependantVector.reaches(first)) {
            		Point second = new Point(first.x, next.myDependantVector.getPoint().y);            		
                	primitiveContainer.createLine(next.myDependeeVector.getPoint().x, next.myDependeeVector.getPoint().y, first.x, first.y);
                	primitiveContainer.createLine(first.x, first.y, second.x, second.y);
                	primitiveContainer.createLine(second.x, second.y, next.myDependantVector.getPoint().x, next.myDependantVector.getPoint().y);
                	int xsign = signum(next.myDependantVector.getPoint().x-second.x);
                	java.awt.Rectangle  arrowBoundary = new java.awt.Rectangle(next.myDependantVector.getPoint(7).x, next.myDependantVector.getPoint().y-3, xsign*7, 6);
                	Rectangle arrow=primitiveContainer.createRectangle(arrowBoundary.x, arrowBoundary.y, arrowBoundary.width, arrowBoundary.height);
                	arrow.setStyle(xsign<0?"dependency.arrow.left":"dependency.arrow.right");
            	}
            	else {
	            	Point forth = next.myDependantVector.getPoint(3);
	            	Point second = new Point(first.x, (first.y+forth.y)/2);
	            	Point third = new Point(forth.x, (first.y+forth.y)/2);
	            	primitiveContainer.createLine(next.myDependeeVector.getPoint().x, next.myDependeeVector.getPoint().y, first.x, first.y);
	            	primitiveContainer.createLine(first.x, first.y, second.x, second.y);
	            	primitiveContainer.createLine(second.x, second.y, third.x, third.y);
	            	primitiveContainer.createLine(third.x, third.y, forth.x, forth.y);
	            	primitiveContainer.createLine(forth.x, forth.y, next.myDependantVector.getPoint().x, next.myDependantVector.getPoint().y);
            	}
            }
		}
	}
    
    private int signum(int value) {
        if (value==0) {
            return 0;
        }
        return value<0 ? -1 : 1;
    }

	/**
	 * @return
	 */
	private List prepareDependencyDrawData() {
		List result = new ArrayList();
		List/*<Task>*/ visibleTasks = ((ChartModelImpl)getChartModel()).getVisibleTasks();
		for (int i=0; i<visibleTasks.size(); i++) {
			Task nextTask = (Task) visibleTasks.get(i);
			prepareDependencyDrawData(nextTask, result);
		}
		return result;
	}

	private void prepareDependencyDrawData(Task task, List result) {
		TaskDependency[] deps = task.getDependencies().toArray();
		for (int i=0; i<deps.length; i++) {
			TaskDependency next = deps[i];
			TaskDependency.ActivityBinding activityBinding = next.getActivityBinding();
			TaskActivity dependant = activityBinding.getDependantActivity();            
			GraphicPrimitiveContainer.Rectangle dependantRectangle = (Rectangle) getPrimitiveContainer().getPrimitive(dependant);
			if (dependantRectangle==null) {
				continue;
			}
			TaskActivity dependee = activityBinding.getDependeeActivity();            
			GraphicPrimitiveContainer.Rectangle dependeeRectangle = (Rectangle) getPrimitiveContainer().getPrimitive(dependee);
			if (dependeeRectangle==null) {
				continue;
			}
            Date[] bounds = activityBinding.getAlignedBounds();
            PointVector dependantVector;
            if (bounds[0].equals(dependant.getStart())) {
                dependantVector = new WestPointVector(new Point(dependantRectangle.myLeftX, dependantRectangle.getMiddleY()));
            }
            else if (bounds[0].equals(dependant.getEnd())) {
                dependantVector = new EastPointVector(new Point(dependantRectangle.getRightX(), dependantRectangle.getMiddleY()));
            }
            else {
                throw new RuntimeException();
            }
            //
            PointVector dependeeVector;
            if (bounds[1].equals(dependee.getStart())) {
                dependeeVector = new WestPointVector(new Point(dependeeRectangle.myLeftX, dependeeRectangle.getMiddleY()));
            }
            else if (bounds[1].equals(dependee.getEnd())) {
                dependeeVector = new EastPointVector(new Point(dependeeRectangle.getRightX(), dependeeRectangle.getMiddleY()));
            }
            else {
                throw new RuntimeException();
            }            
			DependencyDrawData data = new DependencyDrawData(next, dependantRectangle, dependeeRectangle, dependantVector, dependeeVector);
			result.add(data);
		}
	}

	private int getRowHeight() {
        return getConfig().getRowHeight();
    }

    private void pullQueue(Date unitStart, Date unitFinish) {
        for (Iterator activities = myVisibleActivities.iterator(); activities.hasNext();) {
            TaskActivity next = (TaskActivity) activities.next();
            if (next.getStart().after(unitFinish)) {
                break;
            }
            if (next.getStart().compareTo(unitStart)>=0 && next.getStart().compareTo(unitFinish)<0 ||
            	next.getEnd().compareTo(unitStart)>=0 && next.getEnd().compareTo(unitFinish)<0) {
                myCurrentlyProcessed.add(next);
                activities.remove();
            }
        }
    }

    private static class DependencyDrawData {
    	final GraphicPrimitiveContainer.Rectangle myDependantRectangle;
    	final GraphicPrimitiveContainer.Rectangle myDependeeRectangle;
    	final TaskDependency myDependency;
        final PointVector myDependantVector;
        final PointVector myDependeeVector;
    	
		public DependencyDrawData(TaskDependency dependency, GraphicPrimitiveContainer.GraphicPrimitive dependantPrimitive, GraphicPrimitiveContainer.GraphicPrimitive dependeePrimitive, PointVector dependantVector, PointVector dependeeVector) {
			myDependency = dependency;
			myDependantRectangle = (GraphicPrimitiveContainer.Rectangle)dependantPrimitive;
			myDependeeRectangle = (GraphicPrimitiveContainer.Rectangle)dependeePrimitive;
			myDependantVector = dependantVector;
            myDependeeVector = dependeeVector;
		}
        
        public String toString() {
            return "From activity="+myDependency.getActivityBinding().getDependantActivity()+" (vector="+myDependantVector+")\n to activity="+myDependency.getActivityBinding().getDependeeActivity()+" (vector="+myDependeeVector;
        }
    }
    
    private static abstract class PointVector {
        private final Point myPoint;
        protected PointVector(Point point) {
            myPoint = point;
        }
		Point getPoint() {
            return myPoint;
        }
        abstract boolean reaches(Point targetPoint);
        abstract Point getPoint(int i);
    }
    
    private static class WestPointVector extends PointVector {
        protected WestPointVector(Point point) {
            super(point);
        }

        boolean reaches(Point targetPoint) {
            return targetPoint.x <= getPoint().x;
        }

		Point getPoint(int diff) {
			return new Point(getPoint().x-diff, getPoint().y);
		}
        
        public String toString() {
            return "<="+getPoint().toString();
        }
        
    }
    
    private static class EastPointVector extends PointVector {
        protected EastPointVector(Point point) {
            super(point);
        }

        boolean reaches(Point targetPoint) {
            return targetPoint.x>=getPoint().x;
        }

		Point getPoint(int diff) {
			return new Point(getPoint().x+diff, getPoint().y);
		}
        
        public String toString() {
            return ">="+getPoint().toString();
        }
        
        
    }

	public void setProgressRenderingEnabled(boolean renderProgress) {
		myProgressRenderingEnabled = renderProgress;
	}

	public void setDependenciesRenderingEnabled(boolean renderDependencies) {
		myDependenciesRenderingEnabled = renderDependencies;
	}
    
}
