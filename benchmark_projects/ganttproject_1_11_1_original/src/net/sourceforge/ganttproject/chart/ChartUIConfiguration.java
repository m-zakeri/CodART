/*
 * Created on 17.06.2004
 *
 */
package net.sourceforge.ganttproject.chart;

import java.awt.Color;
import java.awt.Font;

import net.sourceforge.ganttproject.gui.UIConfiguration;

/**
 * @author bard
 *
 */
class ChartUIConfiguration {
    
    private final Font mySpanningRowTextFont;
    private final Color mySpanningHeaderBackgroundColor;
	private final Color myHeaderBorderColor;
	private final Color myHorizontalGutterColor1 = new Color(0.807f, 0.807f, 0.807f);
	private final Color myHorizontalGutterColor2 = Color.white;
	private final Color myBottomUnitGridColor;
	private final Font myBottomUnitFont;
    private final Color myWorkingTimeBackgroundColor;
    private final Color myHolidayTimeBackgroundColor;
    private int myRowHeight;
	private UIConfiguration myProjectConfig;
	private int myHeaderHeight = 44;

    ChartUIConfiguration(UIConfiguration projectConfig) {
        mySpanningRowTextFont = new Font("SansSerif", Font.PLAIN, 12);
        myBottomUnitFont = projectConfig.getChartMainFont();
        mySpanningHeaderBackgroundColor = new Color(0.930f, 0.930f, 0.930f);
        myHeaderBorderColor = new Color(0.482f, 0.482f, 0.482f);
        myWorkingTimeBackgroundColor = Color.WHITE;
        myHolidayTimeBackgroundColor = new Color(0.930f, 0.930f, 0.930f);
        //myHeaderBorderColor = new Color(0f, 1f, 0f);
        myBottomUnitGridColor = new Color(0.482f, 0.482f, 0.482f);
        myProjectConfig = projectConfig; 
    }
    
    Font getSpanningHeaderFont() {
        return mySpanningRowTextFont;
    }
    
    Font getBottomUnitFont() {
    	return myBottomUnitFont;
    }

    public int getHeaderHeight() {
        return myHeaderHeight;
    }

    public void setHeaderHeight(int headerHeight){
    	myHeaderHeight= headerHeight;
    }
    public int getSpanningHeaderHeight() {
        return myHeaderHeight/2;
    }

    public Color getSpanningHeaderBackgroundColor() {
        return mySpanningHeaderBackgroundColor;
    }

	public Color getHeaderBorderColor() {
		return myHeaderBorderColor;
	}

	public Color getHorizontalGutterColor1() {
		return myHorizontalGutterColor1;
	}

	public Color getHorizontalGutterColor2() {
		return myHorizontalGutterColor2;
	}

	public Color getBottomUnitGridColor() {
		return myBottomUnitGridColor;
	}

    public Color getWorkingTimeBackgroundColor() {
        return myWorkingTimeBackgroundColor;
    }

    public Color getHolidayTimeBackgroundColor() {
        return myHolidayTimeBackgroundColor;
    }

    public int getRowHeight() {
        return myRowHeight;
    }

    public void setRowHeight(int rowHeight) {
        myRowHeight = rowHeight;
    }
    
    public Color getDefaultTaskColor() {
    	return myProjectConfig.getTaskColor();
    }

	public boolean isRedlineOn() {
		return myProjectConfig.isRedlineOn();
	}
	
	public Font getChartFont() {
		return myProjectConfig.getChartMainFont();
	}
	
	public Color getResourceNormalLoadColor() {
		return myProjectConfig.getResourceColor();
	}
	
	public Color getResourceOverloadColor() {
		return myProjectConfig.getResourceOverloadColor();
	}
}
