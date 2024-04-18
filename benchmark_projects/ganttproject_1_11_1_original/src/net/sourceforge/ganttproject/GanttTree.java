/***************************************************************************
 * GanttTree.java  -  description
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

import java.awt.AlphaComposite;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.awt.GradientPaint;
import java.awt.Graphics2D;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.SystemColor;
import java.awt.datatransfer.DataFlavor;
import java.awt.datatransfer.Transferable;
import java.awt.datatransfer.UnsupportedFlavorException;
import java.awt.dnd.Autoscroll;
import java.awt.dnd.DnDConstants;
import java.awt.dnd.DragGestureEvent;
import java.awt.dnd.DragGestureListener;
import java.awt.dnd.DragSource;
import java.awt.dnd.DragSourceDragEvent;
import java.awt.dnd.DragSourceDropEvent;
import java.awt.dnd.DragSourceEvent;
import java.awt.dnd.DragSourceListener;
import java.awt.dnd.DropTarget;
import java.awt.dnd.DropTargetDragEvent;
import java.awt.dnd.DropTargetDropEvent;
import java.awt.dnd.DropTargetEvent;
import java.awt.dnd.DropTargetListener;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.AdjustmentEvent;
import java.awt.event.AdjustmentListener;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.geom.AffineTransform;
import java.awt.geom.Rectangle2D;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.*;

import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTree;
import javax.swing.Timer;
import javax.swing.ToolTipManager;
import javax.swing.event.TreeExpansionEvent;
import javax.swing.event.TreeExpansionListener;
import javax.swing.event.TreeModelEvent;
import javax.swing.event.TreeModelListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellEditor;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.MutableTreeNode;
import javax.swing.tree.TreeCellRenderer;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;
import javax.swing.tree.TreeSelectionModel;

import net.sourceforge.ganttproject.action.NewTaskAction;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.task.ResourceAssignment;
import net.sourceforge.ganttproject.task.Task;
import net.sourceforge.ganttproject.task.TaskLength;
import net.sourceforge.ganttproject.task.TaskManager;
import net.sourceforge.ganttproject.task.TaskManagerImpl;
import net.sourceforge.ganttproject.task.algorithm.AdjustTaskBoundsAlgorithm;
import net.sourceforge.ganttproject.task.algorithm.RecalculateTaskScheduleAlgorithm;
import net.sourceforge.ganttproject.task.dependency.TaskDependencyException;

/**
 * Class that generate the JTree
 */
public class GanttTree
    extends JPanel implements DragSourceListener, DragGestureListener {
  /** The root node of the Tree */
  private DefaultMutableTreeNode rootNode;

  /** The model for the JTree */
  private DefaultTreeModel treeModel;

  /** The JTree. */
  private JTree tree;

  /** Pointer on graphic area */
  private GanttGraphicArea area = null;

  /** Pointer on application */
  private GanttProject appli;

  /** An array for expansion */
  //private ArrayList expand = new ArrayList();


  private static final int AUTOSCROLL_MARGIN = 12;

  /** The vertical scrollbar on the JTree */
  JScrollBar vbar;
  /** The horizontal scrollbar on the JTree */
  JScrollBar hbar;

  /** The language use*/
  GanttLanguage language = GanttLanguage.getInstance();
  
  /** Number of tasks on the tree. */
  int nbTasks = 0;

  private TreePath dragPath = null;
  private BufferedImage ghostImage=null;         // The 'drag image'
  private Point offsetPoint = new Point();  // Where, in the drag image, the mouse was clicked
  private final TaskManager myTaskManager;

  private class AutoscrollingTree extends JTree implements Autoscroll {

    public AutoscrollingTree(DefaultTreeModel treeModel) {
        super(treeModel);
    }

    // Calculate the insets for the *JTREE*, not the viewport
    // the tree is in. This makes it a bit messy.
    public Insets getAutoscrollInsets()
    {
        Rectangle raOuter = getBounds();
        Rectangle raInner = getParent().getBounds();
        return new Insets(
            raInner.y - raOuter.y + AUTOSCROLL_MARGIN, raInner.x - raOuter.x + AUTOSCROLL_MARGIN,
            raOuter.height - raInner.height - raInner.y + raOuter.y + AUTOSCROLL_MARGIN,
            raOuter.width - raInner.width - raInner.x + raOuter.x + AUTOSCROLL_MARGIN);
    }

    public void autoscroll(Point pt)
    {
        // Figure out which row we’re on.
        int nRow = this.getClosestRowForLocation(pt.x, pt.y);

        // If we are not on a row then ignore this autoscroll request
        if (nRow < 0)
            return;

        Rectangle raOuter = getBounds();
        // Now decide if the row is at the top of the screen or at the
        // bottom. We do this to make the previous row (or the next
        // row) visible as appropriate. If we’re at the absolute top or
        // bottom, just return the first or last row respectively.

        nRow =  (pt.y + raOuter.y <= AUTOSCROLL_MARGIN)         // Is row at top of screen?
                 ?
                (nRow <= 0 ? 0 : nRow - 1)                      // Yes, scroll up one row
                 :
                (nRow < this.getRowCount() - 1 ? nRow + 1 : nRow);   // No, scroll down one row

        this.scrollRowToVisible(nRow);
    }

  }

  /** Constructor. */
  public GanttTree(GanttProject app, TaskManager taskManager) {
    super();

    
    myTaskManager = taskManager;
    this.appli = app;

    //Create the root node
    initRootNode();
    treeModel = new DefaultTreeModel(rootNode);
    treeModel.addTreeModelListener(new GanttTreeModelListener());

    //Create the JTree
    tree = new AutoscrollingTree(treeModel);
    tree.setEditable(false);
    
    tree.addKeyListener(app); //callback for keyboard pressed 
    
    //--Newly added code--CL
    tree.setEditable(true);
    tree.setCellEditor(new DefaultTreeCellEditor(tree,
                                                 new GanttTreeCellRenderer(),
                                                 new GanttTreeCellEditor(tree,
        new JTextField()))
                       );
    //---Newly added code--CL

    tree.setBackground(new Color(1.0f, 1.0f, 1.0f));
    tree.getSelectionModel().setSelectionMode(TreeSelectionModel.DISCONTIGUOUS_TREE_SELECTION);
    tree.setShowsRootHandles(true);
    tree.setRowHeight(20);
    tree.setRootVisible(false);
    tree.addTreeExpansionListener(new GanttTreeExpansionListener());


    ToolTipManager.sharedInstance().registerComponent(tree);
    tree.setCellRenderer(new GanttTreeCellRenderer());

    //Add The tree on a Scrollpane
    JScrollPane scrollpane = new JScrollPane(tree);
    setLayout(new BorderLayout());
    add(scrollpane, BorderLayout.CENTER);
    vbar = scrollpane.getVerticalScrollBar();
    hbar = scrollpane.getHorizontalScrollBar();
    vbar.addAdjustmentListener(new GanttAdjustmentListener());

    //A listener on mouse click (menu)
    MouseListener ml = new MouseAdapter() {
      public void mouseClicked(MouseEvent e) {
        
      	int selRow = tree.getRowForLocation(e.getX(), e.getY());
        TreePath selPath = tree.getPathForLocation(e.getX(), e.getY());
        if (selRow != -1) {
          if (e.getClickCount() == 1 && e.getButton() == MouseEvent.BUTTON3) {
            
          	{//selection path part          	
          		
          		TreePath [] currentSelection = tree.getSelectionPaths();
          		
          		if(currentSelection == null || currentSelection.length==0)
          			tree.setSelectionPath(selPath);
          		else {
          			boolean contains = false;
          			for(int i=0;i<currentSelection.length && !contains;i++)
          				if(currentSelection[i]==selPath)
          					contains=true;
          			if(!contains) tree.setSelectionPath(selPath);
          		}            
          	}
            createPopupMenu(e.getX(), e.getY(), true);
          }
          else if (e.getClickCount() == 2 &&
                   e.getButton() == MouseEvent.BUTTON1) {
            e.consume();
            appli.propertiesTask();
          }
        }
        else {
			tree.setSelectionPath(null);
			if (e.getClickCount() == 1 && e.getButton() == MouseEvent.BUTTON3)
        		  createPopupMenu(e.getX(), e.getY(), false);
        }

      }
    };
    if(!app.isOnlyViewer)
    	tree.addMouseListener(ml);

    DragSource dragSource = DragSource.getDefaultDragSource();
    dragSource.createDefaultDragGestureRecognizer(tree, DnDConstants.ACTION_COPY_OR_MOVE, this);
    dragSource.addDragSourceListener(this);
    DropTarget dropTarget = new DropTarget(tree, new GanttTreeDropListener());
    dropTarget.setDefaultActions(DnDConstants.ACTION_COPY_OR_MOVE);

  }

    private void initRootNode() {
        rootNode = new DefaultMutableTreeNode(getTaskManager().getRootTask());
    }
    

    /** Create a popup menu when mous click*/
	public void createPopupMenu(int x, int y, boolean all) {
		JPopupMenu menu = new JPopupMenu();

		if(all) {
			boolean bOne = (tree.getSelectionCount()==1);
		if(bOne) menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("propertiesTask")), "/icons/properties_16.gif"));
	    menu.add(new NewTaskAction((IGanttProject)appli));
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("deleteTask")), "/icons/delete_16.gif"));
	    menu.addSeparator();
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("indentTask")), "/icons/indent_16.gif"));
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("dedentTask")), "/icons/unindent_16.gif"));
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("upTask")), "/icons/up_16.gif"));
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("downTask")), "/icons/down_16.gif"));
	    menu.addSeparator();
	    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("unlink")), "/icons/unlink_16.gif"));
	    if(tree.getSelectionCount()>=2)
	    	menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("link")), "/icons/link_16.gif"));
	    menu.addSeparator();
	}
	else {
		menu.add(new NewTaskAction((IGanttProject)appli));
		menu.addSeparator();
	}
		menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("cut")), "/icons/cut_16.gif"));
    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("copy")), "/icons/copy_16.gif"));
    menu.add(appli.createNewItem(GanttProject.correctLabel(language.getText("paste")), "/icons/paste_16.gif"));

    menu.applyComponentOrientation(language.getComponentOrientation());
    menu.show(this, x-hbar.getValue(), y - area.getScrollBar());
  }

  /** Change grpahic part */
  public void setGraphicArea(GanttGraphicArea area) {
    this.area = area;
  }

  /** Return the array of expansion  */
  /*public ArrayList getExpand() {
    return expand;
  }*/

  /** Set the expand array and modify in consequence */
  /*public void setExpand(ArrayList exp) {
    expand = exp;
    expandRefresh(rootNode);
  }*/

  /** add an object with the expand information */
  public DefaultMutableTreeNode addObjectWithExpand(Object child,
        DefaultMutableTreeNode parent) {
  	
  	DefaultMutableTreeNode childNode =
		new DefaultMutableTreeNode(child);

	if (parent == null)  parent = rootNode;

	treeModel.insertNodeInto(childNode, parent, parent.getChildCount());
	//forwardScheduling();
  	
	Task task = (Task)(childNode.getUserObject());

	boolean res = true;
	
	if (parent == null) res = false;
	 
	//test for expantion
	while (parent != null) {
	   Task taskFather = (Task)(parent.getUserObject()); 
	   if(!taskFather.getExpand()) 
	      res = false;
	    
	   parent = (DefaultMutableTreeNode)(parent.getParent());
	}
	
	if(res)
  		tree.scrollPathToVisible(new TreePath(childNode.getPath()));
  	else task.setExpand(false);
	
	nbTasks++;
	appli.refreshProjectInfos();
	
  	return childNode;
  }
  
  /** Add a sub task. */
  public DefaultMutableTreeNode addObject(Object child,
                                          DefaultMutableTreeNode parent) {
		DefaultMutableTreeNode childNode =
			new DefaultMutableTreeNode(child);

		if (parent == null)  parent = rootNode;

		//GanttTask tmpTask = (GanttTask)(childNode.getUserObject());
		//tmpTask.indentID((String)(((GanttTask)(parent.getUserObject())).getID()));

		treeModel.insertNodeInto(childNode, parent, parent.getChildCount());
		forwardScheduling();

		tree.scrollPathToVisible(new TreePath(childNode.getPath()));
		
		nbTasks++;
		appli.refreshProjectInfos();
		
		return childNode;
  }


  /** Return the selected task */
  public GanttTask getSelectedTask() {
  	DefaultMutableTreeNode node = getSelectedNode();
	if(node==null) return null;
	return (GanttTask)(node.getUserObject());
  }
 
  

  /** Return the selected node */
  public DefaultMutableTreeNode getSelectedNode() {
    TreePath currentSelection = tree.getSelectionPath();
    if (currentSelection == null) {
      return null;
    }
    DefaultMutableTreeNode dmtnselected = (DefaultMutableTreeNode)currentSelection.getLastPathComponent();
    return dmtnselected;
  }
  
  /** @return the list of the selected nodes. */
  public DefaultMutableTreeNode [] getSelectedNodes()
  {  	
  	TreePath [] currentSelection = tree.getSelectionPaths();
  	
  	if(currentSelection==null || currentSelection.length==0) //no elements are selectionned
  	 	return null;
  	
  	DefaultMutableTreeNode [] dmtnselected = new DefaultMutableTreeNode[currentSelection.length];
  	
  	for(int i=0; i<currentSelection.length; i++)
  		dmtnselected[i] = (DefaultMutableTreeNode)currentSelection[i].getLastPathComponent();
  	
  	return dmtnselected;
  }

  /** Returne the task with the name name*/
  public Task getTask(String name) {
    DefaultMutableTreeNode base;
    base = (DefaultMutableTreeNode) tree.getModel().getRoot();
    Enumeration e = base.preorderEnumeration();
    while (e.hasMoreElements()) {
      base = (DefaultMutableTreeNode) e.nextElement();
      if (base.toString().equals(name)) {
        return (Task) (base.getUserObject());
      }
    }
    return null;
  }

  /** Return the DefaultMutableTreeNodequi with the name name. */
  public DefaultMutableTreeNode getNode(int id /*String name*/) {
    DefaultMutableTreeNode res, base;
    base = (DefaultMutableTreeNode) tree.getModel().getRoot();
    Enumeration e = base.preorderEnumeration();
    while (e.hasMoreElements()) {
      res = ( (DefaultMutableTreeNode) e.nextElement());
      if (((Task)(res.getUserObject())).getTaskID()==id) {
        return res;
      }
    }
    return null;
  }


	/** Return tru if the Project has tasks and false is no tasks on the project */
	public boolean hasTasks() {
		Enumeration e = (rootNode).preorderEnumeration();
		while (e.hasMoreElements() ) {
			if(rootNode != (DefaultMutableTreeNode)e.nextElement())
				return true;
		}
		return false;
	}

  /** Returnan ArrayList with all tasks. */
  public ArrayList getAllTasks() {
      return Collections.list(rootNode.preorderEnumeration());
  }


  /** Return all sub task for the tree node base */
  public ArrayList getAllChildTask(Task task) {
    ArrayList res = new ArrayList();
    if(task==null)return null;
    DefaultMutableTreeNode base = (DefaultMutableTreeNode) getNode(task.getTaskID());
    if (base == null) return res;
    Enumeration e = base.children();
    while (e.hasMoreElements()) {
      res.add(e.nextElement());
    }
    return res;
  }


  /** Return all sub task for the tree node base */
  public ArrayList getAllChildTask(DefaultMutableTreeNode base) {
    ArrayList res = new ArrayList();
    if (base == null) return res;
    Enumeration e = base.children();
    while (e.hasMoreElements()) {
      res.add(e.nextElement());
    }
    return res;
  }


	/** Compute the percent complete for a parent task and return the value*/
	private void computePercentComplete (DefaultMutableTreeNode parent) {
		float totallength = 0;
		float totalcomplete = 0;
		float taskcomplete = 0;
		Enumeration e = parent.preorderEnumeration();
		DefaultMutableTreeNode node;
		Task task = (Task) parent.getUserObject();
		e.nextElement(); //skip the current parent task
		while (e.hasMoreElements()) {
    	node = (DefaultMutableTreeNode) e.nextElement();
			GanttTask temptask = (GanttTask) node.getUserObject();
      totallength = totallength + temptask.getLength();
			float tasklength = temptask.getLength();
			float taskpct = temptask.getCompletionPercentage();
      taskcomplete = (tasklength * (taskpct / 100));
      totalcomplete = totalcomplete + taskcomplete;
		}
		task.setCompletionPercentage((int) ((totalcomplete / totallength) * 100));
	}


	/** Return the last default tree node */
  public DefaultMutableTreeNode getLastNode() {
   return rootNode.getLastLeaf();
  }


  /** Return all tasks on an array */
  public Object[] getAllTaskArray() {
    ArrayList al = getAllTasks();
    return al.toArray();
  }

  /** Return all task exept the task in parameter */
  public String[] getAllTaskString(String except) {
    ArrayList l = getAllTasks();
    String[] res;
    if (except == null) {
      res = new String[l.size()];
    }
    else {
      res = new String[l.size() - 1];

    }
    int i = 0, j = 0;
    for (; i < l.size(); i++) {
      if (except == null || (l.get(i).toString() != except)) {
        Array.set(res, j, l.get(i).toString());
        j++;
      }
    }
    return res;
  }

  /** Return an ArrayList with String for all tasks */
  public ArrayList getArryListTaskString(String except) {
    ArrayList l = getAllTasks();
    ArrayList res = new ArrayList();
    for (int i = 0; i < l.size(); i++) {
      if ( (except != null && l.get(i).toString() != except) || except == null) {
        res.add(l.get(i).toString());
      }
    }
    return res;
  }

  /** Remove the current node. */
  public void removeCurrentNode() {
    TreePath currentSelection = tree.getSelectionPath();
    if (currentSelection != null) {
      DefaultMutableTreeNode currentNode = (DefaultMutableTreeNode)
          (currentSelection.getLastPathComponent());
      DefaultMutableTreeNode parent = (DefaultMutableTreeNode) (currentNode.getParent());
      if (parent != null) {
        treeModel.removeNodeFromParent(currentNode);
				forwardScheduling();
		nbTasks--;
		appli.refreshProjectInfos();
        return;
      }
    }
  }

  /** Clear the JTree. */
  public void clearTree() {
    //expand.clear();
    rootNode.removeAllChildren();
    initRootNode();
    treeModel.setRoot(rootNode);
    treeModel.reload();
    nbTasks=0;
  }


  /** Select the row of the tree */
  public void selectTreeRow(int row) {
    tree.setSelectionRow(row);
  }

	public void selectTask(Task task) {
		DefaultMutableTreeNode taskNode = null;
		for (Enumeration nodes = rootNode.preorderEnumeration(); nodes.hasMoreElements();) {
			DefaultMutableTreeNode nextNode = (DefaultMutableTreeNode) nodes.nextElement();
			if (nextNode.getUserObject().equals(task)) {
				taskNode = nextNode;
				break;
			}
		}
		if (taskNode!=null) {
			TreePath taskPath = new TreePath(taskNode.getPath());
			tree.getSelectionModel().setSelectionPath(taskPath);
		}			
	}

  /** Returne the mother task.*/
  public DefaultMutableTreeNode getFatherNode(Task node) {
    if (node == null) {
      return null;
    }
    DefaultMutableTreeNode tmp = (DefaultMutableTreeNode) getNode(node.getTaskID());
    if (tmp == null) {
      return null;
    }

    return (DefaultMutableTreeNode) tmp.getParent();
  }

  /** Returne the mother task.*/
  public DefaultMutableTreeNode getFatherNode(DefaultMutableTreeNode node) {
    if (node == null) {
      return null;
    }
    return (DefaultMutableTreeNode) node.getParent();
  }

  /** Return the JTree. */
  public JTree getJTree() {
    return tree;
  }

  /** Return the root node */
  public DefaultMutableTreeNode getRoot() {
    return rootNode;
  }

  //!@#
  /**
   * Check if task1 can be the successor of task2
   * @param task1 successor
   * @param task2 predecessor
   * @return true if task1 can be the successor of task2.
   */
  public boolean checkDepend(Task task1, GanttTask task2) {
    if(task1==null||task2==null){
      return false;
    }
    if (task1.getTaskID()==task2.getTaskID()) {
      return false;
    }
    if (getAllChildTask(task2/*.toString()*/).size() != 0) {
      return false; //question of CL
    }
    Vector successors = task2.getSuccessorsOld();

    for (int i = 0; i < successors.size(); i++) {
      int tempTaskID = ( (GanttTaskRelationship) successors.get(i)).
          getSuccessorTaskID();
      GanttTask tempTask = getTaskManager().getTask(tempTaskID);
      if (!checkDepend(task1, tempTask)) {
        return false;
      }
    }
    return true;
  }


  /** Function to put up the selected tasks */
  public void upCurrentNodes() {

    DefaultMutableTreeNode [] cdmtn = getSelectedNodes();
    if(cdmtn==null) {
    	appli.getStatusBar().setFirstText(language.getText("msg21"),2000);
    	return ;
  	}
    TreePath [] selectedPaths = new TreePath[cdmtn.length];
    for(int i=0; i<cdmtn.length; i++)
    {
    	DefaultMutableTreeNode father = this.getFatherNode(cdmtn[i]);
    	int index = father.getIndex( (TreeNode) cdmtn[i]);

    	if (index != 0) {

    		cdmtn[i].removeFromParent();
    		treeModel.nodesWereRemoved(father,
                               new int[] {index} ,
                               new Object[] {cdmtn});
    		//	New position
    		index--;

    		treeModel.insertNodeInto( (MutableTreeNode) cdmtn[i], (MutableTreeNode) father,
                             index);

    		//	Select tagain this node
    		TreeNode[] treepath = cdmtn[i].getPath();
    		TreePath path = new TreePath(treepath);
    		//tree.setSelectionPath(path);
    		selectedPaths[i]=path;

    		expandRefresh(cdmtn[i]);

    		forwardScheduling();
    		//refreshAllId(father);
    	}
    }
    tree.setSelectionPaths(selectedPaths);
    area.repaint();
  }
  
  
  /** Function to put down the selected tasks */
  public void downCurrentNodes() {

    DefaultMutableTreeNode [] cdmtn = getSelectedNodes();
    if(cdmtn==null) {
    	appli.getStatusBar().setFirstText(language.getText("msg21"),2000);
    	return;
    }
    
    TreePath [] selectedPaths = new TreePath[cdmtn.length];
    
    //Parse in reverse mode because tasks are sorted from top to bottom.
    for(int i=cdmtn.length-1; i>=0; i--)
    {
    	DefaultMutableTreeNode father = this.getFatherNode(cdmtn[i]);
    	int index = father.getIndex( (TreeNode) cdmtn[i]);
    	index++;
    	//New position
    	if ( (index < father.getChildCount())) {

    		cdmtn[i].removeFromParent();
    		treeModel.nodesWereRemoved(father,
                               new int[] {index - 1} ,
                               new Object[] {cdmtn});

    		treeModel.insertNodeInto( (MutableTreeNode) cdmtn[i], (MutableTreeNode) father,
                             index);

    		//Select tagain this node
    		TreeNode[] treepath = cdmtn[i].getPath();
    		TreePath path = new TreePath(treepath);
    		//tree.setSelectionPath(path);
    		selectedPaths[i]=path;
    		
    		expandRefresh(cdmtn[i]);

    		forwardScheduling();
    		//refreshAllId(father)
    	}
    }
    tree.setSelectionPaths(selectedPaths);
    area.repaint();
  }

  /** Function to indent selected task this will change
   *  the parent child relationship.
   *  This Code is based on the UP/DOWN Coder I found in here
   *  barmeier
   */  
  /** Indent several nodes that are selected. 
   *  Based on the IndentCurrentNode method. */
  public void indentCurrentNodes() {
  	
  	
		DefaultMutableTreeNode [] cdmtn = getSelectedNodes();
  	if(cdmtn==null) {
  		appli.getStatusBar().setFirstText(language.getText("msg21"),2000);
  		return;
  	}
  	//TreePath [] selectedPaths = new TreePath[cdmtn.length];
  	
  	for (int i=0; i<cdmtn.length; i++) {
  	    DefaultMutableTreeNode nextNode = cdmtn[i];
  	    DefaultMutableTreeNode nextSupertaskNode = cdmtn[i].getPreviousSibling();
  	    if (nextSupertaskNode==null) {
  	        continue;
  	    }
  	    Task nextTask = (Task) nextNode.getUserObject();
  	    Task nextSupertask = (Task) nextSupertaskNode.getUserObject();
  	    getTaskManager().getTaskHierarchy().move(nextTask, nextSupertask);
  	    TaskLength shift = getTaskManager().createLength(nextTask.getDuration().getTimeUnit(), nextTask.getStart().getTime(), nextSupertask.getStart().getTime()); 
        getTaskManager().getAlgorithmCollection().getShiftTaskTreeAlgorithm().run(nextTask, shift);  	    
  	}
  	/*
  	
  	
  	for(int i=0; i<cdmtn.length; i++)
  	{
  		DefaultMutableTreeNode father = this.getFatherNode(cdmtn[i]);
  		 // Where is my nearest sibling in ascending order ?
  	    DefaultMutableTreeNode newFather = cdmtn[i].getPreviousSibling();
  	    // If there is no more indentation possible we must stop
  	    if (newFather == null) {
  	      return;
  	    }
  	    
  	    ( (Task) newFather.getUserObject()).setMilestone(false);

  	    int oldIndex = father.getIndex( (TreeNode) cdmtn[i]);

  	    cdmtn[i].removeFromParent();
  	    treeModel.nodesWereRemoved(father,
                                 new int[] {oldIndex} ,
                                 new Object[] {cdmtn});

  	    treeModel.insertNodeInto( (MutableTreeNode) cdmtn[i],
                               (MutableTreeNode) newFather,
                               newFather.getChildCount());

  	    //Select tagain this node
  	    TreeNode[] treepath = cdmtn[i].getPath();
  	    TreePath path = new TreePath(treepath);
  	    //tree.setSelectionPath(path);
  	    selectedPaths[i]=path;

  	    //refresh the father date
  	    Task current = (Task)(cdmtn[i].getUserObject());
        Task fatherTask = (Task) newFather.getUserObject();
        current.shift(current.getManager().createLength(current.getDuration().getTimeUnit(), current.getStart().getTime(), fatherTask.getStart().getTime()));
  	    //refreshAllFather(current.toString());

  	    expandRefresh(cdmtn[i]);

  	    //forwardScheduling();
  	}

  	
  	
	//refresh the graphic area
    area.repaint();
    */
  	//tree.setSelectionPaths(selectedPaths);
  }
  
  

  /** Function to dedent selected task this will change
   *  the parent child relationship.
   *  This Code is based on the UP/DOWN Coder I found in here
   *  barmeier
   */
  /** Unindent the selected nodes. */
  public void dedentCurrentNodes() {

    DefaultMutableTreeNode [] cdmtn = getSelectedNodes();
    if(cdmtn==null) {
    	appli.getStatusBar().setFirstText(language.getText("msg21"),2000);
    	return;
    }
    
    TreePath [] selectedPaths = new TreePath[cdmtn.length];
    
    for(int i=0; i<cdmtn.length; i++)
    {
    	DefaultMutableTreeNode father = this.getFatherNode(cdmtn[i]);

    	// Getting the fathers father !? The grandpa I think :)
    	DefaultMutableTreeNode newFather = this.getFatherNode(father);
    	// If no grandpa is available we must stop.
    	if (newFather == null) {
    		return;
    	}

    	int oldIndex = father.getIndex( (TreeNode) cdmtn[i]);

    	cdmtn[i].removeFromParent();
    	treeModel.nodesWereRemoved(father,
                               new int[] {oldIndex} ,
                               new Object[] {cdmtn});

    	treeModel.insertNodeInto( (MutableTreeNode) cdmtn[i],
                             (MutableTreeNode) newFather,
                             newFather.getIndex( (TreeNode) father) + 1);

    	//Select tagain this node
    	TreeNode[] treepath = cdmtn[i].getPath();
    	TreePath path = new TreePath(treepath);
    	//tree.setSelectionPath(path);
    	selectedPaths[i]=path;
    	
    	//	refresh the father date
    	//Task current = (Task)(cdmtn[i].getUserObject());
    	//refreshAllFather(current.toString());

    	expandRefresh(cdmtn[i]);

    	forwardScheduling();
    }

    tree.setSelectionPaths(selectedPaths);
    
    area.repaint();

  }

  //update 21/03/2003
  /** Refresh the exapntion (recursive function) */
  public void expandRefresh(DefaultMutableTreeNode moved) {

      Task movedTask = (Task) moved.getUserObject();
      //if (expand.contains(new Integer(movedTask.getTaskID()))) {
      if(movedTask.getExpand())
          tree.expandPath(new TreePath(moved.getPath()));
      

      Enumeration children = moved.children();
      while (children.hasMoreElements()) {
          expandRefresh((DefaultMutableTreeNode) children.nextElement());
      }
  }


  /**
   * In elder version, this function refresh all the related tasks to the
       * taskToMove. In the new version, this function is same as forwardScheduling().
   * It will refresh all the tasks.
   * @param taskToMove
   */
  public void refreshAllChild(String taskToMove) {
    forwardScheduling();
  }

  //////////////////////////////////////////////////////////////////////////////////////////
  /**
   * Listener when scrollbar move
   */
  public class GanttAdjustmentListener
      implements AdjustmentListener {
    public void adjustmentValueChanged(AdjustmentEvent e) {
      if (area != null) {
        area.setScrollBar(e.getValue());
        area.repaint();
      }
    }
  }

  //////////////////////////////////////////////////////////////////////////////////////////
  /**
   * Class for expansion and collapse of node
   */
  public class GanttTreeExpansionListener
      implements TreeExpansionListener {
    /** Expansion */
    public void treeExpanded(TreeExpansionEvent e) {
      if (area != null) {
        area.repaint();
      }
      DefaultMutableTreeNode node = (DefaultMutableTreeNode)(e.getPath().getLastPathComponent());
      Task task = (Task)node.getUserObject();

      /*if(!expand.contains(new Integer(task.getTaskID()))) {
		 expand.add(new Integer(task.getTaskID()));
		 appli.setAskForSave(true);
      }*/ 
      
      task.setExpand(true);
      appli.setAskForSave(true);
      
    }

    /** Collapse */
    public void treeCollapsed(TreeExpansionEvent e) {
      if (area != null) {
        area.repaint();
      }

      DefaultMutableTreeNode node = (DefaultMutableTreeNode)(e.getPath().getLastPathComponent());
      Task task = (Task)node.getUserObject();

      /*int index = expand.indexOf(new Integer(task.getTaskID()));
      if (index >= 0) {
        expand.remove(index);
        appli.setAskForSave(true);
      } */
      
      task.setExpand(false);
      appli.setAskForSave(true);
    }
  }

  //////////////////////////////////////////////////////////////////////////////////////////

  /**
   * Listener to generate modification on the model
   */
  public class GanttTreeModelListener
      implements TreeModelListener {
    /** modify a node */
    public void treeNodesChanged(TreeModelEvent e) {
      if (area != null) {
        area.repaint();
      }
    }

    /** Insert a new node. */
    public void treeNodesInserted(TreeModelEvent e) {

    	DefaultMutableTreeNode node = (DefaultMutableTreeNode)(e.getTreePath().getLastPathComponent());
			Task task = (Task)node.getUserObject();

      /*if (!expand.contains(new Integer(task.getTaskID()))) {
      	expand.add(new Integer(task.getTaskID()));
      }*/
			
	  //task.setExpand(true);
			
      if (area != null) 
        area.repaint();      
    }

    /** Delete a node. */
    public void treeNodesRemoved(TreeModelEvent e) {
      if (area != null) {
        area.repaint();
      }
    }

    /** Structur change. */
    public void treeStructureChanged(TreeModelEvent e) {
      if (area != null) {
        area.repaint();
      }
    }
  }

    private class GanttTreeDropListener implements DropTargetListener {
        private TreePath        lastPath       = null;
        private Rectangle2D     cueLineRect      = new Rectangle2D.Float();
        private Rectangle2D     ghostImageRect        = new Rectangle2D.Float();
        private Color           cueLineColor;
        private Point           lastEventPoint         = new Point();
        private Timer           hoverTimer;

        public GanttTreeDropListener()
        {
            cueLineColor = new Color(
                                        SystemColor.controlShadow.getRed(),
                                        SystemColor.controlShadow.getGreen(),
                                        SystemColor.controlShadow.getBlue(),
                                        64
                                      );

            // Set up a hover timer, so that a node will be automatically expanded or collapsed
            // if the user lingers on it for more than a short time
            hoverTimer = new Timer(1000, new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    if (!tree.isExpanded(lastPath)) {
                        tree.expandPath(lastPath);
                    }
                }
            });
            // Set timer to one-shot mode - it will be restartet when the
            // cursor is over a new node
            hoverTimer.setRepeats(false);
        }

        public void dragEnter(DropTargetDragEvent dtde) {
						if (ghostImage==null) {
							//In case if you drag a file from out and it's not an acceptable, and it can crash if the image is null
							ghostImage = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB_PRE);
						}
            if (!isDragAcceptable(dtde))
                dtde.rejectDrag();
            else
                dtde.acceptDrag(dtde.getDropAction());
        }

        public void dragOver(DropTargetDragEvent dtde) {
            if (!isDragAcceptable(dtde))
                dtde.rejectDrag();
            else
                dtde.acceptDrag(dtde.getDropAction());

            // Even if the mouse is not moving, this method is still invoked
            // 10 times per second
            Point pt = dtde.getLocation();
            if (pt.equals(lastEventPoint))
                return;

            lastEventPoint = pt;


            Graphics2D g2 = (Graphics2D) tree.getGraphics();

            // If a drag image is not supported by the platform, then draw our own drag image
            if (!DragSource.isDragImageSupported())
            {
                // Rub out the last ghost image and cue line
                tree.paintImmediately(ghostImageRect.getBounds());
                // And remember where we are about to draw the new ghost image
                ghostImageRect.setRect(pt.x - offsetPoint.x, pt.y - offsetPoint.y, ghostImage.getWidth(), ghostImage.getHeight());
                g2.drawImage(ghostImage, AffineTransform.getTranslateInstance(ghostImageRect.getX(), ghostImageRect.getY()), null);
            }
            else {
                // Just rub out the last cue line
                tree.paintImmediately(cueLineRect.getBounds());
            }

            TreePath path = tree.getClosestPathForLocation(pt.x, pt.y);
            if (!(path == lastPath))
            {
                lastPath = path;
                hoverTimer.restart();
            }

            // In any case draw (over the ghost image if necessary) a cue line indicating where a drop will occur
            Rectangle raPath = tree.getPathBounds(path);
						if(raPath==null) raPath = new Rectangle (1,1);
            cueLineRect.setRect(0,  raPath.y+(int)raPath.getHeight(), getWidth(), 2);

            g2.setColor(cueLineColor);
            g2.fill(cueLineRect);

            // And include the cue line in the area to be rubbed out next time
            ghostImageRect = ghostImageRect.createUnion(cueLineRect);

        }

        public void dropActionChanged(DropTargetDragEvent dtde) {
            if (!isDragAcceptable(dtde))
                dtde.rejectDrag();
            else
                dtde.acceptDrag(dtde.getDropAction());
        }

        public void drop(DropTargetDropEvent dtde) {
            if (!isDropAcceptable(dtde))
            {
                dtde.rejectDrop();
                return;
            }

            // Prevent hover timer from doing an unwanted expandPath or collapsePath
            hoverTimer.stop();

            dtde.acceptDrop(dtde.getDropAction());

            Transferable transferable = dtde.getTransferable();

            DataFlavor[] flavors = transferable.getTransferDataFlavors();
            for (int i = 0; i < flavors.length; i++ )
            {
                DataFlavor flavor = flavors[i];
                if (flavor.isMimeTypeEqual(DataFlavor.javaJVMLocalObjectMimeType))
                {
                    try
                    {
                        Point pt = dtde.getLocation();
                        DefaultMutableTreeNode target = (DefaultMutableTreeNode) tree.getClosestPathForLocation(pt.x, pt.y).getLastPathComponent();
                        TreePath pathSource = (TreePath) transferable.getTransferData(flavor);
                        DefaultMutableTreeNode source = (DefaultMutableTreeNode) pathSource.getLastPathComponent();

                        TreePath pathNewChild = null;

                        TreeNode sourceFather = source.getParent();
                        int index = sourceFather.getIndex(source);
                        source.removeFromParent();

                        treeModel.nodesWereRemoved(sourceFather, new int[] {index}, new Object[] {source});

                        treeModel.insertNodeInto(
                            source,
                            target,
                            0);

                        pathNewChild = new TreePath(((DefaultMutableTreeNode) pathSource.getLastPathComponent()).getPath());

                        if (pathNewChild != null) {
                            tree.setSelectionPath(pathNewChild); // Mark this as the selected path in the tree
                        }

                        //refreshAllFather(source.getUserObject().toString());

                        expandRefresh(source);

                        forwardScheduling();

                        area.repaint();

                        appli.setAskForSave(true);

                        break; // No need to check remaining flavors
                    }
                    catch (UnsupportedFlavorException ufe)
                    {
                        System.out.println(ufe);
                        dtde.dropComplete(false);
                        return;
                    }
                    catch (IOException ioe)
                    {
                        System.out.println(ioe);
                        dtde.dropComplete(false);
                        return;
                    }
                }
            }
            dtde.dropComplete(true);
        }

        public void dragExit(DropTargetEvent dte) {
            if (!DragSource.isDragImageSupported())
            {
                repaint(ghostImageRect.getBounds());
            }
            tree.repaint();
        }

        public boolean isDragAcceptable(DropTargetDragEvent e)
        {
            // Only accept COPY or MOVE gestures (ie LINK is not supported)
            if ((e.getDropAction() & DnDConstants.ACTION_COPY_OR_MOVE) == 0) {
                return false;
            }

            // Only accept this particular flavor
            if (!e.isDataFlavorSupported(GanttTransferableTreePath.TREEPATH_FLAVOR)) {
                return false;
            }

            // Do not accept dropping on the source node
            Point pt = e.getLocation();
            TreePath path = tree.getClosestPathForLocation(pt.x, pt.y);
            if (dragPath.isDescendant(path)) {
                return false;
            }
            if (path.equals(dragPath)) {
                return false;
            }

						//Check if the task is a milestone task
						Task task = (Task)(((DefaultMutableTreeNode)path.getLastPathComponent()).getUserObject());
						if(task.isMilestone())
							return false;

            return true;
       }

        public boolean isDropAcceptable(DropTargetDropEvent e)
        {
            // Only accept COPY or MOVE gestures (ie LINK is not supported)
            if ((e.getDropAction() & DnDConstants.ACTION_COPY_OR_MOVE) == 0) {
                return false;
            }

            // Only accept this particular flavor
            if (!e.isDataFlavorSupported(GanttTransferableTreePath.TREEPATH_FLAVOR)) {
                return false;
            }

            // prohibit dropping onto the drag source
            Point pt = e.getLocation();
            TreePath path = tree.getClosestPathForLocation(pt.x, pt.y);
            if (path.equals(dragPath))  {
                return false;
            }
            return true;
         }

    }

    private static class GanttTransferableTreePath implements Transferable {
        // The type of DnD object being dragged...
        public static final DataFlavor TREEPATH_FLAVOR = new DataFlavor(DataFlavor.javaJVMLocalObjectMimeType, "TreePath");

        private TreePath        _path;

        private DataFlavor[]    _flavors =
                                {
                                    TREEPATH_FLAVOR
                                };

        /**
        * Constructs a transferrable tree path object for the specified path.
        */
        public GanttTransferableTreePath(TreePath path)
        {
            _path = path;
        }

        // Transferable interface methods...
        public DataFlavor[] getTransferDataFlavors()
        {
            return _flavors;
        }

        public boolean isDataFlavorSupported(DataFlavor flavor)
        {
            return java.util.Arrays.asList(_flavors).contains(flavor);
        }

        public synchronized Object getTransferData(DataFlavor flavor) throws UnsupportedFlavorException
        {
            if (flavor.isMimeTypeEqual(TREEPATH_FLAVOR.getMimeType())) // DataFlavor.javaJVMLocalObjectMimeType))
                return _path;
            else
                throw new UnsupportedFlavorException(flavor);
        }


    }

  /**
   * Render the cell of the tree
   */
  public class GanttTreeCellRenderer
      extends DefaultTreeCellRenderer //JLabel-CL
      implements TreeCellRenderer {

    public GanttTreeCellRenderer() {
      setOpaque(true);
    }

    public Component getTreeCellRendererComponent(JTree tree,
                                                  Object value,
                                                  boolean selected,
                                                  boolean expanded,
                                                  boolean leaf,
                                                  int row,
                                                  boolean hasFocus) {

      Task task = (Task)((DefaultMutableTreeNode)value).getUserObject();//getTask(value.toString());
      if (task==null) {
      	return this;
      }
      int type = 0;

      setFont(new Font("SansSerif", Font.PLAIN, 11));

      if (task.isMilestone()) {
        setIcon(new ImageIcon(getClass().getResource("/icons/meeting.gif")));
        type = 1;
      }
      else if (leaf) {
        if (task.getPriority() == GanttTask.LOW) {
          setIcon(new ImageIcon(getClass().getResource("/icons/task1.gif")));
        }
        else if (task.getPriority() == GanttTask.NORMAL) {
          setIcon(new ImageIcon(getClass().getResource("/icons/task.gif")));
        }
        else if (task.getPriority() == GanttTask.HIGHT) {
          setIcon(new ImageIcon(getClass().getResource("/icons/task2.gif")));
        }
        type = 2;
      }
      else {
        setIcon(new ImageIcon(getClass().getResource("/icons/mtask.gif")));
	setFont(new Font("SansSerif", Font.BOLD, 12));
      }


      setText(task.toString());
      setToolTipText(getToolTip(task, type));
      setBackground(selected ?
                    new Color( (float) 0.290, (float) 0.349, (float) 0.643) :
                    row % 2 == 0 ? Color.white :
                    new Color( (float) 0.933, (float) 0.933, (float) 0.933));
      setForeground(selected ? Color.white : Color.black);
      return this;
    }

      public String getToolTip(Task task, int type) {
          String res = "<html><body bgcolor=#EAEAEA>";
          res += "<b>" + task.toString() + "</b>" + "<br>" + task.getStart();
          if (type != 1) {
              res += "  -  " + task.getEnd();
          }
          if (type == 1) {
              res += "<br>" + language.getText("meetingPoint");
          }

          res += "<br><b>Pri</b> " +
                  (task.getPriority() == 0 ? language.getText("low") : task.getPriority() == 1 ?
                  language.getText("normal") : language.getText("hight"));

          ResourceAssignment[] assignments = task.getAssignments();
          if (assignments.length>0) {
              res += "<br><b>Assign to </b><br>";
              for (int j = 0; j < assignments.length; j++) {
                  res += "&nbsp;&nbsp;" + assignments[j].getResource().getName() + "<br>";
              }
          }

          if (task.getNotes() != null && !task.getNotes().equals("")) {
              String notes = task.getNotes();
              res += "<br><b>Notes </b>: ";
              int maxLength = 150;
              if (notes.length() > maxLength) {
                  notes = notes.substring(0, maxLength);
                  int i = maxLength - 1;
                  for (; i >= 0 && notes.charAt(i) != ' '; i--) ;
                  notes = notes.substring(0, i);
                  notes += " <b>( . . . )</b>";
              }
              notes = notes.replaceAll("\n", "<br>");
              res += "<font size=\"-2\">" + notes + "</font>";
          }

          res += "</body></html>";
          return res;
      }

  }

  //----------Newly Added Code--------------//CL
  /** Temporary treeNode for copy and paste */
  private DefaultMutableTreeNode cpNode;


  /** Cut the current selected tree node */
  public void cutSelectedNode() {
    TreePath currentSelection = tree.getSelectionPath();
    if (currentSelection != null) {
      cpNode = (DefaultMutableTreeNode)
          (currentSelection.getLastPathComponent());

      //delete the current node
      DefaultMutableTreeNode father = getFatherNode(getSelectedNode()/*ttask*/);

      removeCurrentNode();

      GanttTask taskFather = (GanttTask) father.getUserObject();

        AdjustTaskBoundsAlgorithm alg = getTaskManager().getAlgorithmCollection().getAdjustTaskBoundsAlgorithm();
        alg.run(taskFather);
      //taskFather.refreshDateAndAdvancement(this);
      father.setUserObject(taskFather);
      area.repaint();

    }
  }

  /** Copy the current selected tree node */
  public void copySelectedNode() {
    TreePath currentSelection = tree.getSelectionPath();
    if (currentSelection != null) {
      cpNode = (DefaultMutableTreeNode)
          (currentSelection.getLastPathComponent());

    }
  }

  /** Paste the node and its child node to current selected position*/
  public void pasteNode() {
    if (cpNode != null) {

      DefaultMutableTreeNode current = (DefaultMutableTreeNode) tree.
          getLastSelectedPathComponent();

      if (current == null) {
        current = rootNode;

      }
      insertClonedNode(current, cpNode, 0, true);
    }
  }

  /** Insert the cloned node and its children*/
  private void insertClonedNode(DefaultMutableTreeNode parent,
                                DefaultMutableTreeNode child,
                                int location, boolean first) {
    if (parent == null) {
      return; //it is the root node
    }

		if(first) {
			GanttTask _t = (GanttTask)(parent.getUserObject());
			if(_t.isMilestone()) {
				_t.setMilestone(false);
				GanttTask _c = (GanttTask)(child.getUserObject());
				_t.setLength(_c.getLength());
				_t.setStart(_c.getStart());
			}
		}

    GanttTask originalTask = (GanttTask) child.getUserObject();
    GanttTask newTask = originalTask.Clone();

    newTask.setName( (first?language.getText("copy2")+"_":"") + newTask.toString());

    TaskManagerImpl tmi= (TaskManagerImpl)getTaskManager();
    newTask.setTaskID(tmi.getMaxID()+1);
    getTaskManager().registerTask(newTask);

    DefaultMutableTreeNode cloneChildNode = new DefaultMutableTreeNode(newTask);

    for (int i = 0; i < child.getChildCount(); i++) {
      insertClonedNode(cloneChildNode,
                       (DefaultMutableTreeNode) child.getChildAt(i), i, false);
    }
    treeModel.insertNodeInto(cloneChildNode, parent, location);

    tree.scrollPathToVisible(new TreePath(cloneChildNode.getPath()));

    //Remove the node from the expand list
    /*int index = expand.indexOf(new Integer(newTask.getTaskID())cloneChildNode.toString());
    if (index >= 0) 
      expand.remove(index);
    */
    newTask.setExpand(false);

  }

  //Add by Cui Lu
  /** Return a GanttTask when editing the tree node instead of a String*/
  class GanttTreeCellEditor
      extends javax.swing.DefaultCellEditor {
    private JTree tree;
    private JTextField textField;
      private final FocusListener myFocusListener = new FocusAdapter() {
          public void focusGained(FocusEvent e) {
              textField.select(0, textField.getText().length());
          }
      };

    public GanttTreeCellEditor(JTree tree, JTextField textField) {
      super(textField);
      this.tree = tree;
      this.textField = textField;
        textField.addFocusListener(myFocusListener);
    }

    //overwrite to return a GanttTask object when editing tree node
    public Object getCellEditorValue() {
			DefaultMutableTreeNode tmpMutableTreeNode = (DefaultMutableTreeNode) tree.getLastSelectedPathComponent();
			if(tmpMutableTreeNode==null) return null;
      Object userObject = tmpMutableTreeNode.getUserObject();

      appli.setAskForSave(true);

      if (userObject instanceof Task) {
        Task ganttTask = (Task) userObject;
		/*if (expand.contains(new Integer(ganttTask.getTaskID()))) {
			expand.remove(expand.indexOf(new Integer(ganttTask.getTaskID())));
			expand.add(new Integer(ganttTask.getTaskID()));
		}*/ //?????

        ganttTask.setName(textField.getText());

		return ganttTask;
      }
      else return null;
     
    }

  }

    public void forwardScheduling() {
        RecalculateTaskScheduleAlgorithm alg = getTaskManager().getAlgorithmCollection().getRecalculateTaskScheduleAlgorithm();
        try {
            alg.run();
        } catch (TaskDependencyException e) {
            e.printStackTrace();  //To change body of catch statement use Options | File Templates.
        }
    }
  //static int count=0; //for Debug CL
  ///////////////////////////////////////////////////////////////////////
  /*forward calculate the earliest start and finish of all the task*/
  //-By CL 15-May-2003
    /*
  private void _forwardScheduling() {
      //new Exception().printStackTrace();
    //System.out.println("forword scheduling: "+count++); //for Debug CL
    setAllTasksUnchecked(); //for the purpose to ckeck all the relationships
    /////////////////////////////////
    //setAllDependencies();
////Code should be deleted after the depend has been replaced by successors
    ////////////////////////////////
    ArrayList taskNodes = getAllTasks();
    for (int i = 0; i < taskNodes.size(); i++) {
      DefaultMutableTreeNode node = (DefaultMutableTreeNode) taskNodes.get(i);
      if (node.getChildCount() == 0) { //it is not a mother task
        GanttTask task = (GanttTask) node.getUserObject();
        if (!task.isChecked()) {
          findEarliestStart(task);
        }
      }
    }
    //Treat the mother task. (the children have been scheduled.)
    //start date of mother task should be the earliest start date of its children
    //finish date of mother task is the last finish date of its children
    for (int i = 0; i < taskNodes.size(); i++) {
      DefaultMutableTreeNode node = (DefaultMutableTreeNode) taskNodes.get(i);
      if (node.getChildCount() != 0) { //it is a mother task
        if (node.isRoot()) {
          continue;
        }
        Task task = (Task) node.getUserObject();
        GanttCalendar earliestStartDate = new GanttCalendar(2949, 10, 1);
        GanttCalendar earliestFinishDate = new GanttCalendar(1049, 10, 1);
        //find the earliest date of children's start dates
        //find the last finish date of children's finish dates
        Enumeration childNodes = node.children();
        while (childNodes.hasMoreElements()) {
          Task childTask = (Task) ( (DefaultMutableTreeNode)
                                             childNodes.nextElement()).
              getUserObject();
          if (earliestStartDate.compareTo(childTask.getStart()) > 0) {
            earliestStartDate = childTask.getStart().Clone();
          }
          if (earliestFinishDate.compareTo(childTask.getEnd()) < 0) {
            earliestFinishDate = childTask.getEnd().Clone();
          }
        }
        task.setStart(earliestStartDate);
        task.setEnd(earliestFinishDate);
      }
    }
  }
      */
  //static int countFindEarliestStart=0;//for Debug CL
    /*
  private void findEarliestStart(GanttTask task) {
    //System.out.println("I m in findEarliestStart for "+countFindEarliestStart++);//for Debug CL

    GanttCalendar earliestStart = new GanttCalendar(1099, 10, 1); //set the earliest start date to be some date impossible. at least where I don't care:)
    if (!task.isChecked()) {
      Vector predecessors = task.getPredecessorsOld();
      //for the task without predecessor, the start date is the earliest start date
      if (predecessors.size() == 0) {
        task.setChecked(true);
      }
      //If there are predecessors, the earliest date should be depended
      //on the relationship type and start or end date of each predecessor.
      for (int i = 0; i < predecessors.size(); i++) {
        GanttTask predecessorTask = ( (GanttTaskRelationship) predecessors.get(
            i)).getPredecessorTask();
        int relationshipType = ( (GanttTaskRelationship) predecessors.get(
            i)).getRelationshipType();
        if (relationshipType == GanttTaskRelationship.FS) {
          ////////////////////////////////////
          //FS realtionship: the earliest start date should be the
          //latest earliest finish date of all the predecessors
          ////////////////////////////////////
          if (!predecessorTask.isChecked()) { //If ther predecessor has not been checked, check it here. It is a recursive algorithm
	   				 findEarliestStart(predecessorTask);
          }
          if (predecessorTask.isChecked()) { //if checked, the start and end date are valid
            GanttCalendar temp = predecessorTask.getEnd().Clone();
            //temp.add(1); //should be one day behind the predecessor finish date.
            if (temp.compareTo(earliestStart) > 0) { //if the current earliest start is earlier than the end date of one of its prodecessor, it set equal to the end date of this predecessor
              earliestStart = temp;
            }
          }
        }
        else if (relationshipType == GanttTaskRelationship.FF) {
          ////////////////////////////////////
          //FF realtionship: As soon as the predecessor task finishes,
          //the successor task can finish
          ////////////////////////////////////
          if (!predecessorTask.isChecked()) {
            findEarliestStart(predecessorTask); //check the predecessor
          }
          if (predecessorTask.isChecked()) {
            GanttCalendar temp = predecessorTask.getEnd().Clone();
            GanttCalendar earliestFinish = earliestStart;
            earliestFinish.add(task.getLength());
            if (earliestFinish.compareTo(temp) < 0) { //if the earliest finish is earlier than the end date of its predecessor, it set equal to the end date of predecessor
              earliestFinish = temp.Clone();
              earliestStart = earliestFinish.Clone();
              earliestStart.add( -task.getLength());
            }
            else { //do nothing, if it is behind end date of predecessor

            }
          }
        }
        else if (relationshipType == GanttTaskRelationship.SF) {
          ////////////////////////////////////
          //SF realtionship: As soon as the predecessor task starts,
          //the successor task can finish.
          ////////////////////////////////////
          if (!predecessorTask.isChecked()) {
            findEarliestStart(predecessorTask); //if the predecessor has not been checked, check it here. it is a recursive algorithm
          }
          if (predecessorTask.isChecked()) {
            GanttCalendar temp = predecessorTask.getStart().Clone();
            GanttCalendar earliestFinish = earliestStart;
            earliestFinish.add(task.getLength());

            if (earliestFinish.compareTo(temp) < 0) { //if the earliest finish of the task is earlier than the start date of one of its predecessors, it set equal to the start date of the predecessor
              earliestFinish = temp.Clone();
              earliestStart = earliestFinish.Clone();
              earliestStart.add( -task.getLength());
            }
            else { //already satisfied the SF relationship, do nothing

            }
          }
        }
        else if (relationshipType == GanttTaskRelationship.SS) {
          ////////////////////////////////////
          //SS realtionship: As soon as the predecessor task starts,
          //the successor task can start.
          ////////////////////////////////////
          if (!predecessorTask.isChecked()) {
            findEarliestStart(predecessorTask); //if the predecessor has not been checked, check it here. it is a recursive algorithm
          }
          if (predecessorTask.isChecked()) {
            GanttCalendar temp = predecessorTask.getStart().Clone();

            if (earliestStart.compareTo(temp) < 0) { // if the start date of the task is earlier than the start date of its predecessor, it set equal to the start date of predecessor
              earliestStart = temp.Clone();
            }
            else { //already satisfied the SS relationship, do nothing.

            }
          }
        }
      }
      if (earliestStart.compareTo(task.getStart()) < 0) { //if the actual start is behind earliest start, don't need to do anything

      }
      else {
        task.setStart(earliestStart);
        GanttCalendar temp = earliestStart.Clone();
        temp.add(task.getLength());
        task.setEnd(temp);
      }
      task.setChecked(true);
    }
    return;
  }
      */
  /** instead of returning a list of DefautMutableTreeNode it return
   * a list of GanttTask */
  public ArrayList getAllGanttTasks() {
    ArrayList res = new ArrayList();
    Enumeration e = (rootNode).preorderEnumeration();
    while (e.hasMoreElements()) {
      DefaultMutableTreeNode node = (DefaultMutableTreeNode) e.nextElement();
      res.add(node.getUserObject());
    }
    return res;
  }

      /**set all the earliestStart and earliestFinish to be null before scheduling */
  private void setAllTasksUnchecked() {
    ArrayList tasks = getAllGanttTasks();
    for (Iterator it = tasks.iterator(); it.hasNext();)
    {
	GanttTask task = (GanttTask)it.next();
	task.setChecked(false);
    }


    //for (int i = 0; i < tasks.size(); i++) {
      //( (GanttTask) tasks.get(i)).setChecked(false);
      //( (GanttTask) tasks.get(i)).getPredecessorsOld().clear();
      //( (GanttTask) tasks.get(i)).getSuccessorsOld().clear();
    //}
  }

  /**This method set the predecessors and successors in all the task
   * It is a intermedia method for the migration to newer version
   * from the old version (1.9.6). The only relationsihp is FS.
   * After the depend has been replaced by successor, this method
   * does not need any longer
   */
  /*
  private void setAllDependencies() {
    ArrayList tasks = getAllGanttTasks();
    for (int i = 0; i < tasks.size(); i++) {
      GanttTask task = (GanttTask) tasks.get(i);
      ArrayList successors = task.getDepend();
      for (int j = 0; j < successors.size(); j++) {

        //following code add all depends as successor to the task
        GanttTaskRelationship successorRel = new GanttTaskRelationship();
        successorRel.setSuccessorTask(getTask( (String) successors.get(j))); //should be changed in the future
        successorRel.setRelationshipType(GanttTaskRelationship.FS);
        task.addSuccessor(successorRel);

        //following code add the task as predecessor to each of the depends
        GanttTaskRelationship precessorRel = new GanttTaskRelationship();
        precessorRel.setPredecessorTask(task);
        precessorRel.setRelationshipType(GanttTaskRelationship.FS);
        (getTask( (String) successors.get(j))).addPredecessor(precessorRel);
      }
    }
  }*/

  ///////////////////////////////////////////////////////////////////
  //--End CL 15-May-2003

    private TaskManager getTaskManager() {
    	return myTaskManager;
    }

    public void dragEnter(DragSourceDragEvent dsde) {
    }

    public void dragOver(DragSourceDragEvent dsde) {
    }

    public void dropActionChanged(DragSourceDragEvent dsde) {
    }

    public void dragDropEnd(DragSourceDropEvent dsde) {
    }

    public void dragExit(DragSourceEvent dse) {
    }

    public void dragGestureRecognized(DragGestureEvent dge) {

        Point ptDragOrigin = dge.getDragOrigin();
        TreePath path = tree.getPathForLocation(ptDragOrigin.x, ptDragOrigin.y);
        if (path == null) {
						return;
        }

        // Work out the offset of the drag point from the TreePath bounding rectangle origin
        Rectangle raPath = tree.getPathBounds(path);
        offsetPoint.setLocation(ptDragOrigin.x-raPath.x, ptDragOrigin.y-raPath.y);

        // Get the cell renderer (which is a JLabel) for the path being dragged
        JLabel lbl = (JLabel) tree.getCellRenderer().getTreeCellRendererComponent
                                (
                                    tree,                                           // tree
                                    path.getLastPathComponent(),                    // value
                                    false,                                          // isSelected   (dont want a colored background)
                                    tree.isExpanded(path),                               // isExpanded
                                    tree.getModel().isLeaf(path.getLastPathComponent()), // isLeaf
                                    0,                                              // row          (not important for rendering)
                                    false                                           // hasFocus     (dont want a focus rectangle)
                                );
        lbl.setSize((int)raPath.getWidth(), (int)raPath.getHeight()); // <-- The layout manager would normally do this

        // Get a buffered image of the selection for dragging a ghost image
        ghostImage = new BufferedImage((int)raPath.getWidth(), (int)raPath.getHeight(), BufferedImage.TYPE_INT_ARGB_PRE);
        Graphics2D g2 = ghostImage.createGraphics();

        // Ask the cell renderer to paint itself into the BufferedImage
        g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC, 0.5f));      // Make the image ghostlike
        lbl.paint(g2);

        // Now paint a gradient UNDER the ghosted JLabel text (but not under the icon if any)
        // Note: this will need tweaking if your icon is not positioned to the left of the text
        Icon icon = lbl.getIcon();
        int nStartOfText = (icon == null) ? 0 : icon.getIconWidth()+lbl.getIconTextGap();
        g2.setComposite(AlphaComposite.getInstance(AlphaComposite.DST_OVER, 0.5f)); // Make the gradient ghostlike
        g2.setPaint(new GradientPaint(nStartOfText, 0, SystemColor.controlShadow,
                                      getWidth(),   0, new Color(255,255,255,0)));
        g2.fillRect(nStartOfText, 0, getWidth(), ghostImage.getHeight());

        g2.dispose();



        tree.setSelectionPath(path); // Select this path in the tree

        // Wrap the path being transferred into a Transferable object
        Transferable transferable = new GanttTransferableTreePath(path);

        // Remember the path being dragged (because if it is being moved, we will have to delete it later)
        dragPath = path;

        // We pass our drag image just in case it IS supported by the platform
        dge.startDrag(null, ghostImage, new Point(5,5), transferable, this);
    }

    public DefaultTreeModel getModel() {
        return treeModel;
    }
}
