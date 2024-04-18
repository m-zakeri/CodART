package org.gudy.azureus2.ui.swt.views.table.impl;

import org.gudy.azureus2.ui.swt.views.table.TableViewSWT;
import org.gudy.azureus2.ui.swt.views.table.painted.TableViewPainted;

import com.aelitis.azureus.ui.common.table.TableColumnCore;

public class TableViewFactory
{
	public static<V> TableViewSWT<V> createTableViewSWT(Class<?> pluginDataSourceType, String _sTableID,
			String _sPropertiesPrefix, TableColumnCore[] _basicItems,
			String _sDefaultSortOn, int _iTableStyle) {
		//return new TableViewSWTImpl<V>(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems, _sDefaultSortOn, _iTableStyle);
		return (TableViewSWT<V>) new TableViewPainted(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems, _sDefaultSortOn, _iTableStyle);
	}

	public static<V> TableViewSWT<V> createTableViewSWT(boolean newCode, Class<?> pluginDataSourceType, String _sTableID,
			String _sPropertiesPrefix, TableColumnCore[] _basicItems,
			String _sDefaultSortOn, int _iTableStyle) {
		if (newCode) {
			return (TableViewSWT<V>) new TableViewPainted(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems, _sDefaultSortOn, _iTableStyle);
		}
		return new TableViewSWTImpl<V>(pluginDataSourceType, _sTableID, _sPropertiesPrefix, _basicItems, _sDefaultSortOn, _iTableStyle);
	}
}
