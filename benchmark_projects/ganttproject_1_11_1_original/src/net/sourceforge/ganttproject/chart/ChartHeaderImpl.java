    /*
 * Created on 17.06.2004
 *
 */
package net.sourceforge.ganttproject.chart;

import java.awt.Graphics;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.GraphicPrimitive;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Line;
import net.sourceforge.ganttproject.time.TimeFrame;
import net.sourceforge.ganttproject.time.TimeUnit;
import net.sourceforge.ganttproject.time.TimeUnitText;

/**
 * @author bard
 *
 */
public class ChartHeaderImpl extends ChartRendererBase implements ChartHeader, TimeUnitVisitor {

    private final GraphicPrimitiveContainer myPrimitiveContainer;
    private PrimitivesBuilder myPrimitivesBuilder;

    public ChartHeaderImpl(ChartModelBase model) {
    	super(model);
        myPrimitiveContainer = new GraphicPrimitiveContainer();
    }

    public GraphicPrimitiveContainer getPrimitiveContainer() {
        return myPrimitiveContainer;
    }
    public void beforeProcessingTimeFrames() {
        myPrimitiveContainer.clear();
        createGreyRectangleWithNiceBorders();
        myPrimitivesBuilder = new PrimitivesBuilder();
    }

    public void startTimeFrame(TimeFrame timeFrame) {
        myPrimitivesBuilder.startTimeFrame(timeFrame);
    }

    public void endTimeFrame(TimeFrame timeFrame) {
        myPrimitivesBuilder.endTimeFrame(timeFrame);
    }

    public void startUnitLine(TimeUnit timeUnit) {
        myPrimitivesBuilder.startUnitLine(timeUnit);
    }

    public void endUnitLine(TimeUnit timeUnit) {
        myPrimitivesBuilder.endUnitLine(timeUnit);
    }

    public void nextTimeUnit(int unitIndex) {
        myPrimitivesBuilder.nextTimeUnit(unitIndex);
    }

	private void createGreyRectangleWithNiceBorders() {
        int sizex = getWidth();
        int sizey = getHeight();        
        int spanningHeaderHeight = getChartModel().getChartUIConfiguration().getSpanningHeaderHeight();
        
        GraphicPrimitiveContainer.Rectangle headerRectangle = myPrimitiveContainer.createRectangle(0, 0, sizex, spanningHeaderHeight*2);
        headerRectangle.setBackgroundColor(getChartModel().getChartUIConfiguration().getSpanningHeaderBackgroundColor());
        //
        GraphicPrimitiveContainer.Rectangle spanningHeaderBorder = myPrimitiveContainer.createRectangle(0, 0, sizex-1, spanningHeaderHeight);
        spanningHeaderBorder.setForegroundColor(getChartModel().getChartUIConfiguration().getHeaderBorderColor());
        //
        GraphicPrimitiveContainer.Rectangle timeunitHeaderBorder = myPrimitiveContainer.createRectangle(0, spanningHeaderHeight, sizex-1, spanningHeaderHeight);
        timeunitHeaderBorder.setForegroundColor(getChartModel().getChartUIConfiguration().getHeaderBorderColor());
        //
        GraphicPrimitiveContainer.Line middleGutter1 = myPrimitiveContainer.createLine(1, spanningHeaderHeight-1, sizex-2, spanningHeaderHeight-1);
        middleGutter1.setForegroundColor(getChartModel().getChartUIConfiguration().getHorizontalGutterColor1());
        //
        GraphicPrimitiveContainer.Line bottomGutter = myPrimitiveContainer.createLine(0, spanningHeaderHeight*2-2, sizex-2, spanningHeaderHeight*2-2);
        bottomGutter.setForegroundColor(getChartModel().getChartUIConfiguration().getHorizontalGutterColor1());
        //
        GraphicPrimitiveContainer.Line topGutter = myPrimitiveContainer.createLine(1, 1, sizex - 2, 1);
        topGutter.setForegroundColor(getChartModel().getChartUIConfiguration().getHorizontalGutterColor2());
        //
        GraphicPrimitiveContainer.Line middleGutter2 = myPrimitiveContainer.createLine(0, spanningHeaderHeight+1, sizex-2, spanningHeaderHeight+1);
        topGutter.setForegroundColor(getChartModel().getChartUIConfiguration().getHorizontalGutterColor2());		
	}

    private class PrimitivesBuilder {
        final int totalWidth = getWidth();
        int bottomUnitWidth;
        final ChartUIConfiguration config = getChartModel().getChartUIConfiguration();
        int posX;
        TopUnitTextBuilder myTopUnitTextBuilder;
        BottomUnitGridBuilder myBottomUnitGridBuilder;
        private TimeFrame myCurrentFrame;
        private boolean areUnitsAccepted;

        private PrimitivesBuilder() {
            myTopUnitTextBuilder = new TopUnitTextBuilder();
            myBottomUnitGridBuilder = new BottomUnitGridBuilder();
        }

        void startTimeFrame(TimeFrame nextFrame) {
            myCurrentFrame = (posX>totalWidth)  ? null : nextFrame;
            bottomUnitWidth = getChartModel().getBottomUnitWidth(nextFrame);
            //myBottomUnitGridBuilder.createBottomUnitGrid(posX, nextFrame);
        }

        void endTimeFrame(TimeFrame timeFrame) {
            myTopUnitTextBuilder.createTopUnitText(posX);
            posX+=myBottomUnitGridBuilder.getWidth();
        }

        void startUnitLine(TimeUnit timeUnit) {
            if (myCurrentFrame==null) {
                return;
            }
            if (timeUnit==myCurrentFrame.getTopUnit()) {
            }
            if (timeUnit==myCurrentFrame.getBottomUnit()) {
                myBottomUnitGridBuilder.beforeProcessingGrid(posX);
                areUnitsAccepted = true;
            }
        }

        void endUnitLine(TimeUnit timeUnit) {
            if (areUnitsAccepted) {
                myBottomUnitGridBuilder.afterProcessingGrid();
            }
            areUnitsAccepted = false;
        }

        void nextTimeUnit(int unitIndex) {
            if (areUnitsAccepted) {
                myBottomUnitGridBuilder.visitUnit(myCurrentFrame, unitIndex);
            }
        }


        class TopUnitTextBuilder {
            void createTopUnitText(int posFrameStart) {
            	int topUnitHeight = getChartModel().getChartUIConfiguration().getSpanningHeaderHeight();
                int posX = posFrameStart+2;
                int maxLength = myBottomUnitGridBuilder.getWidth()-2;
                TimeUnitText timeUnitText = myCurrentFrame.getUnitText(myCurrentFrame.getTopUnit(), 0); 
                String unitText = timeUnitText.getText(-1);
                int posY = topUnitHeight-5;
                GraphicPrimitiveContainer.Text text = myPrimitiveContainer.createText(posX+2, posY, unitText);
                text.setMaxLength(maxLength);
                text.setFont(config.getSpanningHeaderFont());
                Line delimiter = myPrimitiveContainer.createLine(posFrameStart, 0, posFrameStart, topUnitHeight);
                myPrimitiveContainer.bind(text, timeUnitText);
            }
        }

        class BottomUnitGridBuilder {
            int myWidth=0;
            int posX;
            private int myPosFrameStart;

            void beforeProcessingGrid(int posFrameStart) {
                myWidth =0;
                posX = posFrameStart;
                myPosFrameStart = posFrameStart;
            }

            void visitUnit(TimeFrame currentFrame, int unitIndex) {
                posX+=bottomUnitWidth;
            }

            void afterProcessingGrid() {
                myWidth = posX - myPosFrameStart;
            }

            int getWidth() {
                return myWidth;
            }
        }
    }

//	private int getHeight() {
//        return (int) myChartModel.getBounds().getHeight();
//    }
//
//    private int getWidth() {
//        return (int) myChartModel.getBounds().getWidth();
//    }

	/* (non-Javadoc)
	 * @see net.sourceforge.ganttproject.chart.TimeUnitVisitor#afterProcesingTimeFrames()
	 */
	public void afterProcessingTimeFrames() {
		// TODO Auto-generated method stub
		
	}

}
