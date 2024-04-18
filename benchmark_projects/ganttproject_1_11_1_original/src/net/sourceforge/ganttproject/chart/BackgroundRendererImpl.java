package net.sourceforge.ganttproject.chart;

import java.awt.Color;

public class BackgroundRendererImpl extends ChartRendererBase {

    public BackgroundRendererImpl(ChartModelBase model) {
        super(model);
    }

    public void beforeProcessingTimeFrames() {
        GraphicPrimitiveContainer.Rectangle r = getPrimitiveContainer().createRectangle(0, 0, getWidth(), getHeight());
        r.setBackgroundColor(Color.WHITE);        
    }
}
