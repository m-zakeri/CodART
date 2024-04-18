package org.gudy.azureus2.ui.swt.views.table.impl;

import java.util.ArrayList;
import java.util.Iterator;

import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.*;
import org.eclipse.swt.events.*;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.*;
import org.eclipse.swt.widgets.*;

import org.gudy.azureus2.core3.config.impl.ConfigurationManager;
import org.gudy.azureus2.core3.util.IndentWriter;
import org.gudy.azureus2.pluginsimpl.local.PluginCoreUtils;
import org.gudy.azureus2.ui.swt.Messages;
import org.gudy.azureus2.ui.swt.plugins.UISWTInstance;
import org.gudy.azureus2.ui.swt.plugins.UISWTViewEvent;
import org.gudy.azureus2.ui.swt.plugins.UISWTInstance.UISWTViewEventListenerWrapper;
import org.gudy.azureus2.ui.swt.pluginsimpl.*;
import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;

import com.aelitis.azureus.ui.swt.UIFunctionsManagerSWT;
import com.aelitis.azureus.ui.swt.UIFunctionsSWT;

public class TableViewSWT_TabsCommon
{
	TableViewSWT<?> tv;
	
	/** TabViews */
	private ArrayList<UISWTViewCore> tabViews = new ArrayList<UISWTViewCore>(1);

	/** TabViews */
	private CTabFolder tabFolder;

	/** Composite that stores the table (sometimes the same as mainComposite) */
	public Composite tableComposite;


	public TableViewSWT_TabsCommon(TableViewSWT<?> tv) {
		this.tv = tv;
	}

	public void triggerTabViewsDataSourceChanged(boolean sendParent) {
		if (tabViews == null || tabViews.size() == 0) {
			return;
		}
		
		if (sendParent) {
			for (int i = 0; i < tabViews.size(); i++) {
				UISWTViewCore view = tabViews.get(i);
				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_DATASOURCE_CHANGED,
							tv.getParentDataSource());
				}
			}
			return;
		}

		// Set Data Object for all tabs.  

		Object[] dataSourcesCore = tv.getSelectedDataSources(true);
		Object[] dataSourcesPlugin = null;

		for (int i = 0; i < tabViews.size(); i++) {
			UISWTViewCore view = tabViews.get(i);
			if (view != null) {
				if (view.useCoreDataSource()) {
					view.triggerEvent(UISWTViewEvent.TYPE_DATASOURCE_CHANGED,
							dataSourcesCore.length == 0 ? tv.getParentDataSource()
									: dataSourcesCore);
				} else {
					if (dataSourcesPlugin == null) {
						dataSourcesPlugin = tv.getSelectedDataSources(false);
					}

					view.triggerEvent(
							UISWTViewEvent.TYPE_DATASOURCE_CHANGED,
							dataSourcesPlugin.length == 0 ? PluginCoreUtils.convert(
									tv.getParentDataSource(), false) : dataSourcesPlugin);
				}
			}
		}
	}

	public void triggerTabViewDataSourceChanged(UISWTViewCore view) {
		if (view != null) {
			view.triggerEvent(UISWTViewEvent.TYPE_DATASOURCE_CHANGED, tv.getParentDataSource());

			if (view.useCoreDataSource()) {
				Object[] dataSourcesCore = tv.getSelectedDataSources(true);
				if (dataSourcesCore.length > 0) {
					view.triggerEvent(UISWTViewEvent.TYPE_DATASOURCE_CHANGED,
							dataSourcesCore.length == 0 ? tv.getParentDataSource()
									: dataSourcesCore);
				}
			} else {
				Object[] dataSourcesPlugin = tv.getSelectedDataSources(false);
				if (dataSourcesPlugin.length > 0) {
					view.triggerEvent(
							UISWTViewEvent.TYPE_DATASOURCE_CHANGED,
							dataSourcesPlugin.length == 0 ? PluginCoreUtils.convert(
									tv.getParentDataSource(), false) : dataSourcesPlugin);
				}
			}
		}
		
	}

	public void delete() {
		if (tabViews != null && tabViews.size() > 0) {
			for (int i = 0; i < tabViews.size(); i++) {
				UISWTViewCore view = tabViews.get(i);
				if (view != null) {
      		view.triggerEvent(UISWTViewEvent.TYPE_DESTROY, null);
				}
			}
		}
	}

	public void generate(IndentWriter writer) {
		writer.println("# of SubViews: " + tabViews.size());
		writer.indent();
		try {
			for (Iterator<UISWTViewCore> iter = tabViews.iterator(); iter.hasNext();) {
				UISWTViewCore view = iter.next();
				writer.println(view.getTitleID() + ": " + view.getFullTitle());
			}
		} finally {
			writer.exdent();
		}
	}

	public void localeChanged() {
		if (tabViews != null && tabViews.size() > 0) {
			for (int i = 0; i < tabViews.size(); i++) {
				UISWTViewCore view = tabViews.get(i);
				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_LANGUAGEUPDATE, null);
				}
			}
		}
	}

	public UISWTViewCore getActiveSubView() {
		if (!tv.isTabViewsEnabled() || tabFolder == null || tabFolder.isDisposed()
				|| tabFolder.getMinimized()) {
			return null;
		}

		CTabItem item = tabFolder.getSelection();
		if (item != null) {
			return (UISWTViewCore) item.getData("IView");
		}

		return null;
	}

	public void refreshSelectedSubView() {
		UISWTViewCore view = getActiveSubView();
		if (view != null && view.getComposite().isVisible()) {
			view.triggerEvent(UISWTViewEvent.TYPE_REFRESH, null);
		}
	}

	// TabViews Functions
	public void addTabView(UISWTViewCore view) {
		if (view == null || tabFolder == null) {
			return;
		}
		
		triggerTabViewDataSourceChanged(view);

		CTabItem item = new CTabItem(tabFolder, SWT.NULL);
		item.setData("IView", view);
		Messages.setLanguageText(item, view.getTitleID());
		view.initialize(tabFolder);
		item.setControl(view.getComposite());
		tabViews.add(view);
	}


	public Composite createSashForm(final Composite composite) {
		if (!tv.isTabViewsEnabled()) {
			tableComposite = tv.createMainPanel(composite);
			return tableComposite;
		}

		ConfigurationManager configMan = ConfigurationManager.getInstance();

		int iNumViews = 0;

		UIFunctionsSWT uiFunctions = UIFunctionsManagerSWT.getUIFunctionsSWT();
		UISWTViewEventListenerWrapper[] pluginViews = null;
		if (uiFunctions != null) {
			UISWTInstance pluginUI = uiFunctions.getUISWTInstance();

			if (pluginUI != null) {
				pluginViews = pluginUI.getViewListeners(tv.getTableID());
				iNumViews += pluginViews.length;
			}
		}

		if (iNumViews == 0) {
			tableComposite = tv.createMainPanel(composite);
			return tableComposite;
		}

		FormData formData;

		final Composite form = new Composite(composite, SWT.NONE);
		FormLayout flayout = new FormLayout();
		flayout.marginHeight = 0;
		flayout.marginWidth = 0;
		form.setLayout(flayout);
		GridData gridData;
		gridData = new GridData(GridData.FILL_BOTH);
		form.setLayoutData(gridData);

		// Create them in reverse order, so we can have the table auto-grow, and
		// set the tabFolder's height manually

		final int TABHEIGHT = 20;
		tabFolder = new CTabFolder(form, SWT.TOP | SWT.BORDER);
		tabFolder.setMinimizeVisible(true);
		tabFolder.setTabHeight(TABHEIGHT);
		final int iFolderHeightAdj = tabFolder.computeSize(SWT.DEFAULT, 0).y;

		final Sash sash = new Sash(form, SWT.HORIZONTAL);

		tableComposite = tv.createMainPanel(form);
		Composite cFixLayout = tableComposite;
		while (cFixLayout != null && cFixLayout.getParent() != form) {
			cFixLayout = cFixLayout.getParent();
		}
		if (cFixLayout == null) {
			cFixLayout = tableComposite;
		}
		GridLayout layout = new GridLayout();
		layout.numColumns = 1;
		layout.horizontalSpacing = 0;
		layout.verticalSpacing = 0;
		layout.marginHeight = 0;
		layout.marginWidth = 0;
		cFixLayout.setLayout(layout);

		// FormData for Folder
		formData = new FormData();
		formData.left = new FormAttachment(0, 0);
		formData.right = new FormAttachment(100, 0);
		formData.bottom = new FormAttachment(100, 0);
		int iSplitAt = configMan.getIntParameter(tv.getPropertiesPrefix() + ".SplitAt",
				3000);
		// Was stored at whole
		if (iSplitAt < 100) {
			iSplitAt *= 100;
		}

		double pct = iSplitAt / 10000.0;
		if (pct < 0.03) {
			pct = 0.03;
		} else if (pct > 0.97) {
			pct = 0.97;
		}

		// height will be set on first resize call
		sash.setData("PCT", new Double(pct));
		tabFolder.setLayoutData(formData);
		final FormData tabFolderData = formData;

		// FormData for Sash
		formData = new FormData();
		formData.left = new FormAttachment(0, 0);
		formData.right = new FormAttachment(100, 0);
		formData.bottom = new FormAttachment(tabFolder);
		formData.height = 5;
		sash.setLayoutData(formData);

		// FormData for table Composite
		formData = new FormData();
		formData.left = new FormAttachment(0, 0);
		formData.right = new FormAttachment(100, 0);
		formData.top = new FormAttachment(0, 0);
		formData.bottom = new FormAttachment(sash);
		cFixLayout.setLayoutData(formData);

		// Listeners to size the folder
		sash.addSelectionListener(new SelectionAdapter() {
			public void widgetSelected(SelectionEvent e) {
				final boolean FASTDRAG = true;

				if (FASTDRAG && e.detail == SWT.DRAG) {
					return;
				}

				if (tabFolder.getMinimized()) {
					tabFolder.setMinimized(false);
					refreshSelectedSubView();
					ConfigurationManager configMan = ConfigurationManager.getInstance();
					configMan.setParameter(tv.getPropertiesPrefix() + ".subViews.minimized",
							false);
				}

				Rectangle area = form.getClientArea();
				tabFolderData.height = area.height - e.y - e.height - iFolderHeightAdj;
				form.layout();

				Double l = new Double((double) tabFolder.getBounds().height
						/ form.getBounds().height);
				sash.setData("PCT", l);
				if (e.detail != SWT.DRAG) {
					ConfigurationManager configMan = ConfigurationManager.getInstance();
					configMan.setParameter(tv.getPropertiesPrefix() + ".SplitAt",
							(int) (l.doubleValue() * 10000));
				}
			}
		});

		final CTabFolder2Adapter folderListener = new CTabFolder2Adapter() {
			public void minimize(CTabFolderEvent event) {
				tabFolder.setMinimized(true);
				tabFolderData.height = iFolderHeightAdj;
				CTabItem[] items = tabFolder.getItems();
				for (int i = 0; i < items.length; i++) {
					CTabItem tabItem = items[i];
					tabItem.getControl().setVisible(false);
				}
				form.layout();

				UISWTViewCore view = getActiveSubView();
				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_FOCUSLOST, null);
				}

				
				ConfigurationManager configMan = ConfigurationManager.getInstance();
				configMan.setParameter(tv.getPropertiesPrefix() + ".subViews.minimized", true);
			}

			public void restore(CTabFolderEvent event) {
				tabFolder.setMinimized(false);
				CTabItem selection = tabFolder.getSelection();
				if (selection != null) {
					selection.getControl().setVisible(true);
				}
				form.notifyListeners(SWT.Resize, null);

				UISWTViewCore view = getActiveSubView();
				if (view != null) {
					view.triggerEvent(UISWTViewEvent.TYPE_FOCUSGAINED, null);
				}
				refreshSelectedSubView();

				ConfigurationManager configMan = ConfigurationManager.getInstance();
				configMan.setParameter(tv.getPropertiesPrefix() + ".subViews.minimized", false);
			}

		};
		tabFolder.addCTabFolder2Listener(folderListener);

		tabFolder.addSelectionListener(new SelectionListener() {
			public void widgetSelected(SelectionEvent e) {
				// make sure its above
				try {
					((CTabItem) e.item).getControl().setVisible(true);
					((CTabItem) e.item).getControl().moveAbove(null);

					// TODO: Need to viewDeactivated old one
					UISWTViewCore view = getActiveSubView();
					if (view != null) {
						view.triggerEvent(UISWTViewEvent.TYPE_FOCUSGAINED, null);
					}
					
				} catch (Exception t) {
				}
			}

			public void widgetDefaultSelected(SelectionEvent e) {
			}
		});

		tabFolder.addMouseListener(new MouseAdapter() {
			public void mouseDown(MouseEvent e) {
				if (tabFolder.getMinimized()) {
					folderListener.restore(null);
					// If the user clicked down on the restore button, and we restore
					// before the CTabFolder does, CTabFolder will minimize us again
					// There's no way that I know of to determine if the mouse is 
					// on that button!

					// one of these will tell tabFolder to cancel
					e.button = 0;
					tabFolder.notifyListeners(SWT.MouseExit, null);
				}
			}
		});

		form.addListener(SWT.Resize, new Listener() {
			public void handleEvent(Event e) {
				if (tabFolder.getMinimized()) {
					return;
				}

				Double l = (Double) sash.getData("PCT");
				if (l != null) {
					tabFolderData.height = (int) (form.getBounds().height * l.doubleValue())
							- iFolderHeightAdj;
					form.layout();
				}
			}
		});

		// Call plugin listeners
		if (pluginViews != null) {
			for (UISWTViewEventListenerWrapper l : pluginViews) {
				if (l != null) {
					try {
						UISWTViewImpl view = new UISWTViewImpl(tv.getTableID(), l.getViewID(), l, null);
						addTabView(view);
					} catch (Exception e) {
						// skip, plugin probably specifically asked to not be added
					}
				}
			}
		}

		if (configMan.getBooleanParameter(
				tv.getPropertiesPrefix() + ".subViews.minimized", false)) {
			tabFolder.setMinimized(true);
			tabFolderData.height = iFolderHeightAdj;
		} else {
			tabFolder.setMinimized(false);
		}

		tabFolder.setSelection(0);

		return form;
	}

	public void swt_refresh() {
		if (tv.isTabViewsEnabled() && tabFolder != null && !tabFolder.isDisposed()
				&& !tabFolder.getMinimized()) {
			refreshSelectedSubView();
		}
	}
}
