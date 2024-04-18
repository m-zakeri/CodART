package net.sourceforge.ganttproject.chart;

import java.awt.AlphaComposite;
import java.awt.Composite;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.Graphics2D;
import java.util.Map;
import java.util.HashMap;

import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Rectangle;
import net.sourceforge.ganttproject.chart.GraphicPrimitiveContainer.Text;
import net.sourceforge.ganttproject.shape.ShapePaint;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskActivity;
import net.sourceforge.ganttproject.time.TimeUnitText;
import net.sourceforge.ganttproject.util.TextLengthCalculator;
import net.sourceforge.ganttproject.util.TextLengthCalculatorImpl;

/**
 * Created by IntelliJ IDEA.
 * User: bard
 */
public class StyledPainterImpl implements Painter {
    private Graphics myGraphics;
    private final Map myStyle2painter = new HashMap();
    private final TextLengthCalculatorImpl myTextLengthCalculator;
    private ChartUIConfiguration myConfig;
    
    public StyledPainterImpl(ChartUIConfiguration configuration) {
        //myGraphics = g;
        myStyle2painter.put("task", myTaskRectanglePainter);
        myConfig = configuration;
        myStyle2painter.put("calendar.holiday", myCalendarHolidayPainter);
        myStyle2painter.put("task.milestone", myMilestonePanter);
        myStyle2painter.put("task.holiday", myTaskHolidayRectanglePainter);
        myStyle2painter.put("task.supertask", myTaskSupertaskRectanglePainter);
        myStyle2painter.put("task.supertask.start", mySupertaskStartPainter);
        myStyle2painter.put("task.supertask.end", mySupertaskEndPainter);
        myStyle2painter.put("task.progress", new ColouredRectanglePainter(Color.BLACK));
        myStyle2painter.put("task.progress.end", new ColouredRectanglePainter(Color.BLACK));
        myStyle2painter.put("load.normal", myResourceLoadPainter);
        myStyle2painter.put("load.normal.first", myResourceLoadPainter);
        myStyle2painter.put("load.normal.last", myResourceLoadPainter);
        myStyle2painter.put("load.normal.first.last", myResourceLoadPainter);
        myStyle2painter.put("load.overload", myResourceLoadPainter);
        myStyle2painter.put("dependency.arrow.down", myArrowDownPainter);
        myStyle2painter.put("load.overload.first", myResourceLoadPainter);
        myStyle2painter.put("load.overload.last", myResourceLoadPainter);
        myStyle2painter.put("load.overload.first.last", myResourceLoadPainter);
        myStyle2painter.put("dependency.arrow.up", myArrowUpPainter);
        myStyle2painter.put("dependency.arrow.left", myArrowLeftPainter);
        myStyle2painter.put("dependency.arrow.right", myArrowRightPainter);
        myTextLengthCalculator = new TextLengthCalculatorImpl(myGraphics);
    }
    
    private Map myGraphics2calculator = new HashMap();
    
    public void setGraphics(Graphics g) {
        myGraphics = g;
        myTextLengthCalculator.setGraphics(g);
    }
    public void paint(GraphicPrimitiveContainer.Rectangle next) {
        if (myGraphics==null) {
            throw new RuntimeException("Graphics is null");
        }
        Graphics g = myGraphics;
        RectanglePainter painter = (RectanglePainter) myStyle2painter.get(next.getStyle());
        if (painter!=null) {
            painter.paint(next);
        }
        else {
            if (next.getBackgroundColor()==null) {
                Color foreColor = next.getForegroundColor();
                if (foreColor==null) {
                    foreColor = Color.BLACK;
                }
                g.setColor(foreColor);
                g.drawRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
            }
            else {
                g.setColor(next.getBackgroundColor());
                g.fillRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
            }
        }
    }

    private RectanglePainter myCalendarHolidayPainter = new RectanglePainter() {
        Composite myAlphaComposite = AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.6f);
        public void paint(Rectangle next) {
            Color c = next.getBackgroundColor();
            Graphics2D g = (Graphics2D) myGraphics;
            g.setColor(c);
            Composite was = g.getComposite();
            g.setComposite(myAlphaComposite);
            g.fillRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
            g.setComposite(was);
        }
    };
    private RectanglePainter myTaskRectanglePainter = new RectanglePainter() {
        public void paint(GraphicPrimitiveContainer.Rectangle next) {
        	Object modelObject = next.getModelObject();
        	if (modelObject instanceof TaskActivity==false) {
        		throw new RuntimeException("Model object is expected to be TaskActivity ");
        	}
        	Task task = ((TaskActivity)modelObject).getTask();
            Color c = task.getColor();
            if (c==null) {
                c = getDefaultColor();
            }
            Graphics g = myGraphics;
            g.setColor(c);
            ShapePaint shapePaint = task.getShape();
            
            if (shapePaint!=null && g instanceof Graphics2D) {
            	((Graphics2D)g).setPaint(shapePaint);
            }
            g.fillRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
            g.setColor(Color.black);
            g.drawRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
        }
        private Color getDefaultColor() {
            return Color.BLUE;
        }

    };

    private RectanglePainter myTaskHolidayRectanglePainter = new RectanglePainter() {
        public void paint(GraphicPrimitiveContainer.Rectangle next) {
            Object modelObject = next.getModelObject();
            if (modelObject instanceof TaskActivity==false) {
                throw new RuntimeException("Model object is expected to be TaskActivity ");
            }
            Task task = ((TaskActivity)modelObject).getTask();
            Color c = task.getColor();
            if (c==null) {
                c = getDefaultColor();
            }
            Graphics g = myGraphics;
            g.setColor(c);            
            g.fillRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
            g.setColor(Color.black);
            g.drawRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);            
        }
        private Color getDefaultColor() {
            return Color.BLUE;
        }


    };
    
    private RectanglePainter myTaskSupertaskRectanglePainter = new RectanglePainter() {
		public void paint(Rectangle next) {
            Color c = next.getBackgroundColor();
            if (c==null) {
                c = getDefaultColor();
            }
            Graphics g = myGraphics;
            g.setColor(c);            
            g.fillRect(next.myLeftX, next.myTopY+next.myHeight-6, next.myWidth, 3);			
		}

		private Color getDefaultColor() {
			return Color.BLACK;
		}
    	
    };
    
    private RectanglePainter mySupertaskStartPainter = new RectanglePainter() {
		public void paint(Rectangle next) {
			Graphics g = myGraphics;
			g.setColor(Color.BLACK);
			int topy = next.myTopY+next.myHeight-3;
			g.fillPolygon(new int[] {next.myLeftX, next.myLeftX+3, next.myLeftX}, new int[] {topy, topy, topy+3}, 3);
		}    	
    };
    private RectanglePainter mySupertaskEndPainter = new RectanglePainter() {
		public void paint(Rectangle next) {
			Graphics g = myGraphics;
			g.setColor(Color.BLACK);
			int topy = next.myTopY+next.myHeight-3;
			int rightx = next.myLeftX+next.myWidth;
			g.fillPolygon(new int[] {rightx-3, rightx, rightx}, new int[] {topy, topy, topy+3}, 3);
		}    	
    };
 
    private RectanglePainter myMilestonePanter = new RectanglePainter() {
    	private int[] myXPoints = new int[4];
    	private int[] myYPoints = new int[4];
		public void paint(Rectangle next) {
        	Object modelObject = next.getModelObject();
        	if (modelObject instanceof TaskActivity==false) {
        		throw new RuntimeException("Model object is expected to be TaskActivity ");
        	}
        	Task task = ((TaskActivity)modelObject).getTask();
            Color c = task.getColor();
            Graphics g = myGraphics;
            g.setColor(c);
			int middleX = (next.myWidth<=next.myHeight) ? 
                    next.getRightX() - next.myWidth/2 :
                    next.myLeftX + next.myHeight/2;
			int middleY = next.getBottomY() - next.myHeight/2;
			myXPoints[0] = next.myLeftX;
			myXPoints[1] = middleX;
			myXPoints[2] = (next.myWidth<=next.myHeight) ?
                    next.getRightX() : next.myLeftX + next.myHeight;
			myXPoints[3] = middleX;
			myYPoints[0] = middleY;
			myYPoints[1] = next.myTopY;
			myYPoints[2] = middleY;
			myYPoints[3] = next.getBottomY();
			
			g.fillPolygon(myXPoints, myYPoints, 4);
		}
    	
    };
    private RectanglePainter myArrowDownPainter = new RectanglePainter() {
        private int[] myXPoints = new int[3];
        private int[] myYPoints = new int[3];
        
        public void paint(Rectangle next) {
            Graphics g = myGraphics;
            g.setColor(Color.BLACK);
            myXPoints[0] = next.myLeftX;
            myXPoints[1] = next.getRightX();
            myXPoints[2] = next.getMiddleX();
            myYPoints[0] = next.myTopY;
            myYPoints[1] = next.myTopY;
            myYPoints[2] = next.getBottomY();
            g.fillPolygon(myXPoints, myYPoints, 3);
        }        
    };
    private RectanglePainter myArrowUpPainter = new RectanglePainter() {
        private int[] myXPoints = new int[3];
        private int[] myYPoints = new int[3];
        
        public void paint(Rectangle next) {
            Graphics g = myGraphics;
            g.setColor(Color.BLACK);
            myXPoints[0] = next.myLeftX;
            myXPoints[1] = next.getRightX();
            myXPoints[2] = next.getMiddleX();
            myYPoints[0] = next.getBottomY();
            myYPoints[1] = next.getBottomY();
            myYPoints[2] = next.myTopY;
            g.fillPolygon(myXPoints, myYPoints, 3);
        }        
    };
    private RectanglePainter myArrowLeftPainter = new RectanglePainter() {
        private int[] myXPoints = new int[3];
        private int[] myYPoints = new int[3];
        
        public void paint(Rectangle next) {
            Graphics g = myGraphics;
            g.setColor(Color.BLACK);
            myXPoints[0] = next.myLeftX;
            myXPoints[1] = next.getRightX();
            myXPoints[2] = next.getRightX();
            myYPoints[0] = next.getMiddleY();
            myYPoints[1] = next.myTopY;
            myYPoints[2] = next.getBottomY();
            g.fillPolygon(myXPoints, myYPoints, 3);
        }        
    };
    private RectanglePainter myArrowRightPainter = new RectanglePainter() {
        private int[] myXPoints = new int[3];
        private int[] myYPoints = new int[3];
        
        public void paint(Rectangle next) {
            Graphics g = myGraphics;
            g.setColor(Color.BLACK);
            myXPoints[0] = next.myLeftX;
            myXPoints[1] = next.getRightX();
            myXPoints[2] = next.myLeftX;
            myYPoints[0] = next.myTopY;
            myYPoints[1] = next.getMiddleY();
            myYPoints[2] = next.getBottomY();
            g.fillPolygon(myXPoints, myYPoints, 3);
        }        
    };
    
    private RectanglePainter myResourceLoadPainter = new RectanglePainter() {
		public void paint(Rectangle next) {
			Graphics g = myGraphics;
			String style = next.getStyle();
			Color color =  (style.startsWith("load.normal") ? myConfig.getResourceNormalLoadColor() : myConfig.getResourceOverloadColor());
			g.setColor(color);
			int margin = 3;
			g.fillRect(next.myLeftX, next.myTopY+margin, next.myWidth, next.myHeight-2*margin);
			if (style.indexOf(".first")>0) {
				g.setColor(Color.BLACK);
				g.drawLine(next.myLeftX, next.myTopY+margin, next.myLeftX, next.getBottomY()-margin);
			}
			if (style.indexOf(".last")>0) {
				g.setColor(Color.BLACK);
				g.drawLine(next.getRightX(), next.myTopY+margin, next.getRightX(), next.getBottomY()-margin);
			}
			g.setColor(Color.BLACK);
			g.drawLine(next.myLeftX, next.myTopY+margin, next.getRightX(), next.myTopY+margin);
			g.drawLine(next.myLeftX, next.getBottomY()-margin, next.getRightX(), next.getBottomY()-margin);
		}    	
    };
    private interface RectanglePainter {
        public void paint(GraphicPrimitiveContainer.Rectangle next);
    }

    private class ColouredRectanglePainter implements RectanglePainter {
    	private Color myColor;
		private ColouredRectanglePainter(Color color) {
    		myColor = color;
    	}
		public void paint(Rectangle next) {
			Graphics g = myGraphics;
			g.setColor(myColor);
			g.fillRect(next.myLeftX, next.myTopY, next.myWidth, next.myHeight);
		}
    	
    }

    
    public void paint(Text next) {
        int requestedMaxLength = next.getMaxLength();        
        Color foreColor = next.getForegroundColor();
        if (foreColor==null) {
            foreColor = Color.BLACK;
        }
        myGraphics.setColor(foreColor);
        if (next.getFont()!=null) {
            myGraphics.setFont(next.getFont());
        }
        else {
        	myGraphics.setFont(myConfig.getChartFont());
        }
        //
        String nextTextString = next.getText();
        if (next.getModelObject()!=null) {
            TimeUnitText nextText = (TimeUnitText) next.getModelObject();
            nextTextString = nextText.getText(requestedMaxLength, myTextLengthCalculator);
        }
        else {
            if (requestedMaxLength>=0) {
                int actualLength = TextLengthCalculatorImpl.getTextLength(myGraphics, next.getText());
                if (actualLength>requestedMaxLength) {
                    return;
                }
            }
        }
        myGraphics.drawString(nextTextString, next.getLeftX(), next.getBottomY());
    }
}
