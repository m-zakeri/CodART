/***************************************************************************

                           GanttGraphicArea.java  -  description

                             -------------------

    begin                : dec 2002

    copyright            : (C) 2002 by Thomas Alexandre

    email                : alexthomas(at)ganttproject.org

 ***************************************************************************/



/***************************************************************************

 *                                                                         *

 *   This program is free software; you can redistribute it and/or modify  *

 *   it under the terms of the GNU General Public License as published by  *

 *   the Free Software Foundation; either version 2 of the License, or     *

 *   (at your option) any later version.                                   *

 *                                                                         *

 ***************************************************************************/



package net.sourceforge.ganttproject;



import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.image.BufferedImage;
import java.awt.print.PrinterJob;
import java.io.File;
import java.io.OutputStream;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import javax.imageio.ImageIO;
import javax.swing.tree.DefaultMutableTreeNode;

import net.sourceforge.ganttproject.chart.ChartModel;
import net.sourceforge.ganttproject.chart.ChartModelBase;
import net.sourceforge.ganttproject.chart.ChartModelImpl;
import net.sourceforge.ganttproject.chart.DependencyInteractionRenderer;
import net.sourceforge.ganttproject.chart.TaskInteractionHintRenderer;
import net.sourceforge.ganttproject.chart.VisibleNodesFilter;
import net.sourceforge.ganttproject.chart.item.ChartItem;
import net.sourceforge.ganttproject.chart.item.TaskBoundaryChartItem;
import net.sourceforge.ganttproject.chart.item.TaskProgressChartItem;
import net.sourceforge.ganttproject.chart.item.TaskRegularAreaChartItem;
import net.sourceforge.ganttproject.gui.UIConfiguration;
import net.sourceforge.ganttproject.gui.UIFacade;
import net.sourceforge.ganttproject.gui.zoom.ZoomListener;
import net.sourceforge.ganttproject.gui.zoom.ZoomManager;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.task.TaskMutator;
import net.sourceforge.ganttproject.task.algorithm.RecalculateTaskScheduleAlgorithm;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyException;
import net.sourceforge.ganttproject.task.event.TaskDependencyEvent;
import net.sourceforge.ganttproject.task.event.TaskListenerAdapter;
import net.sourceforge.ganttproject.task.event.TaskScheduleEvent;
import net.sourceforge.ganttproject.time.gregorian.GregorianCalendar;





/**

 * Class for the graphic part of the soft

 */

public class GanttGraphicArea extends ChartComponentBase  {

	static {
		Toolkit toolkit = Toolkit.getDefaultToolkit();
		URL cursorResource = GanttGraphicArea.class.getClassLoader().getResource("icons/cursorpercent.gif");
		Image image = toolkit.getImage(cursorResource);
		CHANGE_PROGRESS_CURSOR = toolkit.createCustomCursor(image, new Point(10, 5), "CursorPercent");		
	}
    private static final Cursor DEFAULT_CURSOR = new Cursor(Cursor.DEFAULT_CURSOR); 
    private static final Cursor W_RESIZE_CURSOR= new Cursor(Cursor.W_RESIZE_CURSOR);
    private static final Cursor E_RESIZE_CURSOR= new Cursor(Cursor.E_RESIZE_CURSOR);
    private static final Cursor CHANGE_PROGRESS_CURSOR;

  /** Begin of display. */

  public GanttCalendar date;



  /** Reference to the GanttTree */

  public GanttTree tree;



  /** Default color for tasks */

  public static Color taskDefaultColor

   //   = new Color( (float) 0.549, (float) 0.713, (float) 0.807);

	= new Color( 140, 182, 206);

  /** This value is connected to the GanttTRee Scrollbar to move up or down */

  private int margY;



  /** UpperLeft Point (for the margin of printing) */

  //private Point upperLeft = new Point(0, 0);



  /** Render on the window or for printing*/

  private boolean printRendering = false;



  /** Render the depends */


  /** Render the depends */


  /** Render the name*/

  private boolean drawName = false;

  /** render the 3d borders. */

  private boolean draw3dBorders = true;

  /* Render the ganttproject version*/

  private boolean drawVersion = false;



  /** The language */

  private GanttLanguage language = GanttLanguage.getInstance();



  /*! The main application */

  private GanttProject appli;


  /** Begin of project */

  public GanttCalendar beg = new GanttCalendar();



  /**End date for the project */

  public GanttCalendar end = new GanttCalendar();



    private final UIConfiguration myUIConfiguration;

    private Color myProjectLevelTaskColor;
    private final ChartModelImpl myChartModel;



    private final TaskManager myTaskManager;
    private static final boolean RENDERER_1_11 = true;




    /** Constructor */

  public GanttGraphicArea(GanttProject app, GanttTree ttree, TaskManager taskManager, ZoomManager zoomManager, UIConfiguration uiConfiguration) {
      super((IGanttProject)app, (UIFacade)app, zoomManager);
        myTaskManager = taskManager;
        myUIConfiguration = uiConfiguration;
        //
        myChartModel = new ChartModelImpl(getTaskManager(), app.getTimeUnitStack(), app.getUIConfiguration());
        getViewState().addStateListener(myChartModel);
        getViewState().setStartDate(GregorianCalendar.getInstance().getTime());
        myTaskManager.addTaskListener(new TaskListenerAdapter() {
            public void taskScheduleChanged(TaskScheduleEvent e) {
                adjustDependencies((Task) e.getSource());
            }

            public void dependencyAdded(TaskDependencyEvent e) {
                adjustDependencies(e.getDependency().getDependee());
            }

            private void adjustDependencies(Task task) {
                RecalculateTaskScheduleAlgorithm alg = myTaskManager.getAlgorithmCollection().getRecalculateTaskScheduleAlgorithm();
                if (!alg.isRunning()) {
                    try {
                        alg.run(task);
                    } catch (TaskDependencyException e1) {
                        e1.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
                    }
                    repaint();
                }
            }
        });

        date = new GanttCalendar();

    date.setDay(1);

    this.tree = ttree;




    margY = 0;

    appli = app;



    //creation of the different color use to paint

    //arrayColor[0] = new Color((float)0.905,(float)0.905,(float)0.905);


  }



  /** Return the color of the task */

  public Color getTaskColor() {

    return myProjectLevelTaskColor==null ? myUIConfiguration.getTaskColor() : myProjectLevelTaskColor;

  }



  /** Change the color of the task */

  public void setProjectLevelTaskColor(Color c) {

    myProjectLevelTaskColor = c;

  }





  /** The size of the panel. */

  public Dimension getPreferredSize() {

    return new Dimension(465, 600);

  }





    public void paintComponent(Graphics g) {
        myChartModel.setBounds(getSize());
    	myChartComponentImpl.paintComponent(g);
    }


	

	public void drawGPVersion(Graphics g){

		g.setColor(Color.black);

      g.setFont(new Font("SansSerif", Font.PLAIN, 10));

      g.drawString("GanttProject (" + GanttProject.version + ")", 3, getHeight() - 6);

	}

	



  /** Is the Task visible on the JTree */

  public boolean isVisible(Task thetask) {



    boolean res = true;

    //ArrayList expand = tree.getExpand();

    DefaultMutableTreeNode father = tree.getFatherNode(thetask);



    //The roor task is not visible

    if (father == null) {

      return false;

    }



    while (father != null) {

      //if (!expand.contains(new Integer(((Task)(father.getUserObject())).getTaskID()))) {

      Task taskFather = (Task)(father.getUserObject()); 

      if(!taskFather.getExpand()) 

        res = false;

      

      //Task t = (Task)father.getUserObject();

      //father = tree.getFatherNode(t);

      	father = (DefaultMutableTreeNode)(father.getParent());

    }



    return res;



  }



  /** Change the velue connected to the JTree's Scrollbar */

  public void setScrollBar(int v) {

    margY = v;

  }



  /** Return the value of the JTree's Scrollbar */

  public int getScrollBar() {

    return margY;

  }




	/** Return an image with the gantt chart*/
//TODO: 1.11 take into account flags "render this and don't render that"
	public BufferedImage getChart(GanttExportSettings settings) {	

		

		int rendering = 0;

		

		GanttCalendar date2 = new GanttCalendar(date);

		date = new GanttCalendar(beg);

		GanttCalendar  start =  new GanttCalendar(date);

		date = new GanttCalendar(date2);

		

		

//		while(start.compareTo(end)<=0){
//
//			rendering++;
//
//		}

		

		

		//Make save of parameters

		int oldMargY = margY;

		int oldHeight=getHeight();

		int height = 20;

		int width=getWidth();

		margY=0;

		


		drawName = settings.name;

		draw3dBorders = settings.border3d;

    

		//change the Height of the panel

		

		int sizeTOC=0; //Size of the content table for the tasks list

		BufferedImage tmpImage = new BufferedImage(10, 10, BufferedImage.TYPE_INT_RGB);

		FontMetrics fmetric = tmpImage.getGraphics().getFontMetrics(new Font("SansSerif", Font.PLAIN, 10));

		

		ArrayList lot = getTree().getAllTasks();

    for (Iterator tasks = lot.iterator(); tasks.hasNext(); ) {

      DefaultMutableTreeNode nextTreeNode = (DefaultMutableTreeNode) tasks.next();

      Task next = (Task) nextTreeNode.getUserObject();

      if ("None".equals(next.toString())) {

        continue;

      }

      if (isVisible(next)) {

        height += 20;

				int nbchar = fmetric.stringWidth(next.getName());

				if(nbchar>sizeTOC)sizeTOC=nbchar;

      }

		}

		sizeTOC+=50;	//for the indentation of the tasks, but I fiw 50 pixel correcpond to 7 sub-taks indentation

	

		//If there is only the root task

		if(lot.size()==1){ setSize(width, oldHeight); rendering=1;}

		else setSize(width, height + 40);

    		

		int calculateWidth=width*rendering;

		if(drawName){

			rendering++;

			calculateWidth+=sizeTOC;

		}

		

		

		

		start=new GanttCalendar(date);

		date=new GanttCalendar(beg);

		

		
		
        TaskLength projectLength = getTaskManager().getProjectLength();
        int chartWidth = (int) ((projectLength.getLength(getViewState().getBottomTimeUnit())+1)*getViewState().getBottomUnitWidth());
        int chartHeight = (getTaskManager().getTaskCount()+1)*tree.getJTree().getRowHeight()+100;
		int transx=0, transx2;
        BufferedImage result = new BufferedImage(chartWidth + (drawName ? sizeTOC : 0), chartHeight, BufferedImage.TYPE_INT_RGB);
        Graphics g = result.getGraphics();
		{
            // Render task tree view here
			if(drawName){
				rowCount=0;
				BufferedImage image2 = new BufferedImage(sizeTOC, chartHeight, BufferedImage.TYPE_INT_RGB);
				//setSize(sizeTOC, getHeight());
				Graphics g2 = image2.getGraphics();
				g2.setColor(Color.white);
				g2.fillRect(0, 0, sizeTOC, chartHeight);				
				printTasks(g2);
				setSize(width, getHeight());
				transx2=sizeTOC;
                g.drawImage(image2,0,0,null);
                g.translate(sizeTOC, 0);
			}
        }
        {
            // Render chart
		    BufferedImage image2 = new BufferedImage(chartWidth, chartHeight, BufferedImage.TYPE_INT_RGB);
		    getViewState().setStartDate(getTaskManager().getProjectStart());
			Graphics g2 = image2.getGraphics();
			g2.setColor(Color.white);
			g2.fillRect(0, 0, chartWidth, chartHeight);				
            myChartModel.setBounds(new Dimension(chartWidth, chartHeight));
            myChartModel.setTuningOptions(new ChartModelImpl.TuningOptions(settings.percent, settings.depend));
			myChartComponentImpl.paintComponent(g2);
			myChartModel.setTuningOptions(ChartModelImpl.TuningOptions.DEFAULT);
			//changeDate2(date);

			transx2=width;
            g.drawImage(image2,0,0,null);

		}

    	


		//upperLeft = new Point(0,0);

		drawGPVersion(g);		

		

		

		date=new GanttCalendar(start);

		margY=oldMargY;



		drawName = false;

		draw3dBorders = true;

		//setSize(getSize().width, oldHeight);

		repaint();

		

		return result;		

	}



	private int rowCount=0;

	

	/** Print the list of tasks */

	private void printTasks(Graphics g){




		g.setColor(Color.black);

		g.setFont(myUIConfiguration.getChartMainFont());

		

		printTask(g,5,42,getTree().getAllChildTask(getTree().getRoot()));

		

	}	

		

	private int printTask (Graphics g, int x, int y, ArrayList child) {

		

			for(Iterator tasks = child.iterator(); tasks.hasNext(); ) {

				DefaultMutableTreeNode nextTreeNode = (DefaultMutableTreeNode) tasks.next();

				Task next = (Task) nextTreeNode.getUserObject();

				

				if(isVisible(next)) {

					if(rowCount%2==1) {

						g.setColor(new Color( (float) 0.933, (float) 0.933, (float) 0.933));

						g.fillRect(0,y,getWidth()-10, 20);	

					}

					g.setColor(Color.black);

					g.drawRect(0,y,getWidth()-10, 20);	

					g.drawString(next.getName(), x, y+13);
					g.setColor(new Color( (float) 0.807, (float) 0.807, (float) 0.807));

					if(draw3dBorders)

						g.drawLine(1,y+19,getWidth()-11,y+19);

					y+=20;

					rowCount++;

					if(nextTreeNode.getChildCount()!=0) {

						y=printTask(g, x+10, y, getTree().getAllChildTask(nextTreeNode));

					} 

				}					

			}			

			return y;

	}

		

		





  /** Print the project */

  public void printProject(GanttExportSettings settings) {

		//For printing the project, begin to create temporary BufferedImage for the entire graphics

		//Then use a class to print it 

		

		printRendering = true;

		BufferedImage image = getChart(settings);

		printRendering = false;

		

		PrinterJob printJob = PrinterJob.getPrinterJob();



		printJob.setPrintable(new GanttPrintable(image));

		if(printJob.printDialog()){

       try { 

					printJob.print(); 

			 

			 } catch (Exception PrintException) {

			 	System.out.println("Print Error" + PrintException);

				PrintException.printStackTrace(); 

			 }

    }



  }



  /** Function able to export in PNG format the graphic area */

  public void export(File file, GanttExportSettings settings, String format) {  

  	

  	

  	/*BufferedImage image = new BufferedImage(getWidth(), getHeight(),

                                            BufferedImage.TYPE_INT_RGB);



    drawdepend = depend;

    drawPercent = percent;

    drawName = name;

    drawVersion = true;

    paintComponent(image.getGraphics());

    drawdepend = true;

    drawPercent = true;

    drawName = false;

    drawVersion = false;*/

		



	

	BufferedImage image = getChart(settings);

		



    try {

		

    		if(file==null)

				ImageIO.write(image, format, System.out);

			else ImageIO.write(image, format, file);

			

    }

    catch (Exception e) {

      System.out.println(e);

    }

  }
  
  
    /** Function able to export in PNG format the graphic area */
  public void export(OutputStream os, GanttExportSettings settings, String format) {  
  	
	BufferedImage image = getChart(settings);
	try {
		 ImageIO.write(image, format, os);			
	}
	catch (Exception e) {
	  System.out.println(e);
	}
  }



  private GanttTree getTree() {

    return this.tree;

  }



  IGanttProject getProject() {
      return appli;
  }

    protected ChartModelBase getChartModel() {
        return myChartModel;
    }
    
    
    protected MouseListener getMouseListener() {
        return getChartImplementation().getMouseListener();
    }
        
    protected MouseMotionListener getMouseMotionListener() {
        return getChartImplementation().getMouseMotionListener();
    }
  class MouseSupport {
      protected Task findTaskUnderMousePointer(int xpos, int ypos) {
          //int taskID = detectPosition(xpos, ypos, false);
          //return taskID==-1 ? null : getTaskManager().getTask(taskID);
      	ChartItem chartItem = myChartModel.getChartItemWithCoordinates(xpos, ypos);
      	return chartItem==null ? null : chartItem.getTask();
      }     
      protected ChartItem getChartItemUnderMousePoint(int xpos,int ypos) {
        ChartItem result = myChartModel.getChartItemWithCoordinates(xpos, ypos);
        return result;
      }
  }
    
    

	abstract class ChangeTaskBoundaryInteraction extends MouseInteractionBase {
		private TaskInteractionHintRenderer myLastNotes;
		private final Task myTask;
		private final float myInitialDuration;
		
		protected ChangeTaskBoundaryInteraction(MouseEvent initiatingEvent, TaskBoundaryChartItem taskBoundary) {
        	super(initiatingEvent);
        	myTask = taskBoundary.getTask();
        	myInitialDuration = myTask.getDuration().getLength(getViewState().getBottomTimeUnit());
		}
		public void apply(MouseEvent e) {
            if (myLastNotes==null) {
                myLastNotes = new TaskInteractionHintRenderer("", e.getX(), e.getY());
            }
			float diff= getLengthDiff(e);
			apply(diff);
			myLastNotes.setString(getNotesText());
			myLastNotes.setX(e.getX());
		}
		
		protected Task getTask() {
			return myTask;
		}

		protected float getInitialDuration() {
			return myInitialDuration;
		}
		public void finish() {
			myLastNotes = null;
			try {
				getTaskManager().getAlgorithmCollection().getRecalculateTaskScheduleAlgorithm().run();
			} catch (TaskDependencyException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			GanttGraphicArea.this.repaint();
		}

        public void paint(Graphics g) {
            if (myLastNotes!=null) {
                myLastNotes.paint(g);
            }
        }
		
		protected abstract void apply(float diff);
		protected abstract String getNotesText();
	}
	class ChangeTaskEndInteraction extends ChangeTaskBoundaryInteraction implements MouseInteraction {
        private TaskMutator myMutator;
        public ChangeTaskEndInteraction(MouseEvent initiatingEvent, TaskBoundaryChartItem taskBoundary) {
        	super(initiatingEvent, taskBoundary);
			setCursor(E_RESIZE_CURSOR);
			myMutator = getTask().createMutator();
		}
		protected void apply(float diff) {
			TaskLength newLength = getTaskManager().createLength(getViewState().getBottomTimeUnit(), getInitialDuration()+diff);
			TaskLength translated = getTask().translateDuration(newLength);
			if (translated.getLength()!=0) {
				myMutator.setDuration(translated);
			}			
		}
		
		protected String getNotesText(){
			return getTask().getEnd().toString();
		}		   
		
		public void finish() {
			myMutator.commit();
			super.finish();
		}
	}
	
	class ChangeTaskStartInteraction extends ChangeTaskBoundaryInteraction implements MouseInteraction {
		private TaskLength myInitialLength;
        private TaskMutator myMutator;
        private GanttCalendar myInitialStart;

		ChangeTaskStartInteraction(MouseEvent e, TaskBoundaryChartItem taskBoundary) {
            super(e, taskBoundary);
            setCursor(W_RESIZE_CURSOR);
            myInitialLength = getTask().getDuration();
            myMutator = getTask().createMutator();
            myInitialStart = getTask().getStart();
		}

		protected void apply(float diff) {
			TaskLength newLength = getTaskManager().createLength(getViewState().getBottomTimeUnit(), getInitialDuration()+diff);
			TaskLength translated = getTask().translateDuration(newLength);
			int dayDiff = (int) (translated.getValue()-myInitialLength.getValue());
			//System.err.println("[ChangeTaskStart] dayDiff="+dayDiff+" newLength="+newLength+" translated="+translated);
			if (dayDiff!=0) {
                //System.err.println("[ChangeTaskStartInteraction] apply(): oldStart="+getTask().getStart());
				GanttCalendar newStart = myInitialStart.newAdd(dayDiff);
				//System.err.println("newStart"+newStart);
				myMutator.setStart(newStart);
				//mutator.commit();
				//myInitialLength = getTask().getDuration();
			}
		}
        
        public void finish() {
            myMutator.commit();
            super.finish();
        }
        
		protected String getNotesText() {
			return getTask().getStart().toString();
		}
	}
    
	class ChangeTaskProgressInteraction extends MouseInteractionBase implements MouseInteraction {
		private TaskProgressChartItem myTaskProgrssItem;
		private TaskMutator myMutator;
        private TaskInteractionHintRenderer myLastNotes;
        private int myProgressWas;
        
		public ChangeTaskProgressInteraction(MouseEvent e, TaskProgressChartItem taskProgress) {
            super(e);
            Toolkit toolkit = Toolkit.getDefaultToolkit();
            try {
                setCursor(CHANGE_PROGRESS_CURSOR);
            }
            catch (Exception exept) {
                setCursor(E_RESIZE_CURSOR);
            }
            myTaskProgrssItem = taskProgress;
            myMutator = myTaskProgrssItem.getTask().createMutator();
            myProgressWas = myTaskProgrssItem.getTask().getCompletionPercentage();
		}

		public void apply(MouseEvent event) {            
			//int deltaProgress = (int)myTaskProgrssItem.getProgressDelta(event.getX());
            float deltaUnits = getLengthDiff(event);
            int deltaPercents = (int)(100*deltaUnits/myTaskProgrssItem.getTask().getDuration().getLength(getViewState().getBottomTimeUnit()));
			int newProgress = myProgressWas+deltaPercents;
            if (newProgress>100) {
                newProgress = 100;
            }
            if (newProgress<0) {
                newProgress = 0;
            }
			myMutator.setCompletionPercentage(newProgress);
            myLastNotes = new TaskInteractionHintRenderer(newProgress+"%", event.getX(), event.getY()-30);
		}

		public void finish() {
			myMutator.commit();
            repaint();
		}		
        
        
        public void paint(Graphics g) {
            if (myLastNotes!=null) {
                myLastNotes.paint(g);
            }
        }
	}
    
    class DrawDependencyInteraction extends MouseInteractionBase implements MouseInteraction {

        private final Task myTask;
        private Point myStartPoint;
        private DependencyInteractionRenderer myArrow;
        private GanttGraphicArea.MouseSupport myMouseSupport;
        private Task myDependant;

        public DrawDependencyInteraction(MouseEvent initiatingEvent, TaskRegularAreaChartItem taskArea, MouseSupport mouseSupport) {
            super(initiatingEvent);
            myStartPoint = initiatingEvent.getPoint();
            myTask = taskArea.getTask();
            myArrow = new DependencyInteractionRenderer(myStartPoint.x, myStartPoint.y, myStartPoint.x, myStartPoint.y);
            myMouseSupport = mouseSupport;
        }

        public void apply(MouseEvent event) {
            myArrow.changePoint2(event.getX(), event.getY());
            myDependant = myMouseSupport.findTaskUnderMousePointer(event.getX(), event.getY());
        }

        public void finish() {
            Task dependee = myTask;
            if (myDependant!=null) {
                if (getTaskManager().getDependencyCollection().canCreateDependency(myDependant, dependee)) {
                    try {
                        getTaskManager().getDependencyCollection().createDependency(myDependant, dependee);

                    } catch (TaskDependencyException e1) {
                        e1.printStackTrace();
                    }
                    appli.setAskForSave(true);
                }
            }
        }
        
        public void paint(Graphics g) {
            myArrow.paint(g);
        }
    }
    
    class MoveTaskInteraction extends MouseInteractionBase implements MouseInteraction {
		private Task myTask;
		private TaskMutator myMutator;

		MoveTaskInteraction(MouseEvent e, Task task) {
			super(e);
			myTask = task;
			myMutator = task.createMutator();
		}
		public void apply(MouseEvent event) {
			float diff = getChartModel().calculateLengthNoWeekends(getStartX(), event.getX());
			TaskLength bottomUnitLength = getTaskManager().createLength(getViewState().getBottomTimeUnit(), diff);
			TaskLength taskLength = myTask.translateDuration(bottomUnitLength);
			int dayDiff = (int) (taskLength.getValue());
            //System.err.println("[MoveTaskInteraction] apply(): dayDiff="+dayDiff+" bottomUnitLength="+bottomUnitLength+" translated="+taskLength);
			if (dayDiff!=0) {
				myMutator.shift(dayDiff);
			}
		}

		public void finish() {
			myMutator.commit();
		}
    	
    }
    
    private interface ChartImplementation extends ZoomListener {
    	void paintComponent(Graphics g);
        MouseListener getMouseListener();
        MouseMotionListener getMouseMotionListener();
		void beginChangeTaskEndInteraction(MouseEvent initiatingEvent, TaskBoundaryChartItem taskBoundary);
		MouseInteraction getActiveInteraction();
		void beginChangeTaskStartInteraction(MouseEvent e, TaskBoundaryChartItem taskBoundary);
		MouseInteraction finishInteraction();
		void beginChangeTaskProgressInteraction(MouseEvent e, TaskProgressChartItem item);
        void beginDrawDependencyInteraction(MouseEvent initiatingEvent, TaskRegularAreaChartItem taskArea, GanttGraphicArea.MouseSupport mouseSupport);
		void beginMoveTaskInteraction(MouseEvent e, Task task);
        void beginScrollViewInteraction(MouseEvent e);
        
    }
    
    private class ChartImplementationBase extends AbstractChartImplementation {
		public void beginChangeTaskEndInteraction(MouseEvent initiatingEvent, TaskBoundaryChartItem taskBoundary) {
			setActiveInteraction(new ChangeTaskEndInteraction(initiatingEvent, taskBoundary));
		}
		public void beginChangeTaskStartInteraction(MouseEvent e, TaskBoundaryChartItem taskBoundary) {
			setActiveInteraction(new ChangeTaskStartInteraction(e, taskBoundary));
		}
		public void beginChangeTaskProgressInteraction(MouseEvent e, TaskProgressChartItem taskProgress) {
            setActiveInteraction(new ChangeTaskProgressInteraction(e, taskProgress));
		}
        public void beginDrawDependencyInteraction(MouseEvent initiatingEvent, TaskRegularAreaChartItem taskArea, GanttGraphicArea.MouseSupport mouseSupport) {
            setActiveInteraction(new DrawDependencyInteraction(initiatingEvent, taskArea, mouseSupport));
        }
        public void beginMoveTaskInteraction(MouseEvent e, Task task) {
        	setActiveInteraction(new MoveTaskInteraction(e,task));
        }    	
    }
    
    private class NewChartComponentImpl extends ChartImplementationBase implements ChartImplementation {
		public void paintComponent(Graphics g) {
	        GanttGraphicArea.super.paintComponent(g);
	        ChartModel model = myChartModel;
	        model.setTaskContainment(appli.getTaskContainment());
	        //model.setBounds(getSize());
	        //System.err.println("[NewChartComponentImpl] paintComponent. unit width="+getViewState().getBottomUnitWidth());
	        model.setBottomUnitWidth(getViewState().getBottomUnitWidth());
	        model.setRowHeight(tree.getJTree().getRowHeight());
	        model.setTopTimeUnit(getViewState().getTopTimeUnit());
	        model.setBottomTimeUnit(getViewState().getBottomTimeUnit());
	        VisibleNodesFilter visibleNodesFilter = new VisibleNodesFilter();
	        List visibleTasks = visibleNodesFilter.getVisibleNodes(tree.getJTree(), getScrollBar(), getHeight(), 20);
	        model.setVisibleTasks(visibleTasks);
	        model.paint(g);
            if (getActiveInteraction()!=null) {
                getActiveInteraction().paint(g);
            }
		}


        public MouseListener getMouseListener() {
            return myMouseListener;
        }
        
        public MouseMotionListener getMouseMotionListener() {
        	return myMouseMotionListener;
        }
        private OldChartMouseListenerImpl myMouseListener = new OldChartMouseListenerImpl();
    	private OldMouseMotionListenerImpl myMouseMotionListener = new OldMouseMotionListenerImpl();
    	
    }
    
    
    protected AbstractChartImplementation getImplementation() {
        return (AbstractChartImplementation) getChartImplementation();
    }
    private ChartImplementation getChartImplementation() {
        if (myChartComponentImpl==null) {
            myChartComponentImpl = new NewChartComponentImpl();
        }
        return myChartComponentImpl;
    }
    private static final boolean COMPONENT_1_11 = true;
    private ChartImplementation myChartComponentImpl;
    
        
    private class OldChartMouseListenerImpl extends MouseListenerBase implements MouseListener {
        private MouseSupport myMouseSupport = new MouseSupport();
        
        public void mouseClicked(MouseEvent e) {
            if (e.getClickCount() == 2 && e.getButton() == MouseEvent.BUTTON1) {
                if (!appli.isOnlyViewer)
                    appli.propertiesTask();
            }
        }

        public void mousePressed(MouseEvent e) {
            if (appli.isOnlyViewer)
                return;
            Task taskUnderPointer = myMouseSupport.findTaskUnderMousePointer(e.getX(), e.getY());
            if (taskUnderPointer==null) {
                super.mousePressed(e);
                return;
            }
            if (e.isPopupTrigger()) {
                tree.selectTreeRow(taskUnderPointer.getTaskID());
                tree.createPopupMenu((int) getLocation().getX() + e.getX(),
                (int) getLocation().getY() + e.getY() - 45 +
                margY, true);
                repaint();
                return;
            }
            if (e.getButton() == MouseEvent.BUTTON1) {
                tree.selectTask(taskUnderPointer);
                ChartItem itemUnderPoint = myMouseSupport.getChartItemUnderMousePoint(e.getX(), e.getY());
                if (itemUnderPoint instanceof TaskBoundaryChartItem) {
                	TaskBoundaryChartItem taskBoundary = (TaskBoundaryChartItem) itemUnderPoint;
                	if (taskBoundary.isStartBoundary()) {
                		getChartImplementation().beginChangeTaskStartInteraction(e, taskBoundary);
                	}
                	else {                    		
                		getChartImplementation().beginChangeTaskEndInteraction(e, taskBoundary);
                	}
                }
                else if (itemUnderPoint instanceof TaskProgressChartItem) {
                	getChartImplementation().beginChangeTaskProgressInteraction(e, (TaskProgressChartItem)itemUnderPoint);
                    //setCursor(new Cursor(Cursor.E_RESIZE_CURSOR));
                }
                else if (itemUnderPoint instanceof TaskRegularAreaChartItem){
                    getChartImplementation().beginDrawDependencyInteraction(e, (TaskRegularAreaChartItem)itemUnderPoint, myMouseSupport);
                }
                repaint();
            }
            else if (e.getButton() == MouseEvent.BUTTON2) {
            	getChartImplementation().beginMoveTaskInteraction(e, taskUnderPointer);
            }
        }

    }

    private class OldMouseMotionListenerImpl extends MouseMotionListenerBase {
        private MouseSupport myMouseSupport = new MouseSupport();
		public void mouseDragged(MouseEvent e) {
			if (appli.isOnlyViewer)
				return;
            super.mouseDragged(e);
		}

		//Move the move on the area
		public void mouseMoved(MouseEvent e) {
			ChartItem itemUnderPoint = myMouseSupport.getChartItemUnderMousePoint(e.getX(), e.getY());
			Task taskUnderPoint = itemUnderPoint==null ? null : itemUnderPoint.getTask();
			//System.err.println("[OldMouseMotionListenerImpl] mouseMoved: taskUnderPoint="+taskUnderPoint);
			if (taskUnderPoint==null) {
				setDefaultCursor();
			}
			else {
				if (itemUnderPoint instanceof TaskBoundaryChartItem) {
					Cursor cursor = ((TaskBoundaryChartItem)itemUnderPoint).isStartBoundary() ? W_RESIZE_CURSOR : E_RESIZE_CURSOR;
					setCursor(cursor);
				}
				//special cursor
				else if (itemUnderPoint instanceof TaskProgressChartItem) {
					setCursor(CHANGE_PROGRESS_CURSOR);
				}
				else {
					setDefaultCursor();
				}
			}
		}
	}
    
}

