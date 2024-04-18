/***************************************************************************
 * HumanResourcePanel.java  -  description
 * -------------------
 * begin                : jun 2003
 * copyright            : to the world :)
 * email                : alexthomas(at)ganttproject.org
 ***************************************************************************/
/*******************************************************************************
 * * This program is free software; you can redistribute it and/or modify * it
 * under the terms of the GNU General Public License as published by * the Free
 * Software Foundation; either version 2 of the License, or * (at your option)
 * any later version. * *
 ******************************************************************************/
package net.sourceforge.ganttproject;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.ComponentOrientation;
import java.awt.Dimension;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.AdjustmentEvent;
import java.awt.event.AdjustmentListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import javax.swing.AbstractAction;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.ListSelectionModel;
import javax.swing.table.AbstractTableModel;

import net.sourceforge.ganttproject.action.ResourceActionSet;
import net.sourceforge.ganttproject.gui.GanttDialogInfo;
import net.sourceforge.ganttproject.gui.GanttDialogPerson;
import net.sourceforge.ganttproject.language.GanttLanguage;
import net.sourceforge.ganttproject.resource.HumanResource;
import net.sourceforge.ganttproject.resource.HumanResourceManager;
import net.sourceforge.ganttproject.resource.ProjectResource;
import net.sourceforge.ganttproject.resource.ResourceContext;
import net.sourceforge.ganttproject.resource.ResourceEvent;
import net.sourceforge.ganttproject.resource.ResourceView;
import net.sourceforge.ganttproject.util.BrowserControl;
/**
 * Class to edit the differents person that work on the project
 */
public class GanttResourcePanel extends JPanel
		implements
			ResourceView,
			ResourceContext {
	/** Number of personne on the table */
	int nbobj = 0;
	/** The JTable where will be stored the data */
	JTable table;
	/** The Tasktree ... needed till we have a real task manager */
	GanttTree tree;
	/** The model of data */
	GanttTableModel model;
	/** The language uses */
	GanttLanguage lang;
	/** The main application */
	GanttProject appli;
	int cx = 0, cy = 0;
	/** The vertical scrollbar on the JTree */
	JScrollBar vbar;
	private ResourceActionSet myResourceActionSet;
	public ResourceLoadGraphicArea area;
	JScrollPane scrollpane;
	JPanel left;
	JPanel myImagePanel;
	
public GanttResourcePanel(GanttProject prj, GanttTree tree) {
	super();
        this.appli = prj;
        this.lang = GanttLanguage.getInstance();
        
        model = new GanttTableModel(lang);
        table = new JTable(model);
        
        table.addKeyListener(prj); //callback for keyboard pressed 
        
        this.tree = tree;
        setLayout(new BorderLayout());
        
        
        GanttImagePanel but = new GanttImagePanel ("big.png","resources.png",300,42);
        myImagePanel = but;
        left = new JPanel(new BorderLayout());
        table.setRowHeight(20);
        left.add(but, "North");
				scrollpane = new JScrollPane(table);
				vbar = scrollpane.getVerticalScrollBar();
        vbar.addAdjustmentListener(new GanttAdjustmentListener());
	
				left.add(scrollpane,"Center");
        left.setPreferredSize(new Dimension(250, 600));

        
        //A splitpane is use
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        
                
        area = new ResourceLoadGraphicArea (prj, tree, table, prj.getZoomManager()) {
        	protected int getHeaderHeight() {
        		return myImagePanel.getHeight()+table.getTableHeader().getHeight();
        	}
        };
        prj.getZoomManager().addZoomListener(area.getZoomListener());
        area.getChartModel().setRowHeight(table.getRowHeight());
        if (lang.getComponentOrientation() == ComponentOrientation.LEFT_TO_RIGHT) {
        	splitPane.setLeftComponent(left);
        	splitPane.setRightComponent(area);
        } else {
        	splitPane.setRightComponent(left);
        	splitPane.setLeftComponent(area);
        	splitPane.setDividerLocation((int)(Toolkit.getDefaultToolkit()
					.getScreenSize().getWidth()
					- left.getPreferredSize().getWidth()));
			
			
        }
        splitPane.setOneTouchExpandable(true);
        splitPane.setPreferredSize(new Dimension(800, 500));

        
        add(splitPane,BorderLayout.CENTER);
        scrollpane.getViewport().setBackground(new Color(1.0f, 1.0f, 1.0f));
				left.setBackground(new Color(1.0f, 1.0f, 1.0f));
				table.setBackground(new Color(1.0f, 1.0f, 1.0f));
				table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        
        //Add listener for mouse click
        MouseListener ml = new MouseAdapter() {
            public void mousePressed(MouseEvent e) {
                Point p = new Point(e.getX(), e.getY());
                int selRow = table.rowAtPoint(p);
                int selCol = table.columnAtPoint(p);
                cx = selCol;
                cy = selRow;
                
                if(e.getClickCount() == 1 && e.getButton() == MouseEvent.BUTTON3 ) {
                    createPopupMenu(e.getX(), e.getY()) ;
                } else if(e.getClickCount() == 2 && e.getButton() == MouseEvent.BUTTON1 ) {
					propertiesHuman(appli);
				}
            }
        };
        if(!prj.isOnlyViewer)
        {
        	table.addMouseListener(ml);
        	scrollpane.addMouseListener(ml);
        }
        
        this.setBackground(new Color(0.0f, 0.0f, 0.0f));
        applyComponentOrientation(lang.getComponentOrientation());
    }	
	
	/* Create the popup menu */	
	public void createPopupMenu(int x, int y) {
		JPopupMenu menu = new JPopupMenu();
		AbstractAction[] resourceActions = myResourceActionSet.getActions();
		for (int i = 0; i < resourceActions.length; i++) {
			menu.add(new JMenuItem(resourceActions[i]));
		}
		menu.add(appli.createNewItem(GanttProject.correctLabel(lang
				.getText("propertiesHuman")), "/icons/properties_16.gif"));
		menu.add(appli.createNewItem(GanttProject.correctLabel(lang
				.getText("sendMail")), "/icons/send_mail_16.gif"));
		menu.addSeparator();
		menu.add(appli.createNewItem(GanttProject.correctLabel(lang
				.getText("upTask")), "/icons/up_16.gif"));
		menu.add(appli.createNewItem(GanttProject.correctLabel(lang
				.getText("downTask")), "/icons/down_16.gif"));
		menu.applyComponentOrientation(lang.getComponentOrientation());
		menu.show(this, x, y - (cy!=-1?vbar.getValue():table.getRowHeight()) + 60);
	}
	/** Function called when the language is changed */
	public void refresh(GanttLanguage language) {
		lang = language;
		model.changeLanguage(lang);
	}
	/** Return the String of the human number id */
	public String getNameByNumber(int id) {
		HumanResource people = (HumanResource) model.data.get(id);
		return people.getName();
	}
	/** Return the String of the human number id */
	public HumanResource getUserByNumber(int id) {
		return (HumanResource) model.data.get(id);
	}
	/** Create a new Human */
	public void newHuman(HumanResource people) {
		if (people != null)
			model.addRow(people);
	}
//	public void addHumans(ArrayList humans) {
//		for (int i = 0; i < humans.size(); i++) {
//			newHuman((HumanResource) humans.get(i));
//		}
//	}
	/** Delete the selected human */
	public void deleteHuman(GanttProject parent) {
		HumanResource people = null;
		if (cy >= 0 && cy < model.data.size())
			people = (HumanResource) model.data.get(cy);
		if (people != null) {
			GanttDialogInfo gdi = new GanttDialogInfo(parent,
					GanttDialogInfo.WARNING, GanttDialogInfo.YES_NO_OPTION,
					lang.getText("msg6") + people.toString() + "??", lang
							.getText("warning"));
			gdi.show();
			if (gdi.res == GanttDialogInfo.YES) {
				model.deleteRow(cy);
				parent.setAskForSave(true);
			}
		}
	}
	/** Edit the setting for this human */
	public void propertiesHuman(GanttProject parent) {
		HumanResource people = null;
		if (cy >= 0 && cy < model.data.size())
			people = (HumanResource) model.data.get(cy);
		if (people != null) {
			appli.getStatusBar().setFirstText(GanttLanguage.getInstance().
						getText("editingParameters"),2000);
			GanttDialogPerson dp = new GanttDialogPerson(parent, lang, people);
			dp.show();
			if (dp.result()) {
				model.updateRow(cy, people);
				parent.setAskForSave(true);
			}
		}
	}
	
	/** Send an Email to the current resource */
	public void sendMail(GanttProject parent) {
		HumanResource people = null;
		if (cy >= 0 && cy < model.data.size())
			people = (HumanResource) model.data.get(cy);
		if (people != null) {
			try {
				BrowserControl.displayURL("mailto:"+people.getMail());
			} catch (Exception e) {
				System.err.println(e);
			}
		}
	}
	
	/** Move up the selected resource */
	public void upResource() {
		HumanResource people = null;
		if (cy >= 0 && cy < model.data.size())
			people = (HumanResource) model.data.get(cy);
		if (people != null) {
			if (model.moveUp(cy)) {
				HumanResourceManager resMan = (HumanResourceManager) appli
						.getHumanResourceManager();
				resMan.up(cy);
				cy--;
				table.changeSelection(cy, 0, false, false);
			}
		} else
			System.out.println("No selected line");
	}
	/** Move down the selected resource */
	public void downResource() {
		HumanResource people = null;
		if (cy >= 0 && cy < model.data.size())
			people = (HumanResource) model.data.get(cy);
		if (people != null) {
			if (model.moveDown(cy)) {
				HumanResourceManager resMan = (HumanResourceManager) appli
						.getHumanResourceManager();
				resMan.down(cy);
				cy++;
				table.changeSelection(cy, 0, false, false);
			}
		} else
			System.out.println("No selected line");
	}
	/** Return the arrylist of the person */
	public ArrayList getPeople() {
		return model.data;
	}
	/** Return the number of people on the list */
	public int nbPeople() {
		return model.data.size();
	}
	/** Set the change to the model */
	public void setPeople(ArrayList list) {
		model.changePeople(list);
	}
	/** Reset all human... */
	public void reset() {
		model.reset();
	}
	public void setResourceActions(ResourceActionSet actionSet) {
		myResourceActionSet = actionSet;
	}
	/**
	 * Class model of table to store person data
	 */
	public class GanttTableModel extends AbstractTableModel {
		/** The data */
		public ArrayList data;
		/** The colums title */
		public ArrayList colums;
		GanttTableModel(GanttLanguage language) {
			data = new ArrayList();
			colums = new ArrayList();
			//Add the colums name
			changeLanguage(language);
		}
		/** Number of row on the table */
		public int getRowCount() {
			return data.size();
		}
		/** Number of colums on the table */
		public int getColumnCount() {
			return colums.size();
		}
		/** Return the value at the specificed case */
		public Object getValueAt(int row, int col) {
			if (row < 0 || col < 0 || row >= data.size()
					|| col >= colums.size())
				return null;
			HumanResource people = (HumanResource) data.get(row);
			if (col == 0) //Name
				return people.getName();
			if (col == 2) //mail
				return people.getMail();
			if (col == 3) //Phone
				return people.getPhone();
			return people.getRole().getName();
		}
		/** Return the name of the specified colums */
		public String getColumnName(int col) {
			return (String) colums.get(col);
		}
		/** Change the name of colums in function of the language */
		public void changeLanguage(GanttLanguage language) {
			colums.clear();
			String[] cols = new String[]{language.getText("colName"),
					language.getText("colRole"), language.getText("colMail"),
					language.getText("colPhone")};
			for (int i = 0; i < cols.length; i++)
				colums.add(new String(cols[i]));
			fireTableRowsUpdated(0, data.size() - 1);
			fireTableStructureChanged();
		}
		/** Add a new human */
		public void addRow(HumanResource people) {
			data.add(people);
			fireTableRowsInserted(data.size() - 1, data.size() - 1);
		}
		/** Update the specified row */
		public void updateRow(int row, HumanResource people) {
			data.set(row, people);
			fireTableRowsUpdated(row, row);
		}
		/** Delete the row specidied */
		public void deleteRow(int row) {
			data.remove(row);
			fireTableRowsDeleted(row, row);
		}
		/** Move Up the selected resource */
		public boolean moveUp(int row) {
			if (row > 0) {
				Object obj = data.remove(row);
				data.add(row - 1, obj);
				fireTableDataChanged();
				return true;
			}
			return false;
		}
		/** Move Down the selected resource */
		public boolean moveDown(int row) {
			if (row < data.size() - 1) {
				Object obj = data.remove(row);
				data.add(row + 1, obj);
				fireTableDataChanged();
				return true;
			}
			return false;
		}
		public void deleteRows(ProjectResource[] deleted) {
			Set deletedSet = new HashSet(Arrays.asList(deleted));
			int row = 0;
			for (Iterator i = data.iterator(); i.hasNext();) {
				Object nextData = i.next();
				if (deletedSet.contains(nextData)) {
					i.remove();
					fireTableRowsDeleted(row, row);
				} else {
					row++;
				}
			}
		}
		public void changePeople(ArrayList list) {
			//data.clear();
			data = list;
			//fireTableRowsUpdated(0,list.size()-1);
			fireTableDataChanged();
		}
		/** Are the cell editable */
		public boolean isCellEditable(int rowIndex, int columnIndex) {
			//if(columnIndex==0 || columnIndex==2) return true;
			return false;
		}
		/** Reset all human... */
		public void reset() {
			int size = data.size();
			data.clear();
			if (size > 0)
				fireTableRowsDeleted(0, size - 1);
		}
	}
	public void setTree(GanttTree tree) {
		this.tree = tree;
	}
	/**
	 * see net.sourceforge.ganttproject.resource.ResourceView#resourceAdded(net.sourceforge.ganttproject.resource.ProjectResource)
	 */
	public void resourceAdded(ResourceEvent event) {
		newHuman((HumanResource) event.getResource());
	}
	public void resourcesRemoved(ResourceEvent event) {
		model.deleteRows(event.getResources());
	}
	////////////////////////////////////////////////////////////////////////////
	// ResourceContext interface
	public ProjectResource[] getResources() {
		ProjectResource[] result = (cy >= 0 && cy < model.data.size())
				? new HumanResource[]{(HumanResource) model.data.get(cy)}
				: EMPTY_CONTEXT;
		return result;
	}
	private ProjectResource[] EMPTY_CONTEXT = new ProjectResource[0];
	public ResourceContext getContext() {
		return myContext;
	}
	private final ResourceContext myContext = (ResourceContext) this;
	//////////////////////////////////////////////////////////////////////////////////////////
	/**
	 * Listener when scrollbar move
	 */
	public class GanttAdjustmentListener implements AdjustmentListener {
		public void adjustmentValueChanged(AdjustmentEvent e) {
			if (area != null) {
				area.setScrollBar(e.getValue());
				area.repaint();
			}
		}
	}
}