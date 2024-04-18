package net.sourceforge.ganttproject.chart;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Rectangle;
import net.sourceforge.ganttproject.resource.LoadDistribution;
import net.sourceforge.ganttproject.resource.ProjectResource;
import net.sourceforge.ganttproject.resource.LoadDistribution.Load;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;

public class ResourceLoadRenderer extends ChartRendererBase implements TimeUnitVisitor {

    private TimeFrame myCurrentFrame;
    private TimeUnit myCurrentUnit;
    private List myDistributions;
    public ResourceLoadRenderer(ChartModelResource model) {
        super(model);
    }

    public void beforeProcessingTimeFrames() {
        myDistributions = new ArrayList();
        getPrimitiveContainer().clear();
        ProjectResource[] resources = ((ChartModelResource)getChartModel()).getVisibleResources();
        //Set assignedTasks = new HashSet();
        for (int i=0; i<resources.length; i++) {
        	ProjectResource nextResource = resources[i];
            LoadDistribution nextDistribution = new LoadDistribution(nextResource, getChartModel().getStartDate(),getChartModel().getTimeUnitStack(), getChartModel().getTaskManager());
            myDistributions.add(nextDistribution);
        }   
        
    }

    public void afterProcessingTimeFrames() {
        
    }

    public void startTimeFrame(TimeFrame timeFrame) {
        myCurrentFrame = timeFrame;
    }

    public void endTimeFrame(TimeFrame timeFrame) {
        myCurrentFrame = null;
    }

    public void startUnitLine(TimeUnit timeUnit) {
        if (timeUnit==myCurrentFrame.getBottomUnit()) {
            myCurrentUnit = timeUnit;
        }
    }

    public void endUnitLine(TimeUnit timeUnit) {
        myCurrentUnit = null;
    }

    public void nextTimeUnit(int unitIndex) {
        if (myCurrentUnit!=null && myDistributions!=null) {
            Date unitStart = myCurrentFrame.getUnitStart(myCurrentUnit, unitIndex);
            for (int i=0; i<myDistributions.size(); i++) {
                LoadDistribution next = (LoadDistribution) myDistributions.get(i);
                getLoadRectangles(next.getLoads(), unitStart, i*getConfig().getRowHeight());
            }
            myDistributions = null;
            //Date unitFinish = myCurrentFrame.getUnitFinish(myCurrentUnit, unitIndex);
        }
    }

    private List getLoadRectangles(List myLoads, Date realStart, int myPosY) {
        TimeUnit currentUnit = getChartModel().getBottomUnit();
		List result = new ArrayList(myLoads.size());
		//int startX = myPosX;
		String suffix = "";
		//System.err.println("[ResourceLoadRenderer] getLoadRectangles: realStart="+realStart+" viewStart="+getChartModel().getStartDate());
		for (int i=1; i<myLoads.size(); i++) {
			Load curLoad = (Load) myLoads.get(i);
			Load prevLoad = (Load) myLoads.get(i-1);
			int prevEndX = (int) (curLoad.startDelta.getLength(currentUnit)*getChartModel().getBottomUnitWidth());
			//System.err.println("[LoadDistribution] getRectangles: curLoad="+curLoad+" prevLoad="+prevLoad+" prevEndX="+prevEndX);
            //Rectangle prevRect = (Rectangle) myResource2rect.remove(myResource);
			if (prevLoad.load>0) {
				int prevStartX = (int)(prevLoad.startDelta.getLength(currentUnit)*getChartModel().getBottomUnitWidth());
				int width = prevEndX -prevStartX;
                TaskLength visibleOffset = getChartModel().getTaskManager().createLength(getChartModel().getTimeUnitStack().getDefaultTimeUnit(), realStart,getChartModel().getStartDate() );
                //System.err.println("[ResourceLoadRenderer] getLoadRectangles: visibleOffset="+visibleOffset);
                prevStartX += (int) (visibleOffset.getLength(currentUnit)*getChartModel().getBottomUnitWidth());
                //System.err.println("[LoadDistribution] getRectangles(): realStart="+realStart+" chartmodelstart="+getChartModel().getStartDate()+" offset="+visibleOffset+" startx="+prevStartX);
				Rectangle nextRect = getPrimitiveContainer().createRectangle(prevStartX, myPosY, width, getConfig().getRowHeight());
                suffix += curLoad.load==0 ? ".last" : "";
                //if (prevRect==null) {
                //	suffix = ".first";
                //}
                //myResource2rect.put(myResource, nextRect);
                String style = (prevLoad.load<=100f ? "load.normal" : "load.overload")+suffix;
                nextRect.setStyle(style);
                result.add(nextRect);
                suffix = "";
			}
            else if (curLoad.load>0){
                suffix = ".first";
            	//prevRect.setStyle(prevRect.getStyle()+".last");
            }
            //startX = myPosX + deltaX;
		}
		return result;
	}

}
