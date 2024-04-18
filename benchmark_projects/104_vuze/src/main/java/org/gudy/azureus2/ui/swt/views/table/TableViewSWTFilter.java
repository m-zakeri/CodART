package org.gudy.azureus2.ui.swt.views.table;

import org.eclipse.swt.events.ModifyListener;
import org.eclipse.swt.widgets.Text;

import com.aelitis.azureus.ui.common.table.impl.TableViewImpl.filter;

public class TableViewSWTFilter<DATASOURCETYPE> extends filter {
	public Text widget = null;

	public ModifyListener widgetModifyListener;
}