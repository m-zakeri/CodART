package net.sourceforge.ganttproject.chart;

import java.awt.Graphics;

import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.resource.ProjectResource;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.time.TimeUnitStack;

public class ChartModelResource extends ChartModelBase {

    private ResourceLoadRenderer myResourceLoadRenderer;
    private HumanResourceManager myManager;

    public ChartModelResource(TaskManager taskManager, HumanResourceManager resourceManager, TimeUnitStack timeUnitStack, UIConfiguration projectConfig) {
        super(taskManager, timeUnitStack, projectConfig);
        myResourceLoadRenderer = new ResourceLoadRenderer(this);
        myTimeUnitVisitors.add(myResourceLoadRenderer);
        myManager = resourceManager;
    }

	protected void enableRenderers1() {
		super.enableRenderers1();
		myResourceLoadRenderer.setEnabled(true);
	}
	protected void enableRenderers2() {
		super.enableRenderers2();
		myResourceLoadRenderer.setEnabled(false);
	}
    protected void paintMainArea(Graphics mainArea, Painter p) {
        super.paintMainArea(mainArea, p);
        myResourceLoadRenderer.getPrimitiveContainer().paint(p, mainArea);
    }


    public ProjectResource[] getVisibleResources() {
        return (ProjectResource[]) myManager.getResources().toArray(new ProjectResource[0]);
    }
}
