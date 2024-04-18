/*
 * Created on 13.11.2004
 */
package net.sourceforge.ganttproject.chart;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Line;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitText;

/**
 * @author bard
 */
public class BottomUnitLineRendererImpl extends ChartRendererBase implements TimeUnitVisitor {

	private TimeFrame myCurrentTimeFrame;
	private boolean areUnitsAccepted;
	private BottomUnitGridBuilder myBottomUnitGridBuilder;
	private int posX;
	
	public BottomUnitLineRendererImpl(ChartModelBase model) {
		super(model);
		myBottomUnitGridBuilder = new BottomUnitGridBuilder(model);
		// TODO Auto-generated constructor stub
	}

	public void beforeProcessingTimeFrames() {
		getPrimitiveContainer().clear();
		posX = 0;
	}

	public void afterProcessingTimeFrames() {
	}

	public void startTimeFrame(TimeFrame timeFrame) {
		myCurrentTimeFrame = timeFrame;
	}

	public void endTimeFrame(TimeFrame timeFrame) {
        posX+=myBottomUnitGridBuilder.getWidth();
		myCurrentTimeFrame = null;
	}

	public void startUnitLine(TimeUnit timeUnit) {
		if (timeUnit==myCurrentTimeFrame.getBottomUnit()) {
            myBottomUnitGridBuilder.beforeProcessingGrid(posX);
			areUnitsAccepted = true;
		}
	}

	public void endUnitLine(TimeUnit timeUnit) {
        if (areUnitsAccepted) {
            myBottomUnitGridBuilder.afterProcessingGrid();
        }
		areUnitsAccepted = false;
	}

	public void nextTimeUnit(int unitIndex) {
		if (areUnitsAccepted) {
            myBottomUnitGridBuilder.visitUnit(myCurrentTimeFrame, unitIndex);			
		}
	}

    class BottomUnitGridBuilder {
        final int totalWidth = getWidth();
        //final int topUnitHeight;
        //final int bottomY;
        //final int bottomUnitWidth;
        final ChartUIConfiguration config;
        int myWidth=0;
        int myPosX;
        private int myPosFrameStart;

        /**
		 * 
		 */
		public BottomUnitGridBuilder(ChartModelBase chartModel) {
			//bottomUnitWidth = chartModel.getBottomUnitWidth();
			config = chartModel.getChartUIConfiguration();
		}
        void beforeProcessingGrid(int posFrameStart) {
            myWidth =0;
            myPosX = posFrameStart;
            myPosFrameStart = posFrameStart;
        }

        void visitUnit(TimeFrame currentFrame, int unitIndex) {
			int topUnitHeight = config.getSpanningHeaderHeight();
			int bottomY = topUnitHeight*2 - 1;
            GraphicPrimitiveContainer.Line nextLine = getPrimitiveContainer().createLine(myPosX, topUnitHeight, myPosX, bottomY);
            nextLine.setForegroundColor(config.getBottomUnitGridColor());
            //
            TimeUnitText timeUnitText = currentFrame.getUnitText(currentFrame.getBottomUnit(), unitIndex);
            String unitText = currentFrame.getUnitText(currentFrame.getBottomUnit(), unitIndex).getText(-1);
            GraphicPrimitiveContainer.Text nextText = getPrimitiveContainer().createText(myPosX+2, bottomY-7, unitText);
            nextText.setMaxLength(getChartModel().getBottomUnitWidth(currentFrame));
            nextText.setFont(config.getBottomUnitFont());
            myPosX+=getChartModel().getBottomUnitWidth(currentFrame);
            getPrimitiveContainer().bind(nextText,timeUnitText);
        }

        void afterProcessingGrid() {
            myWidth = myPosX - myPosFrameStart;
//            Line nextLine = getPrimitiveContainer().createLine(myPosX, 0, myPosX, bottomY);
//            nextLine.setForegroundColor(config.getBottomUnitGridColor());
        }

//        void createBottomUnitGrid(int posFrameStart, TimeFrame timeFrame) {
//            myWidth = 0;
//            int posX = posFrameStart;
//            for (int j=0; j<timeFrame.getUnitCount(timeFrame.getBottomUnit()); j++) {
//                if (posX>totalWidth) {
//                    break;
//                }
//                GraphicPrimitiveContainer.Line nextLine = getPrimitiveContainer().createLine(posX, topUnitHeight, posX, bottomY);
//                nextLine.setForegroundColor(config.getBottomUnitGridColor());
//                //
//                String unitText = timeFrame.getUnitText(timeFrame.getBottomUnit(), j);
//                GraphicPrimitiveContainer.Text nextText = getPrimitiveContainer().createText(posX+2, bottomY-7, unitText);
//                nextText.setFont(config.getBottomUnitFont());
//                posX+=bottomUnitWidth;
//            }
//            myWidth = posX - posFrameStart;
//        }

        int getWidth() {
            return myWidth;
        }
    }
	
}
