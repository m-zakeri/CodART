/***************************************************************************
 * GanttGraphicArea.java  -  description
 * -------------------
 * begin                : dec 2002
 * copyright            : (C) 2002 by Thomas Alexandre
 * email                : alexthomas(at)ganttproject.org
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
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.awt.image.BufferedImage;
import java.awt.print.PrinterJob;
import java.io.File;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.tree.DefaultMutableTreeNode;

import net.sourceforge.ganttproject.ChartComponentBase.AbstractChartImplementation;
import net.sourceforge.ganttproject.chart.ChartModel;
import net.sourceforge.ganttproject.chart.ChartModelBase;
import net.sourceforge.ganttproject.chart.ChartModelImpl;
import net.sourceforge.ganttproject.chart.ChartModelResource;
import net.sourceforge.ganttproject.chart.VisibleNodesFilter;
import net.sourceforge.ganttproject.gui.UIFacade;
import net.sourceforge.ganttproject.gui.zoom.ZoomManager;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.resource.ResourceManager;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.time.gregorian.GregorianCalendar;


/**
 * Classe for the graphic part of the soft
 */
public class ResourceLoadGraphicArea extends ChartComponentBase {
    
    /** Begin of display. */
    public GanttCalendar date, olddate;
    
    /** Reference to the GanttTree */
    public JTable table;
    
    
    
    /** Zoom  to on week */
    public static final int ONE_WEEK=0;
    
    /** Zoom  to two week */
    public static final int TWO_WEEK=1;
    
    /** Zoom  to one month */
    public static final int ONE_MONTH=2;
    
    /** Zoom  to two month */
    public static  final int TWO_MONTH=3;
    
    /** Zoom  to tree month */
    public static  final int THREE_MONTH=4;
    
    /** Zoom  to tree month */
    public static  final int FOUR_MONTH=5;
    
    /** Zoom  to six month */
    public static  final int SIX_MONTH=6;
    
    /** Zoom  to one year */
    public static  final int ONE_YEAR=7;
    
    /** Zoom  to two year */
    public static  final int TWO_YEAR=8;
    
    /** Zoom  to three year */
    public static  final int THREE_YEAR=9;
    
    /** Default color for tasks */
    public static Color taskDefaultColor
    = new Color((float)0.549,(float)0.713,(float)0.807);
    
    /* The Zoom Value */
    private int zoomValue;
    
    /** Array to store parameters of each task (for display) */
    private ArrayList listOfParam = new ArrayList();
    
    /** This value is connected to the GanttTRee Scrollbar to move up or down */
    private int margY;
    
    /** UpperLeft Point (for the margin of printing) */
    private Point upperLeft=new Point(0,0);
    
    /** Render on the window or for printing*/
    private boolean printRendering=false;
    
    /** Render the depends */
    private boolean drawdepend = true;
    /** Render the depends */
    private boolean drawPercent = true;
    /* Render the name*/
    private boolean drawName = false;
    /* Render the ganttproject version*/
    private boolean drawVersion = false;
    /** render the 3d border. */
    private boolean draw3dBorders = true; 
		
		
		
    /** The language */
    private GanttLanguage language;
    
    /*! The main application */
    private GanttProject appli;
    
    /*! Old X and Yposition*/
    private int oldX, oldY;
    
    /** Move the view of the calendar or move a task*/
    private boolean moveView=true;
    
    /** the Task number to move */
    private int moveTask=-1;
    
    /** Cursor by default*/
    boolean curs=false;
    
   
    /** Type of selection 0 -> move duration,   1 -> moveDate,   2->add Depend*/
    int typeSeletion;
    
    /** Parmeters to change the duration of the task*/
    private int storeTaskLength;
    private float addTaskLength;
    private GanttCalendar storeTaskStart;
    private int []storeX =new int[3];
    
    /** The task to move duration*/
    //private Task taskToMove=new GanttTask("toto",new GanttCalendar(),10);
    
    /**Color array use to paint */
    private Color [] arrayColor = new Color[15];
    
    /** List of task recup before painting */
    private ArrayList listOfTask;
    
    /** Begin of project */
    public GanttCalendar beg = new GanttCalendar();
    
    /**End date for the project */
    public GanttCalendar end = new GanttCalendar();
    
    private ArrayList loads;
    
    public final GanttTree tree;
    
    /** The mouse button press */
    public int mouseButton=0;

    private ChartModelResource myChartModel;
    
    /** Constructor */
    public ResourceLoadGraphicArea(GanttProject app, GanttTree tree, JTable table, ZoomManager zoomManager) {
        super((IGanttProject)app, (UIFacade)app, zoomManager);
        myChartModel = new ChartModelResource(getTaskManager(), (HumanResourceManager) app.getHumanResourceManager(), getTimeUnitStack(), getUIConfiguration());
        getViewState().addStateListener(myChartModel);
        getViewState().setStartDate(GregorianCalendar.getInstance().getTime());
        date = new GanttCalendar();
        olddate=new GanttCalendar();
        date.setDay(1);
        this.table = table;
        this.tree= tree;
        zoomValue = ONE_MONTH;	//zoom to one month by default of the current date
        
        margY = 0;
        this.language = GanttLanguage.getInstance();
        appli = app;
        
        //Listener on wheel mouse
            
	    
	    
	    //creation of the different color use to paint
      //arrayColor[0] = new Color((float)0.905,(float)0.905,(float)0.905);
      arrayColor[0] = new Color((float)0.930,(float)0.930,(float)0.930);
      arrayColor[1] = new Color((float)0.745,(float)0.745,(float)0.745);
      arrayColor[2] = new Color((float)0.843,(float)0.890,(float)0.910);
      arrayColor[3] = new Color((float)0.722,(float)0.765,(float)0.780);
      arrayColor[4] = new Color((float)0.482,(float)0.482,(float)0.482);
      arrayColor[5] = new Color((float)0.807,(float)0.807,(float)0.807);
      arrayColor[6] = taskDefaultColor;
      arrayColor[7] = new Color((float)0.741,(float)0.745,(float)0.741);
      arrayColor[8] = new Color((float)0.388,(float)0.396,(float)0.388);
      arrayColor[9] = new Color((float)0.196,(float)0.196,(float)0.196);
      arrayColor[10]= new Color((float)0.192,(float)0.298,(float)0.525);
      arrayColor[11]= new Color((float)0.141,(float)0.141,(float)0.141);
      arrayColor[12]= new Color((float)0.290,(float)0.349,(float)0.643);
      arrayColor[13]= new Color((float)0.851,(float)0.902,(float)0.937);
      arrayColor[14]= new Color((float)0.961,(float)0.961,(float)0.961);
        
    }

   
    /** The size of the panel. */
    public Dimension getPreferredSize() {
        return new Dimension(465, 600);
    }
    
    /** Method to change the date */
    public void changeDate(boolean next) {
        int f=1;
        if(!next)f=-1;
        
        switch(zoomValue) {
            case ONE_WEEK:case TWO_WEEK:date.go(Calendar.WEEK_OF_YEAR,1*f); break;
            case ONE_MONTH:case TWO_MONTH:case THREE_MONTH:case FOUR_MONTH:case SIX_MONTH:date.go(Calendar.MONTH,1*f); break;
            case ONE_YEAR:case TWO_YEAR:case THREE_YEAR:date.go(Calendar.YEAR,1*f);break;
        }
    }
		
		/** Method to change the date */
  public void changeDate2(GanttCalendar gc) {
    switch (zoomValue) {
              case ONE_WEEK:    gc.go(Calendar.WEEK_OF_YEAR, 1); break;
              case TWO_WEEK:    gc.go(Calendar.WEEK_OF_YEAR, 2); break;
              case ONE_MONTH:   gc.go(Calendar.MONTH, 1); break;
              case TWO_MONTH:   gc.go(Calendar.MONTH, 2); break;
              case THREE_MONTH: gc.go(Calendar.MONTH, 3); break;
							case FOUR_MONTH:  gc.go(Calendar.MONTH, 4); break;
              case SIX_MONTH:   gc.go(Calendar.MONTH, 6); break;
              case ONE_YEAR:    gc.go(Calendar.YEAR, 1);break;
              case TWO_YEAR:    gc.go(Calendar.YEAR, 2);break;
              case THREE_YEAR:  gc.go(Calendar.YEAR, 3);break;
							//default:System.out.println("Resource + Should never append -->  zoomValue="+zoomValue);
            }
  }
    
    /** Method when zoomin, to set at the begin for each value */
    public void zoomToBegin() {
        switch(zoomValue) {
            case ONE_WEEK: case TWO_WEEK:
                String d = language.getDay(date.getDayWeek());
                while(!d.equals(language.getDay(2))) {
                    date.add(1);
                    d = language.getDay(date.getDayWeek());
                }
                
                break;
            case ONE_MONTH:case TWO_MONTH:case THREE_MONTH:case FOUR_MONTH:case SIX_MONTH:date.setDay(1);break;
            case ONE_YEAR:case TWO_YEAR:case THREE_YEAR:date.setMonth(0);
            date.setDay(1);
            break;
        }
    }
    
    
    /** draw the panel */
    public void paintComponent(Graphics g) {
        //Super paint component!!!!!!!!!!
        super.paintComponent(g);
        myChartModel.setBounds(getSize());
        myChartModel.setHeaderHeight(getHeaderHeight());
        //System.err.println("[NewChartComponentImpl] paintComponent. unit width="+getViewState().getBottomUnitWidth());
        myChartModel.setBottomUnitWidth(getViewState().getBottomUnitWidth());
        myChartModel.setRowHeight(tree.getJTree().getRowHeight());
        myChartModel.setTopTimeUnit(getViewState().getTopTimeUnit());
        myChartModel.setBottomTimeUnit(getViewState().getBottomTimeUnit());
        myChartModel.paint(g);
        
        //Move if its in printing (for margin)
        /*if(printRendering)
            g.translate((int)upperLeft.getX(),(int)upperLeft.getY());*/
        
        //Vertical bars
        //paintCalendar1(g);
        //The tasks
        //paintLoads(g);
        //The depends
        //        if(drawdepend) paintDepend(g);
        //The part at top
        //paintCalendar2(g);
        
        
        //        arrow.paint(g);
        //        notes.paint(g);
        
        if (drawVersion) {
      		drawGPVersion(g);			
    		}
        
    }
    
    protected int getHeaderHeight() {
		return 0;
	}


	public void drawGPVersion(Graphics g){
		  g.setColor(Color.black);
      g.setFont(new Font("SansSerif", Font.PLAIN, 10));
      g.drawString("GanttProject (" + GanttProject.version + ")", 3, getHeight() - 6);
		}
    
    /** Search for a coef on the arraylist */
    public int indexOf(ArrayList listOfParam, String coef) {
        for(int i=0;i<listOfParam.size();i++)
            if(coef==listOfParam.get(i).toString())
                return i;
        return -1;
    }
    
    /** Change the velue connected to the JTree's Scrollbar */
    public void setScrollBar(int v) { margY = v; }
    
    /** Return the value of the JTree's Scrollbar */
    public int getScrollBar() { return margY; }
    
    /** Change the zoom value */
    public void setZoom(int z) { zoomValue = z; }
    
    /** Add a zoom*/
    public void zoomMore() {
        if(zoomValue==5)olddate=date.Clone();
        zoomValue++;
    }
    
    /**Less a zoom*/
    public void zoomLess() {
        if(zoomValue==6 && date.getYear()==olddate.getYear())date=olddate.Clone();
        zoomValue--;
    }
    
    /** Return  the zoom value */
    public int getZoom() { return zoomValue; }
    
    /** Change the date of the begin to paint */
    public void setDate(GanttCalendar d) { date = d; }
    
    /** Return the date */
    public GanttCalendar getDate() { return date ; }
    
    /** Change language */
    public void setLanguage(GanttLanguage language) { this.language = language; }
    
    /** Return the number of day visible for each level of granularity */
    public int getGranit(boolean day) {
        GanttCalendar cal;
        int res=7;	//by default the 7 days of the week
        switch(zoomValue) {
            case ONE_WEEK: res=7; break;
            
            case TWO_WEEK:res=14;break;
            
            case ONE_MONTH:res=date.getNumberOfDay();break;
            
            case TWO_MONTH:cal = date.Clone();
                res=cal.getNumberOfDay();
                cal.goNextMonth();
                res+=cal.getNumberOfDay();
                break;
            
            case THREE_MONTH:cal = date.Clone();
            res=0;
            for(int i=0;i<3;i++) {
                res+=cal.getNumberOfDay();
                cal.goNextMonth();
            }break;
            
            case FOUR_MONTH:cal = date.Clone();
            res=0;
            for(int i=0;i<4;i++) {
                res+=cal.getNumberOfDay();
                cal.goNextMonth();
            }break;
            
            
            case SIX_MONTH:cal = date.Clone();
            res=0;
            for(int i=0;i<6;i++) {
                res+=cal.getNumberOfDay();
                cal.goNextMonth();
            }break;
            
            case ONE_YEAR:if(!day) res=12;
            else res=(date.getYear()%4==0)?366:365;
            break;
            
            case TWO_YEAR:if(!day) res=12*2;
            else {
                cal = date.Clone();
                res=0;
                for(int i=0;i<2;i++) {
                    if(cal.getYear()%4==0) res+=366;
                    else res+=365;
                    cal.go(Calendar.YEAR,1);
                }
            }
            break;
            
            case THREE_YEAR:if(!day) res=12*3;
            else {
                cal = date.Clone();
                res=0;
                for(int i=0;i<3;i++) {
                    if(cal.getYear()%4==0) res+=366;
                    else res+=365;
                    cal.go(Calendar.YEAR,1);
                }
            }
            break;
        }
        return res;
    }
    
    
    /** Return the advance foot  */
    public int getFoot() {
        int res=1;
        switch(zoomValue) {
            case ONE_YEAR:case TWO_YEAR:case THREE_YEAR:res=date.getNumberOfDay();break;
            //default:res=1;break;
        }
        
        return res;
    }
    
    /** Paint all tasks  */
    public void paintLoads(Graphics g) {
        int sizex = getWidth();
        int sizey = getHeight();
        int headery = 45;
        float fgra = (float)sizex / (float)getGranit(true); //pixels per day
        
        g.setFont(new Font("SansSerif",Font.PLAIN,9));
        
        //Get all task
        ArrayList listOfTask = tree.getAllTasks();

        if (listOfTask.size()<=1)
            return;
        
        calculateLoad(listOfTask);
        
        //Probably optimised on next release
        listOfParam.clear();
        
        GanttCalendar firstStart=new GanttCalendar(),lastEnd=new GanttCalendar();
        int duration=0;//lastEnd=new GanttCalendar();
        
        
        
        firstStart=((Task) ((DefaultMutableTreeNode)listOfTask.get(1)).getUserObject()).getStart();
        lastEnd=firstStart;
        //Calcul all parameters
        for(int i=2;i<listOfTask.size();i++) {
            Task task =(Task) ((DefaultMutableTreeNode)listOfTask.get(i)).getUserObject();
            
            if (firstStart.compareTo(task.getStart())==1)
                firstStart=task.getStart();
            if (lastEnd.compareTo(task.getEnd())==-1)
                lastEnd=task.getEnd();
        }
        
        duration=firstStart.diff(lastEnd);

        int x1=-10, x2=sizex+10;
        int e1;
        int fois;
        int type = 2;

        
        //difference between the start date of the task and the start of the display area
        e1 = date.diff(firstStart);
        
        //System.out.println ("date: "+date);
        
        //Calcul start and end pixel of each task
        float fx1, fx2;
        
        
        fx1 = 0;
        //                fx1 =1;
        fx2 = fx1 + (float)duration * fgra;
        x1 = (int) fx1;
        x2 = (int) fx2;
        
        
        int percent =0, intLoad=-1;
        
        x2 = (int) ((float)getGranit(true)*fgra);
        
        x2=0;
				
				
				
        
        // hier brauche ich ein Mapping zwischen Usern und ihrer y Position        
        HumanResourceManager resMan=(HumanResourceManager) appli.getHumanResourceManager();
        
        ArrayList users=resMan.getResources();
				
				/** State for rendering each cell of the chart*/
				boolean [] state = new boolean[users.size()>0?users.size():1];
				boolean [] oldState = new boolean[users.size()>0?users.size():1];
				
				for(int i=0;i<users.size();i++){
					state[i]=false;
					oldState[i]=false;
				}
				

        for (int i=0; i<getGranit(true); i++) {
            Hashtable load = (Hashtable)loads.get(i);

            if (load!=null) {
						
                for (int y=0; y<users.size();y++) {
                    
										oldState[y] = state[y];
										
										String key=((HumanResource)users.get(y)).toString();
                    //System.out.println(key);
                    if (load.get(key)!=null) {
                        intLoad = ((Integer)load.get(key)).intValue();
	                    	state[y] = true;
										}
                    else {
                        intLoad=-1;
												state[y] = false;
										}

                    if (intLoad > 100)
                        paintAResourceLoad(g, x1+(int)(i*fgra), x2+(int)((i+1)*fgra), y+1,
                                    "xx",appli.getUIConfiguration().getResourceOverloadColor(), state[y], oldState[y] );
                    else if (intLoad >0) {
                        paintAResourceLoad(g, x1+(int)(i*fgra), x2+(int)((i+1)*fgra), y+1,
                                    "xx",appli.getUIConfiguration().getResourceColor(), state[y], oldState[y] );
                    }
                }
            }
         }
        type=2;
        
    }
    
//		public void paintEndBorder(Graphics g, int x2, int y ) {
//			y=y*20+40-margY;
//			if(y<20 || y > getHeight()) return;	//Not draw if the task is not on the area
//			g.setColor(Color.black);
//			g.drawLine(x2,y,x2,y+12);
//			g.setColor(arrayColor[8]);
//			g.drawLine(x2-1,y+2,x2-1,y+11);
//		}
//		
   
    /** Draw a normal task */
    public void paintAResourceLoad(Graphics g, int x1, int x2, int y, String taskName, Color color,
				boolean state, boolean oldState) {
        x2++;
				int d=y;
        y=y*20+40-margY;
        
        if(y<20 || y > getHeight()) return;	//Not draw if the task is not on the area
        if((x1>getWidth() && x2>getWidth()) || (x1<0 && x2<0)) return;
        
        boolean first_cell = (state && !oldState);
				//boolean end_cell = (!state && oldState);
				
				int xd = x1;
				if(!first_cell) xd-=2;
				
				
				//Blue rectangle
        g.setColor(color);
        g.fillRect(xd, y, (x2-x1)+2,12 );

		if(draw3dBorders)
		{	
				g.setColor(Color.black);
				g.drawLine(xd,y, x2-1, y);
				g.drawLine(xd,y+12, x2-1, y+12);
				
				//Down (color mor dark)
				//g.setColor(arrayColor[8]);
				//g.drawLine(xd,y+11, x2-1, y+11);
				
				
				//Top (color more light)
				//g.setColor(arrayColor[7]);
				//g.drawLine(xd,y+1, x2-1, y+1);
				
				
				//draw the begin of the nice border
				if(first_cell){
					g.setColor(Color.black);
					g.drawLine(x1,y,x1,y+12);
					g.setColor(arrayColor[7]);
					g.drawLine(x1+1,y+1,x1+1,y+11);
				}
				
				//draw the end of the bar (not great algorithm because end is design each timt, but it's a first version ....:(
				g.setColor(Color.black);
				g.drawLine(x2,y,x2,y+12);
				g.setColor(arrayColor[8]);
				g.drawLine(x2-1,y+2,x2-1,y+11);
		}		
      
        if(drawName) {
            g.setColor(Color.black);
            g.drawString(taskName, x2+40,y+10);
        }
        
    }

    
    private void calculateLoad (ArrayList tasks) {
        
        loads=new  ArrayList();
        
        for (int i=0; i<getGranit(true); i++)
            loads.add(null);
        
        for (int i=0;i<tasks.size();i++) {
            Task task = (Task)((DefaultMutableTreeNode)tasks.get(i)).getUserObject();

            GanttCalendar displayStart=date.Clone(),displayEnd=date.Clone();
            displayEnd.add(getGranit(true));
            
            // prüfen ob task im sichtbaren Bereich
            if (task.getStart().compareTo(displayStart)==-1 && task.getEnd().compareTo(date)==-1) {// Task is completely before display area
                continue;
            }
            if (task.getStart().compareTo(displayEnd)==1) {
                continue;
            }
            
            // nicht nur der Tag auch der Monat muss gechecked werden
            
//            Welche Struktur welche Daten ???? Wie die Tage über resourcen auftragen.
//            Start liegt vor Display Start also start=1
            
            int start;
            int duration;
            
            if (task.getStart().compareTo(displayStart)==-1) {
                duration = task.getEnd().diff(displayStart);
                start=0;
            }
            else {
                start = date.diff(task.getStart());
                duration = task.getEnd().diff(task.getStart());
            }
            int intLoad=0;
            
            if (start+duration>getGranit(true)) 
                duration=getGranit(true)-start;
            
            //ArrayList users = task.getUsersList();
            ResourceAssignment[] assignments = task.getAssignments();
            for (int j=0;j<assignments.length;j++) {
                //Hashtable resData = (Hashtable) users.get(j);
                ResourceAssignment next = assignments[j];

                for (int d=start; d<start+duration; d++) {
                    Hashtable load=(Hashtable)loads.get(d);
                    if (load==null) {
                        load=new Hashtable();
                        loads.set(d, load);
                    }
                    Integer lo=(Integer)load.get(next.getResource().getName());
                    if (lo!=null) 
                        intLoad=lo.intValue();
                    else
                        intLoad=0;
                    
                    intLoad+=next.getLoad();
                    
                    load.put(next.getResource().getName(), new Integer(intLoad));
                }
                
            }
        }
    }
    
		
		/** Return an image with the gantt chart*/
	public BufferedImage getChart(GanttExportSettings settings) {
		int rendering = 0;
		
		GanttCalendar date2 = new GanttCalendar(date);
		date = new GanttCalendar(beg);
		zoomToBegin();
		GanttCalendar  start =  new GanttCalendar(date);
		date = new GanttCalendar(date2);
				
		while(start.compareTo(end)<=0){
			changeDate2(start);
			rendering++;
		}
		
		//Make save of parameters
		int oldMargY = margY;
		int oldHeight=getHeight();
		int height = 20;
		int width=getWidth();
		margY=0;
		draw3dBorders = settings.border3d;
		
		ResourceManager resMan=(HumanResourceManager) appli.getHumanResourceManager();
		ArrayList users=resMan.getResources();
		
		
		int sizeTOC=0; //Size of the content table for the resources list
		BufferedImage tmpImage = new BufferedImage(10, 10, BufferedImage.TYPE_INT_RGB);
		FontMetrics fmetric = tmpImage.getGraphics().getFontMetrics(new Font("SansSerif", Font.PLAIN, 10));
		
		for (Iterator user = users.iterator(); user.hasNext(); ) {
      String nameOfRes=((HumanResource)user.next()).toString();
			int nbchar = fmetric.stringWidth(nameOfRes);
			if(nbchar>sizeTOC)sizeTOC=nbchar;
		}
		sizeTOC+=20;
	
		//If there is only the root task
		setSize(width, users.size()*20 + 80);
    
		int calculateWidth=width*rendering;
		if(settings.name) {
			rendering++;
			calculateWidth+=sizeTOC;
		}
		
		BufferedImage image = new BufferedImage(calculateWidth, getHeight(), BufferedImage.TYPE_INT_RGB);
		printRendering = true;
		
		start=new GanttCalendar(date);
		date=new GanttCalendar(beg);
		zoomToBegin();
		if(zoomValue==ONE_WEEK || zoomValue==TWO_WEEK) changeDate(false);
		
		
		int transx=0, transx2;
		
		for(int i=0;i<rendering;i++){

			BufferedImage image2 = new BufferedImage(width, getHeight(), BufferedImage.TYPE_INT_RGB);
			if(i==0 && settings.name){
				rowCount=0;
				image2 = null;
				image2 = new BufferedImage(sizeTOC, getHeight(), BufferedImage.TYPE_INT_RGB);
				setSize(sizeTOC, getHeight());
				printResources(image2.getGraphics());
				setSize(width, getHeight());
				transx2=sizeTOC;
			}
			else {paintComponent(image2.getGraphics());	changeDate2(date);	transx2=width;}	
			
			
			Graphics g = image.getGraphics();
			g.translate(transx,0);
			g.drawImage(image2,0,0,null);
			
			image2=null;
			
			transx+=transx2;
			
		}
		upperLeft = new Point(0,0);
		drawGPVersion(image.getGraphics());		
		printRendering = false;
		
		date=new GanttCalendar(start);
		zoomToBegin();
		margY=oldMargY;
		//drawVersion = false;
		draw3dBorders = true;
		setSize(getSize().width, oldHeight);
		repaint();
		
		return image;		
	}
	
	private int rowCount=0;
	
	/** Print the list of tasks */
	private void printResources(Graphics g){
		g.setColor(Color.white);
		g.fillRect(0, 0, getWidth(), getHeight());

		g.setColor(Color.black);
		g.setFont(new Font("SansSerif", Font.PLAIN, 10));
		
		ResourceManager resMan=(HumanResourceManager) appli.getHumanResourceManager();
		ArrayList users=resMan.getResources();
		
		int y=55;
		
		for(Iterator user = users.iterator(); user.hasNext(); ) {
			String nameOfRes=((HumanResource)user.next()).toString();
			
			if(rowCount%2==1) {
				g.setColor(new Color( (float) 0.933, (float) 0.933, (float) 0.933));
				g.fillRect(0,y,getWidth()-10, 20);	
			}
			g.setColor(Color.black);
			g.drawRect(0,y,getWidth()-10, 20);	
			g.drawString(nameOfRes, 5, y+13);
			g.setColor(arrayColor[5]);
			if(draw3dBorders)
				g.drawLine(1,y+19,getWidth()-11,y+19);
			y+=20;
			rowCount++;
		}
		
	}	
		
    
    /** Function able to export in PNG format the graphic area */
  public void export(File file, String format, GanttExportSettings settings) {
    
		BufferedImage image = getChart(settings);

    try {
      if (!ImageIO.write(image, format, file)) {
        System.out.println("Impossible de sauvegarder dans ce format");

      }
    }
    catch (Exception e) {
      System.out.println(e);
    }
  }
  
      /** Function able to export in PNG format the graphic area */
    public void export(OutputStream os, String format, GanttExportSettings settings) {

        BufferedImage image = getChart(settings);

        try {
            if (!ImageIO.write(image, format, os)) {
                System.out.println("Impossible de sauvegarder dans ce format");

            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }
    
    
     /** Print the project */
    public void printProject(GanttExportSettings settings) {
    	
			
			BufferedImage image = getChart(settings);
		
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
    
    
    protected ChartModelBase getChartModel() {
        return myChartModel;
    }


    protected MouseListener getMouseListener() {
        if (myMouseListener==null) {
            myMouseListener = new MouseListenerBase();
        }
        return myMouseListener;
    }

    
    protected MouseMotionListener getMouseMotionListener() {
        if (myMouseMotionListener==null) {
            myMouseMotionListener = new MouseMotionListenerBase();
        }
        return myMouseMotionListener;
    }
    protected AbstractChartImplementation getImplementation() {
        return myChartImplementation;
    }
    
    private MouseMotionListener myMouseMotionListener;
    private MouseListener myMouseListener;
    private AbstractChartImplementation myChartImplementation = new AbstractChartImplementation();
}

