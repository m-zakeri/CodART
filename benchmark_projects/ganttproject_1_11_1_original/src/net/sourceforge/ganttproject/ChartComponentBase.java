package net.sourceforge.ganttproject;

import java.awt.Cursor;
import java.awt.Graphics;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionAdapter;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import javax.swing.JPanel;

import net.sourceforge.ganttproject.chart.ChartModelBase;
import net.sourceforge.ganttproject.chart.ChartViewState;
import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.gui.UIFacade;
import net.sourceforge.ganttproject.gui.zoom.ZoomEvent;
import net.sourceforge.ganttproject.gui.zoom.ZoomListener;
import net.sourceforge.ganttproject.gui.zoom.ZoomManager;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.time.TimeUnitStack;

public abstract class ChartComponentBase extends JPanel {
    private static final Cursor DEFAULT_CURSOR = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR);
    protected final ChartViewState myChartViewState;
    private final IGanttProject myProject;
	private final ZoomManager myZoomManager;
	private MouseWheelListenerBase myMouseWheelListener;
	private final UIFacade myUIFacade;
    public ChartComponentBase(IGanttProject project, UIFacade uiFacade, ZoomManager zoomManager) {
        myProject = project;
        myUIFacade = uiFacade;
        myZoomManager = zoomManager;
        myChartViewState = new ChartViewState(project, uiFacade);
        myChartViewState.addStateListener(new ChartViewState.Listener() {
            public void startDateChanged(ChartViewState.ViewStateEvent e) {
                repaint();
            }

			public void zoomChanged(ZoomEvent e) {
				getImplementation().zoomChanged(e);
			}
        });
        myMouseWheelListener = new MouseWheelListenerBase();
        addMouseListener(getMouseListener());    
        addMouseMotionListener(getMouseMotionListener());
        addMouseWheelListener(myMouseWheelListener);
    }
    

    public ChartViewState getViewState() {
        return myChartViewState;
    }
    
    public ZoomListener getZoomListener() {
    	return getImplementation();
    }
    
    private UIFacade getUIFacade() {
    	return myUIFacade;
    }
    
    protected TaskManager getTaskManager() {
        return myProject.getTaskManager();
    }
    
    protected TimeUnitStack getTimeUnitStack() {
        return myProject.getTimeUnitStack();
    }
    
    protected UIConfiguration getUIConfiguration() {
        return myProject.getUIConfiguration();
    }

    protected void setDefaultCursor() {
        setCursor(DEFAULT_CURSOR);
    }

    protected abstract ChartModelBase getChartModel();
    protected abstract MouseListener getMouseListener();
    protected abstract MouseMotionListener getMouseMotionListener();
    //protected abstract MouseWheelListener getMouseWheelListener();
    
    protected interface MouseInteraction {
        abstract void apply(MouseEvent event);
        abstract void finish();
        void paint(Graphics g);
    }
    
    protected abstract class MouseInteractionBase  {
        private int myStartX;
        protected MouseInteractionBase(MouseEvent e) {
            myStartX = e.getX();            
        }
        protected float getLengthDiff(MouseEvent event) {
            float diff = getChartModel().calculateLength(myStartX, event.getX(), event.getY()); 
            return diff;
        }           
        public void paint(Graphics g) {
        }
        protected int getStartX() {
            return myStartX;
        }
    }
    
    
    protected class ScrollViewInteraction extends MouseInteractionBase implements MouseInteraction {
        private float myPreviousAbsoluteDiff;
        
        protected ScrollViewInteraction(MouseEvent e) {
            super(e);
        }

        public void apply(MouseEvent event) {
            float absoluteDiff = getLengthDiff(event);
            float relativeDiff = myPreviousAbsoluteDiff - absoluteDiff;
            TaskLength diff = getTaskManager().createLength(getViewState().getBottomTimeUnit(), relativeDiff);
            
            int days = (int) diff.getLength(getTimeUnitStack().getDefaultTimeUnit());
            if (days==0) {
                return;
            }
            if (days>0) {
                getUIFacade().getScrollingManager().scrollRight();                                
            }
            if (days<0) {
            	getUIFacade().getScrollingManager().scrollLeft();                                
            }
            myPreviousAbsoluteDiff = absoluteDiff;
        }

        public void finish() {
        }
        
    }
    
    protected class MouseListenerBase extends MouseAdapter {        
        public void mousePressed(MouseEvent e) {
            super.mousePressed(e);
            switch(e.getButton()) {
                case MouseEvent.BUTTON1: {
                    processLeftButton(e);
                    break;
                }
                default: {
                    
                }
            }
        }
        
        private void processLeftButton(MouseEvent e) {
            getImplementation().beginScrollViewInteraction(e);
        }
        public void mouseReleased(MouseEvent e) {
            super.mouseReleased(e);
            MouseInteraction activeInteraction = getImplementation().finishInteraction();            
        }
        public void mouseEntered(MouseEvent e) {
            setDefaultCursor();
        }

        public void mouseExited(MouseEvent e) {
            setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
        }        
    }
    
    protected class MouseMotionListenerBase extends MouseMotionAdapter {
        public void mouseDragged(MouseEvent e) {
            super.mouseDragged(e);
            MouseInteraction activeInteraction = getImplementation().getActiveInteraction();
            if (activeInteraction != null) {
                activeInteraction.apply(e);
                repaint();
                e.consume();
                return;
            }
        }
    }
    
    protected class MouseWheelListenerBase implements MouseWheelListener {
		public void mouseWheelMoved(MouseWheelEvent e) {
			if (isRotationUp(e)) {
				fireZoomOut();
			}
			else {
				fireZoomIn();
			}			
		}

		private void fireZoomIn() {
			if (myZoomManager.canZoomIn()) {
				myZoomManager.zoomIn();
			}
		}

		private void fireZoomOut() {
			if (myZoomManager.canZoomOut()) {
				myZoomManager.zoomOut();
			}
		}

		private boolean isRotationUp(MouseWheelEvent e) {
			return e.getWheelRotation()<0;
		}    	
    }
    
    protected abstract AbstractChartImplementation getImplementation();
    
    protected class AbstractChartImplementation implements ZoomListener {
        public void beginScrollViewInteraction(MouseEvent e) {
            setActiveInteraction(new ScrollViewInteraction(e));
        }
        
        public MouseInteraction finishInteraction() {
            try {
                if (getActiveInteraction()!=null) {
                    getActiveInteraction().finish();
                }
                return getActiveInteraction();
            }
            finally {
                setActiveInteraction(null);
            }
        }
        protected void setActiveInteraction(MouseInteraction myActiveInteraction) {
            this.myActiveInteraction = myActiveInteraction;
        }
        public MouseInteraction getActiveInteraction() {
            return myActiveInteraction;
        }
		public void zoomChanged(ZoomEvent e) {
			invalidate();
			repaint();
		}        
        private MouseInteraction myActiveInteraction;        
    }
}
